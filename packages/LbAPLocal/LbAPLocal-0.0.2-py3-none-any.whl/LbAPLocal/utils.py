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
import glob
import os
from os.path import dirname, join
import subprocess
import tempfile

import click
from LbAPCommon import write_jsroot_compression_options


def validate_environment():
    click.secho("Validating environment", fg="green")
    check_proxy()
    check_cvmfs()


def inside_ap_datapkg():
    """Check if script is run from main directory"""
    if not os.path.exists("./AnalysisProductions.xenv"):
        raise click.ClickException(
            "Running command in wrong directory! Please run from the AnalysisProductions base folder."
        )


def check_proxy():
    try:
        subprocess.check_call(
            ["lb-dirac", "dirac-proxy-info", "--checkvalid"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "No grid proxy found, please get one with lhcb-proxy-init"
        )


def check_cvmfs():
    for path in ["/cvmfs/lhcb.cern.ch", "/cvmfs/lhcb-condb.cern.ch"]:
        if not os.listdir(path):
            raise click.ClickException(f"Missing CVMFS repository: {path}")


def pool_xml_catalog(lfns):
    click.secho("Generating pool XML catalog", fg="green")

    # First check if we already have access
    with tempfile.TemporaryDirectory() as tmp_dir:
        proc = subprocess.run(
            ["lb-dirac", "dirac-bookkeeping-genXMLCatalog", "--LFNs", ",".join(lfns)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=tmp_dir,
        )
        if proc.returncode != 0:
            click.secho("********** stdout was:", fg="red")
            click.echo(proc.stdout)
            click.secho("********** stderr was:", fg="red")
            click.echo(proc.stderr)
            raise click.ClickException(
                f"Failed to generate pool XML catalog with: {proc.args}"
            )
        with open(join(tmp_dir, "pool_xml_catalog.xml"), "rt") as fp:
            return fp.read()


def available_productions():
    """Function that finds all production folders with an info.yaml"""

    # Glob all the info.yaml and extract production name
    folders_with_info = glob.glob("*/info.yaml", recursive=True)
    production_names = []
    for folder in folders_with_info:
        folder_name = dirname(folder)
        production_names.append(folder_name)

    return production_names


def check_production(production_name):
    if production_name not in available_productions():
        raise click.ClickException(
            f"Can't find production {production_name}. Does it have an info.yaml?"
        )


def create_output_dir(production_name):
    """Function to create the output dir a test"""

    from datetime import datetime

    date_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    testing_dir = join(os.getcwd(), "local-tests", f"{production_name}-{date_string}")
    click.secho(f"Running tests in {testing_dir}", fg="green")
    os.makedirs(testing_dir)

    dynamic_dir = join(testing_dir, "dynamic")
    os.makedirs(dynamic_dir)
    out_dir = join(testing_dir, "output")
    os.makedirs(out_dir)

    main_dynamic_dir = join(os.getcwd(), "dynamic")
    if os.path.exists(main_dynamic_dir):
        click.secho(
            f"Found existing dynamic dir pointing to "
            f"{os.readlink(main_dynamic_dir)}, unlinking",
            fg="green",
        )
        os.unlink(main_dynamic_dir)
    os.symlink(dynamic_dir, main_dynamic_dir)
    write_jsroot_compression_options(dynamic_dir)

    # Create the fake install directory for lb-run
    click.secho(f"Setting CMAKE_PREFIX_PATH to {testing_dir}", fg="green")
    os.environ["CMAKE_PREFIX_PATH"] = testing_dir
    fake_install_dir = join(
        testing_dir, "DBASE", "AnalysisProductions", "v999999999999"
    )
    os.makedirs(dirname(fake_install_dir), exist_ok=True)
    if os.path.exists(fake_install_dir):
        os.unlink(fake_install_dir)
    os.symlink(os.getcwd(), fake_install_dir)

    return dynamic_dir, out_dir
