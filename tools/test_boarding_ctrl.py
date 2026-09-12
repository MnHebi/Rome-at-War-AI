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

if __name__=='__main__':
    unittest.main()
