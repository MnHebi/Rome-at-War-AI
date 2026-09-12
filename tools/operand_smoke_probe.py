"""Generate a standalone, one-pass DE operand experiment; never install it.

Use the same data mod, one probe AI, and AI file logging. Each operation has
BEGIN/END markers. No production AI loads this script. It only reads facts,
sets private goals and clears/creates an empty local search group.
"""
import argparse
from pathlib import Path


def render():
    cases = []
    for value, native in enumerate(('dark-age', 'feudal-age', 'castle-age')):
        cases.extend([(f'age-number-{value}', f'(current-age == {value})', None),
                      (f'age-native-{native}', f'(current-age == {native})', None),
                      (f'age-alias-{value}', f'(current-age == probe-age-{value})', None)])
    # Zero is explicitly documented as a special operand in these commands.
    # Bracket them separately rather than claiming every goal-typed zero is bad.
    cases.extend([
        ('clock-zero', None, '(up-get-precise-time 0 101)'),
        ('can-build-zero', '(up-can-build 0 c: market)', None),
        ('can-build-goal', '(up-can-build 102 c: market)', None),
        ('can-build-line-zero', '(up-can-build-line 0 103 c: market)', None),
        ('can-build-line-goal', '(up-can-build-line 102 103 c: market)', None),
        ('distance-zero', None, '(up-get-point-distance 103 0 105)'),
        ('empty-group-zero', None, '(up-create-group 0 0 c: 0)'),
        ('empty-group-goals', None, '(up-create-group 106 107 c: 0)'),
    ])
    rules = []
    def rule(facts, actions):
        rules.append('(defrule\n\t'+'\n\t'.join(facts)+'\n=>\n\t'+'\n\t'.join(actions)+'\n)\n')
    def log(label, operand='c: 0'):
        return f'(up-log-data 0 "RAW-OPERAND {label} %d" {operand})'
    rule(['(true)'], ['(set-goal 102 0)', '(set-goal 103 0)', '(set-goal 104 0)',
                     '(set-goal 106 40)', '(set-goal 107 0)', '(up-full-reset-search)',
                     '(up-set-target-point 103)'])
    for native in ('dark-age', 'feudal-age', 'castle-age'):
        rule(['(true)'], [log('builtin-value-'+native, 'c: '+native)])
    for label, fact, action in cases:
        rule(['(true)'], [log('BEGIN-'+label)])
        rule([fact or '(true)'], [action or log('TRUE-'+label)])
        rule(['(true)'], [log('END-'+label)])
    rule(['(true)'], [log('COMPLETE'), '(set-goal 100 1)'])
    # On subsequent sweeps skip every test, including false predicates.
    header = '(defrule\n\t(goal 100 1)\n=>\n\t(up-jump-rule '+str(len(rules))+')\n)\n'
    constants = ''.join(f'(defconst probe-age-{i} {native})\n' for i,native in
                        enumerate(('dark-age','feudal-age','castle-age')))
    return constants+header+''.join(rules)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(render(), encoding='ascii')
