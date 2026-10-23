"""Fail-closed personal first-plan tests; no SDK, cloud, or deployment ZIP."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("personal_plan", Path(__file__).parents[1] / "environments/personal/check_plan.py")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def scoped_policy():
    def statement(sid, actions, targets, condition=None):
        value = {"Sid": sid, "Effect": "Allow", "Action": actions, "Resource": targets}
        if condition:
            value["Condition"] = condition
        return value

    account, region, prefix = GATE.ACCOUNT, GATE.REGION, GATE.PREFIX
    topic = f"arn:aws:sns:{region}:{account}:{prefix}-user-*"
    return {"Version": "2012-10-17", "Statement": [
        statement("ProjectTableRecords", ["dynamodb:GetItem", "dynamodb:Query", "dynamodb:Scan", "dynamodb:PutItem", "dynamodb:DeleteItem"],
                  [f"arn:aws:dynamodb:{region}:{account}:table/{prefix}-{name}" for name in sorted(GATE.TABLES)]),
        statement("ProjectBucketListing", ["s3:ListBucket", "s3:ListBucketVersions"], [f"arn:aws:s3:::{GATE.BUCKET}"]),
        statement("ProjectMediaObjects", ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject", "s3:DeleteObject", "s3:DeleteObjectVersion"],
                  [f"arn:aws:s3:::{GATE.BUCKET}/*"]),
        statement("ProjectWorkQueues", ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
                  [f"arn:aws:sqs:{region}:{account}:{prefix}-{name}" for name in sorted(GATE.QUEUES)]),
        statement("ProjectNotificationTopics", ["sns:CreateTopic", "sns:ListSubscriptionsByTopic", "sns:Publish"], [topic]),
        statement("ProjectEmailSubscriptions", ["sns:Subscribe"], [topic], {"StringEquals": {"sns:Protocol": "email"}}),
        statement("RegionalAnimalLabelDetection", ["rekognition:DetectLabels"], ["*"], {"StringEquals": {"aws:RequestedRegion": region}}),
        statement("ProjectFunctionLogs", ["logs:CreateLogStream", "logs:PutLogEvents"],
                  [f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/{prefix}-{name}:log-stream:*" for name in sorted(GATE.FUNCTIONS)]),
    ]}


def plan_fixture():
    planned = [{"address": address, "mode": "managed", "type": address[len(GATE.MODULE):].split(".")[0], "values": {}}
               for address in sorted(GATE.expected_addresses())]
    index = {r["address"][len(GATE.MODULE):]: r["values"] for r in planned}
    for name in GATE.FUNCTIONS:
        index[f'aws_lambda_function.zip["{name}"]'].update({
            "filename": "/fixture/not-created.zip", "source_code_hash": "fixture-only-not-a-built-package",
            "reserved_concurrent_executions": 0, "runtime": "python3.12", "architectures": ["x86_64"],
            "function_name": f"{GATE.PREFIX}-{name}"})
    for name in ("infer", "delete", "notify"):
        index[f'aws_lambda_event_source_mapping.zip_queues["{name}"]']["enabled"] = False
    for name in ("outbox", "cleanup"):
        index[f'aws_cloudwatch_event_rule.maintenance["{name}"]']["state"] = "DISABLED"
    for name in GATE.TABLES:
        index[f'aws_dynamodb_table.data["{name}"]'].update({"billing_mode": "PAY_PER_REQUEST", "name": f"{GATE.PREFIX}-{name}"})
    index["aws_apigatewayv2_api.app[0]"]["disable_execute_api_endpoint"] = True
    # The provider can include unrelated optional/default block fields.
    index["aws_cognito_user_pool.users"]["admin_create_user_config"] = [{"allow_admin_create_user_only": True, "invite_message_template": []}]
    for address in ("aws_s3_bucket_public_access_block.media", "aws_s3_bucket_server_side_encryption_configuration.media",
                    "aws_s3_bucket_cors_configuration.media", "aws_s3_bucket_policy.media_tls"):
        index[address]["bucket"] = GATE.BUCKET
    index["aws_s3_bucket_policy.media_tls"]["policy"] = json.dumps({"Statement": [{
        "Sid": "DenyDataAccessWhileRuntimePaused", "Effect": "Deny", "Principal": "*",
        "Action": ["s3:GetObject*", "s3:PutObject*", "s3:DeleteObject*", "s3:RestoreObject", "s3:AbortMultipartUpload",
                   "s3:ListMultipartUploadParts", "s3:ListBucket", "s3:ListBucketVersions", "s3:ListBucketMultipartUploads"],
        "Resource": [f"arn:aws:s3:::{GATE.BUCKET}", f"arn:aws:s3:::{GATE.BUCKET}/*"]}]})
    index["aws_iam_role.runtime[0]"].update({"name": f"{GATE.PREFIX}-lambda", "assume_role_policy": json.dumps({
        "Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": "sts:AssumeRole", "Principal": {"Service": "lambda.amazonaws.com"}}]})})
    index["aws_iam_role_policy.runtime[0]"].update({"name": f"{GATE.PREFIX}-runtime", "role": f"{GATE.PREFIX}-lambda", "policy": json.dumps(scoped_policy())})
    identity = {"address": GATE.MODULE + "data.aws_caller_identity.current", "type": "aws_caller_identity",
                "mode": "data", "values": {"account_id": GATE.ACCOUNT}}
    return {
        "variables": {"lambda_zip": {"value": "/fixture/not-created.zip"}},
        "configuration": {"root_module": {"module_calls": {"ecoguard": {"source": "../..", "expressions": {
            name: {"constant_value": copy.deepcopy(value)} for name, value in GATE.ROOT_INPUTS.items()}}}}},
        "planned_values": {"root_module": {"child_modules": [{"address": "module.ecoguard", "resources": [identity, *planned]}]}},
        "resource_changes": [{"address": r["address"], "type": r["type"], "mode": "managed", "change": {"actions": ["create"]}}
                             for r in planned],
    }


def value(plan, address):
    return next(r["values"] for r in GATE.resources(plan["planned_values"]["root_module"]) if r["address"] == GATE.MODULE + address)


class PersonalFirstPlanTests(unittest.TestCase):
    def test_scoped_paused_fixture_passes_without_claiming_a_real_zip_or_cloud(self):
        report = GATE.inspect_plan(plan_fixture())
        self.assertEqual(report["status"], "offline-first-plan-passed", report["checks"])
        self.assertEqual(report["managedResources"], 53)
        for flag in ("cloudVerified", "billingVerified", "crossCloudVerified", "applyAuthorized"):
            self.assertFalse(report[flag])
        self.assertNotIn("localArchiveVerified", report)
        with self.assertRaises(ValueError):
            GATE.verify_archive(plan_fixture())

    def test_wrong_account_region_and_missing_allowlist_fail(self):
        for change in ("account", "region", "allowlist"):
            with self.subTest(change=change):
                plan = plan_fixture()
                expressions = plan["configuration"]["root_module"]["module_calls"]["ecoguard"]["expressions"]
                if change == "account":
                    plan["planned_values"]["root_module"]["child_modules"][0]["resources"][0]["values"]["account_id"] = "360493183467"
                elif change == "region":
                    expressions["region"]["constant_value"] = "ap-southeast-2"
                else:
                    expressions["allowed_account_ids"]["constant_value"] = []
                self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_read_identity_may_live_in_refreshed_prior_state(self):
        plan = plan_fixture()
        rows = plan["planned_values"]["root_module"]["child_modules"][0]["resources"]
        identity = rows.pop(0)
        plan["prior_state"] = {"values": {"root_module": {"resources": [identity]}}}
        self.assertEqual(GATE.inspect_plan(plan)["status"], "offline-first-plan-passed")
        identity["values"]["account_id"] = "360493183467"
        self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_updates_deletes_imports_old_state_and_extra_resources_fail(self):
        for change in ("update", "delete", "replace", "import", "state", "extra"):
            with self.subTest(change=change):
                plan = plan_fixture()
                if change in {"update", "delete", "replace"}:
                    plan["resource_changes"][0]["change"]["actions"] = ["delete", "create"] if change == "replace" else [change]
                elif change == "import":
                    plan["resource_changes"][0]["change"]["importing"] = {"id": "old-resource"}
                elif change == "state":
                    plan["prior_state"] = {"values": {"root_module": {"resources": [{"mode": "managed"}]}}}
                else:
                    plan["resource_changes"].append({"address": "aws_instance.unexpected", "mode": "managed", "change": {"actions": ["create"]}})
                self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_each_runtime_pause_gate_must_hold(self):
        changes = [('aws_lambda_function.zip["api"]', "reserved_concurrent_executions", -1),
                   ('aws_lambda_event_source_mapping.zip_queues["delete"]', "enabled", True),
                   ('aws_cloudwatch_event_rule.maintenance["outbox"]', "state", "ENABLED"),
                   ("aws_apigatewayv2_api.app[0]", "disable_execute_api_endpoint", False),
                   ("aws_cognito_user_pool.users", "admin_create_user_config", [{"allow_admin_create_user_only": False}])]
        for address, key, changed in changes:
            with self.subTest(address=address):
                plan = plan_fixture()
                value(plan, address)[key] = changed
                self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_broader_permissions_trust_and_subscription_conditions_fail(self):
        for change in ("wildcard", "extra_action", "region", "email", "trust", "attached_admin", "shared_role"):
            with self.subTest(change=change):
                plan = plan_fixture()
                policy = scoped_policy()
                if change == "wildcard":
                    policy["Statement"][0]["Resource"] = ["*"]
                elif change == "extra_action":
                    policy["Statement"][0]["Action"].append("dynamodb:DeleteTable")
                elif change in {"region", "email"}:
                    target = "RegionalAnimalLabelDetection" if change == "region" else "ProjectEmailSubscriptions"
                    next(s for s in policy["Statement"] if s["Sid"] == target).pop("Condition")
                elif change == "trust":
                    value(plan, "aws_iam_role.runtime[0]")["assume_role_policy"] = json.dumps({"Statement": [{"Principal": "*"}]})
                elif change == "attached_admin":
                    value(plan, "aws_iam_role.runtime[0]")["managed_policy_arns"] = ["arn:aws:iam::aws:policy/AdministratorAccess"]
                else:
                    value(plan, "aws_iam_role_policy.runtime[0]")["role"] = "LabRole"
                value(plan, "aws_iam_role_policy.runtime[0]")["policy"] = json.dumps(policy)
                self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_external_bucket_settings_cannot_target_a_retained_course_bucket(self):
        for address in ("aws_s3_bucket_public_access_block.media", "aws_s3_bucket_server_side_encryption_configuration.media",
                        "aws_s3_bucket_cors_configuration.media", "aws_s3_bucket_policy.media_tls"):
            with self.subTest(address=address):
                plan = plan_fixture()
                value(plan, address)["bucket"] = "ecoguard3184-dev-360493183467-media"
                self.assertEqual(GATE.inspect_plan(plan)["status"], "blocked")

    def test_failed_cli_report_does_not_echo_private_plan_fields(self):
        plan = plan_fixture()
        value(plan, 'aws_lambda_function.zip["api"]')["environment"] = {"variables": {"PRIVATE_FIXTURE": "do-not-echo-this-fixture"}}
        value(plan, 'aws_lambda_function.zip["api"]')["reserved_concurrent_executions"] = -1
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "private-plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(GATE.main(["--plan-json", str(path)]), 1)
            self.assertNotIn("do-not-echo-this-fixture", output.getvalue())
            path.write_text("not JSON", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(GATE.main(["--plan-json", str(path)]), 2)


if __name__ == "__main__":
    unittest.main()
