terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 6.0, < 7.0" }
  }
  # Relative to THIS root, never infra/aws or the course deployment's state.
  backend "local" {
    path = "state/terraform.tfstate"
  }
}

variable "lambda_zip" {
  type        = string
  description = "Absolute POSIX path to the real, reviewed Linux Python 3.12 Lambda ZIP; no default or placeholder archive."
  validation {
    condition     = startswith(var.lambda_zip, "/") && endswith(var.lambda_zip, ".zip") && fileexists(var.lambda_zip)
    error_message = "Supply an existing real .zip via its absolute POSIX path. Build and review the actual Lambda package first."
  }
}

# infra/aws contains its own provider. This legacy-provider module must remain
# a single unconditional call: no count, for_each, depends_on or provider alias.
# Child modules do not load deployment.auto.tfvars from the child's directory.
module "ecoguard" {
  source = "../.."

  allowed_account_ids   = ["011154879765"]
  region                = "us-east-1"
  prefix                = "ecoguard3184"
  environment           = "personal"
  manage_execution_role = true
  execution_role_arn    = ""
  deploy_api            = true
  runtime_enabled       = false
  lambda_zip            = var.lambda_zip

  model_manifest_version = "ecoguard-models-2026-10-08-v3"
  frontend_origins       = ["http://localhost:5173", "http://127.0.0.1:5173"]
  web_url                = "http://127.0.0.1:5173"
  worker_image           = ""
  inference_url          = ""
  google_invoker_email   = ""
  lex_bot_id             = ""
  lex_alias_id           = ""
}

output "deployment_identity" {
  value = { account_id = module.ecoguard.account_id, region = module.ecoguard.region }
}
output "execution_role_arn" { value = module.ecoguard.execution_role_arn }
output "media_bucket" { value = module.ecoguard.media_bucket }
output "api_url" { value = module.ecoguard.api_url }
output "cognito_user_pool_id" { value = module.ecoguard.cognito_user_pool_id }
output "cognito_client_id" { value = module.ecoguard.cognito_client_id }
output "worker_repository_url" { value = module.ecoguard.worker_repository_url }
output "runtime_enabled" { value = module.ecoguard.runtime_enabled }
output "processing_enabled" { value = module.ecoguard.processing_enabled }
