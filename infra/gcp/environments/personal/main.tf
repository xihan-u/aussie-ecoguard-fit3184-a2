terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    google = { source = "hashicorp/google", version = ">= 6.0, < 8.0" }
  }
  backend "local" {
    path = "state/terraform.tfstate"
  }
}

# The existing provider-containing module must stay unconditional. Child-module
# deployment.auto.tfvars are not loaded by this separate root.
module "ecoguard" {
  source = "../.."

  project_id            = "ecoguard-fit3184-a2-2026"
  identity_only         = true
  region                = "us-central1"
  prefix                = "ecoguard3184"
  aws_account_id        = "011154879765"
  aws_role_name         = "ecoguard3184-personal-lambda"
  aws_region            = "us-east-1"
  manifest_sha256       = "639595e1e9ffe18cb11ead1c7480ffe7a31bf767f6cbaf6b8375829227a569ae"
  image                 = ""
  cognito_issuer        = ""
  cognito_client_id     = ""
  media_bucket          = ""
  inference_environment = {}
}

output "deployment_identity" {
  value = {
    project_id     = module.ecoguard.project_id
    project_number = tostring(module.ecoguard.project_number)
  }
  precondition {
    condition     = tostring(module.ecoguard.project_number) == "995070689587"
    error_message = "The personal root requires project number 995070689587. Stop if the project identity differs."
  }
}
output "invoker_service_account" { value = module.ecoguard.invoker_service_account }
output "wif_provider_audience" { value = module.ecoguard.wif_provider_audience }
