variable "region" {
  type    = string
  default = "us-east-1"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "prefix" {
  type    = string
  default = "ecoguard3184"
}
variable "manage_media_bucket" {
  type        = bool
  description = "Opt in to a new Terraform-managed media bucket and BucketOwnerEnforced ownership. False preserves the course's externally bootstrapped bucket."
  default     = false
}
variable "frontend_origins" {
  type    = list(string)
  default = ["http://localhost:5173", "http://127.0.0.1:5173"]
}
variable "execution_role_arn" {
  type        = string
  description = "Existing execution role. Learner Lab normally permits LabRole; record its broader permissions."
  default     = ""
}
variable "manage_execution_role" {
  type        = bool
  description = "Opt in to a dedicated project Lambda role. False preserves the existing-role/LabRole behavior."
  default     = false
  validation {
    condition     = !var.manage_execution_role || var.execution_role_arn == ""
    error_message = "Choose either manage_execution_role=true or an existing execution_role_arn, not both."
  }
}
variable "allowed_account_ids" {
  type        = list(string)
  description = "AWS provider account allowlist. Empty preserves historical behavior; new environments must set an explicit account."
  default     = []
  validation {
    condition     = alltrue([for account in var.allowed_account_ids : can(regex("^[0-9]{12}$", account))])
    error_message = "Each allowed account ID must contain exactly 12 decimal digits."
  }
}
variable "deploy_api" {
  type    = bool
  default = false
}
variable "runtime_enabled" {
  type        = bool
  description = "Reversible runtime/access pause. Keep deploy_api and all existing resource inputs unchanged; false retains resources and data."
  default     = true
}
variable "lambda_zip" {
  type    = string
  default = "../../build/aws-lambda.zip"
}
variable "worker_image" {
  type        = string
  description = "Immutable ECR image digest containing FFmpeg. Empty keeps preprocessing disabled."
  default     = ""
}
variable "inference_url" {
  type    = string
  default = ""
}
variable "google_invoker_email" {
  type    = string
  default = ""
}
variable "web_url" {
  type    = string
  default = "http://127.0.0.1:5173"
}
variable "model_manifest_version" {
  type    = string
  default = "ecoguard-models-2026-10-08-v3"
}
variable "lex_bot_id" {
  type    = string
  default = ""
}
variable "lex_alias_id" {
  type    = string
  default = ""
}
