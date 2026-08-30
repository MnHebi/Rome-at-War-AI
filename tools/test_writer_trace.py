from pathlib import Path
from historical_test_source import historical_runtime
import re
import tempfile
import unittest

from audit_writer_trace import analyze_writer_trace
from validate_naval_doctrine import rule_blocks
from validate_per import code_without_comments_or_strings, validate_file
from writer_trace import (BLOCK, PRIVATE, TRACE_TEXT, MARKER, VALUE, RESERVATION_MUTATION,
                          compile_payload, strip_payload, string_budget)

ROOT = Path(__file__).resolve().parents[1]


def normalized(text):
    return ' '.join(' '.join(code_without_comments_or_strings(line)
                            for line in text.splitlines()).split())


class WriterTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # R4 diagnostics remain analyzable with immutable historical site IDs.
        # T11 behavior is independently tested in test_ownership_contract.
        cls.source = historical_runtime()
        cls.payload, cls.manifest = compile_payload(cls.source)

    def identity(self, player=2):
        return [dict(sequence=-4+i, milliseconds=0, player=player, action='CHAT',
                     message=f'RAW44W map{i}: {self.manifest["map_sha256"][i*16:(i+1)*16]}')
                for i in range(4)]

    def test_every_original_rule_survives_with_original_jump_destinations(self):
        restored = strip_payload(self.payload, self.manifest)
        for name, body in restored.items():
            original = self.source[name].decode('utf-8-sig')
            if name == 'rawai-init-goals.per':
                body = body.replace(f'{MARKER}" c: {VALUE}', 'RAWAI-P3B44T9: %d" c: 450')
            self.assertEqual(normalized(original), normalized(body), name)

    def test_compiled_rules_fit_engine_structure_and_operand_checks(self):
        with tempfile.TemporaryDirectory(prefix='rawai-writer-test-') as directory:
            for name, data in self.payload.items():
                if not name.endswith('.per'):
                    continue
                path = Path(directory) / name
                path.write_bytes(data)
                self.assertEqual(validate_file(path), [], name)

    def test_trace_templates_are_defined_once_and_every_chat_keeps_its_text(self):
        main = self.payload['AI RAW.per'].decode()
        start = main.index('; RAW44W BEGIN PRELUDE')
        end = main.index('; RAW44W END', start)
        definitions = re.findall(r'\(defconst str-writer-([\w-]+) "([^"]+)"\)', main[start:end])
        self.assertEqual(dict(definitions), TRACE_TEXT)
        self.assertEqual(len(definitions), 12)
        self.assertLess(end, main.index('(load "rawai-map")'))
        refs = []
        for name, data in self.payload.items():
            if not name.endswith('.per'):
                continue
            text = data.decode('utf-8-sig')
            self.assertEqual(len(re.findall(r'\(defconst str-writer-', text)),
                             12 if name == 'AI RAW.per' else 0)
            for inserted in BLOCK.finditer(text):
                if not re.match(r'; RAW44W BEGIN \d+ (?:PRE|POST)\n', inserted[0]):
                    continue
                self.assertNotIn('"', inserted[0])
                for field, operand in re.findall(
                        r'\(up-chat-data-to-all str-writer-([\w-]+) ([^()]*)\)', inserted[0]):
                    refs.append(field)
                    self.assertIn(field, TRACE_TEXT)
                    self.assertIn('%d', TRACE_TEXT[field])
                    self.assertRegex(operand, r'^(?:c: \d+|g: gl-[\w-]+)$')
        self.assertEqual(len(refs), len(self.manifest['sites']) * 12)
        for field in TRACE_TEXT:
            self.assertEqual(refs.count(field), len(self.manifest['sites']))

    def test_string_budget_counts_allocations_not_unique_text_and_rejects_old_t10(self):
        budget = string_budget(self.payload)
        self.assertEqual(budget, self.manifest['string_budget'])
        self.assertEqual(budget['payload_literals'], 1466)
        self.assertEqual(budget['writer_literals'], 19)
        self.assertEqual(budget['eight_player_literal_projection'], 11728)
        # Restore the exact broken allocation pattern: one quoted template per
        # command at each site, instead of one reusable string-table constant.
        broken = {}
        for name, data in self.payload.items():
            if name.endswith('.per'):
                text = data.decode('utf-8-sig')
                text = re.sub(r'\(defconst str-writer-[\w-]+ "[^"]+"\)\n', '', text)
                text = re.sub(r'\bstr-writer-([\w-]+)\b',
                              lambda m: '"' + TRACE_TEXT[m[1]] + '"', text)
                if name == 'AI RAW.per':
                    # R1 did not contain the R3 delayed marker literal.
                    text = text.replace(f'(up-chat-data-to-all "{MARKER}" c: {VALUE})', '')
                data = text.encode()
            broken[name] = data
        with self.assertRaisesRegex(ValueError, '5665/1500 payload, 4219/32 writer'):
            string_budget(broken)
        # Comments don't allocate; a semicolon/escaped quote inside a string does.
        fixture = {'test.per': b'; "ignore"\n(chat-to-all "a;\\\"b") ; "ignore"\n'
                              b'(chat-to-all "a;\\\"b")\n'}
        self.assertEqual(string_budget(fixture)['payload_literals'], 2)
        changed = dict(self.source)
        changed['future.per'] = b'(defrule (true) => (chat-to-all "repeated"))\n' * 100
        with self.assertRaisesRegex(ValueError, 'string budget exceeded'):
            compile_payload(changed)

    def test_observers_never_search_command_mutate_groups_or_gameplay_goals(self):
        allowed = {'set-goal', 'up-modify-goal', 'up-get-fact', 'up-get-object-data',
                   'up-chat-data-to-all', 'disable-self', 'up-jump-rule'}
        for name, data in self.payload.items():
            if not name.endswith('.per'):
                continue
            for block in BLOCK.finditer(data.decode('utf-8-sig')):
                for _, _, _, _, actions in rule_blocks(block[0]):
                    for command, operands in re.findall(r'\(([\w-]+) ([^()]*)\)', actions):
                        self.assertIn(command, allowed)
                        if command in {'set-goal', 'up-modify-goal'}:
                            self.assertTrue(operands.startswith('gl-writer-'))
                        if command in {'up-get-fact', 'up-get-object-data'}:
                            self.assertTrue(operands.split()[-1].startswith('gl-writer-'))

    def test_scratch_collision_and_double_instrumentation_fail_closed(self):
        changed = dict(self.source)
        changed['collision.per'] = b'(defconst incompatible 13007)\n'
        with self.assertRaisesRegex(ValueError, 'collision'):
            compile_payload(changed)
        with self.assertRaisesRegex(ValueError, 'already instrumented'):
            compile_payload(self.payload)
        changed['collision.per'] = b'(defconst str-writer-begin "collision")\n'
        with self.assertRaisesRegex(ValueError, 'namespace collision'):
            compile_payload(changed)
        self.assertEqual(len(set(PRIVATE.values())), len(PRIVATE))
        changed['collision.per'] = b'(defconst incompatible 13011)\n'
        with self.assertRaisesRegex(ValueError, 'collision'):
            compile_payload(changed)

    def test_identity_is_delayed_staggered_bounded_and_independent_of_trace_quota(self):
        main = self.payload['AI RAW.per'].decode()
        announce = next(b[0] for b in BLOCK.finditer(main) if b[0].startswith('; RAW44W BEGIN MAP\n'))
        facts, actions = rule_blocks(announce)[0][3:]
        self.assertIn('(up-compare-goal gl-writer-identity-left c:> 0)', facts)
        self.assertIn('(up-compare-goal gl-writer-now g:>= gl-writer-identity-next)', facts)
        self.assertNotIn('gl-writer-minute', announce)
        self.assertNotIn('gl-writer-remaining', announce)
        self.assertIn(f'(up-chat-data-to-all "{MARKER}" c: {VALUE})', actions)
        self.assertEqual(actions.count('"RAW44W map'), 4)
        self.assertIn('(up-modify-goal gl-writer-identity-left c:- 1)', actions)
        self.assertIn('(up-modify-goal gl-writer-identity-next g:= gl-writer-now)', actions)
        self.assertIn('(up-modify-goal gl-writer-identity-next c:+ 30)', actions)
        self.assertEqual(self.manifest['identity_attempts'], 3)
        self.assertIn('(set-goal gl-writer-identity-next my-player-number)', main)
        self.assertIn('(up-modify-goal gl-writer-identity-next c:* 3)', main)
        self.assertIn('(up-modify-goal gl-writer-identity-next c:+ 5)', main)
        self.assertIn('(set-goal gl-writer-identity-left 3)', main)
        # Nominal one-second sweeps: even with invocation quota exhausted,
        # staggered players get three identity attempts, none at startup.
        schedule = {}
        for player in range(1, 9):
            due, left = player * 3 + 5, 3
            for now in range(181):
                if left > 0 and now >= due:
                    schedule.setdefault(player, []).append(now)
                    due, left = now + 30, left - 1
        self.assertEqual(schedule[1], [8, 38, 68])
        self.assertEqual(schedule[8], [29, 59, 89])
        self.assertEqual(len({time for times in schedule.values() for time in times}), 24)

    def test_relocated_jumps_reach_same_original_rule_or_its_observer(self):
        for name, entries in self.manifest['jumps'].items():
            text = self.payload[name].decode('utf-8-sig')
            inserted = [(m.start(), m.end()) for m in BLOCK.finditer(text)]
            compiled = rule_blocks(text)
            indices = [i for i, (start, *_rest) in enumerate(compiled)
                       if not any(a <= start < b for a, b in inserted)]
            sites = {s['rule']: s for s in self.manifest['sites'] if s['file'] == name}
            for old_index, jump in entries.items():
                old_index = int(old_index)
                at = indices[old_index]
                destination = at + int(re.search(r'\(up-jump-rule (-?\d+)\)', compiled[at][4])[1]) + 1
                if old_index in sites and sites[old_index]['jumping']:
                    self.assertEqual(destination, at + 1)  # footer, then guarded dispatch
                    self.assertIn('gl-writer-jumping', compiled[at + 2][3])
                    self.assertIn('(set-goal gl-writer-jumping 0)', compiled[at + 2][4])
                    destination = at + 3 + int(re.search(r'\(up-jump-rule (-?\d+)\)', compiled[at + 2][4])[1])
                target = jump['target']
                expected = indices[target] - (2 if target in sites else 0) if target < len(indices) else len(compiled)
                self.assertEqual(destination, expected, (name, old_index))

    def test_coverage_has_workers_recalls_and_group_lifecycle_with_explicit_exclusions(self):
        files = {s['file'] for s in self.manifest['sites']}
        self.assertTrue({'rawai-economy.per', 'rawai-general.per', 'rawai-hunt.per',
                         'rawai-homebase.per', 'rawai-military.per', 'rawai-tauntcommands.per'} <= files)
        self.assertTrue(any(s['reservation_boundary'] for s in self.manifest['sites']))
        self.assertEqual(self.manifest['excluded_sites'], [])
        jumping = [s for s in self.manifest['sites'] if s['jumping']]
        self.assertEqual(len(jumping), 1)
        self.assertIn('up-build-line', jumping[0]['delegation'])

    def test_budget_is_explicit_and_once_observers_disable_with_original(self):
        self.assertEqual(self.manifest['total_limit'], 512)
        self.assertEqual(self.manifest['per_minute_limit'], 96)
        main = self.payload['AI RAW.per'].decode()
        self.assertIn('RAW44W coverage gap:', main)
        self.assertIn('RAW44W coverage resumed:', main)
        for s in self.manifest['sites']:
            text = self.payload[s['file']].decode()
            before = next(b[0] for b in BLOCK.finditer(text)
                          if b[0].startswith(f"; RAW44W BEGIN {s['id']} PRE\n"))
            arm = rule_blocks(before)[0][4]
            self.assertEqual('(disable-self)' in arm, s['single_use'])

    def test_reservation_classification_uses_mutation_target_not_filter_reference(self):
        cleanup = next(s for s in self.manifest['sites'] if s['id'] == 41)
        self.assertEqual(cleanup['file'], 'rawai-general.per')
        self.assertIn('object-data-group-flag == migration-boarding-group', cleanup['actions'])
        self.assertFalse(cleanup['reservation_boundary'])
        self.assertFalse(RESERVATION_MUTATION.search(cleanup['actions']))
        for name in ('migration-boarding-group', 'migration-transport-group',
                     'attack-boarding-group', 'attack-transport-group'):
            for expression in (f'(up-create-group 0 0 c: {name})',
                               f'(up-modify-group-flag 1 c: {name})',
                               f'(up-modify-group-flag 0 c: {name})',
                               f'(up-reset-group c: {name})'):
                self.assertTrue(RESERVATION_MUTATION.fullmatch(expression), expression)
            read_only = (f'(up-remove-objects search-local object-data-group-flag == {name})\n'
                         '(up-create-group 0 0 c: 0)\n(up-modify-group-flag 1 c: 0)')
            self.assertFalse(RESERVATION_MUTATION.search(read_only))
            self.assertFalse(RESERVATION_MUTATION.search(f'(up-set-group search-local c: {name})'))
        # Previously omitted acquisition/release aliases are also recognized.
        for ident in (131, 132, 197, 233, 240):
            self.assertTrue(next(s for s in self.manifest['sites'] if s['id'] == ident)
                            ['reservation_boundary'])

    def test_only_actual_reservation_mutations_and_one_time_setup_bypass_boarding_gate(self):
        for s in self.manifest['sites']:
            text = self.payload[s['file']].decode()
            before = next(b[0] for b in BLOCK.finditer(text)
                          if b[0].startswith(f"; RAW44W BEGIN {s['id']} PRE\n"))
            facts = rule_blocks(before)[0][3]
            needs_boarding = not s['single_use'] and not s['reservation_boundary']
            self.assertEqual('(goal gl-writer-active 1)' in facts, needs_boarding, s['id'])
            if not s['single_use']:
                self.assertIn('(up-compare-goal gl-writer-remaining c:> 0)', facts)
                self.assertIn('(up-compare-goal gl-writer-minute c:> 0)', facts)
        # Site 41 still exists and is observable during boarding: don't solve
        # irrelevant idle logging by suppressing a possible passenger writer.
        site = next(s for s in self.manifest['sites'] if s['id'] == 41)
        text = self.payload[site['file']].decode()
        pre = next(b[0] for b in BLOCK.finditer(text) if b[0].startswith('; RAW44W BEGIN 41 PRE\n'))
        facts = rule_blocks(pre)[0][3]
        self.assertIn('(goal gl-writer-active 1)', facts)
        self.assertIn('(true)', facts)
        self.assertIn('(up-chat-data-to-all str-writer-begin c: 41)', pre)

    def test_brackets_are_player_specific_and_keep_packets_and_release_context(self):
        site = next(s for s in self.manifest['sites'] if s['direct'])
        def event(n, player, text=None):
            return dict(sequence=n, milliseconds=1000, action='CHAT' if text else 'WORK',
                        player=player, message=text or '', object_ids=[42], target_id=99)
        rows = [event(1, 2, f"RAW44W begin: {site['id']}"), event(2, 3), event(3, 2),
                event(4, 2, 'RAW44W post migration: 0'),
                event(5, 2, f"RAW44W end: {site['id']}"), event(6, 2)]
        window = dict(player=2, start={'sequence': 0}, terminal={'sequence': 7},
                      hull=30, owner='migration', passengers=[{'unit': 42}])
        out = analyze_writer_trace(self.identity() + rows, self.manifest, [window])
        self.assertEqual([p['sequence'] for p in out['invocations'][0]['packets']], [3])
        self.assertEqual(out['invocations'][0]['fields']['post migration'], 0)
        self.assertFalse(out['incomplete'])
        self.assertEqual(out['invocations'][0]['passenger_intersections'][0]['units'], [42])
        missing = analyze_writer_trace(rows, self.manifest, [window])
        self.assertFalse(missing['invocations'])
        self.assertIn('fingerprint', missing['incomplete'][0]['reason'])

    def test_source_map_fingerprint_changes_when_runtime_changes(self):
        changed = dict(self.source)
        changed['rawai-economy.per'] += b'\n; source identity change\n'
        _, manifest = compile_payload(changed)
        self.assertNotEqual(self.manifest['map_sha256'], manifest['map_sha256'])

    def test_unreviewed_consuming_predicates_are_explicitly_untraced(self):
        changed = dict(self.source)
        changed['future.per'] = b'(defrule\n(up-find-local c: villager c: 1)\n=>\n(up-target-point 0 action-stop -1 -1)\n)\n'
        compiled, manifest = compile_payload(changed)
        self.assertEqual(compiled['future.per'], changed['future.per'])
        self.assertEqual(manifest['excluded_sites'][0]['file'], 'future.per')

    def test_deferred_command_after_end_keeps_all_compatible_issuers(self):
        sites = [s for s in self.manifest['sites'] if '(up-retreat-now)' in s['actions']][:2]
        self.assertEqual(len(sites), 2)
        rows = self.identity()
        for i, site in enumerate(sites):
            rows += [dict(sequence=1+i*2, milliseconds=1000, player=2, action='CHAT', message=f'RAW44W begin: {site["id"]}'),
                     dict(sequence=2+i*2, milliseconds=1000, player=2, action='CHAT', message=f'RAW44W end: {site["id"]}')]
        rows += [dict(sequence=5, milliseconds=1018, player_id=2, action='DE_RETREAT', object_ids=[42])]
        report = analyze_writer_trace(rows, self.manifest)
        self.assertEqual(len(report['deferred_packets']), 1)
        self.assertEqual(len(report['deferred_packets'][0]['candidate_issuers']), 2)
        self.assertIn('ambiguous', report['deferred_packets'][0]['assessment'])

    def test_incomplete_and_gapped_trace_never_proves_native_writer(self):
        rows = [dict(sequence=1, milliseconds=1, player=2, action='CHAT', message='RAW44W begin: 1'),
                dict(sequence=2, milliseconds=2, player=2, action='CHAT', message='RAW44W coverage gap: 0')]
        out = analyze_writer_trace(rows, self.manifest)
        self.assertFalse(out['invocations'])
        self.assertEqual(len(out['incomplete']), 1)
        self.assertEqual(len(out['coverage_gaps']), 1)


if __name__ == '__main__':
    unittest.main()
