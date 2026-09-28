"""Offline acceptance check for the deployed operand-repair candidate.

Reads an AoE2:DE AI engine log (and optionally a replay cache and the file-trace
records) and reports the specific evidence the repair must show:

* the former engine error families: ``up-can-build`` / ``up-can-build-line`` /
  ``up-get-point-distance`` with ``Invalid goal used (0)`` must be gone, while
  the unrelated families stay present as a comparability control;
* invocation coverage: which traced sites that carry the repaired operands were
  actually reached (an unexercised call does not pass);
* migration state-machine transitions (file-trace type 32), including
  ``MIGRATION-DROPSITE-FAILED``;
* the shipyard sampler reason histogram (diag 545) against the 508 baseline;
* the order-706 packet count, reported without attributing any change to the
  operand repair.

Nothing here launches the game, edits a runtime file or proves gameplay success.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# 508 baselines, measured from the original recording (see T61/T62 reports).
BASELINE_ERRORS = {
    'up-can-build': 86277,
    'up-can-build-line': 3001,
    'up-get-point-distance': 24490,
    'up-get-object-target-data': 44076,
    'up-remove-objects': 12302,
    'up-find-remote': 4273,
    'up-set-offense-priority': 896,
}
REPAIRED = ('up-can-build', 'up-can-build-line', 'up-get-point-distance')
CONTROLS = ('up-get-object-target-data', 'up-remove-objects', 'up-find-remote',
            'up-set-offense-priority')
ERROR_PATTERNS = {
    name: re.compile(r'\(%s\): Invalid goal used \((-?\d+)\)' % name)
    for name in ('up-can-build', 'up-can-build-line', 'up-get-point-distance')
}
RETURN_PATTERNS = {
    'up-get-object-target-data': re.compile(r'\(up-get-object-target-data\): Object was invalid, returning (-?\d+)'),
    'up-remove-objects': re.compile(r'\(up-remove-objects\): Object was invalid, returning (-?\d+)'),
    'up-find-remote': re.compile(r'\(up-find-remote\): Focus player is invalid \((-?\d+)\)'),
    'up-set-offense-priority': re.compile(r'\(up-set-offense-priority\): Unit type was invalid \((-?\d+)\)'),
}
BASELINE_SHIPYARD = {64: 6186, 62: 599, 65: 256, 66: 60, 67: 38}
BASELINE_SHIPYARD_SAMPLES = 7139


def migration_states():
    """MIGRATION-* value -> name, from the runtime constants in this checkout."""
    text = (REPO / 'rawai-customconstants.per').read_text(encoding='utf-8-sig')
    return {int(value): name for name, value in
            re.findall(r'\(defconst (MIGRATION-[\w-]+) (-?\d+)\)', text)}


def scan_engine_log(path: Path):
    counts = collections.Counter()
    operands = collections.defaultdict(collections.Counter)
    patterns = dict(ERROR_PATTERNS, **RETURN_PATTERNS)
    with Path(path).open('r', encoding='utf-8-sig', errors='replace') as stream:
        for line in stream:
            for name, pattern in patterns.items():
                match = pattern.search(line)
                if match:
                    counts[name] += 1
                    operands[name][int(match.group(1))] += 1
                    break
    return counts, operands


def repaired_sites(registry_path: Path):
    registry = json.loads(Path(registry_path).read_text(encoding='utf-8'))
    sites = {}
    for site in registry['sites']:
        original = site['original'] if isinstance(site['original'], str) else ' '.join(site['original'])
        if 'gl-no-escrow-state' in original:
            sites[site['id']] = site['file']
    return sites


def scan_records(path: Path, sites, states):
    reached = collections.Counter()
    migration = collections.Counter()
    failures = collections.Counter()
    with Path(path).open() as stream:
        for line in stream:
            record = json.loads(line)
            if not record.get('complete'):
                failures[record.get('error') or 'incomplete'] += 1
                continue
            if record['type'] == 1 and record['site'] in sites:
                reached[record['site']] += 1
            elif record['type'] == 32 and record['values']:
                migration[states.get(record['values'][0], record['values'][0])] += 1
    return reached, migration, failures


def scan_cache(path: Path):
    cache = json.loads(Path(path).read_text())
    diagnostics = cache['diagnostics']
    replay = collections.Counter({
        'shipyard_reason': collections.Counter(x['value'] for x in diagnostics if x['diag_id'] == 545),
        'shipyard_stage_samples': sum(1 for x in diagnostics if x['diag_id'] in (543, 544)),
        'migration_issue_dropsite': sum(1 for x in diagnostics if x['diag_id'] == 567),
        'migration_check_dropsite': sum(1 for x in diagnostics if x['diag_id'] == 579),
        'order_706_packets': sum(1 for e in cache['events'] if e.get('order_id') == 706),
    })
    return replay


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--records', type=Path)
    parser.add_argument('--cache', type=Path)
    parser.add_argument('--registry', type=Path,
                        default=REPO / 'command-boundary-registry.json')
    parser.add_argument('--json', type=Path, help='write the report as JSON')
    args = parser.parse_args()

    counts, operands = scan_engine_log(args.log)
    report = {'engine_errors': {}, 'acceptance': {}}
    for name, baseline in BASELINE_ERRORS.items():
        observed = counts.get(name, 0)
        report['engine_errors'][name] = dict(observed=observed, baseline=baseline,
                                             operand_values=dict(operands.get(name, {})))
    report['acceptance']['repaired_families_zero'] = all(
        counts.get(name, 0) == 0 for name in REPAIRED)
    report['acceptance']['control_families_present'] = {
        name: counts.get(name, 0) > 0 for name in CONTROLS}

    if args.records:
        sites = repaired_sites(args.registry)
        reached, migration, failures = scan_records(args.records, sites, migration_states())
        report['repaired_sites'] = dict(
            total=len(sites), reached=len(reached), invocations=sum(reached.values()),
            unexercised=sorted(set(sites) - set(reached))[:20],
            failures=dict(failures))
        report['migration_states'] = dict(migration)
        report['acceptance']['repaired_sites_exercised'] = len(reached) > 0
    if args.cache:
        replay = scan_cache(args.cache)
        report['replay'] = replay
        shipyard = replay['shipyard_reason']
        samples = sum(shipyard.values())
        report['acceptance']['shipyard_reason64_share'] = (
            round(shipyard.get(64, 0) / samples, 4) if samples else None)
        report['acceptance']['shipyard_reason64_baseline_share'] = round(
            BASELINE_SHIPYARD[64] / BASELINE_SHIPYARD_SAMPLES, 4)

    print(json.dumps(report, indent=1))
    if args.json:
        args.json.write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
