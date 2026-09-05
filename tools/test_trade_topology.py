"""Executable and mechanical contracts for the land/water trade topology."""
import operator
import re
import unittest

from test_pre_backlog import expressions, source
from validate_naval_doctrine import rule_blocks


CMP = {'==': operator.eq, '!=': operator.ne, '>': operator.gt,
       '>=': operator.ge, '<': operator.lt, '<=': operator.le}
CONSTANTS = {name: int(value) for name, value in re.findall(
    r"\(defconst ([\w-]+) (-?\d+)\)", source("rawai-customconstants.per"))}


class SourceGate:
    """Small fixture which deliberately models a clobbered shared DUC list."""

    def __init__(self, **goals):
        self.goals = goals

    def value(self, token):
        if re.fullmatch(r"-?\d+", token):
            return int(token)
        return self.goals.get(token, CONSTANTS.get(token, token))

    def fact(self, expr):
        op, *args = expr
        if op == "or":
            return any(self.fact(item) for item in args)
        if op == "goal":
            return self.value(args[0]) == self.value(args[1])
        if op == "up-compare-goal":
            return CMP[args[1].split(":")[-1]](
                self.value(args[0]), self.value(args[2]))
        if op == "up-set-target-object":
            return False
        raise AssertionError("unmodelled land-source fact: " + repr(expr))

    def accepts(self, facts):
        return all(self.fact(expr) for expr in expressions(facts))


def rules(name="rawai-economy.per"):
    return list(rule_blocks(source(name)))


def matching(facts=(), actions=(), name="rawai-economy.per"):
    return [r for r in rules(name)
            if all(x in r[3] for x in facts) and all(x in r[4] for x in actions)]


class TradeTopologyTests(unittest.TestCase):
    def setUp(self):
        self.economy = source("rawai-economy.per")
        self.constants = source("rawai-customconstants.per")
        self.init = source("rawai-init-goals.per")

    def test_private_topology_slots_and_runtime_identity_are_initialized(self):
        expected = {
            "gl-trade-land-mask": 373,
            "gl-trade-water-mask": 374,
            "gl-trade-land-source-x": 375,
            "gl-trade-land-source-y": 376,
            "gl-trade-land-producer-total": 377,
            "gl-trade-water-producer-total": 378,
            "gl-trade-land-verified": 379,
            "gl-trade-water-verified": 380,
            "gl-trade-land-active-count": 381,
            "gl-trade-water-active-count": 382,
            "gl-trade-land-growth-limit": 383,
            "gl-trade-water-growth-limit": 384,
            "gl-trade-scan-count": 385,
            "gl-trade-topology-next": 386,
            "gl-trade-land-proof-mask": 387,
            "gl-trade-water-proof-mask": 388,
        }
        found = {name: int(value) for name, value in re.findall(
            r"\(defconst (gl-trade-[\w-]+) (\d+)\)", self.constants)}
        for name, value in expected.items():
            self.assertEqual(found.get(name), value, name)
            self.assertIn(f"(set-goal {name} ", self.init)
        self.assertIn('RAWAI-P3B44T46: %d" c: 494', self.init)

    def test_land_scan_uses_bounded_literal_player_slots(self):
        rows = matching(
            facts=("TRADE-ROUTE-LAND-SOURCE",),
            actions=("set-goal gl-trade-route-player 1",
                     "TRADE-ROUTE-LAND-START"))
        self.assertEqual(len(rows), 1)
        facts = rows[0][3]
        gate = SourceGate(**{
            "gl-trade-route-state": CONSTANTS["TRADE-ROUTE-LAND-SOURCE"],
            "gl-trade-land-producer-total": 1,
            "gl-trade-valid-producer-total": 1,
        })
        self.assertTrue(gate.accepts(facts))
        land_region = self.economy[
            self.economy.index("TRADE-ROUTE-LAND-SOURCE"):
            self.economy.index(";Water scanning always follows")]
        self.assertNotIn("up-find-player ally find-ordered", land_region)
        self.assertNotIn("up-find-next-player ally find-ordered", land_region)
        advance = matching(
            facts=("TRADE-ROUTE-LAND-ADVANCE", "gl-trade-scan-count c:< 8"),
            actions=("gl-trade-route-player c:+ 1", "TRADE-ROUTE-LAND-START"))
        self.assertEqual(len(advance), 1)

    def test_each_land_census_persists_a_safe_source_anchor(self):
        for colony, x, y in (
                ("NO", "gl-home-anchor-x", "gl-home-anchor-y"),
                ("YES", "gl-island-colony-x", "gl-island-colony-y")):
            rows = matching(
                facts=(f"gl-island-colony-established {colony}",),
                actions=(f"gl-trade-land-source-x g:= {x}",
                         f"gl-trade-land-source-y g:= {y}",
                         "TRADE-ROUTE-LAND-SOURCE"))
            self.assertEqual(len(rows), 1, colony)

    def test_land_scan_admits_cross_zone_markets_to_bounded_cart_probe(self):
        bits = (1, 2, 4, 8, 16, 32, 64, 128)
        scans = []
        for player, bit in enumerate(bits, 1):
            player_scans = matching(
                facts=("TRADE-ROUTE-LAND-START",
                       f"gl-trade-route-player {player}",
                       f"not (player-number {player})",
                       f"player-in-game {player}",
                       f"stance-toward {player} ally"),
                actions=(f"sn-focus-player-number c:= {player}",
                         "up-find-remote c: market c: 20",
                         "up-get-search-state local-total",
                         "gl-trade-valid-producer-total g:= remote-total",
                         "TRADE-ROUTE-LAND-CHECK"))
            self.assertEqual(len(player_scans), 1, ("scan", player))
            scans.extend(player_scans)
            rows = matching(
                facts=("TRADE-ROUTE-LAND-CHECK",
                       f"gl-trade-route-player c:== {player}",
                       "gl-trade-valid-producer-total c:> 0"),
                actions=(f"gl-trade-land-mask c:+ {bit}",
                         "gl-trade-scan-count c:+ 1",
                         "TRADE-ROUTE-LAND-ADVANCE"))
            self.assertEqual(len(rows), 1, player)
        self.assertNotIn("up-path-distance gl-trade-land-source-x", self.economy)
        self.assertNotIn("trade land candidate unreachable", self.economy)
        self.assertNotIn(
            "object-data-map-zone-id g:!= gl-trade-land-zone", self.economy)
        missing = matching(
            facts=("TRADE-ROUTE-LAND-CHECK",
                   "gl-trade-valid-producer-total c:<= 0"),
            actions=("gl-trade-scan-count c:+ 1", "TRADE-ROUTE-LAND-ADVANCE"))
        self.assertEqual(len(missing), 1)
        self.assertNotIn("gl-trade-land-mask c:+", missing[0][4])
        land_checks = [r for r in rules()
                       if "TRADE-ROUTE-LAND-CHECK" in r[3]]
        self.assertTrue(land_checks)
        self.assertTrue(all("up-set-target-object search-remote" not in r[3]
                            for r in land_checks))
        skipped = matching(
            facts=("TRADE-ROUTE-LAND-START",),
            actions=("set-goal gl-trade-valid-producer-total 0",
                     "TRADE-ROUTE-LAND-CHECK"))
        self.assertEqual(len(skipped), 1)
        self.assertTrue(all(scan[0] < skipped[0][0] for scan in scans))

    def test_land_completion_always_continues_into_water_scan(self):
        by_bound = matching(
            facts=("TRADE-ROUTE-LAND-ADVANCE", "gl-trade-scan-count c:>= 8"),
            actions=("TRADE-ROUTE-WATER-SOURCE",))
        self.assertEqual(len(by_bound), 1)
        self.assertNotIn("TRADE-ROUTE-IDLE", by_bound[0][4])

    def test_water_scan_has_independent_player_mask_and_no_land_gate(self):
        bits = (1, 2, 4, 8, 16, 32, 64, 128)
        for player, bit in enumerate(bits, 1):
            rows = matching(
                facts=("TRADE-ROUTE-WATER-CHECK",
                       f"gl-trade-route-player c:== {player}"),
                actions=(f"gl-trade-water-mask c:+ {bit}",
                         "gl-trade-scan-count c:+ 1",
                         "TRADE-ROUTE-WATER-ADVANCE"))
            self.assertEqual(len(rows), 1, player)
            self.assertNotIn("gl-land-trade-route", rows[0][3])

    def test_topology_publication_never_claims_execution_proof(self):
        for mask, route in (("gl-trade-land-mask", "gl-land-trade-route"),
                            ("gl-trade-water-mask", "gl-water-trade-route")):
            rows = matching(
                facts=("TRADE-ROUTE-FINALIZE", f"{mask} c:> 0"),
                actions=(f"(set-goal {route} YES)",))
            self.assertEqual(len(rows), 1)
            self.assertNotIn("verified YES", rows[0][4])
        candidate_rules = [r for r in rules()
                           if "TRADE-ROUTE-LAND-CHECK" in r[3]
                           or "TRADE-ROUTE-WATER-CHECK" in r[3]
                           or "TRADE-ROUTE-FINALIZE" in r[3]]
        self.assertTrue(candidate_rules)
        self.assertTrue(all("gl-trade-action-verified YES" not in r[4]
                            for r in candidate_rules))

    def test_execution_proof_records_exact_target_player_and_action(self):
        for prefix, check in (("land", "ACTION"), ("water", "WATER")):
            start = matching(
                facts=(f"TRADE-ROUTE-{prefix.upper()}-PROOF-START",),
                actions=("object-data-action != actionid-trade",
                         f"TRADE-ROUTE-{check}-PROOF-CHECK"))
            self.assertEqual(len(start), 1)
            bits = (1, 2, 4, 8, 16, 32, 64, 128)
            for player, bit in enumerate(bits, 1):
                success = matching(
                    facts=(f"TRADE-ROUTE-{check}-PROOF-CHECK",
                           f"up-object-target-data object-data-player c:== {player}"),
                    actions=(f"gl-trade-{prefix}-proof-mask {bit}",
                             f"gl-trade-{prefix}-verified YES"))
                self.assertEqual(len(success), 1, (prefix, player))

    def test_candidate_probes_are_bounded_but_full_growth_is_proof_gated(self):
        for prefix, unit, producer in (("land", "trade-cart", "market"),
                                       ("water", "trade-cog", "dock")):
            probe = matching(
                facts=(f"gl-trade-{prefix}-verified NO", f"{unit} < 3"),
                actions=(f"(train {unit})",))
            self.assertEqual(len(probe), 1)
            self.assertNotIn("gl-trade-action-verified YES", probe[0][3])
            full = matching(
                facts=(f"gl-trade-{prefix}-verified YES",
                       "gl-trade-action-verified YES",
                       f"{unit} g:< gl-trade-{prefix}-growth-limit",
                       f"building-type-count {producer} g:== gl-trade-{prefix}-producer-total"),
                actions=(f"(train {unit})",))
            self.assertEqual(len(full), 1)
        water_full = matching(
            facts=("gl-trade-water-verified YES", "gl-trade-action-verified YES"),
            actions=("(train trade-cog)",))
        self.assertEqual(len(water_full), 1)
        self.assertNotIn("(goal gl-land-trade-route NO)", water_full[0][3])

    def test_retirement_and_large_transition_cannot_use_candidate_masks(self):
        transition = matching(
            facts=("TRADE-TRANSITION-NONE", "gl-trade-action-verified YES"),
            actions=("TRADE-TRANSITION-ROUTE",))
        retirement = matching(
            facts=("gl-trade-action-verified YES", "gl-trade-active-count c:>= 3"),
            actions=("TRADE-RETIRE-SELECT",))
        self.assertEqual(len(transition), 1)
        self.assertEqual(len(retirement), 1)
        for row in transition + retirement:
            self.assertNotIn("gl-trade-land-mask", row[3])
            self.assertNotIn("gl-trade-water-mask", row[3])
        fallback = matching(
            facts=("gl-trade-route-failures c:>= 3", "gl-trade-probe-trained c:< 3"),
            actions=("(train trade-cog)", "gl-trade-probe-trained c:+ 1"))
        self.assertEqual(len(fallback), 1)


if __name__ == "__main__":
    unittest.main()
