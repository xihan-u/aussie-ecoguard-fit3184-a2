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
does not expose a runtime-enable switch. Protected inference URL, worker image and Lex IDs
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
- For a local CLI, first configure and independently verify the intended
  `ecoguard-personal` AWS profile; this task has not installed local AWS keys or
  a local profile. In the verified CloudShell, use its existing identity without
  that local profile.
  Immediately before planning, check STS returns **011154879765**. The provider's
  `allowed_account_ids` also rejects other accounts. Browser login alone does not
  authenticate a local CLI.
- `lambda_zip` has no default. Supply the absolute POSIX path of the **real,
  reviewed Linux/Python 3.12 package**, containing the app, domain module and
  locked Linux dependencies. Missing/relative paths are rejected. No sample or
  empty ZIP is provided. The first-plan checker also checks the local archive,
  its basic contents, integrity, size and SHA-256 against every planned function.
  It also rejects historical WIF identities and arbitrary credential sources.
  This does not prove model behavior or dependency/runtime compatibility.
- Review the packaged `config/google-wif.json` before any future activation:
  the repository's historical JSON targets another Google project/account.
  This paused AWS preparation does not authorize changing GCP trust. The new
  public external-account JSON can describe the intended personal provider
  before it exists; that is configuration preparation, not working federation.
  Complete the personal-account WIF and protected inference wiring before any
  future runtime activation.

The personal root opts into creation of
`ecoguard3184-personal-011154879765-media`, with `force_destroy=false`, explicit
`BucketOwnerEnforced` ownership and the existing private/encrypted/TLS/CORS
settings. No separate bucket bootstrap is required. The shared module keeps
bucket creation disabled by default to preserve the historical course SCP
workaround. A plan does not prove permission to create the bucket, create roles
or pass them; a conflicting existing bucket or access denial needs review.

## Portable local ZIP preparation

`scripts/build_lambda_zip.py` uses a fresh temporary stage and a caller-reviewed
**existing local image ID**, never a tag or a registry pull. It installs only
`services/aws/requirements.lock.txt`, with hashes, binary wheels and explicit
CPython 3.12 / manylinux x86_64 targets. The Lambda ZIP uses AWS's managed Python
bootstrap; the separate container RIC lock and ffmpeg binaries are not copied.
The app/domain modules and frozen calibration are copied without bytecode.
The old Windows recipe and historical `config/google-wif.json` remain intact;
this helper requires an explicit reviewed WIF path and never uses that default.

Prepare the public JSON outside Git with the standard AWS external-account
format, audience
`//iam.googleapis.com/projects/995070689587/locations/global/workloadIdentityPools/ecoguard-aws/providers/aws-role`,
the fixed AWS metadata source from `scripts/lambda_wif.py`, and the Google STS
token URL. If an impersonation URL is present it must name
`ecoguard-aws-invoker@ecoguard-fit3184-a2-2026.iam.gserviceaccount.com`.
Other credential types, source files/executables, arbitrary URLs, extra fields
and duplicate JSON keys are rejected. This public document contains no keys or
tokens. The intended trusted AWS role is
`arn:aws:iam::011154879765:role/ecoguard3184-personal-lambda`; preparing this
document does not create that role or any GCP trust.

From the repository root, use the full `sha256:...` image ID independently
reviewed from the already-built Linux amd64 ingest image:

```sh
python3 scripts/build_lambda_zip.py \
  --image-id "$ECOGUARD_REVIEWED_IMAGE_ID" \
  --wif-config /absolute/path/to/reviewed-personal-wif.json \
  --output build/aws-personal-lambda.zip --dry-run
```

The default is print-only with no Docker calls, downloads or writes. After
review, replace `--dry-run` with `--build`. Existing output files are refused;
choose a new versioned filename for another build. Bind paths containing commas
or control characters and source symlinks are rejected. Only the dependency
lock and fresh package stage are mounted into Docker, without host credentials
or the whole checkout. The install downloads wheels; a second container then
uses `--network none`, a read-only stage and `python -S` to test imports/native
libraries without falling back to image site-packages. No handlers run. The
deterministic archive creator enforces the Lambda unpacked size, and this helper
enforces the personal gate's 50 MiB direct-upload limit before publishing output.
The owned temporary stage is cleaned even on failure. These are local checks,
not evidence of AWS execution, federation, models or cloud acceptance.

## Plan procedure after prerequisites are satisfied

These commands describe the review procedure. The actual first saved plan and
its checks are recorded in [the 24 October review](../../../../docs/c-personal-first-plans-20261024.md);
no apply has occurred. Terraform 1.10+ and the locked AWS provider are required. Run from the
repository root. On a local computer, prefix Terraform/STS commands with
`AWS_PROFILE=ecoguard-personal` only after configuring/verifying that profile;
omit that prefix in the verified CloudShell.
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
**55 creates, 0 updates, 0 deletes, 0 replacements**, including the new bucket
and its ownership control. The checker rejects imports, prior managed state,
unexpected resource addresses, account/region drift, runtime activation, broad IAM grants and an
unavailable/changed archive. Do not loosen the checker to accept an unexpected
plan. A later worker/inference/Lex deployment needs a new reviewed plan and a gate
that matches that separately authorized scope; this gate intentionally blocks it.

All seven ZIP functions must name the known exact execution role
`arn:aws:iam::011154879765:role/ecoguard3184-personal-lambda`; a missing/unknown
ARN or a different role is rejected even when the intended role also appears in
the plan. That role must use path `/`. The bucket checks require all four public
access blocks, default AES256 encryption, unconditional paused data-access denial
and the full bucket/object TLS denial. S3 and HTTP API CORS must keep the two
explicit local frontend origins and their reviewed method sets; wildcard or
additional origins/methods fail. These checks inspect planned configuration;
they do not claim live IAM, HTTPS or browser verification.

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

On 2026-10-23, CloudShell reverified account 011154879765 in us-east-1. Its fresh
name/prefix inventory found no matching EcoGuard IAM roles or global S3 buckets,
or matching us-east-1 Lambda, ECR, DynamoDB, SQS, SNS, EventBridge, API Gateway,
Cognito or CloudWatch Logs resources, without API errors. An earlier narrower
Lambda/ECR/Cognito/API check also covered ap-southeast-2. These checks describe
those names/services/regions, not an account-wide emptiness claim.
The fifteen focused first-plan tests and nine packaging-helper tests passed
locally without cloud access or dependency downloads. `terraform validate`
also passed for the new bucket/ownership configuration on macOS arm64 using Terraform
1.17.0 and the officially signed AWS provider 6.67.0. The personal provider lock
includes verified macOS arm64 and Linux amd64 checksums; the course lock is unchanged.
The expanded 25-test AWS infrastructure suite and nine packaging checks passed
in the reviewed local ingest image with networking disabled, including the
existing shutdown checks that require `botocore`.
The real new ZIP build passed: 3,998 files, 72,766,834 bytes unpacked and
33,286,409 bytes compressed, SHA-256
`fafb94bf948312f1fef8998b5619567ad3c3471381a34e9e816cec87b034d9f6`.
The helper's staged package imports and native-library operations passed in a
network-disabled `python -S` container, using the actual staged dependencies.
A real saved plan subsequently passed 28/28 checks in AWS CloudShell, with
55 creates and no updates or deletes. See the linked 24 October review for its
exact source and hashes. Role/bucket creation, deploy/apply, runtime tests,
protected inference and WIF remain unperformed.

Run the focused offline checker regression without cloud access or extra packages:

```sh
python3 -m unittest discover -s infra/aws/tests -p test_personal_plan.py -v
```

After deployment is separately authorized, do not use the course-specific
`scripts/check-project-shutdown.py` as proof of this personal stack's suspension:
it intentionally checks the old account and prefix. Prepare a reviewed personal
restore/verification procedure before activation. Pausing retains storage and
does not by itself guarantee a zero bill.
