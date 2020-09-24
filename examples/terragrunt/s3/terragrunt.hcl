include {
  path = "${find_in_parent_folders()}"
}

inputs = {
  region = "us-east-2"
  bucket = "terratesting1"
  acl    = "private"
  tags = {
    managed_by  = "tftest"
    poc         = "tucker.m.mccoy"
    project     = "terratesting"
    environment = "test"
  }
}
