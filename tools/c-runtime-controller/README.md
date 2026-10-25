# Frozen member-C controller candidate V13

This is a reviewable **inert code snapshot**, not a deployment or a cloud entry
point. It preserves the V13 driver with `ARM_REVIEWED = False`, preparer pin
`None` and all 60 actual pins pending. The ARMTrue RELEASE file, consumed
bindings/approvals, credentials, private logs, saved plans and Terraform state
are deliberately absent. No existing approval can be replayed from this tree.

V13 starts durable writer heartbeats before watchdog startup and uses a readiness
bound within the original 600-second window, capped by the existing stop reserve.
It does not weaken fixture, funding, identity, boundary, once-only or drain gates.
These changes passed nine deterministic injected-stub tests and independent
static review in the original work snapshot. This does not prove native Linux
scheduling, CloudShell SDK startup, real IAM/WIF, model processing, or recovery
under active work. Attempts 1 and 2 remain failed media tests.

## Run only the offline tests

From the repository root, using Python 3.10 or newer and the standard library:

```sh
python3 -B -m unittest discover -s tools/c-runtime-controller/tests -v
```

Or from this directory:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests inject clock, thread, process, IPC and cloud-port stubs. They start no
real thread or process, invoke no signal/CLI/SDK, and contact no cloud service.
The snapshot uses the original first eight tests unchanged except their module
location. The ninth test compares the same dependencies and old function ASTs
against a compact V12 static baseline, replacing the unavailable sibling work
directory. `SNAPSHOT.json` records both test hashes and this packaging change.
The original independent review covers the upstream candidate, not an independent
review of this repository packaging or a cloud release.

## Deliberately incomplete runtime binding

The unchanged driver contains exact historical Linux CloudShell paths and hash
pins. The current VM, CLI/SDK package inventory, source tree, native plans,
funding, fixture IDs, fresh GCP metadata and human authority are **not completely
bound** here. The referenced private artifacts and executable release are not
included. Do not run this snapshot against cloud resources, set ARMTrue, replace
pins, or treat a passing local test as permission to activate an application.

The ten production candidate modules and pending-binding template are byte-for-
byte copies of V13. `reference/automatic_fixture_DRAFT.py` is the fixed inert
fixture helper for source review; its relocated reference path intentionally
does not satisfy the driver's original runtime path. Source Terraform gate files
remain in `infra/aws/environments/personal`; their historical pins do not assert
fresh deployment acceptance. No product implementation or Terraform is changed
by this snapshot.

See [actual attempts and recovery](../../docs/c-runtime-attempt-and-recovery-20261025.md)
for current operational limits. Real image/WIF success remains zero at this
checkpoint; continuous paused controls/funding do not establish fixture drain.
