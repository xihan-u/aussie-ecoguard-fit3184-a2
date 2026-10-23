# Personal GCP deployment stages

This root manages **ecoguard-fit3184-a2-2026**, project number
**995070689587**, in `us-central1`. Seven identity resources have actually been
applied from `fdfaf23`; their exact provider, single service-account grant and
zero user-managed keys were verified. See the [actual deployment report](../../../../docs/c-personal-foundation-deployed-20261024.md).
The AWS application remains paused. Token exchange and cloud inference remain
unverified.

The current source prepares two later increments. **Neither has been planned or
applied in the real cloud.** The default stage is `identity`; committing this
source does not activate compute. The child module's historical
`deployment.auto.tfvars` is not loaded by this separate root.

## Existing state and source custody

The authoritative personal backend is the existing GCP CloudShell workspace
`~/ecoguard-c-personal-20261023/source/infra/gcp/environments/personal/state/terraform.tfstate`.
Its checkout remains at `fdfaf23` until an operator deliberately prepares the next
plan. Preserve the private post-apply backup and use one operator. Git does not
share state. Do not create a second owner, copy/import the historical team's
state, or initialize this local clone and apply against an empty state.

Before a future plan, verify the operator, exact project ID/number, default
Terraform workspace, current source, state lineage/serial and backup. Update the
state-owning checkout only as a controlled step; use the signed provider lock,
not an upgrade. Keep full plans, JSON, logs and backups in ignored `private/`.

## Bounded increments

| Stage | Expected transition | New managed resources |
| --- | --- | --- |
| `identity` (default) | Existing seven remain | None |
| `registry` | Seven no-ops, two creates; nine total | Artifact Registry API and private Docker repository |
| `private-inference` | Nine no-ops, four creates; thirteen total | Run API, dedicated runtime account, service and one service-level invoker grant |

The stages preserve existing addresses. The personal route omits the unused GCS
model bucket, storage API and bucket-reader grant: the unchanged locked manifest
uses pinned HTTPS artifacts with exact byte/hash verification. Historical shared
module defaults retain their previous model storage and deletion protection.

The personal image is empty before `private-inference`. That stage requires
`us-central1-docker.pkg.dev/ecoguard-fit3184-a2-2026/ecoguard/inference@sha256:<64 lowercase hex>`.
Tags and other registries/paths are rejected. Publish and independently verify
the actual image before making its service plan. No image was published by the
local preparation batch.

The root fixes the actual AWS account/role/region, Cognito issuer/client, media
bucket and manifest hash. It permits no arbitrary environment override. Existing
WIF access remains limited to normalized assumed role
`arn:aws:sts::011154879765:assumed-role/ecoguard3184-personal-lambda` and existing
`ecoguard-aws-invoker@ecoguard-fit3184-a2-2026.iam.gserviceaccount.com`.
CloudShell/root is not this runtime role; do not broaden trust to simplify tests.

The future service explicitly checks invoker IAM. Its sole new grant is
`roles/run.invoker` on `ecoguard-inference` to that existing invoker account.
There is no public or project-wide grant. The dedicated runtime account receives
no new IAM role. The service uses four CPUs, 8 GiB, request concurrency one,
minimum zero, automatic service/revision maximum one, request timeout 360s and application deadline
240s. These are reviewed limits, not proven cloud performance or a hard cost cap.

Personal deletion protection is explicitly false so a bounded test can be
cleaned up through a separately reviewed reverse plan. After leaving identity,
**pass the intended stage and image to every plan**. Terraform does not remember
previous input values: omitting them can propose deleting later resources. Never
accept those deletes as a routine update. Keep an ignored private var-file or
supply both inputs explicitly, and review the saved plan every time.

## Offline plan gates

The original `check_plan.py` is frozen for the first seven-create plan at
`fdfaf23`. It intentionally rejects existing state and must not be loosened or
used for these increments. Its earlier commands and actual result are recorded
in the [first-plan review](../../../../docs/c-personal-first-plans-20261024.md).

The separate `check_runtime_plan.py` reviews private `terraform show -json`
output for exactly one forward increment:

```sh
python3 infra/gcp/environments/personal/check_runtime_plan.py \
  --stage registry \
  --plan-json infra/gcp/environments/personal/private/registry.json
```

For a private-inference plan, additionally supply `--stage private-inference`
and `--image` with the independently verified full registry digest. The gate
requires exact prior/new addresses, unchanged existing identities and resources,
known security settings, an immutable image, the exact service account/member,
authentication, environment and resource limits. Drift, imports, replacements,
updates, deletes, extra resources and command/volume overrides are rejected.
The [preparation evidence](../../../../evidence/c-private-inference-prepared-20261024.json) records the actual local checks.
Inspect the textual saved plan too, freeze its binary hash and recheck the live
identity/state immediately before applying that same binary.

Exit 0 only confirms offline constraints; it does not authorize apply, verify
funding or image provenance, or prove cloud operation. New runtime access and
funded testing require a concrete execution review. Google can initialize its
own service agents when APIs are enabled; include that setup in the review.

## Actual local checks and remaining work

The prepared source passed Terraform **1.17.0** / Google **7.46.1** validation in
a Linux amd64 container using official archives matched to the reviewed hashes,
with networking disabled: **zero errors and warnings**. The earlier macOS
provider startup failed before schema checking; the Linux result resolves that
local validation gap. All **38 GCP offline tests** passed, including 23 new
increment regressions. These tests use synthetic plans; no real increment plan
or cloud apply has occurred.

```sh
python3 -m unittest discover -s infra/gcp/tests -v
```

A separate [real local model smoke](../../../../docs/c-local-real-model-smoke-20261024.md)
passed using predownloaded weights and a public image. It does not establish
Cloud Run's in-memory cache envelope, cold download deadline, authenticated warmup,
concurrency, video processing or Lambda-role federation. Complete those actual
checks before application activation and retain failed attempts.

Existing Google credits expire **28 October**. The additional personal-spend
budget remains **A$0**. Reverify eligible funding and define bounded tests plus
cleanup no later than 27 October Melbourne, unless a separately verified funded
period is available. Minimum zero does not remove image-storage charges. There
is no automatic cleanup or guaranteed account-wide spend stop. A return to
`registry` or `identity` is a destructive reverse increment that needs its own
reviewed plan, retained artifacts and state backup; the forward gate rejects it.

Prepared with Codex assistance; no next-stage cloud resources were created by
this source-preparation batch.
