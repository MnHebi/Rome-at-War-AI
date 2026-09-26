"""Isolated modifier and observer regression contract; not engine acceptance."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_naval_doctrine import rule_blocks
from validate_villager_keystates import validate_repository, SET_CTRL, RESET_KEYS
from generate_boarding_ctrl_diag import render, NAMES
from villager_command_policy import inventory

def normalized(facts,actions):
    # Remove ONLY the new post-issuance observation sequence and modifier.
    actions=re.sub(r'\(up-get-search-state gl-board-diag-local\)\s*'
        r'\(up-set-target-object search-local c: 0\)\s*'
        r'\(up-get-object-data object-data-id gl-board-diag-issued-actor\)\s*'
        r'\(set-goal gl-board-diag-issued \d+\)', '',actions)
    actions=actions.replace(SET_CTRL,'').replace(RESET_KEYS,'')
    # Existing phase chat moved to the adjacent observer solely for rule size.
    actions=re.sub(r'\(up-chat-data[^\n]*', '',actions)
    return ' '.join((facts+actions).split())

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()

class BoardingCtrlTests(unittest.TestCase):
    def test_exact_five_mining_wrappers_and_existing_economy(self):
        self.assertEqual(validate_repository(ROOT),[])

    def test_all_original_military_command_contracts_survive(self):
        baseline=json.loads((ROOT/'tools/fixtures/boarding-ctrl-contracts.json').read_text())
        old=Counter(baseline['contracts'])
        matched=Counter()
        for a,b,block,facts,actions in rule_blocks((ROOT/'rawai-military.per').read_text(encoding='utf-8-sig')):
            if not re.search(r'\(up-target-(objects|point) ',actions):
                continue
            key=digest(normalized(facts,actions))
            if key not in old:
                facts=facts.replace('(not (goal gl-island-migration-mission MIGRATION-MISSION-MINING))','')
                facts=facts.replace('(goal gl-island-migration-mission MIGRATION-MISSION-MINING)','')
                key=digest(normalized(facts,actions))
            self.assertIn(key,old,'Changed selection, command, ownership, deadline or retry contract')
            matched[key]+=1
        self.assertEqual(set(old),set(matched))
        # Four shared rules split into mutually exclusive mining/non-mining.
        self.assertEqual(sum(matched.values())-sum(old.values()),4)

    def test_scout_counterparts_are_unchanged_not_ctrl(self):
        rules=rule_blocks((ROOT/'rawai-military.per').read_text(encoding='utf-8-sig'))
        copies=[r for r in rules if '(not (goal gl-island-migration-mission MIGRATION-MISSION-MINING))' in r[3]]
        self.assertEqual(len(copies),4)
        for r in copies:
            self.assertNotIn('sn-keystates',r[4])
            self.assertIn('action-garrison',r[4])

    def test_private_four_goal_output_block_is_contiguous(self):
        text=render()['rawai-boarding-ctrl-defs.per']
        for index,name in enumerate(NAMES[:4]):
            self.assertIn(f'(defconst gl-board-diag-{name} {15838+index})',text)

    def test_observers_are_bounded_and_have_no_gameplay_writes(self):
        files=render()
        capture=files['rawai-boarding-ctrl-capture.per']
        post=files['rawai-boarding-ctrl-post.per']
        self.assertIn('(set-goal gl-board-diag-left 8)',capture)
        self.assertIn('(up-modify-goal gl-board-diag-next c:+ 300)',capture)
        self.assertIn('(up-compare-goal gl-board-diag-local c:> 0)',capture)
        self.assertIn('(fe-filter-garrisoned c: 1)',post)
        self.assertIn('(up-add-object-by-id search-local g: gl-board-diag-actor)',post)
        self.assertIn('(goal gl-farm-staffing-state FARM-STAFFING-IDLE)',post)
        self.assertIn('(up-timer-status t-farm-staffing == timer-triggered)',post)
        for text in [capture,post]:
            self.assertNotRegex(text,r'\((up-target-(?:point|objects)|up-set-timer|set-strategic-number|up-modify-group-flag) ')
            for name in re.findall(r'\((?:set-goal|up-modify-goal) ([^ ]+)',text):
                self.assertTrue(name.startswith('gl-board-diag-'),name)
        for field in ['actor','hull','writer','modifier','observed','time','mission-state','action','target','order','garrisoned','carry','group']:
            self.assertIn('post-'+field,post)

    def test_capture_preserves_lists_and_has_no_target_reader_before_reset(self):
        for a,b,block,facts,actions in rule_blocks((ROOT/'rawai-military.per').read_text(encoding='utf-8-sig')):
            if SET_CTRL not in actions:
                continue
            before,after=actions.split('(set-goal gl-board-diag-issued ',1)
            self.assertIn('action-garrison',before)
            # The read-only selected-object pointer change occurs after issuance.
            # Original suffix never reads it; where a later command exists, it
            # rebuilds its own list first (rendezvous hull move).
            self.assertNotIn('up-get-object-data',after)
            self.assertNotIn('up-get-point',after)
            if 'up-target-' in after:
                self.assertLess(after.index('up-full-reset-search'),after.index('up-target-'))

    def test_generated_files_and_explicit_per_site_policy(self):
        for name,text in render().items():
            self.assertEqual((ROOT/name).read_text(encoding='utf-8-sig'),text)
        policy=json.loads((ROOT/'villager-command-modifier-policy.json').read_text())
        self.assertEqual(policy,inventory())
        self.assertEqual(sum(s['policy']=='EXPERIMENT: mining boarding' for s in policy['sites']),5)
        self.assertTrue(all(s['assessment'] for s in policy['sites']))

    def test_passenger_task_selections_bar_entering_units(self):
        """A selection that commands reserved passengers must exclude units that
        are already entering a transport, exactly as the stock AI does. Without
        this guard the boarding retry re-tasks villagers that are mid-board
        (T66: every sustained ORDER storm follows such a re-task)."""
        registry=json.loads((ROOT/'command-boundary-registry.json').read_text())
        guarded=0
        for site in registry['sites']:
            original=site.get('original') or ''
            if 'migration-boarding-group' not in original:
                continue
            if '(up-remove-objects search-local object-data-garrisoned == 1)' not in original:
                continue
            if not re.search(r'\(up-target-(objects|point) ',original):
                continue
            guarded+=1
            self.assertIn('(up-remove-objects search-local object-data-action == actionid-enter)',
                original,f'site {site["id"]} commands passengers without the enter guard')
            self.assertIn('(up-remove-objects search-local object-data-order == orderid-enter)',
                original,f'site {site["id"]} commands passengers without the enter-order guard')
        self.assertGreaterEqual(guarded,17)

    def test_passenger_task_selections_bar_laden_villagers(self):
        """514: a villager carrying resources is not admitted to the transport
        boarding command. T78/T80: every sustained ORDER storm follows a laden
        passenger that actually boards, and the carried load is what leaves the
        native return intent alive inside the hull. Laden units stay with the
        economy (no stop/reset/idle) and re-enter the boarding list once their
        carry reaches zero."""
        registry=json.loads((ROOT/'command-boundary-registry.json').read_text())
        guarded=0
        for site in registry['sites']:
            original=site.get('original') or ''
            if 'migration-boarding-group' not in original:
                continue
            if not re.search(r'\(up-target-objects 0 action-garrison ',original):
                continue
            guarded+=1
            self.assertIn('(up-remove-objects search-local object-data-carry > 0)',
                original,f'site {site["id"]} boards passengers without the laden filter')
            # The filter is an admission rule only: no release, stop or reset.
            for command in ('(up-reset-unit','action-stop','(up-retreat-now',
                            '(up-retreat-to','(up-delete-idle-units','(up-ungarrison'):
                self.assertNotIn(command,original,
                    f'site {site["id"]} mixes {command} into boarding admission')
        self.assertGreaterEqual(guarded,11)

    def test_migration_boarding_issuance_always_bars_entering_passengers(self):
        """215629: actor p4 34669 was commanded into the migration hull 42461 by
        MIGRATION-RENDEZVOUS-PASSENGER (writers 25/21, 2833-2849 s) while its own
        state was already `actionid-enter`/`orderid-enter` toward hull 36219, and
        it then stormed for 46,911 ORDER packets. The four migration
        boarding-issue sites applied the 514 zero-carry filter but omitted the
        entering guard that every sibling boarding site carries, so a passenger
        already entering one transport was re-commanded into a second hull. The
        guard is required of every site that commands a migration-boarding-group
        list, not only of the sites that also rebuild it via fe-filter-garrisoned.
        """
        registry=json.loads((ROOT/'command-boundary-registry.json').read_text())
        guarded=0
        for site in registry['sites']:
            original=site.get('original') or ''
            if 'object-data-group-flag != migration-boarding-group' not in original:
                continue
            if not re.search(r'\(up-target-objects 0 action-garrison ',original):
                continue
            guarded+=1
            self.assertIn('(up-remove-objects search-local object-data-action == actionid-enter)',
                original,f'site {site["id"]} commands migration passengers without the enter guard')
            self.assertIn('(up-remove-objects search-local object-data-order == orderid-enter)',
                original,f'site {site["id"]} commands migration passengers without the enter-order guard')
        self.assertEqual(guarded,11)

    def test_attack_lift_passenger_selections_bar_entering_units(self):
        """190351: the attack lift re-ordered a rotating subset of
        attack-boarding-group every ~4 s (10-18 distinct units, single units up to
        47 times, first and last packet sets disjoint) and finished with 0-4
        soldiers aboard at the deadline, so the hull aborted and stranded. The
        stock-AI guard that bars units already entering a transport now applies to
        the attack lift list exactly as it does to every migration selection."""
        registry=json.loads((ROOT/'command-boundary-registry.json').read_text())
        guarded=0
        for site in registry['sites']:
            original=site.get('original') or ''
            if 'attack-boarding-group' not in original:
                continue
            if not re.search(r'\(up-target-objects 0 action-garrison ',original):
                continue
            guarded+=1
            self.assertIn('(up-remove-objects search-local object-data-action == actionid-enter)',
                original,f'site {site["id"]} boards attackers without the enter guard')
            self.assertIn('(up-remove-objects search-local object-data-order == orderid-enter)',
                original,f'site {site["id"]} boards attackers without the enter-order guard')
        self.assertGreaterEqual(guarded,7)

if __name__=='__main__':
    unittest.main()
