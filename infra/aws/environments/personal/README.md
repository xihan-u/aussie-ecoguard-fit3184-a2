# Personal AWS environment: reviewable preparation only

This root reuses `infra/aws` for account **011154879765 / us-east-1** under
`ecoguard3184-personal`. It does not deploy by being committed or pushed. No
creation, role change, cross-cloud trust change or application resume has been
performed by this preparation. The account's Free plan and credits were checked
in the console separately; service eligibility, available credits and A$0 extra
personal spend must still hold when a deployment is authorized.

The historical course root and its `deployment.auto.tfvars` remain intact.
Terraform does not load a child module's auto tfvars. This root explicitly sets
the account allowlist, region, dedicated role and all paused runtime inputs; it
does not expose a runtime-enable switch. Oracle URL, worker image and Lex IDs
remain empty. The default API endpoint, every Lambda, queue consumer, maintenance
schedule, public registration and S3 data access are paused in the proposed stack.

## State, account and package prerequisites

- Always work from this root with `terraform -chdir=infra/aws/environments/personal`.
  Its local backend is **`state/terraform.tfstate` inside this directory**. This is
  an ignored private file, separate from the course root. Keep a private backup;
  pushing Git does not share state. Only one operator may manage this local
  backend at a time. Agree on state custody before another teammate applies.
- Use the default Terraform workspace. Do not copy/import course state, migrate
  its backend, use `-migrate-state`, or override this backend with an old path.
  `TF_DATA_DIR` alone only separates plugin data and does not separate state.
  If this personal state already contains resources, stop using the first-plan
  checker and review the existing state's ownership and current deployment.
- Locally select the verified `ecoguard-personal` AWS profile; in the already
  verified CloudShell use its existing identity without that local profile.
  Immediately before planning, check STS returns **011154879765**. The provider's
  `allowed_account_ids` also rejects other accounts. Browser login alone does not
  authenticate a local CLI.
- `lambda_zip` has no default. Supply the absolute POSIX path of the **real,
  reviewed Linux/Python 3.12 package**, containing the app, domain module and
  locked Linux dependencies. Missing/relative paths are rejected. No sample or
  empty ZIP is provided. The first-plan checker also checks the local archive,
  its basic contents, integrity, size and SHA-256 against every planned function.
  This does not prove model behavior or dependency/runtime compatibility.
- Review the packaged `config/google-wif.json` before any future activation:
  the repository's historical JSON targets another Google project/account.
  This paused AWS preparation does not authorize changing GCP trust. Complete
  the separately approved personal-account WIF and Oracle wiring, regenerate the
  public JSON, then rebuild the ZIP before runtime can be enabled.

The shared module intentionally does not create the S3 bucket because of the
historical course SCP workaround. The planned bucket settings target only
`ecoguard3184-personal-011154879765-media`. A separately authorized deployment
must create/verify ownership and region of that exact new bucket before applying
its settings. No bucket bootstrap or creation is performed here. Likewise,
`terraform plan` does not prove permission to create roles or to pass them.

## Plan procedure after prerequisites are satisfied

These are review steps for a future authorized session, not evidence that a plan
has been run. Terraform 1.10+ and the locked AWS provider are required. Run from the
repository root. On a local computer, prefix Terraform/STS commands with
`AWS_PROFILE=ecoguard-personal`; omit that prefix in the verified CloudShell.
Do not put access keys into Terraform inputs or files in this directory.

```sh
aws sts get-caller-identity --region us-east-1 --query Account --output text
terraform -chdir=infra/aws/environments/personal init -input=false -lockfile=readonly
terraform -chdir=infra/aws/environments/personal validate
terraform -chdir=infra/aws/environments/personal workspace show
```

The workspace must be `default`. Create `private/` in this root with permissions
0700 and use `umask 077` before saving plans; the directory is ignored. Set
`ECOGUARD_LAMBDA_ZIP` to the already built archive's absolute path, then:

```sh
terraform -chdir=infra/aws/environments/personal plan -input=false \
  -var="lambda_zip=$ECOGUARD_LAMBDA_ZIP" -out=private/first-paused.tfplan
terraform -chdir=infra/aws/environments/personal show -json \
  private/first-paused.tfplan > infra/aws/environments/personal/private/first-paused.json
python3 infra/aws/environments/personal/check_plan.py \
  --plan-json infra/aws/environments/personal/private/first-paused.json
```

Review the ordinary textual plan too. Plan/state JSON can contain private values;
never commit or paste it. The checker prints only named checks and public account
metadata. Exit 0 means the offline first-plan and local archive checks passed;
1 means checks failed; 2 means invalid/incomplete input or archive. None authorizes
an apply or proves cloud permissions, credit coverage or acceptance.

For a clean first deployment with the current fixed inputs, the expected plan is
**53 creates, 0 updates, 0 deletes, 0 replacements**. The bucket itself is outside
that count. The checker rejects imports, prior managed state, unexpected resource
addresses, account/region drift, runtime activation, broad IAM grants and an
unavailable/changed archive. Do not loosen the checker to accept an unexpected
plan. A later worker/Oracle/Lex deployment needs a new reviewed plan and a gate
that matches that separately authorized scope; this gate intentionally blocks it.

There is no `apply` command in this preparation. Deployment authorization and a
review of the concrete saved plan remain prerequisites. A fresh plan must replace
a stale one after configuration, package, state or account changes.

## Runtime role scope and SDK mapping

`manage_execution_role` defaults to false in the shared module, preserving the
course's existing-role/LabRole behavior. Only this personal root opts in. It
creates `ecoguard3184-personal-lambda`, trusted solely by Lambda, and the inline
`ecoguard3184-personal-runtime` policy. It never modifies `LabRole`. Both ZIP and
future ingest Lambdas explicitly wait for this inline policy as well as their log
groups, so SQS event-source creation does not race missing runtime permissions.
The root calls the legacy provider-containing module once, without module-level
`depends_on`, `count`, `for_each` or a provider alias.

| Actual use | Runtime permission boundary |
| --- | --- |
| `repository.py`: GetItem, Query, Scan; TransactWriteItems Put/Delete members | GetItem/Query/Scan/PutItem/DeleteItem on the exact five project table ARNs. Transaction members use the underlying IAM actions, not an invented TransactWriteItems IAM action. No table administration. |
| `storage.py`: head/get/put/copy/delete and list current/versioned keys | Exact dedicated bucket: ListBucket/ListBucketVersions; object GetObject/GetObjectVersion/PutObject/DeleteObject/DeleteObjectVersion. Copy uses source-read and destination-write. No bucket-policy administration. |
| `AwsQueue.send` and Lambda SQS polling | SendMessage/ReceiveMessage/DeleteMessage/GetQueueAttributes on the four project work queues, without DLQ, purge or queue-management rights. |
| `SnsNotifier`: per-user topic, confirmation lookup, email subscribe, publish | Only `${prefix}-user-*` topics in this account/region; Subscribe additionally requires `sns:Protocol=email`. No account-wide topic/subscription inventory or SNS administration. |
| `Preprocessor.detect_labels`: image bytes | Only `rekognition:DetectLabels`; this API has no resource-level target, so Resource `*` is restricted by `aws:RequestedRegion=us-east-1`. This is the policy's only global resource wildcard. |
| Lambda process logs | CreateLogStream/PutLogEvents only under its seven exact project log groups. Terraform creates the groups; runtime cannot create groups. |
| `LexClient.recognize`: not configured in this root | No Lex grant while IDs are empty. The shared policy adds only RecognizeText on the exact bot-alias ARN when both reviewed IDs are present. Lex model deployment and its separate service role are outside this runtime policy. |
| `api.py`: Cognito GetUser with the forwarded access token | Token-authorized operation, not an IAM administrative operation; no Lambda Cognito admin grant. |
| WIF signed STS GetCallerIdentity then Google token exchange | No static cloud keys, AWS role-creation, PassRole or cross-cloud grant in the runtime policy. Google must separately allow this exact account/role. |

The deployment caller, separately from the runtime role, needs the approved
project infrastructure actions, role create/read/tag and inline-policy actions,
plus PassRole limited to the exact new runtime role for `lambda.amazonaws.com`.
The runtime role has no IAM/ECR write, billing, CloudFormation or other-project
permissions. This shared application role is a scoped starting point; it does not
claim per-function separation. The existing private S3 policy and API/application
authorization still enforce media visibility.

## What this preparation has and has not verified

The current account check found no matching EcoGuard roles/buckets or matching
Lambda/ECR/Cognito/API resources in us-east-1 and ap-southeast-2. That is an
inventory of those names/services/regions, not an account-wide emptiness claim.
On 2026-10-23, the eight focused standard-library checks and independent static
review passed. `terraform validate` also passed on macOS arm64 using Terraform
1.17.0 and the officially signed AWS provider 6.67.0. The personal provider lock
includes that platform's additional checksum; the course lock is unchanged.
The full AWS test suite was not completed in this local Python environment:
one existing shutdown check requires the unavailable `botocore` package.
A real saved plan, role creation, bucket bootstrap, deploy/apply, runtime tests,
Oracle and WIF all remain unperformed.

Run the focused offline checker regression without cloud access or extra packages:

```sh
python3 -m unittest discover -s infra/aws/tests -p test_personal_plan.py -v
```

After deployment is separately authorized, do not use the course-specific
`scripts/check-project-shutdown.py` as proof of this personal stack's suspension:
it intentionally checks the old account and prefix. Prepare a reviewed personal
restore/verification procedure before activation. Pausing retains storage and
does not by itself guarantee a zero bill.
