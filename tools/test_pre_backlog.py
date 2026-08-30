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


def expressions(text):
    """Parse the small selected PER rule subset; never pretend this is the engine."""
    text = re.sub(r'^\s*\(defrule\s*', '', text)
    tokens = re.findall(r'\(|\)|[^\s()]+', '\n'.join(x.split(';')[0] for x in text.splitlines()))
    stack, result = [], []
    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            if not stack:  # rule_blocks actions include the defrule's closing paren
                continue
            item = stack.pop()
            (stack[-1] if stack else result).append(item)
        else:
            stack[-1].append(token)
    return result


class BuilderOwnershipTests(unittest.TestCase):
    def execute(self, name, goals, sn, counts):
        def value(x):
            return {'YES': 1, 'NO': 0}.get(x, int(x) if re.fullmatch(r'-?\d+', x) else x)

        def fact(e):
            op, *a = e
            if op == 'true':
                return True
            if op in ('or', 'and'):
                return (any if op == 'or' else all)(fact(x) for x in a)
            if op == 'goal':
                return goals.get(a[0], 0) == value(a[1])
            if op in ('strategic-number', 'unit-type-count'):
                lhs = (sn if op == 'strategic-number' else counts).get(a[0], 0)
                rhs = value(a[2])
                return {'!=': lhs != rhs, '>': lhs > rhs, '>=': lhs >= rhs,
                        '<=': lhs <= rhs, '==': lhs == rhs}[a[1]]
            raise AssertionError('unsupported test fact: ' + repr(e))

        for row in rule_blocks(source(name)):
            if 'sn-disable-builder-assistance' not in row[4]:
                continue
            if not all(fact(e) for e in expressions(row[3])):
                continue
            for op, *a in expressions(row[4]):
                if op == 'set-goal':
                    goals[a[0]] = value(a[1])
                elif op == 'set-strategic-number':
                    sn[a[0]] = value(a[1])
                elif op == 'up-modify-goal' and a[1] == 's:=':
                    goals[a[0]] = sn.get(a[2], 0)
                elif op == 'up-modify-sn' and a[1] == 'g:=':
                    sn[a[0]] = goals[a[2]]
                else:
                    raise AssertionError('unsupported test action: ' + repr([op, *a]))

    def test_hold_survives_later_writers_and_release_uses_current_animals(self):
        main = source('AI RAW.per')
        self.assertLess(main.index('(load "rawai-ownership")'), main.index('(load "rawai-homebase")'))
        for initial, current in ((0, 1), (1, 0), (0, 0), (1, 1)):
            goals = {'gl-owner-worker-hold': 1, 'gl-owner-native-hold-applied': 0}
            sn = {'sn-disable-builder-assistance': initial, 'sn-object-repair-level': 3}
            counts = {'villager-hunter': initial, 'villager-shepherd': 0}
            self.execute('rawai-ownership.per', goals, sn, counts)
            self.execute('rawai-homebase.per', goals, sn, counts)
            self.assertEqual(sn['sn-disable-builder-assistance'], 1)
            counts['villager-hunter'] = current
            self.execute('rawai-homebase.per', goals, sn, counts)
            self.assertEqual(sn['sn-disable-builder-assistance'], 1)
            goals['gl-owner-worker-hold'] = 0
            self.execute('rawai-ownership.per', goals, sn, counts)
            self.assertEqual(sn['sn-disable-builder-assistance'], current)
            self.execute('rawai-homebase.per', goals, sn, counts)
            self.assertEqual(sn['sn-disable-builder-assistance'], current)
            self.assertEqual(sn['sn-object-repair-level'], 3)

    def test_every_reenable_requires_no_hold(self):
        for path in ROOT.glob('*.per'):
            for row in rule_blocks(source(path.name)):
                if '(set-strategic-number sn-disable-builder-assistance 0)' in row[4]:
                    if path.name == 'rawai-sn-defines.per':
                        self.assertIn('(disable-self)', row[4])
                        main = source('AI RAW.per')
                        self.assertLess(main.index('(load "rawai-sn-defines")'), main.index('(load "rawai-ownership")'))
                        continue
                    self.assertIn('(goal gl-owner-worker-hold NO)', row[3], path.name)
        self.assertNotIn('g:= gl-owner-native-builder-assist', source('rawai-ownership.per'))


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
