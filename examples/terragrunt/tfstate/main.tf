terraform {
  required_version = ">= 0.12.19"
}

# ---------------------------------------------------------------------------------------------------------------------
# PREPARE PROVIDERS
# ---------------------------------------------------------------------------------------------------------------------
provider "aws" {
  version = "~> 3.0"
  region  = "us-east-2"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE A TFSTATE-BACKEND
# ---------------------------------------------------------------------------------------------------------------------
module "tfstate-backend" {
  source  = "cloudposse/tfstate-backend/aws"
  version = "0.25.0"

  namespace     = "test-tfstate"
  stage         = "terra"
  name          = "testing"
  force_destroy = true

  attributes = ["terraform", "state"]

  tags = {
    managed_by  = "tfstate"
    poc         = "tucker.m.mccoy"
    project     = "terratesting"
    environment = "test"
  }
}
