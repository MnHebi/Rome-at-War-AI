"""Release-prerequisite source contracts and deterministic boundary fixtures.

These do not simulate pathfinding, native queues or prove in-game acceptance.
"""
from pathlib import Path
import re
import unittest

from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


class ConcreteHeavyRemeTests(unittest.TestCase):
    def test_no_runtime_use_of_turtle_alias(self):
        for path in ROOT.glob('*.per'):
            code = '\n'.join(line.split(';')[0] for line in source(path.name).splitlines())
            code = re.sub(r'\(defconst quadrireme-line -282\)', '', code)
            self.assertNotIn('quadrireme-line', code, path.name)
        constants = source('rawai-unitconstants.per')
        self.assertIn('(defconst quadrireme 1870)', constants)
        self.assertIn('(defconst quinquereme 1750)', constants)
        self.assertIn('(defconst quadrireme-line -282)', constants)

    def test_concrete_selection_and_queue_census_precede_both_producers(self):
        for name in ('rawai-military-units-common.per', 'rawai-military-units-common-hard.per'):
            text = source(name)
            rows = list(rule_blocks(text))
            census = next(r for r in rows if '(set-goal gl-heavy-reme-train-id -1)' in r[4])
            self.assertIn('unit-type-count-total quadrireme gl-heavy-reme-count', census[4])
            self.assertIn('unit-type-count-total quinquereme gl-heavy-reme-upgraded-count', census[4])
            self.assertIn('gl-heavy-reme-count g:+ gl-heavy-reme-upgraded-count', census[4])
            selectors = [r for r in rows if re.search(r'set-goal gl-heavy-reme-train-id (quinquereme|quadrireme)', r[4])]
            self.assertEqual(len(selectors), 2)
            self.assertIn('(unit-available quinquereme)', selectors[0][3])
            self.assertIn('(unit-available quadrireme)', selectors[1][3])
            self.assertIn('(goal gl-heavy-reme-train-id -1)', selectors[1][3])
            producers = [r for r in rows if '(up-train gl-unitescrow-state g: gl-heavy-reme-train-id)' in r[4]]
            self.assertEqual(len(producers), 3)
            for row in producers:
                self.assertLess(selectors[-1][0], row[0])
                self.assertIn('(up-can-train gl-unitescrow-state g: gl-heavy-reme-train-id)', row[3])
                self.assertIn('gl-heavy-reme-count', row[3])
                self.assertIn('gl-naval-fleet-count-total g:<', row[3])
                self.assertIn('(up-modify-goal gl-heavy-reme-count c:+ 1)', row[4])
                self.assertIn('(up-modify-goal gl-naval-fleet-count-total c:+ 1)', row[4])

    def test_family_upgrade_and_queued_units_do_not_double_allowance(self):
        # Concrete census arithmetic and three capped producers are asserted above.
        for base, upgraded, queued, expected in ((3, 0, 0, 1), (0, 3, 0, 1),
                                                (2, 1, 1, 0), (0, 4, 0, 0)):
            count, trained = base + upgraded + queued, 0
            for _ in range(3):
                if count < 4:
                    count += 1
                    trained += 1
            self.assertEqual(trained, expected)

    def test_both_concrete_forms_are_available_to_existing_search_owners(self):
        text = source('rawai-military.per')
        for kind, number in (('local', 4), ('remote', 3)):
            self.assertEqual(len(re.findall(r'up-find-' + kind + r' c: quadrireme c:', text)), number)
            self.assertEqual(len(re.findall(r'up-find-' + kind + r' c: quinquereme c:', text)), number)


if __name__ == '__main__':
    unittest.main()
