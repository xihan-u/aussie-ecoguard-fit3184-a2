# Personal GCP deployment stages

This root manages **ecoguard-fit3184-a2-2026**, project number
**995070689587**, in `us-central1`. It now has **nine managed resources**: the
seven deployed identity resources plus the approved Artifact Registry API and
private `us-central1/ecoguard` repository. The registry apply exited zero and its
live verification passed; see the [registry deployment report](../../../../docs/c-registry-deployed-20261024.md).
The original identity provider, single service-account grant and zero
user-managed keys remain verified in the [foundation report](../../../../docs/c-personal-foundation-deployed-20261024.md).
The AWS application remains paused. Token exchange and cloud inference remain
unverified.

The registry saved plan passed **12/12 checks**, with two creates and seven no-ops,
and was subsequently applied under its matching approval. The repository was
empty at the post-apply check. The approved inference image has since been
published and its actual manifest/config bytes verified; see the
[image publication report](../../../../docs/c-private-image-published-20261024.md).
The second real private-inference saved plan now passed **13/13 checks** with
four creates, nine no-ops and no drift, warnings or unknown security fields;
see the [private-service plan review](../../../../docs/c-private-inference-saved-plan-review-20261024.md).
It has not been applied or authorized for execution. The earlier
[saved-plan review](../../../../docs/c-registry-saved-plan-review-20261024.md)
and deployment reports retain their respective historical observations.
The default stage is `identity`; committing this source does not activate compute. The child module's historical
`deployment.auto.tfvars` is not loaded by this separate root.

## Existing state and source custody

The authoritative personal backend is the existing GCP CloudShell workspace
`~/ecoguard-c-personal-20261023/source/infra/gcp/environments/personal/state/terraform.tfstate`.
After the exact state-only publication metadata refresh at `00d58e0`, the
controlled checkout moved to `3dd63c8` for the second private-service plan.
The current state still has nine resources, serial 12. The verified checkpoint
retains private A/B backups; state, lock and `.gitignore` were unchanged across
the source transition. Preserve that checkpoint and use one operator. Git does not
share state. Do not create a second owner, copy/import the historical team's
state, or initialize this local clone and apply against an empty state.

Before a future plan, verify the operator, exact project ID/number, default
Terraform workspace, current source, state lineage/serial and backup. Update the
state-owning checkout only as a controlled step; use the signed provider lock,
not an upgrade. Keep full plans, JSON, logs and backups in ignored `private/`.

## Bounded increments

| Stage | Expected transition | New managed resources |
| --- | --- | --- |
| `identity` (default) | Historical seven-resource baseline; returning from nine proposes removal | None |
| `registry` | Applied: seven no-ops, two creates; current nine total | Artifact Registry API and private Docker repository |
| `private-inference` | Real plan passed: nine no-ops, four creates; thirteen proposed total, not applied | Run API, dedicated runtime account, service and one service-level invoker grant |

The stages preserve existing addresses. The personal route omits the unused GCS
model bucket, storage API and bucket-reader grant: the unchanged locked manifest
uses pinned HTTPS artifacts with exact byte/hash verification. Historical shared
module defaults retain their previous model storage and deletion protection.

The personal image is empty before `private-inference`. That stage requires
`us-central1-docker.pkg.dev/ecoguard-fit3184-a2-2026/ecoguard/inference@sha256:<64 lowercase hex>`.
Tags and other registries/paths are rejected. The separately approved publication
verified this actual immutable image URI:

`us-central1-docker.pkg.dev/ecoguard-fit3184-a2-2026/ecoguard/inference@sha256:7e481399309c8a90276c864e9765545657e44c00e9061ee668b4e56db4f22fdb`

The raw remote manifest/config matched the reviewed archive. The subsequent
private-service plan verified that provenance through its exact metadata refresh
checkpoint. State remains at nine resources; runtime approval and cloud inference
remain outstanding.

The root fixes the actual AWS account/role/region, Cognito issuer/client, media
bucket and manifest hash. It permits no arbitrary environment override. Existing
WIF access remains limited to normalized assumed role
`arn:aws:sts::011154879765:assumed-role/ecoguard3184-personal-lambda` and existing
`ecoguard-aws-invoker@ecoguard-fit3184-a2-2026.iam.gserviceaccount.com`.
CloudShell/root is not this runtime role; do not broaden trust to simplify tests.

The proposed service explicitly checks invoker IAM and HTTP/1 on port 8080.
Its sole new grant is
`roles/run.invoker` on `ecoguard-inference` to that existing invoker account.
Invoker access adds no public or project-wide invoker role. The dedicated runtime account receives
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

Exit 0 only confirms offline constraints. This plan's provenance and refresh
checkpoint were additionally checked against retained successful evidence;
funding and runtime operation still require separate verification. A new actual
approval must cover the exact four-create saved binary, service invoker access,
startup compute and Google's automatic Run service agent with
`roles/run.serviceAgent`. The prepared apply/HTTP helpers do not confer approval.
If approved separately, bounded HTTP testing consists of anonymous health,
operator-authenticated health and one authenticated warmup. A cold warmup may
download 15 files totaling 2,229,943,281 bytes; none has run under this plan.

## Actual local checks and remaining work

The prepared source passed Terraform **1.17.0** / Google **7.46.1** validation in
a Linux amd64 container using official archives matched to the reviewed hashes,
with networking disabled: **zero errors and warnings**. The earlier macOS
provider startup failed before schema checking; the Linux result resolves that
local validation gap. All **38 GCP offline tests** passed, including 23 new
increment regressions. These regression tests use synthetic plans. A separate
real registry plan passed its 12 checks and the approved apply now completed,
with nine-resource state and live configuration verification. The actual image
publication then passed remote digest/byte verification without changing that
state or IAM. The first private-service plan was retained as blocked (11/13)
because of an unknown protocol name and publication metadata drift. Explicit
`http1` and a separate exact state-only refresh resolved those issues without
weakening the gate. The second real plan passed 13/13 with the existing nine
resources unchanged; its concrete source, plan hash and checkpoint chain are in
the linked plan review. No private-service apply or HTTP warmup has occurred.

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
is no automatic cleanup or guaranteed account-wide spend stop. Stepping back to
an earlier stage is a destructive reverse increment that needs its own reviewed
plan, retained artifacts and state backup; the forward gate rejects it.

Source/evidence delivery now targets the approved
[private repository](https://github.com/xihan-u/aussie-ecoguard-fit3184-a2-private).
Full state, plans, policies, approval records and credentials remain outside Git.

Prepared with Codex assistance. Private inference remains a reviewed plan awaiting
new execution approval.
