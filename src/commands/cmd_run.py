"""Standard library"""
import os

"""Third party modules"""
import click
from colorama import Fore

"""Internal application modules"""
from src.main import pass_environment
from src.lib import (
    check_tf_extension,
    tf_init,
    tf_apply,
    tf_destroy,
)
from src.lib.subprocess import Command


@click.group("run", short_help="Run the tests and compliance checks on Terraform file.")
@pass_environment
def cli(ctx):
    """tftest test and compliance."""


@cli.command("test", short_help="Run the tests.")
@click.option(
    "--path", "-p", required=True, help="Path to Terraform directory.",
)
@click.option(
    "--var", required=False, multiple=True, help="Variables for Terraform files."
)
@pass_environment
def test(ctx, path, var):
    """Run the tests for the Terraform modules and files\n
       Ex. tftest run -p path/to/tf_directory\n
       Ex. tftest run -p path/to/tf_directory --var key=value --var key=value"""

    # Ensure path provided to Terraform directory exists
    tf_directory = os.path.join(path)
    if not os.path.exists(tf_directory):
        raise click.UsageError(
            "Path to Terraform directory does not exist: '%s'" % path
        )

    # Check if Terraform directory contains Terragrunt file
    tf_type = check_tf_extension(ctx, tf_directory)
    if tf_type is None:
        raise click.UsageError(
            "Terraform directory does not contain necessary files: '%s'" % path
        )

    # Setup command subprocess
    if tf_type == "hcl":
        tf_command = Command("terragrunt")
    else:
        tf_command = Command("terraform")

    # Run terraform init command to initialize a working directory
    init_result = tf_init(ctx, tf_command, tf_directory, var)

    # Run terraform/terragrunt apply command to apply new resources or changes
    apply_result = tf_apply(ctx, tf_command, tf_directory, var)

    # Run terraform/terragrunt destroy to destroy the Terraform-managed infrastructure
    destroy_result = tf_destroy(ctx, tf_command, tf_directory, var)

    # Output whether the tests ran were succesful or failed
    passed_checks = 0
    failed_checks = 0
    for check in [init_result, apply_result, destroy_result]:
        if check == 0:
            passed_checks += 1
        else:
            failed_checks += 1

    ctx.log(Fore.WHITE + "RESULTS:")
    ctx.log(Fore.WHITE + "-------------------------\n")

    ctx.log(
        Fore.WHITE
        + "Passed checks: {0}, Failed checks: {1}\n".format(
            passed_checks, failed_checks
        )
    )

    if init_result == 0:
        ctx.log("INIT -- SUCCESS")
    else:
        ctx.log("INIT -- FAILED", level="error")
    if apply_result == 0:
        ctx.log("APPLY -- SUCCESS", level="warning")
    else:
        ctx.log("APPLY -- FAILED", level="error")
    if destroy_result == 0:
        ctx.log("DESTROY -- SUCCESS")
    else:
        ctx.log("DESTROY -- FAILED", level="error")


@cli.command("compliance", short_help="Run the compliance checks.")
@click.option(
    "--path", "-p", required=True, help="Path to Terraform directory.",
)
@pass_environment
def compliance(ctx, path):
    """Run the compliance checks for the Terraform modules and files\n
       Ex. tftest compliance -p path/to/tf_directory"""

    # Setup command subprocess
    checkov_command = Command("checkov")

    tf_directory = os.path.join(path)
    prefix_command = "cd {0} &&".format(tf_directory)

    # terraform init on tfstate module
    result = checkov_command.prefix_run(prefix_command, "-d .")

    while result.poll() is None:
        line = result.stdout.readline()
        print(line.decode("utf-8").rstrip())

    output, error = result.communicate()
    if error:
        ctx.log("Error: %s" % error.decode("utf-8"), level="error")
    ctx.vlog("%s" % output.decode("utf-8"))
