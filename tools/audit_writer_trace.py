"""Correlate exact command packets with complete RAW44W rule brackets.

Do not attribute unbracketed packets to native tasking: persistent delegation,
excluded sites, runtime delivery and quota gaps preclude that inference.
"""
from __future__ import annotations

from collections import Counter
import re


def compatible(packet: dict, site: dict) -> bool:
    """Conservative command-family match, never nearest-log attribution."""
    kind, order = packet['action'], packet.get('order_id')
    for expression in re.findall(r'\([^()]*\)', site['actions']):
        command = expression[1:-1].split()[0]
        if command in {'up-retreat-now', 'up-retreat-to'} and kind == 'DE_RETREAT':
            return True
        if command in {'up-target-point', 'up-target-objects'}:
            if 'action-garrison' in expression:
                if kind == 'SPECIAL' and order == 5:
                    return True
            elif 'action-unload' in expression:
                if kind == 'UNGARRISON':
                    return True
            elif 'action-stop' in expression:
                if kind == 'STOP' or (kind == 'AI_ORDER' and order == 706):
                    return True
            elif 'action-move' in expression:
                if kind in {'MOVE', 'ORDER'} and packet.get('target_id', -1) == -1:
                    return True
            elif kind in {'WORK', 'ORDER', 'AI_ORDER', 'GUARD', 'FOLLOW', 'PATROL', 'DE_ATTACK_MOVE'}:
                return True
        elif command == 'up-reset-unit' and (kind == 'STOP' or kind == 'AI_ORDER' and order == 706):
            return True
        elif command in {'delete-unit', 'up-delete-idle-units', 'delete-building'} and kind == 'DELETE':
            return True
        elif command in {'up-send-scout', 'up-reset-scouts'} and kind in {'AI_ORDER', 'DE_AUTOSCOUT'}:
            return True
        elif command in {'up-garrison', 'up-ungarrison'} and kind in {'SPECIAL', 'UNGARRISON'}:
            return True
        elif command == 'up-guard-unit' and kind in {'GUARD', 'AI_ORDER'}:
            return True
        elif command == 'up-retask-gatherers' and kind in {'WORK', 'ORDER'}:
            return True
    return False


def intersections(packet, player, windows):
    rows = []
    for window in windows:
        if (window['player'] != player or not window['start']['sequence'] <= packet['sequence'] <= window['terminal']['sequence']):
            continue
        overlap = sorted({p['unit'] for p in window['passengers']}.intersection(packet.get('object_ids', [])))
        if overlap:
            rows.append(dict(sequence=packet['sequence'], hull=window['hull'], task=window['owner'],
                             units=overlap, action=packet['action'], target=packet.get('target_id'),
                             assessment='distinguish owner load/terminal from competing order'))
    return rows


def analyze_writer_trace(events: list[dict], manifest: dict, windows: list[dict] = ()) -> dict:
    sites = {site['id']: site for site in manifest['sites']}
    identities = {}
    for event in events:
        if event.get('action') != 'CHAT':
            continue
        match = re.fullmatch(r'RAW44W map([0-3]): ([0-9A-F]{16})', event.get('message', ''))
        if match:
            player = event.get('player_id', event.get('player'))
            identities.setdefault(player, {})[int(match[1])] = match[2]
    valid = {player for player, parts in identities.items()
             if ''.join(parts.get(i, '') for i in range(4)) == manifest['map_sha256']}
    opened, invocations, gaps, incomplete = {}, [], [], []
    for event in events:
        player = event.get('player_id', event.get('player'))
        text = event.get('message', '') if event.get('action') == 'CHAT' else ''
        begin = re.match(r'RAW44W begin: (\d+)$', text)
        end = re.match(r'RAW44W end: (\d+)$', text)
        if begin:
            if player in opened:
                incomplete.append(dict(opened.pop(player), reason='new begin before end'))
            opened[player] = dict(player=player, site_id=int(begin[1]), begin=event['sequence'],
                                  begin_ms=event['milliseconds'], fields={}, packets=[])
        elif end:
            current = opened.pop(player, None)
            if not current or current['site_id'] != int(end[1]):
                incomplete.append(dict(player=player, end=event['sequence'],
                                       reason='missing/mismatched begin', abandoned=current))
                continue
            current['end'] = event['sequence']
            current['end_ms'] = event['milliseconds']
            if player not in valid:
                incomplete.append(dict(current, reason='missing/mismatched replay source-map fingerprint'))
                continue
            site = sites.get(current['site_id'])
            if not site:
                incomplete.append(dict(current, reason='site absent from supplied build manifest'))
                continue
            current.update(file=site['file'], line=site['line'], commands=site['direct'],
                           group_changes=site['group'], native_policy=site['native_policy'],
                           delegation=site['delegation'])
            current['passenger_intersections'] = []
            for packet in current['packets']:
                current['passenger_intersections'].extend(intersections(packet, player, windows))
            current['assessment'] = ('command packets inside rule bracket' if current['packets']
                else 'policy/group/delegation or no immediate command; not evidence of a passenger overwrite')
            invocations.append(current)
        elif text.startswith('RAW44W coverage '):
            gaps.append(dict(player=player, sequence=event['sequence'], message=text))
        elif text.startswith('RAW44W ') and player in opened:
            label, _, value = text.removeprefix('RAW44W ').rpartition(': ')
            if re.fullmatch(r'-?\d+', value):
                opened[player]['fields'][label] = int(value)
        elif event.get('action') != 'CHAT' and player in opened:
            opened[player]['packets'].append({k: event[k] for k in
                ('sequence', 'milliseconds', 'action', 'object_ids', 'target_id', 'order_id', 'x', 'y')
                if k in event})
    incomplete.extend(dict(row, reason='replay ended before bracket end') for row in opened.values())
    # T8 direct evidence: after-command chat precedes its ORDER packet by 14/18
    # ms; recall caller tags precede DE_RETREAT bundles by 14-38 ms. Commands
    # are queued, so a closed chat bracket is NOT a packet delivery boundary.
    # 100 ms is a bounded candidate search, not proof that later calls cannot
    # belong. Keep every compatible issuer; never pick the nearest one.
    by_player = {}
    for invocation in invocations:
        by_player.setdefault(invocation['player'], []).append(invocation)
    inside = {p['sequence'] for inv in invocations for p in inv['packets']}
    deferred = []
    cursors = Counter()
    for packet in events:
        player = packet.get('player_id', packet.get('player'))
        if packet.get('action') == 'CHAT' or packet['sequence'] in inside or player not in valid:
            continue
        timeline = by_player.get(player, [])
        while cursors[player] < len(timeline) and timeline[cursors[player]]['end_ms'] < packet['milliseconds'] - 100:
            cursors[player] += 1
        candidates = []
        for index in range(cursors[player], len(timeline)):
            invocation = timeline[index]
            if invocation['end'] >= packet['sequence']:
                break
            site = sites[invocation['site_id']]
            if compatible(packet, site):
                candidates.append(dict(site_id=site['id'], file=site['file'], line=site['line'],
                    begin=invocation['begin'], end=invocation['end'],
                    delay_ms=packet['milliseconds']-invocation['end_ms'],
                    selected_member_match=invocation['fields'].get('selected') in packet.get('object_ids', []),
                    selected_flag=invocation['fields'].get('selected flag')))
        if candidates:
            deferred.append(dict(sequence=packet['sequence'], player=player, action=packet['action'],
                object_ids=packet.get('object_ids', []), target_id=packet.get('target_id'),
                candidate_issuers=candidates, passenger_intersections=intersections(packet, player, windows),
                assessment='single compatible traced issuer; correlate operands and ownership' if len(candidates)==1
                    else 'ambiguous traced issuers; do not select by proximity'))
    return dict(marker=manifest['marker'], map_sha256=manifest['map_sha256'],
                identity_verified_players=sorted(valid), invocations=invocations, incomplete=incomplete,
                coverage_gaps=gaps, deferred_packets=deferred,
                counts_by_file=dict(Counter(row['file'] for row in invocations)),
                excluded_sites=[{k: row[k] for k in ('id', 'file', 'line', 'reason')}
                                for row in manifest['excluded_sites']],
                limitations=manifest['limitations'] + [
                    'A bracket identifies the source rule window, not an engine call stack.',
                    'Queued packets can arrive after end tags; the 100ms candidate window is not a native/external exclusion proof.',
                    'Post-state changes and source group operations describe release/acquire intent; no ownership lock is implied.',
                    'Packets may reflect human/native activity; require matching API/action/targets before causal closure.'])
