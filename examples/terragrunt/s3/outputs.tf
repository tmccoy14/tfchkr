output "bucket" {
  value = "${aws_s3_bucket.test-bucket.bucket}"
}

output "acl" {
  value = "${aws_s3_bucket.test-bucket.acl}"
}

output "tags" {
  value = "${aws_s3_bucket.test-bucket.tags}"
}
