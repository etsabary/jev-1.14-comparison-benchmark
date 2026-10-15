# Results by function and load level

The [main report](README.md) explains the historical and new-run conditions. All cells below use strict primary results.

## What the question types mean

These short illustrations explain the task families. They are not additional scored questions or answer-key entries. Every actual item supplies its own rules, facts and five choices.

| Family | What the model has to do | Simple illustration |
|---|---|---|
| F01 Record lookup and filtering | Select records that meet stated conditions | Which listed request is both signed and marked urgent? |
| F02 Forward conditional reasoning | Apply an implication from its trigger | If an active badge grants entry and this badge is active, what follows? |
| F03 Necessary conditions and contraposition | Reason backward from a missing required condition | Every approved request needs a valid ticket; can one without a ticket be approved? |
| F04 Boolean scope and exclusivity | Track combinations such as both, either and exactly one | Which choice satisfies exactly one of two stated conditions? |
| F05 Quantifiers and set relations | Track all, some, none and overlapping groups | All teal tokens are marked; no marked token is blank; which relation follows? |
| F06 Transitive comparisons | Combine ordered comparisons | A is taller than B and B than C; how do A and C compare? |
| F07 Scheduling constraints | Fit events around order and exclusion rules | Which timetable puts one meeting before another without overlapping a break? |
| F08 One-to-one assignments | Give each item a unique partner while satisfying clues | Assign three people different desks using location restrictions. |
| F09 Exact truth counting | Count precisely how many statements hold | Under the supplied facts, how many of six claims are true? |
| F10 Truth-teller consistency | Find a consistent pattern of truthful and false statements | Which assignment of honest and dishonest speakers fits their claims? |
| F11 Sufficiency and inconsistency | Determine whether facts force an answer or contradict one another | Is a proposed arrangement determined, impossible or still underdetermined? |
| F12 Object tracking through swaps | Update locations after repeated exchanges | A red token starts in box A; several box contents are swapped; where does it end? |
| F13 Sequential procedure execution | Apply each ordered edit to the current state | Toggle one flag, swap two values, then conditionally reset another flag. |
| F14 Temporal interval relations | Compare starts, ends and overlapping periods | Which interval overlaps a specified event without containing it? |
| F15 Verbal spatial tracking | Update position or direction from described movement | Follow successive turns and moves, then identify the final direction. |
| F16 Nested role and reference binding | Resolve chains of names, roles and references | Identify the mentor of the colleague named in a nested description. |
| F17 Perspective and belief tracking | Distinguish what different observers witnessed | An object moves while one observer is absent; where will that observer look? |
| F18 Deterministic causal intervention | Recompute consequences of changing a specified input | Force a switch off while holding other inputs fixed; which lamp now lights? |
| F19 Exceptions and priority rules | Apply a rule, its exception and stated precedence | A badge permits entry unless a higher-priority suspension applies. |
| F20 Planning with preconditions | Choose an action sequence whose requirements are met | Obtain a key before opening a locked door, with limited moves available. |
| F21 Directed reachability | Follow arrows in their permitted direction | Can node A reach node D through the listed directed links? |
| F22 Deterministic preference ordering | Rank candidates using explicit tie-break rules | Rank by priority first, then age when priorities tie. |
| F23 Rule verification and counterexamples | Find a case that violates a stated rule | Which listed record disproves the claim that every approved item is signed? |
| F24 Source authority and stale records | Select the valid source rather than an outdated conflicting one | Two records disagree; which controls under the stated authority and date policy? |
| F25 Deterministic fault diagnosis | Match observed symptoms to explicit fault rules | Which fault is consistent with the supplied test results? |

## All 25 functions

| Function | n | Jev 1.14 | Jev 1.13 | Luna 6 regular | Mercury 2.5 | Luna 6 Decisions | Gemini 2.5 Flash-Lite | Qwen3-30B-A3B Instruct 2507 | Granite 4.2 8B | GPT-5.4 nano | Phi-4 14B | Mistral NeMo 12B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Record lookup and filtering | 37 | 37 (100.0%) | 37 (100.0%) | 37 (100.0%) | 36 (97.3%) | 37 (100.0%) | 36 (97.3%) | 31 (83.8%) | 31 (83.8%) | 30 (81.1%) | 32 (86.5%) | 29 (78.4%) |
| Forward conditional reasoning | 39 | 39 (100.0%) | 39 (100.0%) | 32 (82.1%) | 25 (64.1%) | 24 (61.5%) | 31 (79.5%) | 23 (59.0%) | 19 (48.7%) | 16 (41.0%) | 7 (17.9%) | 13 (33.3%) |
| Necessary conditions and contraposition | 46 | 46 (100.0%) | 45 (97.8%) | 13 (28.3%) | 24 (52.2%) | 13 (28.3%) | 25 (54.3%) | 17 (37.0%) | 5 (10.9%) | 8 (17.4%) | 0 (0.0%) | 10 (21.7%) |
| Boolean scope and exclusivity | 48 | 48 (100.0%) | 47 (97.9%) | 40 (83.3%) | 37 (77.1%) | 33 (68.8%) | 22 (45.8%) | 24 (50.0%) | 14 (29.2%) | 13 (27.1%) | 6 (12.5%) | 17 (35.4%) |
| Quantifiers and set relations | 43 | 42 (97.7%) | 42 (97.7%) | 38 (88.4%) | 39 (90.7%) | 38 (88.4%) | 32 (74.4%) | 38 (88.4%) | 35 (81.4%) | 24 (55.8%) | 29 (67.4%) | 21 (48.8%) |
| Transitive comparisons | 34 | 34 (100.0%) | 34 (100.0%) | 31 (91.2%) | 34 (100.0%) | 33 (97.1%) | 31 (91.2%) | 29 (85.3%) | 30 (88.2%) | 28 (82.4%) | 32 (94.1%) | 31 (91.2%) |
| Scheduling constraints | 69 | 46 (66.7%) | 43 (62.3%) | 27 (39.1%) | 36 (52.2%) | 25 (36.2%) | 16 (23.2%) | 24 (34.8%) | 25 (36.2%) | 16 (23.2%) | 21 (30.4%) | 19 (27.5%) |
| One-to-one assignments | 61 | 56 (91.8%) | 49 (80.3%) | 35 (57.4%) | 36 (59.0%) | 35 (57.4%) | 32 (52.5%) | 30 (49.2%) | 31 (50.8%) | 25 (41.0%) | 28 (45.9%) | 24 (39.3%) |
| Exact truth counting | 65 | 24 (36.9%) | 24 (36.9%) | 18 (27.7%) | 18 (27.7%) | 19 (29.2%) | 14 (21.5%) | 16 (24.6%) | 12 (18.5%) | 13 (20.0%) | 9 (13.8%) | 8 (12.3%) |
| Truth-teller consistency | 62 | 31 (50.0%) | 31 (50.0%) | 19 (30.6%) | 21 (33.9%) | 20 (32.3%) | 18 (29.0%) | 14 (22.6%) | 14 (22.6%) | 10 (16.1%) | 13 (21.0%) | 14 (22.6%) |
| Sufficiency and inconsistency | 35 | 29 (82.9%) | 28 (80.0%) | 22 (62.9%) | 18 (51.4%) | 19 (54.3%) | 14 (40.0%) | 14 (40.0%) | 21 (60.0%) | 14 (40.0%) | 20 (57.1%) | 15 (42.9%) |
| Object tracking through swaps | 46 | 29 (63.0%) | 29 (63.0%) | 17 (37.0%) | 20 (43.5%) | 16 (34.8%) | 16 (34.8%) | 21 (45.7%) | 10 (21.7%) | 14 (30.4%) | 18 (39.1%) | 14 (30.4%) |
| Sequential procedure execution | 42 | 6 (14.3%) | 5 (11.9%) | 9 (21.4%) | 6 (14.3%) | 9 (21.4%) | 7 (16.7%) | 11 (26.2%) | 5 (11.9%) | 9 (21.4%) | 7 (16.7%) | 8 (19.0%) |
| Temporal interval relations | 36 | 34 (94.4%) | 35 (97.2%) | 24 (66.7%) | 28 (77.8%) | 19 (52.8%) | 17 (47.2%) | 14 (38.9%) | 16 (44.4%) | 9 (25.0%) | 11 (30.6%) | 11 (30.6%) |
| Verbal spatial tracking | 43 | 32 (74.4%) | 24 (55.8%) | 27 (62.8%) | 19 (44.2%) | 21 (48.8%) | 23 (53.5%) | 16 (37.2%) | 12 (27.9%) | 20 (46.5%) | 8 (18.6%) | 14 (32.6%) |
| Nested role and reference binding | 44 | 34 (77.3%) | 34 (77.3%) | 24 (54.5%) | 21 (47.7%) | 20 (45.5%) | 21 (47.7%) | 19 (43.2%) | 14 (31.8%) | 14 (31.8%) | 19 (43.2%) | 12 (27.3%) |
| Perspective and belief tracking | 44 | 40 (90.9%) | 39 (88.6%) | 16 (36.4%) | 21 (47.7%) | 32 (72.7%) | 26 (59.1%) | 20 (45.5%) | 20 (45.5%) | 22 (50.0%) | 24 (54.5%) | 19 (43.2%) |
| Deterministic causal intervention | 44 | 36 (81.8%) | 36 (81.8%) | 25 (56.8%) | 16 (36.4%) | 20 (45.5%) | 9 (20.5%) | 12 (27.3%) | 9 (20.5%) | 13 (29.5%) | 11 (25.0%) | 11 (25.0%) |
| Exceptions and priority rules | 52 | 45 (86.5%) | 48 (92.3%) | 45 (86.5%) | 41 (78.8%) | 45 (86.5%) | 32 (61.5%) | 37 (71.2%) | 24 (46.2%) | 35 (67.3%) | 14 (26.9%) | 14 (26.9%) |
| Planning with preconditions | 37 | 36 (97.3%) | 35 (94.6%) | 27 (73.0%) | 21 (56.8%) | 28 (75.7%) | 13 (35.1%) | 19 (51.4%) | 10 (27.0%) | 10 (27.0%) | 11 (29.7%) | 11 (29.7%) |
| Directed reachability | 37 | 37 (100.0%) | 37 (100.0%) | 37 (100.0%) | 33 (89.2%) | 37 (100.0%) | 30 (81.1%) | 17 (45.9%) | 17 (45.9%) | 21 (56.8%) | 23 (62.2%) | 11 (29.7%) |
| Deterministic preference ordering | 45 | 45 (100.0%) | 44 (97.8%) | 45 (100.0%) | 45 (100.0%) | 44 (97.8%) | 38 (84.4%) | 40 (88.9%) | 35 (77.8%) | 36 (80.0%) | 28 (62.2%) | 33 (73.3%) |
| Rule verification and counterexamples | 46 | 45 (97.8%) | 45 (97.8%) | 44 (95.7%) | 36 (78.3%) | 36 (78.3%) | 29 (63.0%) | 31 (67.4%) | 27 (58.7%) | 22 (47.8%) | 19 (41.3%) | 17 (37.0%) |
| Source authority and stale records | 37 | 37 (100.0%) | 37 (100.0%) | 37 (100.0%) | 36 (97.3%) | 31 (83.8%) | 31 (83.8%) | 25 (67.6%) | 25 (67.6%) | 17 (45.9%) | 18 (48.6%) | 25 (67.6%) |
| Deterministic fault diagnosis | 44 | 44 (100.0%) | 43 (97.7%) | 38 (86.4%) | 35 (79.5%) | 33 (75.0%) | 35 (79.5%) | 22 (50.0%) | 17 (38.6%) | 25 (56.8%) | 20 (45.5%) | 20 (45.5%) |

## Core and related item types

| Group | n | Jev 1.14 | Jev 1.13 | Luna 6 regular | Mercury 2.5 | Luna 6 Decisions | Gemini 2.5 Flash-Lite | Qwen3-30B-A3B Instruct 2507 | Granite 4.2 8B | GPT-5.4 nano | Phi-4 14B | Mistral NeMo 12B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| contrast | 42 | 36 (85.7%) | 36 (85.7%) | 32 (76.2%) | 26 (61.9%) | 27 (64.3%) | 19 (45.2%) | 21 (50.0%) | 17 (40.5%) | 21 (50.0%) | 20 (47.6%) | 17 (40.5%) |
| core | 640 | 543 (84.8%) | 530 (82.8%) | 431 (67.3%) | 404 (63.1%) | 401 (62.7%) | 352 (55.0%) | 334 (52.2%) | 279 (43.6%) | 276 (43.1%) | 258 (40.3%) | 240 (37.5%) |
| probe | 80 | 41 (51.2%) | 36 (45.0%) | 17 (21.2%) | 28 (35.0%) | 32 (40.0%) | 24 (30.0%) | 21 (26.2%) | 25 (31.2%) | 17 (21.2%) | 9 (11.2%) | 19 (23.8%) |
| robustness | 374 | 312 (83.4%) | 308 (82.4%) | 247 (66.0%) | 244 (65.2%) | 227 (60.7%) | 203 (54.3%) | 188 (50.3%) | 157 (42.0%) | 150 (40.1%) | 141 (37.7%) | 145 (38.8%) |

## Engineered load levels

| Group | n | Jev 1.14 | Jev 1.13 | Luna 6 regular | Mercury 2.5 | Luna 6 Decisions | Gemini 2.5 Flash-Lite | Qwen3-30B-A3B Instruct 2507 | Granite 4.2 8B | GPT-5.4 nano | Phi-4 14B | Mistral NeMo 12B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 306 | 285 (93.1%) | 285 (93.1%) | 246 (80.4%) | 238 (77.8%) | 234 (76.5%) | 206 (67.3%) | 209 (68.3%) | 169 (55.2%) | 172 (56.2%) | 159 (52.0%) | 157 (51.3%) |
| 2 | 286 | 236 (82.5%) | 236 (82.5%) | 178 (62.2%) | 157 (54.9%) | 180 (62.9%) | 145 (50.7%) | 142 (49.7%) | 122 (42.7%) | 99 (34.6%) | 100 (35.0%) | 114 (39.9%) |
| 3 | 265 | 207 (78.1%) | 198 (74.7%) | 143 (54.0%) | 154 (58.1%) | 131 (49.4%) | 123 (46.4%) | 113 (42.6%) | 96 (36.2%) | 97 (36.6%) | 77 (29.1%) | 77 (29.1%) |
| 4 | 279 | 204 (73.1%) | 191 (68.5%) | 160 (57.3%) | 153 (54.8%) | 142 (50.9%) | 124 (44.4%) | 100 (35.8%) | 91 (32.6%) | 96 (34.4%) | 92 (33.0%) | 73 (26.2%) |
