"""Pure review of a NEW normal-refresh adopted60 reactivation plan.

No clients, subprocess, writes, original gate main or synthetic document rewrite.
The actual raw85 stores an empty adopted notification and seven active controls.
Its refreshed prior may differ ONLY by observed approved emergency reductions.
This reviewer never
authorizes apply or proves a plan's invocation mode from JSON alone.
"""
import copy
import json
from datetime import datetime, timezone


def require(ok, message):
    if not ok:
        raise ValueError(message)


def scoped_pause_policy(g, value):
    require(type(value) is str, 'Native S3 policy must remain a JSON string')
    require(g.BASE.root_inventory_policy_is_scoped(json.loads(value)),
            'Only exact approved paused TLS/object-deny/root-list policy allowed')


def control_addresses(g):
    return g.UPDATES | {g.NOTIFICATION}


def refreshed_pause(g, document, physical):
    """Compare original raw-export values and genuine native prior in place."""
    old = g.managed(physical['values']['root_module'])
    prior = g.managed(document['prior_state']['values']['root_module'])
    expected_addresses = g.WIRED | {g.NOTIFICATION}
    require(set(old) == set(prior) == expected_addresses and len(old) == 60,
            'Complete physical60/refreshed60 inventories required')
    updates = control_addresses(g)
    rows = document.get('resource_drift')
    require(type(rows) is list and len(rows) <= 8
            and len({row.get('address') for row in rows}) == len(rows)
            and {row.get('address') for row in rows} <= updates,
            'Only observed resources within the eight emergency reducers may drift')
    for row in rows:
        address = row['address']
        change = row.get('change', {})
        require(row.get('mode') == 'managed'
                and row.get('provider_name') == 'registry.terraform.io/hashicorp/aws'
                and change.get('actions') == ['update']
                and not any(row.get(k) or change.get(k) for k in ('previous_address','deposed','importing','replace_paths'))
                and not g.WIRING.unknown_paths(change.get('after_unknown', {}))
                and g.same(change.get('before'), old[address])
                and g.same(change.get('after'), prior[address]),
                'Native drift must join complete exact old/current values without unknowns')
    for address, before in old.items():
        expected = copy.deepcopy(before)
        if address in {g.FUNCTIONS[n] for n in ('ingest','infer','outbox')}:
            require(type(before.get('reserved_concurrent_executions')) is int
                    and before['reserved_concurrent_executions'] == -1,
                    'Saved active function must be exactly unreserved')
            expected['reserved_concurrent_executions'] = 0
        elif address in {g.MAPPINGS[n] for n in ('ingest','infer')}:
            require(before.get('enabled') is True
                    and g.same(before.get('scaling_config'), [{'maximum_concurrency':2}]),
                    'Saved active SQS mapping/cap differs')
            # Exact native readback of the already-approved emergency disable.
            # No timestamp/state field outside these two actual rows may differ.
            mapping_name = next(n for n in ('ingest','infer') if address == g.MAPPINGS[n])
            before_time, after_time = {'ingest':('2026-10-25T02:56:14Z','2026-10-25T02:56:38Z'),
                                       'infer':('2026-10-25T02:56:14Z','2026-10-25T02:56:40Z')}[mapping_name]
            require(g.same(before.get('state'),'Enabled')
                    and g.same(before.get('last_modified'),before_time),
                    'Exact original mapping operational readback differs')
            expected['enabled'] = False
            expected['state'] = 'Disabled'
            expected['last_modified'] = after_time
        elif address == g.RULES['outbox']:
            require(g.same(before.get('state'),'ENABLED') and before.get('is_enabled') is True,
                    'Saved active outbox state/known enabled mirror differs')
            expected['state'] = 'DISABLED'
            expected['is_enabled'] = False
        elif address == g.BUCKET_POLICY:
            require(g.same(json.loads(before['policy']), g.tls_policy()), 'Saved active policy differs')
            scoped_pause_policy(g, prior[address].get('policy'))
            expected['policy'] = prior[address]['policy']
        elif address == g.NOTIFICATION:
            require(before.get('id') == g.BUCKET
                    and g.same({k:v for k,v in before.items() if k != 'id'}, g.notification(False)),
                    'Actual saved adopted notification must already be exactly empty')
        require(g.same(prior[address], expected),
                'Refresh changed a field outside the exact eight emergency controls: '+address)
    require({row['address'] for row in rows} == {a for a in old if not g.same(old[a], prior[a])},
            'Every and only actual physical/prior difference must have its native drift row')
    return old, prior


def inspect_plan(g, document, physical, *, image, zip_filename, window_seconds,
                 quota_evidence=None, quota_evidence_sha256=None, review_time=None):
    """g is the unchanged hash-verified source47 processing gate, never its main."""
    require(type(window_seconds) is int and 1 <= window_seconds <= 600, 'Bounded window must remain1..600')
    require(type(image) is str and g.FOCUS.IMAGE_PATTERN.fullmatch(image), 'Exact personal immutable Image URI required')
    require(type(zip_filename) is str and zip_filename.startswith('/') and zip_filename.endswith('.zip'), 'Absolute reviewed ZIP required')
    require(document.get('complete') is True and document.get('errored') is False
            and not document.get('deferred_changes') and not document.get('action_invocations'),
            'Incomplete/errored/deferred/action plan')
    quota = g.reviewed_low_quota(quota_evidence, quota_evidence_sha256, review_time)
    old, prior = refreshed_pause(g, document, physical)
    future_root = document['planned_values']['root_module']
    future = g.managed(future_root)
    # These are genuine values from each representation, never edited documents.
    # The actual raw checkpoint already has an empty notification. Validate its
    # existing59 active configuration separately; never manufacture a plan JSON.
    g.profile({a:v for a,v in old.items() if a != g.NOTIFICATION}, active=True, adopted=False,
              image=image, zip_filename=zip_filename)
    g.profile(future, active=True, adopted=True, image=image, zip_filename=zip_filename)
    require(set(future) == set(prior) and future[g.NOTIFICATION].get('id') == g.BUCKET,
            'Adopted resource must remain present with known exact bucket identity')
    identity = {'account_id':g.BASE.ACCOUNT, 'id':g.BASE.ACCOUNT,
                'user_id':g.BASE.ACCOUNT, 'arn':'arn:aws:iam::'+g.BASE.ACCOUNT+':root'}
    for root in (physical['values']['root_module'], document['prior_state']['values']['root_module']):
        data = [r for r in g.BASE.resources(root) if r.get('mode') != 'managed']
        require(len(data) == 1 and data[0].get('mode') == 'data'
                and data[0].get('address') == g.MODULE+'data.aws_caller_identity.current'
                and data[0].get('type') == 'aws_caller_identity' and g.same(data[0].get('values'), identity),
                'Exact known root caller data profile required')
    require(not [r for r in g.BASE.resources(future_root) if r.get('mode') != 'managed']
            and not [r for r in document.get('resource_changes', []) if r.get('mode') != 'managed'],
            'No planned data-resource read/change allowed')
    variables = document.get('variables', {})
    for name, expected in {'deployment_stage':'processing-bounded','adopt_upload_notifications':'true',
                           'worker_image':image,'lambda_zip':zip_filename,'inference_url':g.WIRING.RUN_URL}.items():
        require(g.same(variables.get(name, {}).get('value'), expected), 'Explicit native input differs: '+name)
    call = document.get('configuration', {}).get('root_module', {}).get('module_calls', {}).get('ecoguard', {})
    require(call.get('source') == '../..' and not any(k in call for k in ('count_expression','for_each_expression','depends_on','providers')),
            'Module source/scope differs')
    expressions = call.get('expressions', {})
    for name, expected in g.BASE.ROOT_INPUTS.items():
        if name not in {'worker_image','inference_url','google_invoker_email'}:
            require(g.same(expressions.get(name), {'constant_value':expected}), 'Static module input differs: '+name)
    require(g.same(expressions.get('allow_root_bucket_inventory_while_paused'), {'constant_value':True})
            and g.same(expressions.get('manage_upload_notifications'), {'references':['var.adopt_upload_notifications']})
            and g.same(expressions.get('allow_unreserved_processing_functions'), {'references':['var.deployment_stage']}),
            'Explicit scoped root inventory/notification ownership/unreserved opt-in differs')
    rows = document.get('resource_changes')
    require(type(rows) is list and len(rows) == 60 and len({r.get('address') for r in rows}) == 60
            and {r.get('address') for r in rows} == set(prior), 'Exactly sixty complete native change rows required')
    updates = control_addresses(g)
    paths = {}
    for row in rows:
        address, change = row['address'], row['change']
        require(change.get('actions') == (['update'] if address in updates else ['no-op'])
                and row.get('provider_name') == 'registry.terraform.io/hashicorp/aws'
                and not any(row.get(k) or change.get(k) for k in ('previous_address','deposed','importing','replace_paths'))
                and g.same(change.get('before'), prior[address]), 'Unexpected action or complete before-value mismatch')
        expected = copy.deepcopy(prior[address])
        if address in {g.FUNCTIONS[n] for n in ('ingest','infer','outbox')}:
            expected['reserved_concurrent_executions'] = -1
        elif address in {g.MAPPINGS[n] for n in ('ingest','infer')}:
            expected['enabled'] = True
        elif address == g.RULES['outbox']:
            expected['state'] = 'ENABLED'
        elif address == g.BUCKET_POLICY:
            expected['policy'] = old[address]['policy']
        elif address == g.NOTIFICATION:
            expected['queue'] = g.notification(True)['queue']
        # Existing field-specific metadata unknown catalogue only. Notification
        # is an existing resource: its id/security/destination cannot be unknown.
        paths[address] = g.compared(prior[address], change['after'], future[address],
                                    change.get('after_unknown', {}), address, expected)
    before_outputs = physical['values'].get('outputs', {})
    prior_outputs = document['prior_state']['values'].get('outputs', {})
    outputs = document['planned_values'].get('outputs', {})
    require(set(before_outputs) == g.OUTPUTS and g.same(before_outputs, prior_outputs)
            and g.same(before_outputs, outputs), 'All eleven native output descriptors must be unchanged')
    require(before_outputs['runtime_enabled']['value'] is False
            and before_outputs['processing_enabled']['value'] is True
            and before_outputs['deployment_stage']['value'] == 'processing-bounded'
            and g.same(before_outputs['runtime_controls']['value'], g.controls(True, True)),
            'Saved raw activation outputs differ; API pause is not state/config convergence')
    changes = document.get('output_changes', {})
    require(set(changes) == g.OUTPUTS, 'Exactly eleven output change rows required')
    for name, row in changes.items():
        require(row.get('actions') == ['no-op'] and g.same(row.get('before'), before_outputs[name]['value'])
                and g.same(row.get('after'), before_outputs[name]['value'])
                and not g.WIRING.unknown_paths(row.get('after_unknown', False))
                and row.get('before_sensitive') is False and row.get('after_sensitive') is False,
                'Root output action/value/sensitivity differs: '+name)
    return {'status':'offline-adopted60-processing-plan-passed','mode':'reactivate-adopted',
            'priorManagedResources':60,'managedResources':60,'creates':0,'updates':8,'noops':52,'deletes':0,
            'fullPhysicalPriorEqual':False,'physicalPriorFullyEqual':False,'fullReviewedRefreshedPriorEqual':True,
            'reviewedEmergencyPauseDriftResources':len(document['resource_drift']),
            'reviewedEmergencyPauseTargetAllowlist':8,'allOther52PhysicalValuesExact':True,
            'allElevenNativeOutputDescriptorsUnchanged':True,'savedRawStateNotificationAlreadyEmpty':True,
            'disabledMappingsRetainExistingCapTwo':True,'noNewIAMOrService':True,'securityUnknownsAllowed':False,
            'reviewedUnknownPaths':{a:p for a,p in paths.items() if p},'maximumReviewedWindowSeconds':window_seconds,
            'lowQuotaEvidence':quota,'quotaAtHistoricalPlanTimeOnly':True,'freshQuotaRequiredBeforeActivation':True,
            'unreservedProcessingOptIn':True,'outboxReservationCapOne':False,'applyAuthorized':False,
            'timerCreated':False,'runtimeActivated':False,'automaticFlowVerified':False,
            'normalRefreshModeMustBeProvenByStartedArgvAndBinaryHash':True}
