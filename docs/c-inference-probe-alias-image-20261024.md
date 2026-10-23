# Probe alias image: actual local verification (24 October 2026)

The new inference image contains `/health` and `/ready`, alongside the retained legacy probes. This addresses the reserved-z-path concern recorded in [the first HTTP attempt](c-private-http-first-attempt-20261024.md). The first cloud request remains a 404 failure; this local record does not reinterpret it as authentication denial.

Source is `9b16f12872c067163f41de5c3d29d01e78cebbdd`; the image is Linux amd64 with runtime user `10001:10001`. Actual image manifest is `sha256:0e274acc0dff67b2f233ebd5914235ea328147b8505044de23cfc135217e5c91`, distinct from config `sha256:dea2da475fc169ca21a1fb637e54f61f29d97b48d0604f49cf5c9735c0af0287`. Dependency installation was cached from the reviewed prior build, and the first eight base/dependency layer hashes match.

The regression function ran inside the new image with networking disabled and no mounted application-source overlay. Both readiness states, equivalent legacy/new responses, rejection of unauthenticated warmup, disabled public docs and the exact generated API contract passed. No heavy model was loaded.

The actual 373,263,746-byte gzip export has SHA256 `2f7f395e7e2eb07610270ae730803cbc7e076271bba3f232a45b873ce996ec35`. All twelve OCI blobs, ten expanded layer hashes and twenty installed source/config/lock files were verified against the pinned build inputs; a separate offline archive audit also passed. The archive contains no downloaded model cache or host credential paths.

The [AR-only publication helper](../scripts/publish_personal_gcp_inference_probe_alias_image.py) is inert without `--publish`, requires the exact archive, source, thirteen-resource state and fresh existing-credit observation, and preserves the first tag. This document records local checks only. Registry publication, a new Ready cloud revision, access checks and model warmup require their own actual evidence. AWS remains paused.

Machine-readable record: [local image evidence](../evidence/c-inference-probe-alias-image-20261024.json).
