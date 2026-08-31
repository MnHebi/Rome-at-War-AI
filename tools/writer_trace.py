#!/usr/bin/env python3
"""Build bounded, replay-visible writer brackets from this checkout, in memory.

No alternate development copy. Original command rules are retained, including
their facts, action order and disable-self. Observers repeat only non-consuming
facts; relative jumps are relocated to the SAME original destination. A bracket
is an invocation candidate until a matching command packet corroborates it.
"""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path
import re

from validate_naval_doctrine import rule_blocks

MARKER = 'RAWAI-P3B44T10R4: %d'
VALUE = 455
TOTAL_LIMIT = 512
MINUTE_LIMIT = 96
IDENTITY_ATTEMPTS = 3
IDENTITY_INTERVAL = 30
# Conservative PROJECT budgets, not a claimed DE engine table capacity. Count
# occurrences (including all inactive civ files), not unique message contents.
# T9 input has 1,446 literals; broken T10 expanded this to 5,665. Repeated quoted
# operands allocate again. A string defconst stores one reusable table index:
# https://airef.github.io/commands/commands-details.html#defconst
# https://airef.github.io/commands/commands-details.html#xs-script-call
MAX_PAYLOAD_STRING_LITERALS = 1500
MAX_WRITER_STRING_LITERALS = 32
STRING_TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|;[^\r\n]*')
TRACE_TEXT = {
    'begin': 'RAW44W begin: %d',
    **{f'{phase}-{label}': f'RAW44W {phase} {label.replace("-", " ")}: %d'
       for phase in ('pre', 'post')
       for label in ('assault', 'assault-hull', 'migration', 'migration-hull')},
    'selected': 'RAW44W selected: %d',
    'selected-flag': 'RAW44W selected flag: %d',
    'end': 'RAW44W end: %d',
}
DIRECT = re.compile(r'\((up-target-objects|up-target-point|up-retask-gatherers|'
    r'up-reset-unit|up-retreat-now|up-retreat-to|up-delete-idle-units|up-send-scout|'
    r'up-ungarrison|up-garrison|up-guard-unit|up-reset-scouts|attack-now|'
    r'delete-unit|delete-building)(?=\s|\))')
DELEGATE = re.compile(r'\((build|build-forward|build-wall|build-gate|up-build|'
    r'up-build-line|up-assign-builders)(?=\s|\))')
GROUP = re.compile(r'\((up-create-group|up-modify-group-flag|up-reset-group|'
                   r'up-disband-group-type)(?=\s|\))')
# A reference to a reserved group in a filter is NOT an ownership mutation.
# T10R1 misclassified general villager cleanup (site 41) because it EXCLUDES
# migration-boarding-group, making its unconditional observer run when idle.
# Match the destination operand of the actual DUC group mutation instead.
RESERVATION_MUTATION = re.compile(
    r'\((?:up-create-group\s+\S+\s+\S+|up-modify-group-flag\s+\S+|up-reset-group)'
    r'\s+c:\s+(?:migration-boarding-group|migration-transport-group|'
    r'attack-boarding-group|attack-transport-group)\s*\)')
POLICY = re.compile(r'\((?:set-strategic-number|up-modify-sn)\s+'
                   r'(sn-[\w-]*(?:gather|builder|retask|explor|attack|defend|repair)[\w-]*)\b')
PRIVATE = {'site': 13000, 'remaining': 13001, 'minute': 13002,
           'now': 13003, 'next': 13004, 'active': 13005,
           'gap': 13006, 'selected': 13007, 'flag': 13008, 'jumping': 13009,
           'identity-next': 13010, 'identity-left': 13011}
BLOCK = re.compile(r'; RAW44W BEGIN [^\n]*\n.*?; RAW44W END\n', re.S)
# Audited predicates only. A new RNG/consuming/search-producing fact must NOT
# silently be repeated merely because it lacks a familiar unsafe prefix.
REPEATABLE_FACTS = set('''and building-type-count building-type-count-total
    can-afford-building can-build can-build-gate-with-escrow
    can-build-wall-with-escrow can-build-with-escrow cc-players-unit-type-count
    current-age current-age-time dropsite-min-distance food-amount game-time goal
    housing-headroom nor not or player-in-game players-building-count
    population-headroom soldier-count stance-toward strategic-number taunt-detected
    true unit-type-count unit-type-count-total up-can-build up-can-build-line
    up-compare-goal up-compare-sn up-gaia-type-count up-group-size up-idle-unit-count
    up-object-data up-object-target-data up-object-type-count up-object-type-count-total
    up-path-distance up-pending-objects up-pending-placement up-set-target-object
    up-timer-status wall-completed-percentage warboat-count wood-amount'''.split())


def rule(facts: str, actions: list[str]) -> str:
    return '(defrule\n' + facts.strip() + '\n=>\n\t' + '\n\t'.join(actions) + '\n)\n'


def block(name: str, body: str) -> str:
    return f'; RAW44W BEGIN {name}\n{body}; RAW44W END\n'


def context(prefix: str) -> list[str]:
    return [trace_chat(f'{prefix}-{label}', f'g: {goal}')
            for label, goal in [('assault', 'gl-transport-route-state'),
                                ('assault-hull', 'gl-transport-route-id'),
                                ('migration', 'gl-island-migration-state'),
                                ('migration-hull', 'gl-island-migration-transport-id')]]


def trace_chat(field: str, operand: str) -> str:
    if field not in TRACE_TEXT:
        raise ValueError(f'undefined writer string: {field}')
    return f'(up-chat-data-to-all str-writer-{field} {operand})'


def string_budget(payload: dict[str, bytes]) -> dict:
    """Fail before deployment when generated literals exceed the reviewed budget.

    Semicolons inside strings are text, not comments. Counting every .per file
    conservatively includes unselected civilization branches as well as loads.
    Eight-player projection is informational, not proof of engine allocation.
    """
    literals = [match[0] for name, data in payload.items() if name.endswith('.per')
                for match in STRING_TOKENS.finditer(data.decode('utf-8-sig'))
                if match[0].startswith('"')]
    count = len(literals)
    writer = sum(value.startswith('"RAW44W ') for value in literals)
    if count > MAX_PAYLOAD_STRING_LITERALS or writer > MAX_WRITER_STRING_LITERALS:
        raise ValueError(f'string budget exceeded: {count}/{MAX_PAYLOAD_STRING_LITERALS} '
                         f'payload, {writer}/{MAX_WRITER_STRING_LITERALS} writer literals')
    return dict(payload_literals=count, writer_literals=writer,
                eight_player_literal_projection=count * 8,
                payload_limit=MAX_PAYLOAD_STRING_LITERALS,
                writer_limit=MAX_WRITER_STRING_LITERALS,
                scope='project budget; all files/branches; not an engine capacity claim')


def prelude() -> str:
    constants = ''.join(f'(defconst gl-writer-{name} {value})\n' for name, value in PRIVATE.items())
    # Define ONCE before all observer sites. Merely repeating identical quoted
    # templates at 351 sites exhausted the engine string table in T10:451.
    constants += ''.join(f'(defconst str-writer-{name} "{value}")\n'
                         for name, value in TRACE_TEXT.items())
    startup = rule('(true)', [f'(set-goal gl-writer-{name} {value})'
        for name, value in [('site', 0), ('jumping', 0), ('remaining', TOTAL_LIMIT),
                            ('minute', MINUTE_LIMIT), ('next', 60), ('gap', 0)]] +
        ['(set-goal gl-writer-identity-next my-player-number)',
         '(up-modify-goal gl-writer-identity-next c:* 3)',
         '(up-modify-goal gl-writer-identity-next c:+ 5)',
         f'(set-goal gl-writer-identity-left {IDENTITY_ATTEMPTS})',
         '(up-chat-data-to-all "RAW44W schema: %d" c: 1)', '(disable-self)'])
    clock = rule('(true)', ['(up-get-fact game-time 0 gl-writer-now)',
                            '(set-goal gl-writer-active 0)'])
    replenish = rule('(up-compare-goal gl-writer-now g:>= gl-writer-next)', [
        '(up-modify-goal gl-writer-next g:= gl-writer-now)',
        '(up-modify-goal gl-writer-next c:+ 60)',
        f'(set-goal gl-writer-minute {MINUTE_LIMIT})'])
    # Includes selection, boarding retry and its diagnostic/partial-manifest states.
    boarding = rule('''(or
        (and (up-compare-goal gl-transport-route-state c:>= 30)
             (up-compare-goal gl-transport-route-state c:<= 35))
        (or
          (and (up-compare-goal gl-transport-route-state c:>= 46)
               (up-compare-goal gl-transport-route-state c:<= 49))
          (or (goal gl-island-migration-state MIGRATION-BOARDING)
            (or (goal gl-island-migration-state MIGRATION-LOADING)
              (or (goal gl-island-migration-state MIGRATION-CHECK-LOAD)
                (and (up-compare-goal gl-island-migration-state c:>= 66)
                     (up-compare-goal gl-island-migration-state c:<= 68)))))))''',
        ['(set-goal gl-writer-active 1)'])
    gap = rule('''(goal gl-writer-gap 0)
        (or (up-compare-goal gl-writer-remaining c:<= 0)
            (up-compare-goal gl-writer-minute c:<= 0))''', [
        '(up-chat-data-to-all "RAW44W coverage gap: %d" g: gl-writer-remaining)',
        '(set-goal gl-writer-gap 1)'])
    resume = rule('''(goal gl-writer-gap 1)
        (up-compare-goal gl-writer-remaining c:> 0)
        (up-compare-goal gl-writer-minute c:> 0)''', [
        '(up-chat-data-to-all "RAW44W coverage resumed: %d" g: gl-writer-remaining)',
        '(set-goal gl-writer-gap 0)'])
    return block('PRELUDE', constants + startup + clock + replenish + boarding + gap + resume)


def observers(site: dict, facts: str, once: bool, reservation: bool) -> tuple[str, str]:
    ident = site['id']
    # Single-use engine delegations must be seen even before the first boarding;
    # their observer disables itself together with the original startup rule.
    gate = '' if once else '(up-compare-goal gl-writer-remaining c:> 0)\n(up-compare-goal gl-writer-minute c:> 0)\n'
    if not once and not reservation:
        gate += '(goal gl-writer-active 1)\n'
    arm = [f'(set-goal gl-writer-site {ident})'] + (['(disable-self)'] if once else [])
    header = [trace_chat('begin', f'c: {ident}')] + context('pre')
    header += ['(up-get-object-data object-data-id gl-writer-selected)',
               '(up-get-object-data object-data-group-flag gl-writer-flag)',
               trace_chat('selected', 'g: gl-writer-selected'),
               trace_chat('selected-flag', 'g: gl-writer-flag')]
    if not once:
        header += ['(up-modify-goal gl-writer-remaining c:- 1)',
                   '(up-modify-goal gl-writer-minute c:- 1)']
    before = rule(gate + facts, arm) + rule(f'(goal gl-writer-site {ident})', header)
    after = rule(f'(goal gl-writer-site {ident})', context('post') + [
        trace_chat('end', f'c: {ident}'), '(set-goal gl-writer-site 0)'])
    return block(f'{ident} PRE', before), block(f'{ident} POST', after)


def compile_payload(payload: dict[str, bytes]) -> tuple[dict[str, bytes], dict]:
    """Pure transformation. Return deployment bytes and exact source-site map."""
    decoded = {name: data.decode('utf-8-sig') for name, data in payload.items() if name.endswith('.per')}
    for name, text in decoded.items():
        if 'RAW44W BEGIN' in text:
            raise ValueError(f'already instrumented input: {name}')
        if re.search(r'\bstr-writer-[\w-]+\b', text):
            raise ValueError(f'writer string namespace collision: {name}')
        if any(int(value) in PRIVATE.values() for value in
               re.findall(r'\(defconst\s+\S+\s+(-?\d+)\s*\)', text)):
            raise ValueError(f'writer scratch collision: {name}')
    result = dict(payload)
    sites, excluded, jumps = [], [], {}
    next_id = 1
    for name, text in sorted(decoded.items()):
        if name in {'rawai-init-goals.per', 'rawai-customconstants.per', 'rawai-constants.per',
                    'rawai-unitconstants.per'}:
            continue
        rules = rule_blocks(text)
        wrappers = {}
        for index, (start, end, body, fact_block, actions) in enumerate(rules):
            kinds = dict(direct=DIRECT.findall(actions), delegation=DELEGATE.findall(actions),
                         group=GROUP.findall(actions), native_policy=POLICY.findall(actions))
            if not any(kinds.values()):
                continue
            facts = fact_block.removeprefix('(defrule').strip()
            site = dict(id=next_id, file=name, rule=index, line=text.count('\n', 0, start) + 1,
                        **kinds, facts=facts, actions=actions.rsplit(')', 1)[0].strip(),
                        rule_sha256=hashlib.sha256(body.encode()).hexdigest().upper())
            next_id += 1
            # These predicates consume or mutate state: never run them twice.
            unsafe = set(re.findall(r'\(([\w-]+)', facts)) - REPEATABLE_FACTS
            if unsafe:
                site['reason'] = f'predicate not certified repeatable: {sorted(unsafe)}'
                excluded.append(site)
                continue
            once = '(disable-self)' in actions
            reservation = bool(RESERVATION_MUTATION.search(actions))
            before, after = observers(site, facts, once, reservation)
            jumping = bool(re.search(r'\(up-jump-rule -?\d+\)\s*\)\s*$', actions))
            if 'up-jump-' in actions and not jumping:
                raise ValueError(f'nonterminal/dynamic jump at traced site: {name}:{index}')
            site.update(single_use=once, reservation_boundary=reservation, jumping=jumping)
            wrappers[index] = (before, after, site)
            sites.append(site)
        if not wrappers:
            continue
        # Original jump offsets count rules, not lines, and -1 jumps to self.
        first, original, cursor = {}, {}, 0
        for index in range(len(rules)):
            first[index] = cursor
            original[index] = cursor + (2 if index in wrappers else 0)
            cursor += (5 if wrappers[index][2]['jumping'] else 4) if index in wrappers else 1
        first[len(rules)] = cursor
        pieces, previous = [], 0
        for index, (start, end, body, facts, actions) in enumerate(rules):
            pieces.append(text[previous:start])
            if index in wrappers:
                pieces.append(wrappers[index][0])
            match = re.search(r'\(up-jump-rule (-?\d+)\)', body)
            if match:
                old = int(match[1]); target = index + old + 1
                if target not in first:
                    raise ValueError(f'jump leaves source file: {name}:{index} -> {target}')
                low, high = sorted((start, rules[target][0] if target < len(rules) else len(text)))
                if re.search(r'^\s*#(?:load-if|else|end-if)', text[low:high], re.M):
                    raise ValueError(f'conditional compilation crosses jump: {name}:{index}')
                traced_jump = index in wrappers and wrappers[index][2]['jumping']
                new = 0 if traced_jump else first[target] - original[index] - 1
                jumps.setdefault(name, {})[str(index)] = dict(old=old, new=new, target=target)
                body = body.replace(match[0], f'(up-jump-rule {new})', 1)
                if traced_jump:
                    ident = wrappers[index][2]['id']
                    # Carry only the original jump's firing through the logger.
                    # If original facts fail, this flag stays zero and fallthrough
                    # is untouched. No gameplay actions move to another rule.
                    body = body.replace(f'(up-jump-rule {new})',
                        f'(set-goal gl-writer-jumping {ident})\n\t(up-jump-rule {new})', 1)
            pieces.append(body)
            if index in wrappers:
                pieces.append(wrappers[index][1])
                if wrappers[index][2]['jumping']:
                    ident = wrappers[index][2]['id']
                    target = index + jumps[name][str(index)]['old'] + 1
                    delta = first[target] - (original[index] + 2) - 1
                    pieces.append(block(f'{ident} JUMP', rule(f'(goal gl-writer-jumping {ident})',
                        ['(set-goal gl-writer-jumping 0)', f'(up-jump-rule {delta})'])))
            previous = end
        pieces.append(text[previous:])
        result[name] = ''.join(pieces).encode('utf-8')
    # Place trace prelude after all goal initializers, before any controller.
    main = result['AI RAW.per'].decode('utf-8-sig')
    anchor = '(load "rawai-init-goals")'
    if main.count(anchor) != 1:
        raise ValueError('expected one initializer load')
    result['AI RAW.per'] = main.replace(anchor, anchor + '\n' + prelude(), 1).encode()
    init = result['rawai-init-goals.per'].decode('utf-8-sig')
    init, count = re.subn(r'RAWAI-P3B44T\d+: %d" c: \d+', f'{MARKER}" c: {VALUE}', init)
    if count != 1:
        raise ValueError('expected one runtime marker')
    result['rawai-init-goals.per'] = init.encode()
    manifest = dict(schema_version=1, marker=f'{MARKER.split(":")[0]}:{VALUE}',
        source_files={name: hashlib.sha256(data).hexdigest().upper() for name, data in payload.items()},
        sites=sites, excluded_sites=excluded, jumps=jumps,
        total_limit=TOTAL_LIMIT, per_minute_limit=MINUTE_LIMIT,
        identity_attempts=IDENTITY_ATTEMPTS, identity_interval_seconds=IDENTITY_INTERVAL,
        single_use_sites=sum(site['single_use'] for site in sites),
        limitations=[
            'Brackets repeat non-consuming rule facts; matching packets corroborate execution.',
            'Selected object is NOT a full commanded-member census; use replay packet object_ids.',
            'Builder/strategic-number delegation can produce later native commands outside a bracket.',
            'Unbracketed commands, disabled coverage and quota gaps are unresolved, not native proof.',
            'Excluded sites remain explicit; neither DUC group flags nor these logs enforce ownership.'])
    # Include four fingerprint literals and the delayed marker in the budget
    # before hashing the map, then recheck the exact final payload below.
    budget_payload = dict(result)
    budget_payload['AI RAW.per'] += b'\n' + b'(chat-to-all "RAW44W map")\n' * 4
    budget_payload['AI RAW.per'] += f'(chat-to-all "{MARKER}")\n'.encode()
    manifest['string_budget'] = string_budget(budget_payload)
    # Bind replay site IDs to these exact generated bytes, not just a reusable
    # human build label. Four short records avoid long-message replay loss.
    fingerprint = hashlib.sha256()
    for name, data in sorted(result.items()):
        fingerprint.update(name.encode() + b'\0' + hashlib.sha256(data).digest())
    fingerprint.update(json.dumps(manifest, sort_keys=True).encode())
    manifest['map_sha256'] = fingerprint.hexdigest().upper()
    # R1's replay begins in the tail of startup telemetry: none of the initial
    # marker/map records survived. Don't depend on that first frame. Stagger
    # players, repeat three times, and remain independent of invocation quotas.
    # Exact engine loss mechanism is unresolved; delivery needs a fresh replay.
    announce = rule('''(up-compare-goal gl-writer-identity-left c:> 0)
        (up-compare-goal gl-writer-now g:>= gl-writer-identity-next)''', [
        f'(up-chat-data-to-all "{MARKER}" c: {VALUE})'] + [
        f'(up-chat-data-to-all "RAW44W map{i}: {manifest["map_sha256"][i*16:(i+1)*16]}" c: 0)'
        for i in range(4)] + ['(up-modify-goal gl-writer-identity-left c:- 1)',
            '(up-modify-goal gl-writer-identity-next g:= gl-writer-now)',
            f'(up-modify-goal gl-writer-identity-next c:+ {IDENTITY_INTERVAL})'])
    main = result['AI RAW.per'].decode()
    result['AI RAW.per'] = main.replace(anchor, anchor + '\n' + block('MAP', announce), 1).encode()
    if string_budget(result) != manifest['string_budget']:
        raise ValueError('final string budget differs from fingerprinted budget')
    return result, manifest


def strip_payload(payload: dict[str, bytes], manifest: dict) -> dict[str, str]:
    """For non-regression tests: strip ONLY observers and undo jump relocation."""
    result = {}
    for name, data in payload.items():
        if not name.endswith('.per'):
            continue
        source = BLOCK.sub('', data.decode('utf-8-sig'))
        source = re.sub(r'\(set-goal gl-writer-jumping \d+\)\s*', '', source)
        rules = rule_blocks(source)
        for index, entry in sorted(manifest['jumps'].get(name, {}).items(), key=lambda x: int(x[0]), reverse=True):
            start, end, body, _, _ = rules[int(index)]
            source = source[:start] + body.replace(f"(up-jump-rule {entry['new']})",
                        f"(up-jump-rule {entry['old']})", 1) + source[end:]
        result[name] = source
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, help='Write the generated source-site identity map')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    _, manifest = compile_payload({p.name: p.read_bytes() for p in sorted(root.glob('*.per'))} |
                                  {p.name: p.read_bytes() for p in sorted(root.glob('*.ai'))})
    if args.manifest:
        args.manifest.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(marker=manifest['marker'], sites=len(manifest['sites']),
                         excluded=[{k: s[k] for k in ('id', 'file', 'line', 'reason')}
                                   for s in manifest['excluded_sites']],
                         once=manifest['single_use_sites'],
                         string_budget=manifest['string_budget']), indent=2))


if __name__ == '__main__':
    main()
