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
import os
import shlex
import subprocess

import click
from LbAPCommon import render_yaml, parse_yaml

from .testing import enter_debugging, prepare_reproduce, prepare_test
from .utils import (
    available_productions,
    check_production,
    inside_ap_datapkg,
    validate_environment,
)


class NaturalOrderGroup(click.Group):
    """Group for showing subcommands in the correct order"""

    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def main():
    """Command line tool for the LHCb AnalysisProductions"""
    pass


@main.command()
@click.argument("production_name", type=str, default="", nargs=1)
def list(production_name):
    """List the available production folders by running lb-ap list
    List the available productions for a specific production by running lb-ap list YOUR_PRODUCTION"""
    inside_ap_datapkg()

    if production_name:
        # Check if production exists
        check_production(production_name)
        click.echo(f"The available jobs for {production_name} are: ")

        # Get rendered yaml and find all the production names
        with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
            raw_yaml = fp.read()
        job_names = parse_yaml(render_yaml(raw_yaml))
        for line in job_names:
            click.echo(f"* {line}")
    else:
        click.echo("The available productions are: ")
        for folder in available_productions():
            click.echo(f"* {folder}")


@main.command()
@click.argument("production_name", type=str, nargs=1)
def render(production_name):
    """Render the info.yaml for a given production"""
    inside_ap_datapkg()

    # Check if production exists
    check_production(production_name)

    # Get rendered yaml and print
    click.secho("Rendering info.yaml for {}\n\n".format(production_name), fg="green")
    with open(os.path.join(production_name, "info.yaml"), "rt") as fp:
        raw_yaml = fp.read()
    render = render_yaml(raw_yaml)
    click.echo(render)


@main.command()
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
def test(production_name, job_name):
    """Execute a job locally"""
    validate_environment()
    inside_ap_datapkg()

    out_dir, env_cmd, gaudi_cmd = prepare_test(production_name, job_name)
    cmd = env_cmd + gaudi_cmd
    click.secho(f"Starting lb-run with: {shlex.join(cmd)}", fg="green")
    try:
        subprocess.check_call(cmd, cwd=out_dir)
    except subprocess.CalledProcessError:
        raise click.ClickException("Execution failed, see above for details")
    click.secho(f"Success! Output can be found in {out_dir}", fg="green")


@main.command()
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
def debug(production_name, job_name):
    """Start an interactive session inside the job's environment"""
    validate_environment()
    inside_ap_datapkg()

    enter_debugging(*prepare_test(production_name, job_name))


@main.command()
@click.argument("pipeline_id", type=int, nargs=1)
@click.argument("production_name", type=str, nargs=1)
@click.argument("job_name", type=str, nargs=1)
@click.argument("test_id", type=str, nargs=1, default="latest")
def reproduce(pipeline_id, production_name, job_name, test_id):
    """Reproduce an existing online test locally"""
    validate_environment()
    enter_debugging(*prepare_reproduce(pipeline_id, production_name, job_name))
