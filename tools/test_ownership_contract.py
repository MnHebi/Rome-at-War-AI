"""Execute source predicates/filters against adversarial ownership fixtures.

This is not an AoE engine emulator and cannot close the native-manager boundary.
It tests the actual PER filters, reservation operations and command predicates.
"""
from pathlib import Path
import operator
import re
import unittest

from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]
OPS = {'==': operator.eq, '!=': operator.ne, '>=': operator.ge,
       '<=': operator.le, '>': operator.gt, '<': operator.lt}


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


def constants():
    return {k: int(v) for k, v in re.findall(r'\(defconst\s+(\S+)\s+(-?\d+)\)',
            source('rawai-customconstants.per') + source('rawai-constants.per')
            + source('rawai-unitconstants.per') + source('rawai-assault-mission-defs.per'))}


def select(name, facts, action=None):
    rows = [r for r in rule_blocks(source(name)) if facts in r[3]
            and (action is None or action in r[4])]
    if len(rows) != 1:
        raise AssertionError((name, facts, action, len(rows)))
    return rows[0]


class FilterMachine:
    """Interpret the ownership operations only, refusing unknown filter fields."""
    def __init__(self, units, groups=None, goals=None):
        self.units = {u['object-data-id']: dict(u) for u in units}
        self.local = list(self.units)
        self.groups = dict(groups or {})
        self.values = dict(constants(), **{'my-player-number': 1})
        self.values.update(goals or {})
        self.commands = []
        self.excluded_types = set()

    def value(self, token):
        return int(token) if re.fullmatch(r'-?\d+', token) else self.values[token]

    def run(self, actions):
        for expr in re.findall(r'\([^()\n]+\)', actions):
            t = expr[1:-1].split()
            if t[:2] == ['up-set-group', 'search-local']:
                self.local = list(self.groups.get(self.value(t[-1]), []))
            elif t[:2] == ['up-remove-objects', 'search-local']:
                _, _, field, op, value = t
                op = op.removeprefix('g:').removeprefix('c:')
                rhs = self.value(value)
                self.local = [i for n, i in enumerate(self.local)
                              if not OPS[op](n if field == 'object-data-index'
                                             else self.units[i][field], rhs)]
            elif t[0] == 'up-create-group':
                self.groups[self.value(t[-1])] = self.local[:40]
            elif t[0] == 'up-modify-group-flag':
                group = self.value(t[-1])
                for i in self.groups.get(group, []):
                    self.units[i]['object-data-group-flag'] = group if t[1] == '1' else -2
            elif t[0] == 'up-reset-group':
                self.groups[self.value(t[-1])] = []
            elif t[0] == 'up-get-object-data' and t[1] == 'object-data-type':
                self.values[t[2]] = self.units[self.local[0]][t[1]]
            elif t[0] == 'fe-exclude-from-attack-group':
                self.excluded_types.add(self.value(t[-1]))
            elif t[0] in ('up-target-point', 'up-target-objects'):
                self.commands.append(list(self.local))


def unit(i, flag=-2, player=1, idle=1, zone=4):
    return {'object-data-id': i, 'object-data-group-flag': flag,
            'object-data-player': player, 'object-data-idling': idle,
            'object-data-map-zone-id': zone, 'object-data-garrisoned': 0,
            'object-data-type': 74, 'object-data-class': 906,
            'object-data-under-attack': 0,
            'object-data-action': -1, 'object-data-language-id': 0,
            'object-data-target': -1, 'object-data-distance': 10}


class OwnershipContractTests(unittest.TestCase):
    def test_distinct_transport_and_specialist_slots(self):
        c = constants()
        names = ('attack-boarding-group', 'attack-transport-group',
                 'migration-boarding-group', 'migration-transport-group',
                 'recovery-boarding-group', 'recovery-transport-group',
                 'relic-ferry-passenger-group', 'relic-ferry-transport-group',
                 'naval-scout-group', 'opportunistic-raid-group',
                 'transport-screen-group', 'allied-relief-group')
        self.assertEqual(len(names), len({c[n] for n in names}))
        self.assertTrue(all(0 <= c[n] <= 19 for n in names))

    def test_no_global_reset_stop_or_recall(self):
        for path in ROOT.glob('*.per'):
            for _, _, _, _, actions in rule_blocks(source(path.name)):
                self.assertNotRegex(actions, r'\(up-(retreat-now|reset-unit|reset-attack-now)\b')

    def test_assault_command_refuses_other_owners_and_converted_units(self):
        row = select('rawai-military.per', '(goal gl-transport-route-state TRANSPORT-ROUTE-LOAD-ISSUE)', 'up-target-objects')
        m = FilterMachine([unit(1, 4), unit(2, 11), unit(3, 4, player=2), unit(4)])
        m.run(row[4])
        self.assertEqual(m.commands, [[1]])

    def test_migration_command_protects_other_missions(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if '(goal gl-island-migration-state MIGRATION-ISSUE-BOARD)' in r[3]
                and 'up-target-objects' in r[4]]
        self.assertEqual(len(rows), 2)
        for row in rows:
            m = FilterMachine([unit(1, 11), unit(2, 4), unit(3, 13)])
            m.run(row[4])
            self.assertEqual(m.commands, [[1]])

    def test_selection_to_reservation_race_refuses_worker_command(self):
        row = select('rawai-homebase.per', '(goal gl-farm-staffing-state FARM-STAFFING-CHECK-IDLE)', 'up-target-objects')
        m = FilterMachine([unit(1)], goals={'gl-boar-lurer-id': -1})
        # Selected FREE, then migration acquires it before the delayed command.
        m.units[1]['object-data-group-flag'] = 11
        m.run(row[4])
        self.assertEqual(m.commands, [[]])

    def test_direct_worker_writers_recheck_every_reserved_group(self):
        for filename in ('rawai-homebase.per', 'rawai-economy.per', 'rawai-hunt.per'):
            for _, _, _, _, actions in rule_blocks(source(filename)):
                if 'up-target-' not in actions:
                    continue
                self.assertIn('object-data-group-flag >= 0', actions)
                self.assertIn('object-data-player != my-player-number', actions)

    def test_native_build_and_hunt_delegation_honors_boarding_hold(self):
        for path in ROOT.glob('*.per'):
            for _, _, _, facts, actions in rule_blocks(source(path.name)):
                if re.search(r'\((build|up-build|up-assign-builders|up-request-hunters)\b', actions):
                    self.assertIn('(goal gl-owner-worker-hold NO)', facts, path.name)

    def test_native_explorer_is_reset_before_scout_acquisition(self):
        rows = rule_blocks(source('rawai-military.per'))
        reset = next(i for i, r in enumerate(rows) if 'MIGRATION-BOARDING' in r[3] and '(up-reset-scouts)' in r[4])
        claim = next(i for i, r in enumerate(rows) if 'MIGRATION-BOARDING' in r[3] and 'up-find-local c: scout-cavalry-class' in r[4])
        self.assertLess(reset, claim)
        for sn in ('sn-number-explore-groups', 'sn-total-number-explorers'):
            self.assertIn(f'(set-strategic-number {sn} 0)', rows[reset][4])

    def test_routine_defense_is_bounded_free_and_idle(self):
        row = select('rawai-military.per', '(goal gl-local-response-state LOCAL-RESPONSE-REBUILD)')
        m = FilterMachine([unit(1, 4), unit(2, 11), unit(3, idle=0)] + [unit(i) for i in range(4, 20)],
                          goals={'gl-local-response-zone': 4})
        m.run(row[4])
        self.assertEqual(m.local, list(range(4, 12)))
        self.assertNotIn('(up-retreat-now)', row[4])

    def test_severe_preemption_cancels_before_release_and_new_command(self):
        text = source('rawai-severe-defense.per')
        cancel = text.index('(set-goal gl-transport-route-state TRANSPORT-ROUTE-RECOVERY-WAIT)')
        release = text.index('(up-modify-group-flag 0 c: attack-boarding-group)', cancel)
        command = text.index('(up-target-objects', release)
        self.assertLess(cancel, release)
        self.assertLess(release, command)

    def test_friendly_damage_cannot_establish_severe_emergency(self):
        rows = [r for r in rule_blocks(source('rawai-severe-defense.per'))
                if '(set-goal gl-home-defense-state YES)' in r[4]]
        self.assertEqual(len(rows), 8)
        for p, row in enumerate(rows, 1):
            self.assertIn(f'(stance-toward {p} enemy)', row[3])
            self.assertIn('(up-compare-goal gl-owner-severe-count c:>= 8)', row[3])
        self.assertNotIn('object-data-under-attack', source('rawai-severe-defense.per'))

    def test_terminal_release_preserves_another_owner_and_converted_units(self):
        row = select('rawai-owner-release.per', '(up-group-size c: migration-boarding-group > 0)')
        m = FilterMachine([unit(1, 11), unit(2, 4), unit(3, 11, player=2)], groups={11: [1, 2, 3]})
        m.run(row[4])
        self.assertEqual([m.units[i]['object-data-group-flag'] for i in (1, 2, 3)], [-2, 4, 11])
        self.assertEqual(m.commands, [])

    def test_allied_anchor_captured_only_from_a_real_tc_and_never_overwritten(self):
        for p in range(1, 9):
            rows = [r for r in rule_blocks(source('rawai-home-anchors.per'))
                    if f'(up-get-point position-object gl-ally-home-{p}-x)' in r[4]]
            self.assertEqual(len(rows), 1)
            self.assertIn(f'(goal gl-ally-home-{p}-x -1)', rows[0][3])
        self.assertNotIn('villager-class', source('rawai-home-anchors.per'))
        self.assertEqual(source('rawai-home-anchors.per').count('(up-find-remote c: town-center c: 20)'), 8)

    def test_destroyed_tc_does_not_prevent_relief(self):
        rows = [r for r in rule_blocks(source('rawai-tauntcommands.per'))
                if '(up-copy-point gl-ally-help-target-x gl-ally-home-' in r[4]]
        self.assertEqual(len(rows), 0)
        verified = source('rawai-attack-verification.per')
        self.assertIn('(up-copy-point gl-ally-help-target-x gl-verify-asset-x)', verified)
        self.assertNotIn('town-center', verified)

    def test_relief_requires_a_live_hostile_and_nonempty_owned_responders(self):
        row = select('rawai-tauntcommands.per', '(goal gl-ally-help-state ALLY-HELP-OWNERSHIP-COMMAND)', 'up-target-objects')
        self.assertIn('(up-set-target-object search-remote c: 0)', row[3])
        self.assertIn('(up-group-size c: allied-relief-group > 0)', row[3])
        m = FilterMachine([unit(1, 17), unit(2, 4)], groups={17: [1, 2]})
        m.run(row[4])
        self.assertEqual(m.commands, [[1]])

    def test_full_and_partial_departure_keep_the_hull_owned(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-LOAD-READY)' in r[4]]
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertNotIn('(up-reset-group c: attack-transport-group)', row[4])

    def test_native_attack_type_exclusion_is_finite_and_released_next_sweep(self):
        rows = rule_blocks(source('rawai-native-attack-ownership.per'))
        self.assertEqual(sum('fe-exclude-from-attack-group' in r[4] for r in rows), 20)
        claim = next(r for r in rows if 'up-set-group search-local c: attack-boarding-group' in r[4])
        exclude = next(r for r in rows if 'fe-exclude-from-attack-group' in r[4])
        m = FilterMachine([unit(1, 4), unit(2, 4), unit(3), unit(4, 11)], groups={4: [1, 2, 4]})
        m.units[2]['object-data-type'] = 75
        m.run(claim[4])
        iterations = 0
        while m.local:
            m.run(exclude[4])
            iterations += 1
            self.assertLessEqual(iterations, 40)
        self.assertEqual(m.excluded_types, {74, 75})
        m.groups[4] = []
        m.excluded_types.clear() # actual prepass resets the exclusion list
        m.run(claim[4])
        self.assertEqual(m.local, [])
        self.assertEqual(m.excluded_types, set())

    def test_actual_hostile_filter_rejects_friendly_dead_and_wrong_zone(self):
        row = next(r for r in rule_blocks(source('rawai-severe-defense.per'))
                   if 'object-data-player != 2' in r[4] and 'up-find-remote' in r[4])
        # Execute the real remote filters against a fixture including friendly
        # damage, another island, and a dead unit; the ready search itself is
        # represented by the fixture's ready objects only.
        troops = [unit(i, player=2) for i in range(1, 9)] + [unit(9), unit(10, player=2, zone=5)]
        m = FilterMachine(troops, goals={'gl-home-zone': 4})
        m.run(row[4].replace('search-remote', 'search-local'))
        self.assertEqual(m.local, list(range(1, 9)))
        self.assertEqual(len(m.local), 8)

    def test_native_exclusion_loop_executes_actual_relative_jump_destinations(self):
        rows = rule_blocks(source('rawai-native-attack-ownership.per'))
        troops = [unit(i, 4) for i in range(1, 41)]
        for i, troop in enumerate(troops):
            troop['object-data-type'] = 100 + i
        m = FilterMachine(troops, groups={4: list(range(1, 41))})
        pc, steps = 0, 0
        while pc < len(rows):
            self.assertLess(steps, 200) # every type must make finite progress
            facts, actions = rows[pc][3:5]
            enabled = '(true)' in facts or bool(m.local)
            jump = 0
            if enabled:
                m.run(actions)
                match = re.search(r'\(up-jump-rule (-?\d+)\)', actions)
                if match:
                    jump = int(match[1])
            pc += 1 + jump
            steps += 1
        self.assertEqual(m.excluded_types, set(range(100, 140)))

    def test_relief_refuses_zero_actual_responders_before_promise(self):
        rows = [r for r in rule_blocks(source('rawai-tauntcommands.per'))
                if '(goal gl-ally-help-state ALLY-HELP-OWNERSHIP-COMMAND)' in r[3]]
        preparation = next(r for r in rows if 'gl-ally-help-responders g:= local-total' in r[4])
        command = next(r for r in rows if 'up-target-objects' in r[4])
        m = FilterMachine([unit(1, 4), unit(2, 17, player=2)], groups={17: [1, 2]})
        m.run(preparation[4])
        self.assertEqual(m.local, [])
        self.assertIn('(up-compare-goal gl-ally-help-responders c:> 0)', command[3])

    def test_routine_dispatch_selects_hostile_not_previous_local_tc(self):
        row = select('rawai-military.per', '(goal gl-local-response-state LOCAL-RESPONSE-DISPATCH)', 'up-target-objects')
        self.assertIn('(up-set-target-object search-remote c: 0)', row[3])
        self.assertIn('(up-object-data object-data-player g:== gl-local-response-player)', row[3])

    def test_severe_preemption_refuses_split_or_already_loaded_mission(self):
        rows = rule_blocks(source('rawai-severe-defense.per'))
        release = next(r for r in rows if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-RECOVERY-WAIT)' in r[4])
        selection = rows[rows.index(release)-1]
        troops = [unit(1, 4), unit(2, 4, zone=9), unit(3, 4)]
        troops[2]['object-data-garrisoned'] = 1
        m = FilterMachine(troops, groups={4: [1, 2, 3]}, goals={'gl-home-zone': 4})
        m.run(selection[4])
        self.assertEqual(m.local, [1])
        self.assertIn('(up-compare-goal local-total g:== gl-owner-severe-members)', release[3])

    def test_pass_start_hygiene_removes_foreign_references_without_mutating_them(self):
        row = select('rawai-owner-release.per', '(up-group-size c: 4 > 0)')
        m = FilterMachine([unit(1, 4), unit(2, 4, player=2), unit(3, 11)], groups={4: [1, 2, 3]})
        m.run(row[4])
        self.assertEqual(m.groups[4], [1])
        self.assertEqual([m.units[i]['object-data-group-flag'] for i in (1, 2, 3)], [4, 4, 11])

    def test_partial_migration_releases_ashore_members_but_retains_actual_cargo(self):
        row = select('rawai-military.per', '(goal gl-island-migration-load-terminal TRANSPORT-LOAD-TERMINAL-PARTIAL)', 'action-stop')
        ashore, cargo = unit(1, 11), unit(2, 11)
        cargo['object-data-garrisoned'] = 1
        m = FilterMachine([ashore, cargo], groups={11: [1, 2]}, goals={'position-self-x': 0})
        m.run(row[4])
        self.assertEqual(m.groups[11], [2])
        self.assertEqual(m.units[1]['object-data-group-flag'], -2)
        self.assertEqual(m.units[2]['object-data-group-flag'], 11)

    def test_all_direct_permission_sites_are_in_the_audit(self):
        from audit_ownership_source import inventory
        rows, failures = inventory()
        self.assertGreater(len(rows), 600)
        self.assertEqual(failures, [])

    def test_generated_policy_matches_checked_in_runtime(self):
        from generate_ownership_policy import anchors, severe, releases, native_attack
        for filename, generate in (
            ('rawai-home-anchors.per', anchors), ('rawai-severe-defense.per', severe),
            ('rawai-owner-release.per', releases), ('rawai-native-attack-ownership.per', native_attack)):
            self.assertEqual(source(filename), generate(), filename)

    def test_early_scout_capable_land_claims_cancel_exploration_before_claim(self):
        rows = rule_blocks(source('rawai-military.per'))
        for group in ('attack-boarding-group', 'home-defense-response-group',
                      'opportunistic-raid-group', 'recovery-boarding-group'):
            index = next(i for i, r in enumerate(rows)
                         if f'(up-create-group 0 0 c: {group})' in r[4]
                         and ';OWNERSHIP acquire:' in r[2])
            self.assertIn('(up-reset-scouts)', rows[index-1][4])
            self.assertIn('(goal gl-owner-explore-suspended NO)', rows[index-1][3])


if __name__ == '__main__':
    unittest.main()
