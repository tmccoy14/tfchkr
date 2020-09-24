"""Standard library"""
import os
from os import listdir

"""Third party modules"""
import click


def check_tf_extension(ctx, tf_directory):
    """Check tf file extension for tf or hcl"""

    tf_type = None

    # If a file in the directory contains extension hcl return hcl
    # for terragrunt commands else return extension tf for terraform commands
    if any("hcl" in tf_file for tf_file in listdir(tf_directory)):
        tf_type = "hcl"
    else:
        tf_type = "tf"

    return tf_type


def generate_variables_string(var):
    """Generate a string from list of variables provided"""

    var_list = []

    for item in var:
        var_list.append("--var {}".format(item))

    var_string = " ".join(var_list)

    return var_string


def tf_init(ctx, tf_command, tf_directory, var):
    """Run terraform init"""

    tfstate_directory = os.path.join(tf_directory)
    prefix_command = "cd {0} &&".format(tfstate_directory)

    # terraform init on tfstate module
    result = tf_command.prefix_run(prefix_command, "init")

    while result.poll() is None:
        line = result.stdout.readline()
        print(line.decode("utf-8").rstrip())

    output, error = result.communicate()
    if error:
        ctx.log("Error: %s" % error.decode("utf-8"), level="error")
    ctx.vlog("%s" % output.decode("utf-8"))

    return result.returncode


def tf_apply(ctx, tf_command, tf_directory, var):
    """Run terraform apply"""

    directory = os.path.join(tf_directory)
    prefix_command = "cd {0} &&".format(directory)
    if var:
        vars = generate_variables_string(var)
        process = tf_command.prefix_run(
            prefix_command, "apply -auto-approve {}".format(vars)
        )
    else:
        process = tf_command.prefix_run(prefix_command, "apply -auto-approve")

    while process.poll() is None:
        line = process.stdout.readline()
        print(line.decode("utf-8").rstrip())

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Could not create resource", level="error")
        ctx.log("%s" % error.decode("utf-8"))
    ctx.vlog("%s" % output.decode("utf-8"))

    return process.returncode


def tf_destroy(ctx, tf_command, tf_directory, var):
    """Run terraform destroy"""

    directory = os.path.join(tf_directory)
    prefix_command = "cd {0} &&".format(directory)
    if var:
        vars = generate_variables_string(var)
        process = tf_command.prefix_run(
            prefix_command, "destroy -auto-approve {}".format(vars)
        )
    else:
        process = tf_command.prefix_run(prefix_command, "destroy -auto-approve")

    while process.poll() is None:
        line = process.stdout.readline()
        print(line.decode("utf-8").rstrip())

    output, error = process.communicate()
    if process.returncode != 0:
        ctx.log("Could not destroy resource", level="error")
        ctx.log("%s" % error.decode("utf-8"))
    ctx.vlog("%s" % output.decode("utf-8"))

    return process.returncode
