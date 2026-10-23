# Personal GCP identity-only preparation

This separate root reuses `infra/gcp` for **ecoguard-fit3184-a2-2026**, project
number **995070689587**, in `us-central1`. It fixes `identity_only=true` and leaves
all image, Cognito, media and runtime environment inputs empty. The child module's
historical `deployment.auto.tfvars` is not loaded. The locked manifest SHA-256 is
`639595e1e9ffe18cb11ead1c7480ffe7a31bf767f6cbaf6b8375829227a569ae`.

Committing this root creates no IAM resources or trust. The intended AWS identity
is account **011154879765**, role **ecoguard3184-personal-lambda**, AWS region
`us-east-1`. That role has not yet been created or verified by this preparation.
Before planning, independently verify the Google project ID/number and
authenticated operator, and review the intended role ARN against the separate
AWS plan. A read-only identity plan may refer to that not-yet-created role.
After AWS creation, verify the actual role ARN before applying Google trust.
An AWS root-user session is not the permitted runtime identity.

The proposed provider accepts only that AWS account and the normalized assumed-role
ARN `arn:aws:sts::011154879765:assumed-role/ecoguard3184-personal-lambda`.
The sole grant is `roles/iam.workloadIdentityUser` on
`ecoguard-aws-invoker@ecoguard-fit3184-a2-2026.iam.gserviceaccount.com`, for that
role's `attribute.aws_role` principal set in this project's `ecoguard-aws` pool.
It grants no project-wide roles, service account keys, public access or Cloud Run
invocation role. Real token exchange and caller rejection remain unverified.

## State and first-plan review

Always run from this root, using the default Terraform workspace. Its ignored
local backend is `state/terraform.tfstate` inside this directory, separate from
the historical root. Agree on one operator and private state backup/custody;
Git does not share Terraform state. Do not copy/import old state, migrate an old
backend or apply against `infra/gcp`. If personal managed state already exists,
stop using the first-plan checker and review that existing deployment instead.

After verifying the Google identity and reviewing the intended AWS role, the
review commands from the repository root are:

```sh
terraform -chdir=infra/gcp/environments/personal init -input=false -lockfile=readonly
terraform -chdir=infra/gcp/environments/personal validate
terraform -chdir=infra/gcp/environments/personal workspace show
```

Keep plans and JSON private. The following `private/` directory is ignored:

```sh
umask 077
mkdir -p infra/gcp/environments/personal/private
chmod 700 infra/gcp/environments/personal/private
terraform -chdir=infra/gcp/environments/personal plan -input=false \
  -out=private/first-identity.tfplan
terraform -chdir=infra/gcp/environments/personal show -json \
  private/first-identity.tfplan > infra/gcp/environments/personal/private/first-identity.json
python3 infra/gcp/environments/personal/check_plan.py \
  --plan-json infra/gcp/environments/personal/private/first-identity.json
```

The expected first plan has **7 creates, 0 updates, 0 deletes, 0 replacements**:
three identity API service resources, the invoker service account, pool, AWS
provider and one service-account IAM member. The three APIs were enabled outside
Terraform earlier; the resources bring their enabled state under this root's
management. `disable_on_destroy=false` preserves those API enablements.

The offline gate rejects a different project/number or AWS identity, broad or
unresolved trust, any additional compute/storage/registry/IAM resource, imports,
prior managed state and incomplete plans. The shared module constructs the same
canonical service-account and principal names from configured IDs and the read
project number, retaining resource dependencies. This makes those exact security
fields visible in the first plan instead of depending on computed resource names.
Historical resource addresses, roles, mapping and conditions are unchanged.

Exit 0 confirms only these offline checks; 1 means rejected checks and 2 means
invalid/incomplete input. It does not authorize applying, verify the AWS role,
prove Google permissions or establish a working cross-cloud deployment. Review
the textual plan too. No saved plan or apply has been performed by this preparation.
A runtime deployment requires a different reviewed plan and verified funding;
this root creates no Cloud Run service, model bucket or image registry.

The provider lock retains the shared root's Google 7.46.1 checksums and adds the
verified macOS arm64 checksum. Local `terraform validate` passed with Terraform
1.17.0 and the signature-verified Google provider 7.46.1. All 15 GCP offline tests
passed, including nine new first-plan checks and the six existing identity checks.
Run the focused regressions without cloud SDKs or Terraform:

```sh
python3 -m unittest discover -s infra/gcp/tests -v
```
