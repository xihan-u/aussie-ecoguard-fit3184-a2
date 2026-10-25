# Member C: first bounded runtime attempt and recovery — 25 October 2026

The first approved runtime attempt applied its saved Terraform plan once, but failed the post-activation checks before any test image or fixture seed was submitted. It is not a successful AWS–GCP media test. The original 600-second pause target was missed. A later operator recovery and independent read-only check established that all eight emergency controls were paused.

## Actual results

| Result | Evidence and limitation |
|---|---|
| Saved plan applied once | Exit code 0; resulting AWS state serial 85, 60 managed resources. No replay is authorized. |
| Post-activation validation failed | Function `RevisionId` changed after concurrency updates, and S3 returned the known notification filter name as `Prefix`. The exact comparisons rejected the returned profiles. |
| Media/WIF processing | No image uploaded, no fixture seed submitted, no actual Lambda-to-GCP media or federated invocation verified. Successful real images: **0**. |
| First watchdog recovery | Four controls paused; four remaining reducers were blocked by profile comparison. Original records retained. |
| Operator recovery | The first operator helper failed during read-only checks without mutations. A revised helper then executed only the four previously unused reducers and verified their paused readbacks. |
| Independent post-check | At **03:09:48.489 UTC**, eight controls were paused in both observation rounds, project boundaries were checked, five complete table scans were empty, and eight queues had zero approximate counts. |
| Limits | No continuous application-drain proof; Terraform configuration convergence remains unverified. The eventual pause does not establish the original 600-second recovery target. |
| Later read-only collection | At **03:24:23.566 UTC**, all eight control groups passed, but the SDK boundary worker failed before completion. The attempt was retained without automatic retry, mutations, or media submission. |

## Current operating state

The application remains paused: eight Lambda functions have reserved concurrency zero, queue mappings are disabled, the outbox rule is disabled, the media bucket has no incoming notification, and its data-deny policy is restored. API, signup, mail, Lex and scheduled processing remain disabled. Retained storage and logs may still consume credit; pausing does not guarantee a zero bill. The additional personal spending limit remains **A$0**.

AWS source revision is `40b5d5f603ef362b50ebe4c317772a53f9b24631`; this documentation commit is not a new cloud deployment. The actual serial-85 raw state was preserved, including its observed empty notification configuration; it must not be overwritten with the old serial-76/59-resource snapshot.

## Retained evidence

| Record | SHA-256 |
|---|---|
| Consumed review packet | `e32597d74b57072f52dd7676bfd46a401e68726f9efac1d3ad80b8fcedbd8832` |
| Final controller binding used once | `870441458025caf926479a138b684b9f2d1f2ea82e6550090d13304b001b0f3f` |
| Actual state, serial 85 / 60 resources | `7b4d5aed8ce5fd253fceac940637c67554ec0dadea61ca5a352e44a03b455204` |
| Four-reducer operator recovery receipt | `6e73f4dcaaa38a6046250acf1403677cdccf2bf71609158f03fece1db5993cbb` |
| Independent all-eight post-check | `77b108c8610223d477f2fdff558781d10c2b2575f3e85d3a3d06c19b39db1b9d` |
| Original private archive, 678,913 bytes / 2,203 files | `05fad95ee8aa995cf4925605acd3b3e1c8663dc2e84ecb16a6db13356633f859` |
| Later failed read-only collection summary | `6069e2666fb0ecca94250231aa0b25708d8255b6fa562264296deeb6c1da11f1` |

The original archive was downloaded and every regular file hash checked locally. It contains private raw logs and state and is excluded from Git. Screenshots C12/C13 are retained locally; the clean C13 image shows the actual 03:09 post-check record and is not a new API audit at screenshot time.

## Work still required

1. Resolve the read-only SDK worker startup failure and obtain a new, independently checked normal-refresh plan against the actual 60-resource checkpoint.
2. Obtain fresh quota, funding, GCP and supervisor evidence; present a concrete second test plan. The first scoped approval is consumed and cannot authorize another runtime activation.
3. Execute one actual image through the automatic AWS–GCP path, preserve outputs and identity evidence, and demonstrate timely pause/recovery with the required observation tail.
4. Update the architecture, final personal report and handover from actual results. The personal report is draft 5, 389 words, and has passed layout review, but is not a final submission.

Vendor selection is AWS + GCP, permitted by Spec p2 and Rubric p7. Oracle is not mandatory. Single-image success would still not establish every team acceptance criterion, video processing, user-isolation testing, private repository access or availability through assessment.

No reliable completion percentage or completion time is currently asserted. Deployment and read-only checks must not be counted as successful application processing.
