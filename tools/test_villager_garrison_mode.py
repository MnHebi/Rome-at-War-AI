"""T35 native-garrison boundary contracts; engine behavior needs a fresh match."""

from pathlib import Path
import re
import unittest

from test_pre_backlog import source
from validate_naval_doctrine import matching_rules, rule_blocks


ROOT = Path(__file__).resolve().parents[1]
GARRISON = "(up-target-objects 0 action-garrison -1 stance-no-attack)"


class VillagerGarrisonModeTests(unittest.TestCase):
    def test_mode_two_is_the_only_one_shot_writer(self) -> None:
        writers = []
        for path in ROOT.glob("*.per"):
            text = source(path.name)
            self.assertNotRegex(text, r"up-modify-sn\s+sn-disable-villager-garrison")
            for rule in rule_blocks(text):
                values = re.findall(
                    r"\(set-strategic-number sn-disable-villager-garrison (-?\d+)\)",
                    rule[4],
                )
                for value in values:
                    writers.append((path.name, value, rule))
        self.assertEqual([(name, value) for name, value, _ in writers],
                         [("rawai-sn-defines.per", "2")])
        self.assertIn("(true)", writers[0][2][3])
        self.assertIn("(disable-self)", writers[0][2][4])

    def test_explicit_tc_safety_garrisons_remain(self) -> None:
        hunt = source("rawai-hunt.per")
        military = source("rawai-military.per")
        boar_find = matching_rules(
            hunt,
            facts=("BOAR-COMMIT-RESCUE-GARRISON",),
            actions=("up-find-remote c: town-center", "BOAR-COMMIT-RESCUE-GARRISON-SEND"),
        )
        boar_send = matching_rules(
            hunt,
            facts=("BOAR-COMMIT-RESCUE-GARRISON-SEND",),
            actions=(GARRISON,),
        )
        self.assertEqual(len(boar_find), 1)
        self.assertEqual(len(boar_send), 1)

        evacuations = matching_rules(
            military,
            facts=("LOCAL-RESPONSE-COMMAND",),
            actions=("up-find-remote c: town-center", GARRISON),
        )
        self.assertEqual(len(evacuations), 2)
        self.assertTrue(any("object-data-target != wall-class" in rule[4]
                            for rule in evacuations))
        self.assertTrue(any("object-data-target != gate-class" in rule[4]
                            for rule in evacuations))

    def test_explicit_transport_boarding_remains(self) -> None:
        military = source("rawai-military.per")
        migration = matching_rules(
            military,
            facts=("MIGRATION-ISSUE-BOARD",),
            actions=("migration-boarding-group", GARRISON),
        )
        assault = matching_rules(
            military,
            facts=("TRANSPORT-ROUTE-LOAD-ISSUE",),
            actions=(GARRISON, "gl-transport-route-load-deadline c:+ 30"),
        )
        self.assertEqual(len(migration), 2)
        self.assertEqual(len(assault), 1)


if __name__ == "__main__":
    unittest.main()
