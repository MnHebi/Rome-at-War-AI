"""Non-gameplay maintenance: generation whitespace, provenance and identities."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import good_units_provenance as provenance
import sync_civ_strategies as sync
from validate_good_units import validate_provenance_sources
from validate_per import validate_file

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '#load-if-defined TEST-CIV\n(set-goal good-priests YES)\n(set-goal good-navy NO)\n'


class MaintenanceConsistencyTests(unittest.TestCase):
    def test_conditional_definitions_are_exclusive_not_blanket_exempt(self):
        source = ('#load-if-defined DE-AVAILABLE\n(defconst de-game 1)\n'
                  '(defconst wk-game 1)\n#else\n(defconst de-game 0)\n'
                  '#load-if-defined UP-GAME-WK\n(defconst wk-game 1)\n'
                  '#else\n(defconst wk-game 0)\n#end-if\n#end-if\n')
        with patch.object(Path, 'read_text', return_value=source):
            self.assertEqual(validate_file(Path('fixture.per')), [])
        for suffix in ('(defconst wk-game 0)\n',
                       '#load-if-defined UNRELATED\n(defconst de-game 0)\n#end-if\n'):
            with patch.object(Path, 'read_text', return_value=source + suffix):
                self.assertIn('duplicate_defconst',
                              [x['kind'] for x in validate_file(Path('fixture.per'))])
        with patch.object(Path, 'read_text', return_value='#else\n'):
            self.assertIn('unmatched_else', [x['kind'] for x in validate_file(Path('fixture.per'))])

    def validate_source(self, source, document=None, exists=True):
        if document is None:
            document = {'source_provenance': {
                'AI RAW.per_sha256': hashlib.sha256(SOURCE.encode()).hexdigest(),
                'AI RAW.per_input_schema': provenance.INPUT_SCHEMA,
                provenance.INPUT_HASH_KEY: hashlib.sha256(json.dumps(
                    provenance.parse_affinities(SOURCE), sort_keys=True,
                    separators=(',', ':')).encode()).hexdigest(),
            }}
        with patch.object(Path, 'exists', return_value=exists), patch.object(
                Path, 'read_text', return_value=source):
            return validate_provenance_sources(document, {'AI RAW.per_sha256': Path('fixture')})

    def test_diagnostic_edits_do_not_invalidate_evaluator_inputs(self):
        self.assertEqual(self.validate_source(SOURCE + '\n(load "new-observer")\n'), [])
        self.assertEqual(self.validate_source(';comment\n' + SOURCE.replace('\n', '\r\n')), [])

    def test_changed_doctrine_still_invalidates_provenance(self):
        for old, new in [('good-priests YES', 'good-priests NO'),
                         ('good-navy NO', 'good-navy YES'), ('TEST-CIV', 'OTHER-CIV')]:
            self.assertIn('evaluator inputs changed', self.validate_source(SOURCE.replace(old, new))[0])
        self.assertIn('evaluator inputs changed', self.validate_source('')[0])

    def test_missing_source_is_not_excused_by_semantic_hash(self):
        self.assertIn('authoritative source is missing', self.validate_source(SOURCE, exists=False)[0])

    def test_unknown_input_schema_is_rejected(self):
        document = {'source_provenance': {
            'AI RAW.per_input_schema': 'unknown', provenance.INPUT_HASH_KEY: '0' * 64}}
        self.assertIn('unsupported input schema', self.validate_source(SOURCE, document)[0])

    def test_legacy_and_other_source_hashes_remain_strict(self):
        with patch.object(Path, 'exists', return_value=True), patch(
                'validate_good_units.sha256', return_value='1' * 64):
            for key in ('AI RAW.per_sha256', 'empires2_x2_p1.dat_sha256'):
                issues = validate_provenance_sources(
                    {'source_provenance': {key: '0' * 64}}, {key: Path('fixture')})
                self.assertIn('recorded hash does not match', issues[0])

    def test_live_evaluator_fingerprint_matches_document(self):
        document = json.loads((ROOT / 'good-unit-evaluations.json').read_text())
        self.assertEqual(len(provenance.load_affinities(ROOT / 'AI RAW.per')), 34)
        self.assertEqual(document['source_provenance'][provenance.INPUT_HASH_KEY],
                         provenance.affinities_sha256(ROOT / 'AI RAW.per'))

    def test_four_formatted_civilizations_are_generation_idempotent(self):
        config = json.loads(sync.CONFIG_PATH.read_text())
        overrides = json.loads(sync.HISTORICAL_CONFIG_PATH.read_text())
        historical = {c: sync.historical_profile(v, overrides.get(c, {})) for c, v in config.items()}
        for civ in ('pontus', 'romeemp', 'romerep', 'seleucids'):
            with self.subTest(civ=civ):
                self.assertFalse(sync.update_civ_file(ROOT / f'rawai-civ-{civ}.per', civ,
                    historical[civ], config[civ], historical, config, False))

    def test_candidate_and_deployed_markers_are_separate(self):
        state = json.loads((ROOT / 'context/project-state.json').read_text())
        repo = state['repository']
        candidate = repo['candidate_marker']
        if repo['candidate_status'].startswith('DEPLOYED'):
            self.assertEqual(candidate, repo['runtime_marker'])
        else:
            self.assertNotEqual(candidate, repo['runtime_marker'])
        init = (ROOT / 'rawai-init-goals.per').read_text()
        label, number = candidate.rsplit(':', 1)
        self.assertIn(f'"{label}: %d" c: {number}', init)
        for finding in state['findings']:
            self.assertIsNone(re.search(r'marker[ -](?:500|502)\b', finding['next_action']))


if __name__ == '__main__':
    unittest.main()
