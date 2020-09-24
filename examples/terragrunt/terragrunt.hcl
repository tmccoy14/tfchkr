# ---------------------------------------------------------------------------------------------------------------------
# CREATE REMOTE STATE BACKEND
# ---------------------------------------------------------------------------------------------------------------------
remote_state {
  backend = "s3"

  config = {
    bucket           = "tftest-terraform-state"
    region           = "us-east-2"
    encrypt          = true
    dynamodb_table   = "tftest-terraform-state-lock"
    key              = "tftest/terraformstate.tfstate"
    force_path_style = true
  }
}
