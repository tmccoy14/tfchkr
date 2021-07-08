<img src="assets/tfchkr_logo.png" width="1000" height="400" />

# Tfchkr is a Python Terraform testing framework.

- [Introduction](#introduction)
- [Setup](#setup)
- [Getting Started](#getting-started)

### Introduction

Testing comment for repo syncing purposes.

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

This command will run through the `terraform init, terraform plan, terraform apply, and terraform destroy` commands to ensure the Terraform files are syntactically valid as well as the provider resources are set up correctly.

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
Downloading cloudposse/tfstate-backend/aws 0.25.0 for tfstate-backend...
- tfstate-backend in .terraform/modules/tfstate-backend
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.base_label...
- tfstate-backend.base_label in .terraform/modules/tfstate-backend.base_label
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.dynamodb_table_label...
- tfstate-backend.dynamodb_table_label in .terraform/modules/tfstate-backend.dynamodb_table_label
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.s3_bucket_label...
- tfstate-backend.s3_bucket_label in .terraform/modules/tfstate-backend.s3_bucket_label

Initializing the backend...

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "null" (hashicorp/null) 2.1.2...
- Downloading plugin for provider "aws" (hashicorp/aws) 3.8.0...
- Downloading plugin for provider "template" (hashicorp/template) 2.1.2...
- Downloading plugin for provider "local" (hashicorp/local) 1.4.0...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
 <= read (data resources)

Terraform will perform the following actions:

  # module.tfstate-backend.data.template_file.terraform_backend_config will be read during apply
  # (config refers to values not yet known)
 <= data "template_file" "terraform_backend_config"  {
      + id       = (known after apply)
      + rendered = (known after apply)
      + template = <<~EOT
            terraform {
              required_version = ">= ${terraform_version}"

              backend "s3" {
                region         = "${region}"
                bucket         = "${bucket}"
                key            = "${terraform_state_file}"
                dynamodb_table = "${dynamodb_table}"
                profile        = "${profile}"
                role_arn       = "${role_arn}"
                encrypt        = "${encrypt}"
              }
            }
        EOT
      + vars     = {
          + "bucket"               = (known after apply)
          + "dynamodb_table"       = "test-tfstate-terra-testing-terraform-state-lock"
          + "encrypt"              = "true"
          + "profile"              = ""
          + "region"               = "us-east-2"
          + "role_arn"             = ""
          + "terraform_state_file" = "terraform.tfstate"
          + "terraform_version"    = "0.12.2"
        }
    }

  # module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0] will be created
  + resource "aws_dynamodb_table" "with_server_side_encryption" {
      + arn              = (known after apply)
      + billing_mode     = "PROVISIONED"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "test-tfstate-terra-testing-terraform-state-lock"
      + read_capacity    = 5
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)
      + tags             = {
          + "Attributes"  = "terraform-state-lock"
          + "Name"        = "test-tfstate-terra-testing-terraform-state-lock"
          + "Namespace"   = "test-tfstate"
          + "Stage"       = "terra"
          + "environment" = "test"
          + "managed_by"  = "tfstate"
          + "poc"         = "tucker.m.mccoy"
          + "project"     = "terratesting"
        }
      + write_capacity   = 5

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = false
        }

      + server_side_encryption {
          + enabled     = true
          + kms_key_arn = (known after apply)
        }
    }

  # module.tfstate-backend.aws_s3_bucket.default will be created
  + resource "aws_s3_bucket" "default" {
      + acceleration_status         = (known after apply)
      + acl                         = "private"
      + arn                         = (known after apply)
      + bucket                      = "test-tfstate-terra-testing-terraform-state"
      + bucket_domain_name          = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = true
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + policy                      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "s3:PutObject"
                      + Condition = {
                          + StringNotEquals = {
                              + s3:x-amz-server-side-encryption = [
                                  + "aws:kms",
                                  + "AES256",
                                ]
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*"
                      + Sid       = "DenyIncorrectEncryptionHeader"
                    },
                  + {
                      + Action    = "s3:PutObject"
                      + Condition = {
                          + Null = {
                              + s3:x-amz-server-side-encryption = "true"
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*"
                      + Sid       = "DenyUnEncryptedObjectUploads"
                    },
                  + {
                      + Action    = "s3:*"
                      + Condition = {
                          + Bool = {
                              + aws:SecureTransport = "false"
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = [
                          + "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*",
                          + "arn:aws:s3:::test-tfstate-terra-testing-terraform-state",
                        ]
                      + Sid       = "EnforceTlsRequestsOnly"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "Attributes"  = "terraform-state"
          + "Name"        = "test-tfstate-terra-testing-terraform-state"
          + "Namespace"   = "test-tfstate"
          + "Stage"       = "terra"
          + "environment" = "test"
          + "managed_by"  = "tfstate"
          + "poc"         = "tucker.m.mccoy"
          + "project"     = "terratesting"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + server_side_encryption_configuration {
          + rule {
              + apply_server_side_encryption_by_default {
                  + sse_algorithm = "AES256"
                }
            }
        }

      + versioning {
          + enabled    = true
          + mfa_delete = false
        }
    }

  # module.tfstate-backend.aws_s3_bucket_public_access_block.default[0] will be created
  + resource "aws_s3_bucket_public_access_block" "default" {
      + block_public_acls       = true
      + block_public_policy     = true
      + bucket                  = (known after apply)
      + id                      = (known after apply)
      + ignore_public_acls      = true
      + restrict_public_buckets = true
    }

Plan: 3 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.


module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creation complete after 7s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creating...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creation complete after 0s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creation complete after 8s [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state-lock]
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

Passed checks: 4, Failed checks: 0

INIT -- SUCCESS
PLAN -- SUCCESS
APPLY -- SUCCESS
DESTROY -- SUCCESS
```

```sh
# Run tests with path and variables
$ tfchkr run test -p examples/tfstate_variables --var stage=terra --var name=testing
Initializing modules...
Downloading cloudposse/tfstate-backend/aws 0.25.0 for tfstate-backend...
- tfstate-backend in .terraform/modules/tfstate-backend
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.base_label...
- tfstate-backend.base_label in .terraform/modules/tfstate-backend.base_label
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.dynamodb_table_label...
- tfstate-backend.dynamodb_table_label in .terraform/modules/tfstate-backend.dynamodb_table_label
Downloading git::https://github.com/cloudposse/terraform-null-label.git?ref=tags/0.17.0 for tfstate-backend.s3_bucket_label...
- tfstate-backend.s3_bucket_label in .terraform/modules/tfstate-backend.s3_bucket_label

Initializing the backend...

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "null" (hashicorp/null) 2.1.2...
- Downloading plugin for provider "aws" (hashicorp/aws) 3.8.0...
- Downloading plugin for provider "template" (hashicorp/template) 2.1.2...
- Downloading plugin for provider "local" (hashicorp/local) 1.4.0...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
 <= read (data resources)

Terraform will perform the following actions:

  # module.tfstate-backend.data.template_file.terraform_backend_config will be read during apply
  # (config refers to values not yet known)
 <= data "template_file" "terraform_backend_config"  {
      + id       = (known after apply)
      + rendered = (known after apply)
      + template = <<~EOT
            terraform {
              required_version = ">= ${terraform_version}"

              backend "s3" {
                region         = "${region}"
                bucket         = "${bucket}"
                key            = "${terraform_state_file}"
                dynamodb_table = "${dynamodb_table}"
                profile        = "${profile}"
                role_arn       = "${role_arn}"
                encrypt        = "${encrypt}"
              }
            }
        EOT
      + vars     = {
          + "bucket"               = (known after apply)
          + "dynamodb_table"       = "test-tfstate-terra-testing-terraform-state-lock"
          + "encrypt"              = "true"
          + "profile"              = ""
          + "region"               = "us-east-2"
          + "role_arn"             = ""
          + "terraform_state_file" = "terraform.tfstate"
          + "terraform_version"    = "0.12.2"
        }
    }

  # module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0] will be created
  + resource "aws_dynamodb_table" "with_server_side_encryption" {
      + arn              = (known after apply)
      + billing_mode     = "PROVISIONED"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "test-tfstate-terra-testing-terraform-state-lock"
      + read_capacity    = 5
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)
      + tags             = {
          + "Attributes"  = "terraform-state-lock"
          + "Name"        = "test-tfstate-terra-testing-terraform-state-lock"
          + "Namespace"   = "test-tfstate"
          + "Stage"       = "terra"
          + "environment" = "test"
          + "managed_by"  = "tfstate"
          + "poc"         = "tucker.m.mccoy"
          + "project"     = "terratesting"
        }
      + write_capacity   = 5

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = false
        }

      + server_side_encryption {
          + enabled     = true
          + kms_key_arn = (known after apply)
        }
    }

  # module.tfstate-backend.aws_s3_bucket.default will be created
  + resource "aws_s3_bucket" "default" {
      + acceleration_status         = (known after apply)
      + acl                         = "private"
      + arn                         = (known after apply)
      + bucket                      = "test-tfstate-terra-testing-terraform-state"
      + bucket_domain_name          = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = true
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + policy                      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "s3:PutObject"
                      + Condition = {
                          + StringNotEquals = {
                              + s3:x-amz-server-side-encryption = [
                                  + "aws:kms",
                                  + "AES256",
                                ]
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*"
                      + Sid       = "DenyIncorrectEncryptionHeader"
                    },
                  + {
                      + Action    = "s3:PutObject"
                      + Condition = {
                          + Null = {
                              + s3:x-amz-server-side-encryption = "true"
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*"
                      + Sid       = "DenyUnEncryptedObjectUploads"
                    },
                  + {
                      + Action    = "s3:*"
                      + Condition = {
                          + Bool = {
                              + aws:SecureTransport = "false"
                            }
                        }
                      + Effect    = "Deny"
                      + Principal = {
                          + AWS = "*"
                        }
                      + Resource  = [
                          + "arn:aws:s3:::test-tfstate-terra-testing-terraform-state/*",
                          + "arn:aws:s3:::test-tfstate-terra-testing-terraform-state",
                        ]
                      + Sid       = "EnforceTlsRequestsOnly"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "Attributes"  = "terraform-state"
          + "Name"        = "test-tfstate-terra-testing-terraform-state"
          + "Namespace"   = "test-tfstate"
          + "Stage"       = "terra"
          + "environment" = "test"
          + "managed_by"  = "tfstate"
          + "poc"         = "tucker.m.mccoy"
          + "project"     = "terratesting"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + server_side_encryption_configuration {
          + rule {
              + apply_server_side_encryption_by_default {
                  + sse_algorithm = "AES256"
                }
            }
        }

      + versioning {
          + enabled    = true
          + mfa_delete = false
        }
    }

  # module.tfstate-backend.aws_s3_bucket_public_access_block.default[0] will be created
  + resource "aws_s3_bucket_public_access_block" "default" {
      + block_public_acls       = true
      + block_public_policy     = true
      + bucket                  = (known after apply)
      + id                      = (known after apply)
      + ignore_public_acls      = true
      + restrict_public_buckets = true
    }

Plan: 3 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.


module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creating...
module.tfstate-backend.aws_s3_bucket.default: Creation complete after 7s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creating...
module.tfstate-backend.aws_s3_bucket_public_access_block.default[0]: Creation complete after 0s [id=test-tfstate-terra-testing-terraform-state]
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Creation complete after 8s [id=test-tfstate-terra-testing-terraform-state-lock]
module.tfstate-backend.data.template_file.terraform_backend_config: Refreshing state...

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

module.tfstate-backend.data.aws_region.current: Refreshing state...
module.tfstate-backend.data.aws_iam_policy_document.prevent_unencrypted_uploads[0]: Refreshing state...
module.tfstate-backend.aws_dynamodb_table.with_server_side_encryption[0]: Refreshing state... [id=test-tfstate-terra-testing-terraform-state-lock]
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

Passed checks: 4, Failed checks: 0

INIT -- SUCCESS
PLAN -- SUCCESS
APPLY -- SUCCESS
DESTROY -- SUCCESS
```

#### TFCHKR RUN COMPLIANCE

The `tfchkr run compliance` command accepts one parameter, the path to the Terraform directory. Below are examples of how to use the two commands.

This command will use a third party module called [checkov](https://github.com/bridgecrewio/checkov) to detect any security and compliance misconfigurations in the Terraform files.

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
