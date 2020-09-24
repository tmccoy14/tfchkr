<img src="assets/tfchkr_logo.png" width="1000" height="400" />

# Tfchkr is a Python Terraform testing framework.

- [Introduction](#introduction)
- [Setup](#setup)
- [Getting Started](#getting-started)

### Introduction

Tfchkr is a Python Terraform testing framework that allows us to isolate our infrastructure as code to test for errors and compliance. A lot of the time, we blindly create resources with Terraform hoping the commands will work smoothly and security vulnerabilities are none. We can now test this process before moving forward without throwing it over the wall hoping for the best. With running `tfchkr` you can now test the Terraform code base for any syntax errors, as well as vulnerability errors. It logs each command and returns the results at the end whether they were successful or failed. This serves as a repeatable process that can be ran locally or with a CICD pipeline.

### Setup

The first thing you will need to do before installing `tfchkr` is configure a local virutal environment. If you currently don't have a virtual environment installed, I would highly recommend [pyenv](https://github.com/pyenv/pyenv).

Once you have a local virtual environment configured you only need to do a quick pip install of the `tfchkr` package.

Install and set up `tfchkr` for development

```sh
$ cd tfchkr

$ pip install --editable .
Obtaining file:///Users/tucker.m.mccoy/Github/tmccoy14/tfchkr
Requirement already satisfied: Click==7.0 in /Users/tucker.m.mccoy/.pyenv/versions/3.7.3/envs/tfchkrcli/lib/python3.7/site-packages (from tfchkr==0.1) (7.0)
Requirement already satisfied: colorama==0.4.3 in /Users/tucker.m.mccoy/.pyenv/versions/3.7.3/envs/tfchkrcli/lib/python3.7/site-packages (from tfchkr==0.1) (0.4.3)
Installing collected packages: tfchkr
  Found existing installation: tfchkr 0.1
    Uninstalling tfchkr-0.1:
      Successfully uninstalled tfchkr-0.1
  Running setup.py develop for tfchkr
Successfully installed tfchkr
```

Note: the `--editable` flag will provide you with a way to hot reload changes
while you are working on new features.

If you are trying to install the package for usage just run: `pip install .`.

### Getting Started

Once you have successfully installed tfchkr, you can confirm by running `tfchkr`

```sh
$ tfchkr
Usage: tfchkr [OPTIONS] COMMAND [ARGS]...

  tfchkr is a tool to run tests on Terraform modules and files.

Options:
  --home DIRECTORY  Project folder to operate on.
  -v, --verbose     Enables verbose mode.
  --version         Print the current version of tfchkr.
  --help            Show this message and exit.

Commands:
  run  Run the tests and compliance checks on Terraform file.
```

tfchkr `run` has two commands, `tfchkr run test` and `tfchkr run compliance`, that will run the tests and compliance checks on the specified Terraform modules or files.

```sh
$ tfchkr run --help
Usage: tfchkr run [OPTIONS] COMMAND [ARGS]...

  tfchkr test and compliance.

Options:
  --help  Show this message and exit.

Commands:
  compliance  Run the compliance checks.
  test        Run the tests.
```

#### TFCHKR RUN TEST

The `tfchkr run test` command accepts two parameters, the path to the Terraform directory and variables needed for the Terraform files.

```sh
$ tfchkr run test --help
Usage: tfchkr run test [OPTIONS]

  Run the tests for the Terraform modules and files

  Ex. tfchkr run -p path/to/tf_directory

  Ex. tfchkr run -p path/to/tf_directory --var key=value --var key=value

Options:
  -p, --path TEXT  Path to Terraform directory.  [required]
  --var TEXT       Variables for Terraform files.
  --help           Show this message and exit.
```

```sh
# Run tests with with path only
$ tfchkr run test -p examples/tfstate
Initializing modules...

Initializing the backend...

Initializing provider plugins...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creation complete after 4s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creating...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creation complete after 0s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creation complete after 7s [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_s3_bucket.default: Refreshing state... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Destroying... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Destroying... [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Destruction complete after 0s
module.tfstate-backend.aws_s3_bucket.default: Destroying... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket.default: Destruction complete after 0s
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Destruction complete after 3s

Destroy complete! Resources: 3 destroyed.

RESULTS:
-------------------------

Passed checks: 3, Failed checks: 0

INIT -- SUCCESS
APPLY -- SUCCESS
DESTROY -- SUCCESS
```

```sh
# Run tests with path and variables
$ tfchkr run test -p examples/tfstate_variables --var stage=terra --var name=testing
Initializing modules...

Initializing the backend...

Initializing provider plugins...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creation complete after 4s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creating...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creation complete after 0s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creation complete after 7s [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_s3_bucket.default: Refreshing state... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Destroying... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Destroying... [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Destruction complete after 0s
module.tfstate-backend.aws_s3_bucket.default: Destroying... [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket.default: Destruction complete after 0s
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Destruction complete after 3s

Destroy complete! Resources: 3 destroyed.

RESULTS:
-------------------------

Passed checks: 3, Failed checks: 0

INIT -- SUCCESS
APPLY -- SUCCESS
DESTROY -- SUCCESS
```

#### TFCHKR RUN COMPLIANCE

The `tfchkr run compliance` command accepts one parameter, the path to the Terraform directory. Below are examples of how to use the two commands.

```sh
$ tfchkr run compliance --help
Usage: tfchkr run compliance [OPTIONS]

  Run the compliance checks for the Terraform modules and files

  Ex. tfchkr compliance -p path/to/tf_directory

Options:
  -p, --path TEXT  Path to Terraform directory.  [required]
  --help           Show this message and exit.
```

```sh
$ tfchkr run compliance -p examples/tfstate_variables
terraform scan results:

Passed checks: 1, Failed checks: 0, Skipped checks: 0

Check: CKV_AWS_41: "Ensure no hard coded AWS access key and and secret key exists in provider"
	PASSED for resource: aws.default
	File: /main.tf:8-11
	Guide: https://docs.bridgecrew.io/docs/bc_aws_secrets_5
```
