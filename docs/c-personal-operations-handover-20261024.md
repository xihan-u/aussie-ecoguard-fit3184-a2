# Member C personal deployment handover (24 October 2026)

The current route uses AWS for storage, queues, identity and application functions, and Google Cloud Run for private model inference. These are two cloud providers; the older Oracle-host instructions describe a separate deployment route. This handover identifies the current environment and separates deployed configuration from application acceptance.

```mermaid
flowchart LR
  User[Team web client] -. pending HTTPS/Cognito acceptance .-> API[AWS API and functions]
  API -. pending actual media processing .-> S3[Private AWS media bucket]
  S3 -. disabled notifications .-> Q[Queues and ingest Lambda]
  Q -. pending role-token exchange .-> WIF[Google Workload Identity Federation]
  WIF --> SA[Dedicated AWS-invoker Google service account]
  SA --> Run[Private Cloud Run inference]
  Run --> HF[Exact locked model artifacts over HTTPS]
```

The dotted paths still need real application evidence. A configured IAM relationship or Ready revision alone does not prove that Lambda has exchanged its role identity or processed media.

| Environment | State-owning source and latest recorded configuration | Evidence |
| --- | --- | --- |
| AWS `011154879765`, `us-east-1` | Source `29367645d62d47f16ac64659266dc3ba1540b89d`; 55 resources; 40/40 read-only pause checks at 13:29:56 UTC on 23 October | [Foundation](c-personal-foundation-deployed-20261024.md) |
| Google `ecoguard-fit3184-a2-2026`, `us-central1` | 13 resources; dedicated runtime and invoker accounts; private Run service, 4 CPU/8 GiB, minimum 0/maximum 1 | [Actual Run configuration](c-private-inference-deployed-20261024.md) |
| Inference repair | Source `9b16f12872c067163f41de5c3d29d01e78cebbdd`; private image publication and image-only apply passed; Ready revision `ecoguard-inference-00002-vmh`, state serial19; model startup still blocked | [Image-only apply](c-inference-image2-apply-20261024.md) |

The recorded service URL is `https://ecoguard-inference-adlnb7yumq-uc.a.run.app`. The first anonymous `/healthz` request returned 404, and the test stopped before authenticated health or model warmup. The repair adds `/health` and `/ready`; the [new bounded batch](c-private-http-repair-20261024.md) returned 403/200/401 for anonymous health/authenticated health/warmup. Model startup remains unverified; preserve the [original failure](c-private-http-first-attempt-20261024.md) alongside these results.

## Identity and source custody

Only the intended normalized AWS execution role is trusted by the Google provider. The Google invoker is `ecoguard-aws-invoker@ecoguard-fit3184-a2-2026.iam.gserviceaccount.com`, and the runtime uses its separate dedicated account. Live configuration checks recorded zero user-managed service-account keys. The service has a sole explicit invoker binding; no anonymous invoker grant was added.

Each cloud's existing CloudShell checkout at `~/ecoguard-c-personal-20261023/source` owns that cloud's personal-root state. The state and retained plans/logs remain private. Git transfers source and selected evidence, so a second checkout cannot apply safely merely because it contains the same code. Arrange private state custody and one operator before handover. Every saved binary is bound to its source, image digest, state checkpoint and reviewed scope. Historical first-create plans remain historical records.

The private repository is [xihan-u/aussie-ecoguard-fit3184-a2-private](https://github.com/xihan-u/aussie-ecoguard-fit3184-a2-private). Both `main` and `codex/c-cloud-deployment` receive member-C checkpoints. Team and teaching-staff access still needs the intended recipients; see [repository handoff](c-private-repository-handoff-20261024.md). Existing public upstream/fork exposure remains a separate unresolved requirement.

## Budget, pause and recovery

Additional personal spending remains A$0. The current Google credit observation expires on 28 October, with review/cleanup due by 27 October Melbourne. Recheck live eligible credits and the selected billing identity before each bounded activation. Minimum-zero instances and a one-instance cap reduce runtime use, but they are not a hard account-wide spending cap. Registry images and retained cloud data can incur storage charges. No automatic cleanup is configured.

AWS is recorded paused: seven functions have zero reserved concurrency, three queue consumers and both schedules are disabled, the default API endpoint is disabled, self-signup is restricted and S3 retains its explicit paused-data denial. Resume stages need reviewed incremental plans and current account/credit checks. The prepared ingest archive is [locally verified](c-aws-ingest-export-20261024.md). A first ECR publication preflight stopped before its result directory or push marker; publication is still unverified. The staged wiring implementation is committed with 35 local plan-gate tests passing, but no real 55-to-59 plan or apply has run. ECR publication and the managed ingest runtime require separate results.

For a repair rollback, retain the prior immutable image and its exact manifest. Generate a new image-only plan against the actual current state, review configuration/IAM/capacity preservation, and apply that new binary once under the applicable authorization and funding. An older already-applied saved plan is not a rollback mechanism. Keep the service's dedicated runtime identity, sole invoker, locked model manifest and resource bounds. Validate the resulting Ready revision and authenticated behavior.

Pause/restore acceptance still needs a real exercise after the cross-cloud path works: record a bounded task, pause producers and processing, verify the paused controls, restore only the intended stage, then show the intended recovery and cleanup. These instructions are a procedure, not evidence that this exercise has run. The Week 15 demonstration needs a funding-compatible run/restore arrangement beyond the present credit-expiry date.

## Remaining member-C integration evidence

The next evidence should cover the updated private service and locked-model warmup, immutable AWS ingest image publication, actual Lambda-role federation, real image/video processing, TLS/CORS and cross-user boundaries, plus the pause/restore exercise. Coordinate browser signup/login with B and formal Lex/mail acceptance with D. The complete assignment's 22 criteria remain separate from this infrastructure work.
