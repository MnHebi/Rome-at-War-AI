# Historical strategy model

The AI translates historically attested operational tendencies into mechanics the
AoE2 AI scripting engine can actually control. It does not claim to simulate
formations, command systems, or every army fielded across a civilization's full
history.

`civ-strategy-data.json` defines the Extreme profile for every civilization:

- three strategic specialties;
- four early and four late composition priorities;
- up to two late support priorities; and
- opening affinities on the AI's `0..4` scale.

`civ-strategy-historical-overrides.json` replaces only the fields that differ on
Hardest and every lower difficulty. Those profiles may use broader combined-arms
compositions and historically appropriate openings even when a unit category is
not selected by the focus workbook.

`tools/sync_civ_strategies.py` merges both profiles and emits compile-time
`DIFFICULTY-EXTREME` branches into every civilization PER file. It validates the
Extreme composition, specialties, and unit-based rushes against
`RAW AI unit focus spreadsheet.ods`; the historical profile is checked for valid
unit and strategy constants but is intentionally not restricted by the workbook.
The incomplete `RAW AI good units per civ.ods` is supporting guidance only; blank
cells are not treated as evaluations.

## Matchup and opening model

Enemy-specific rules are derived from the two active civilization profiles, not
from claims that every possible pair of civilizations fought one another. Early
composition slots receive the most weight, late slots receive less, and strategic
specialties reinforce broad battlefield roles such as infantry, missiles,
cavalry, elephants, priests, siege, and defensive play.

Each configured opening is scored against those roles using ordinary
counter-relationships. For example, spear pressure improves against mounted or
elephant-heavy enemies, skirmisher pressure improves against missile-heavy
enemies, cavalry pressure improves against archers, priests, and siege, and
cavalry pressure is reduced against spear or camel screens. Mirror commitments
are reduced when the civilization has a configured alternative. Adjustments are
clamped to the `0..4` affinity range.

Only openings already present in the active difficulty profile can be adjusted.
This preserves the focus-workbook boundary on Extreme while allowing the broader
historical profile below Extreme. The highest post-matchup tier is activated;
ties deliberately allow combined-arms openings.

## Rush execution

Moderate, Hard, Hardest, and Extreme load the shared rush executor. It supports
militia, spear, Horus, scout-cavalry, cavalry/Ratha, skirmisher, priest, siege,
swordsman/Legionary, tower, fast-age, and forward-castle openings. Unit openings
train only a bounded initial force before the normal composition system takes
over. Fast-age openings lower the early age-up target, and an opening force can
attack before the regular late-game periodic timer.

## Civilization profiles

| Civilization | Operational model represented by the AI |
| --- | --- |
| Armenians | Armored cavalry, mounted missiles, and clergy |
| Athenians | Spear line and missile support backed by a naval economy |
| Britons / Iceni | Mobile chariot-style raiding and massed tribal infantry |
| Carthaginians | Cavalry-led combined arms, missile troops, and naval pressure |
| Cretans | Stand-off archery and naval mobility |
| Dacians | Aggressive falx infantry, light cavalry, and siege support |
| Egyptians | Chariot-and-bow maneuver with sacred infantry |
| Gauls | Fast massed infantry attacks followed by cavalry exploitation |
| Germani | Close infantry cooperating with fast cavalry detachments |
| Goths | Sustained infantry pressure with cavalry pursuit |
| Gupta | Mobile royal combined arms with cavalry, bows, and siege |
| Han | Layered infantry and crossbows with engineered siege support |
| Huns | Repeated mounted raids followed by cavalry concentration |
| Iberians | Hit-and-run mounted pressure around a strong infantry core |
| Illyrians | Infantry and missile troops operating from a maritime base |
| Judeans | Defensive missile warfare with priests and siege |
| Kushans | Mounted-archer pressure sustained by a strong clerical arm |
| Macedonians | Phalanx anvil, cavalry hammer, and ranged support |
| Mauryans | Elephant, cavalry, missile, and clerical combined arms |
| Nanda | Elephant shock forces protected by mounted screens |
| Nubians | Archer and camel pressure with chariot mobility |
| Numidians | Dispersed light-cavalry skirmishing and rapid concentration |
| Parthians | Horse-archer harassment followed by armored cavalry shock |
| Persians | Heavy cavalry and chariot attack with a broad missile screen |
| Phoenicians | Naval and siege pressure backed by archers and heavy cavalry |
| Picts | Persistent infantry raids supported by light cavalry |
| Pontus | Flexible legionary infantry with cavalry and mounted missiles |
| Roman Empire | Legion-and-spear advance with crossbows and siege |
| Roman Republic | Manipular infantry with cavalry, missiles, siege, and naval support |
| Scythians | Deep mounted raids, refusal of static battle, and renewed attack |
| Seleucids | Pike and imitation-legion center with heavy cavalry and elephants |
| Spartans | Spear infantry holding the line for ranged and siege support |
| Syracusans | Fortified land-and-sea defense centered on artillery |
| Thracians | Shock infantry and light horse with mounted archers and priests |

## Research basis

The implementation uses primary sources where practical, while treating their
biases and literary conventions with caution:

- Polybius, *Histories* 3.117, for the cavalry exploitation at Cannae:
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0234%3Abook%3D3%3Achapter%3D117>
- Polybius, *Histories* 6.24, for Roman manipular organization:
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0234%3Abook%3D6%3Achapter%3D24>
- Caesar, *Gallic War* 4 and 5, for British chariot action, dispersal, and
  withdrawal:
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0001%3Abook%3D4>
  and
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0001%3Abook%3D5>
- Plutarch, *Life of Crassus*, for Parthian mounted archery and cataphract
  cooperation: <https://classics.mit.edu/Plutarch/crassus.html>
- Herodotus, *Histories* 4, for Scythian mobility and avoidance of a forced
  decisive battle:
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0126%3Abook%3D4&force=y>
- Thucydides, *History of the Peloponnesian War* 2 and 7, for Athenian and
  Syracusan naval operations:
  <https://www.perseus.tufts.edu/hopper/text?doc=urn%3Acts%3AgreekLit%3Atlg0003.tlg001.perseus-eng2%3A2>
  and
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0247%3Abook%3D7>
- Tacitus, *Germania* 7, for infantry and cavalry cooperation:
  <https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0083%3Achapter%3D7>
- Kautilya, *Arthashastra*, for the four-arm Indian force and operational use of
  elephants, cavalry, chariots, and infantry:
  <https://www.wisdomlib.org/hinduism/book/kautilya-arthashastra/d/doc366166.html>
- Arrian's account of Gaugamela, summarized with references by Livius, for the
  Macedonian combined-arms model:
  <https://www.livius.org/articles/battle/gaugamela-331-bce/>

The remaining profiles are conservative abstractions built from the same design
principles and the units explicitly approved in the focus workbook. They should
be refined when the mod developer supplies more specific campaign, period, or
faction interpretations.
