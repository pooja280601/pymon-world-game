# Pymon World

A text-based adventure/battler game built in Python, structured around object-oriented
design - players explore a connected map, collect items, and capture/battle creatures
called Pymon.

Built incrementally across four difficulty tiers (Pass → Credit → DI → HD), each adding
new mechanics on top of the last.

## Features by level

- **Pass** — core movement between locations, inspecting Pymon and surroundings
- **Credit** — inventory system, item pickup/use, Pymon switching
- **DI** — energy management, creature challenges/battles, additional validation
- **HD** — battle statistics tracking, save/load game state to file, custom
  creature/location creation, configurable data files via command-line arguments

## Design

- 13 classes including `Location`, `Creature`, `Pymon(Creature)`, `Item`, `Record`,
  `HDRecord(Record)`, `Operation`, and per-level `GameController` classes
- Custom exceptions (`InvalidDirectionException`, `InvalidInputFileFormat`) for
  input validation
- World data (locations, creatures, items) loaded from CSV files, making the
  game world fully configurable without touching code

## Tech

Python (object-oriented design, inheritance, exception handling, file I/O)

## Run it

```bash
python pymon_game.py
```

Requires `locations.csv`, `creatures.csv`, and `items.csv` in the same directory
(included in this repo). The HD level can optionally accept custom file paths as
command-line arguments:

```bash
python pymon_game.py locations.csv creatures.csv items.csv
```

## Notes

Built as a four-part coursework assignment, with each level demonstrating
progressively more advanced OOP design and software engineering practices.
