###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
import os
from os.path import dirname, join
import shlex
import shutil
import subprocess
from urllib.parse import urlencode, urlparse, urlunparse
import tempfile

import click
from LbAPCommon import render_yaml, parse_yaml, validate_yaml
import requests

from . import cern_sso
from .exceptions import (
    JobNotFoundError,
)
from .utils import pool_xml_catalog, check_production, create_output_dir

# ANA_PROD_HOST = "http://127.0.0.1:5000"
ANA_PROD_HOST = "https://lhcb-analysis-productions.web.cern.ch/"
ANA_PROD_WEB_URL = urlparse(ANA_PROD_HOST)[:2] + ("/dynamic/test-locally/",)


def prepare_test(production_name, job_name):
    """Run a local test job for a specific production job"""
    # Check if production exists
    check_production(production_name)

    # Check if job actually exists in production
    with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
        raw_yaml = fp.read()
    prod_data = parse_yaml(render_yaml(raw_yaml))
    validate_yaml(prod_data, ".", production_name)
    try:
        job_data = prod_data[job_name]
    except KeyError:
        raise JobNotFoundError(
            f"Job {job_name} is not found for production {production_name}!"
        )

    dynamic_dir, out_dir = create_output_dir(production_name)

    application_name, application_version = job_data["application"].rsplit("/", 1)
    options = [*job_data["options"]]

    if "bk_query" not in job_data["input"]:
        raise NotImplementedError("Currently only support bookkeeping inputs")
    params = {
        "application_name": application_name,
        "application_version": application_version,
        "bk_query": job_data["input"]["bk_query"],
    }
    resp = requests.get(
        urlunparse(ANA_PROD_WEB_URL + ("", urlencode(params), "")),
        cookies=cern_sso.sign_in(ANA_PROD_HOST),
    )
    if not resp.ok:
        click.secho(resp.text, fg="red")
        raise click.ClickException("Network request for metadata failed")
    data = resp.json()

    if job_data["automatically_configure"]:
        config_fn = job_name + "_autoconf.py"
        config_path = join(dynamic_dir, production_name, config_fn)
        os.makedirs(dirname(config_path))
        with open(config_path, "wt") as f:
            f.write(data["dynamic_options"]["local_autoconf.py"])
        options.insert(
            0, join("$ANALYSIS_PRODUCTIONS_DYNAMIC", production_name, config_fn)
        )

    prod_conf_fn = "prodConf_DaVinci_00012345_00006789_1.py"
    gaudi_cmd = ["gaudirun.py", "-T", *options, prod_conf_fn]

    if len(job_data["output"]) != 1:
        raise NotImplementedError()
    output_file_type = job_data["output"].pop()

    with open(join(out_dir, "pool_xml_catalog.xml"), "wt") as fp:
        fp.write(pool_xml_catalog(data["lfns"]))

    lfns = json.dumps([f"LFN:{lfn}" for lfn in data["lfns"]])

    with open(join(out_dir, prod_conf_fn), "wt") as fp:
        fp.write(
            "\n".join(
                [
                    "from ProdConf import ProdConf",
                    "ProdConf(",
                    "  NOfEvents=-1,",
                    f"  AppVersion='{application_version}',",
                    "  OptionFormat='WGProd',",
                    "  XMLSummaryFile='summaryDaVinci_00012345_00006789_1.xml',",
                    f"  Application='{application_name}',",
                    "  OutputFilePrefix='00012345_00006789_1',",
                    "  XMLFileCatalog='pool_xml_catalog.xml',",
                    f"  InputFiles={lfns},",
                    f"  OutputFileTypes=['{output_file_type}'],",
                    ")",
                ]
            )
        )

    return out_dir, data["env-command"], gaudi_cmd


def prepare_reproduce(pipeline_id, production_name, job_name, test_id="latest"):
    click.secho(
        f"Reproducing test for test {pipeline_id} {production_name} {job_name}",
        fg="green",
    )

    resp = requests.get(
        f"{ANA_PROD_HOST}/dynamic/{pipeline_id}/{production_name}/{job_name}/{test_id}/reproduce_locally.json",
        cookies=cern_sso.sign_in(ANA_PROD_HOST),
    )
    if not resp.ok:
        click.secho(resp.text, fg="red")
        raise click.ClickException("Network request for reproduce_locally.json failed")
    data = resp.json()

    tmp_dir = tempfile.mkdtemp()

    click.secho(f"Cloning {data['git_repo']}", fg="green")
    subprocess.check_call(["git", "clone", data["git_repo"], tmp_dir])

    click.secho(f"Running test in {tmp_dir}", fg="green")
    os.chdir(tmp_dir)

    click.secho(f"Checking out {data['revision']}", fg="green")
    subprocess.check_call(["git", "checkout", data["revision"]])

    check_production(production_name)

    dynamic_dir, out_dir = create_output_dir(production_name)

    # Write the dynamic option files
    for filename, filecontent in data["dynamic_options"].items():
        filename = join(dynamic_dir, filename)
        os.makedirs(dirname(filename), exist_ok=True)
        with open(filename, "wt") as f:
            f.write(filecontent)

    # Download the job input
    for filename, url in data["download_files"].items():
        click.secho(f"Downloading {filename}", fg="green")
        filename = join(out_dir, filename)
        os.makedirs(dirname(filename), exist_ok=True)
        with requests.get(url, stream=True) as resp:
            if not resp.ok:
                click.secho(resp.text, fg="red")
                raise click.ClickException("Network request for job file failed")
            with open(filename, "wb") as fp:
                shutil.copyfileobj(resp.raw, fp)

    env_cmd = data["env-command"]
    # TODO: This is a temporary hack
    if "AnalysisProductions.v999999999999" not in env_cmd:
        env_cmd = (
            env_cmd[:1] + ["--use=AnalysisProductions.v999999999999"] + env_cmd[1:]
        )
    return out_dir, env_cmd, data["command"]


def enter_debugging(out_dir, env_cmd, gaudi_cmd):
    with tempfile.NamedTemporaryFile("wt", delete=False) as fp:
        bash_env_fn = fp.name

        fp.write("echo\n")
        fp.write("echo Welcome to analysis productions debug mode:\n")
        fp.write("echo\n")
        fp.write("echo The production can be tested by running:\n")
        fp.write("echo\n")
        fp.write(f"echo {shlex.quote(shlex.join(gaudi_cmd))}\n")
        fp.write("echo\n")
        fp.write(f"rm {shlex.quote(bash_env_fn)}\n")

    cmd = env_cmd + ["bash", "--rcfile", bash_env_fn]
    click.secho(f"Starting lb-run with: {shlex.join(cmd)}", fg="green")

    os.chdir(out_dir)
    os.execlp(cmd[0], *cmd)
