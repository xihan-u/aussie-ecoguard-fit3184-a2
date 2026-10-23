variable "project_id" { type = string }
variable "identity_only" {
  type        = bool
  description = "Only free IAM/WIF identity resources. No Cloud Run, model storage or registry."
  default     = true
}
variable "region" {
  type    = string
  default = "us-central1"
}
variable "prefix" {
  type    = string
  default = "ecoguard3184"
}
variable "aws_account_id" { type = string }
variable "aws_role_name" {
  type    = string
  default = "LabRole"
}
variable "image" {
  type    = string
  default = ""
}
variable "cognito_issuer" {
  type    = string
  default = ""
}
variable "cognito_client_id" {
  type    = string
  default = ""
}
variable "media_bucket" {
  type    = string
  default = ""
}
variable "manifest_sha256" {
  type    = string
  default = "639595e1e9ffe18cb11ead1c7480ffe7a31bf767f6cbaf6b8375829227a569ae"
  validation {
    condition     = var.manifest_sha256 == filesha256("${path.module}/../../config/model.locked.json")
    error_message = "Manifest hash must match this checkout's config/model.locked.json. Rebuild the image when the locked manifest changes."
  }
}
variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "inference_environment" {
  type    = map(string)
  default = {}
}
