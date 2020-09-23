"""Standard library"""
import os

"""Third party modules"""
import click

"""Internal application modules"""
from src.main import pass_environment


@click.command("run", short_help="Run the tests.")
@pass_environment
def cli(ctx):
    """Run the tests for the Terraform modules and files"""

    ctx.log("Running tests...")

    ctx.log("Done...")
