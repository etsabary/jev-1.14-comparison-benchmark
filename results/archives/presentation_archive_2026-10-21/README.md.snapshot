# System 1 Decision Benchmark

23 specialized decision models and 3 high-end LLM references on 1,342 text questions.

Updated October 20, 2026. Added complete d3-turbo, Amos Large and Sqwish kettei-fat runs; all earlier measurements are unchanged.

**Respan Span-02 remains the leading specialized decision model at 1127/1342 (84.0%). Newcomer d3-turbo is fourth at 1106/1342 (82.4%); Amos Large and kettei-fat score 80.0% and 79.4%.**

[Interactive report](https://etsabary.github.io/system-1-decision-benchmark/report.html) · [New findings](https://etsabary.github.io/system-1-decision-benchmark/report.html#new-additions) · [Named, color-coded categories](https://etsabary.github.io/system-1-decision-benchmark/report.html#functions) · [Which models read images?](IMAGE_CAPABILITIES.md).

![All 26 routes: accuracy, speed and cost](direct_additions_2026-10-20/accuracy_speed_cost.png)

## Results, speed and cost

Every row covers 1342 first attempts. Per-1000 costs are normalized; actual 1342-question totals are separate. Free public access is not a metered production price of zero. Qwen’s amount is a prepaid-quota valuation, not a cash invoice. + ? means additional unreported charges.

| Model | Type | Correct /1342 | Accuracy | Median | p95 | Cost per 1000 | Actual 1342-question cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-6 Sol — no reasoning | LLM reference | 1143/1342 | 85.2% | 1023 ms 🟥 Slow | 1546 ms | $0.63211 🟥 Highest | $0.848294 |
| Respan Span-02 | Decision model | 1127/1342 | 84.0% | 206 ms 🟩 Fastest | 2157 ms | $0.00354 🟩 Lowest | $0.004746 |
| Perplexity Decider v1.2 | Decision model | 1120/1342 | 83.5% | 249 ms 🟩 Fastest | 332 ms | $0.00700 🟩 Lowest + ? | $0.009394 + ? |
| Nimble v4 Max | Decision model | 1115/1342 | 83.1% | 235 ms 🟩 Fastest | 329 ms | ~$0.02763 🟧 Mid | ~$0.037084 |
| d3-turbo | Decision model | 1106/1342 | 82.4% | 165 ms 🟩 Fastest | 298 ms | Free public access* | Free public access* |
| Liquid d1-ultra | Decision model | 1084/1342 | 80.8% | 200 ms 🟩 Fastest | 393 ms | $0.01212 🟨 Low + ? | $0.016270 + ? |
| Amos 1 Large | Decision model | 1074/1342 | 80.0% | 311 ms 🟨 Fast | 360 ms | Free public access* | Free public access* |
| Sonnet 5.5 — no thinking, JSON-choice | LLM reference | 1070/1342 | 79.7% | 1506 ms 🟥 Slow | 2424 ms | $1.43361 🟥 Highest | $1.923908 |
| kettei-fat | Decision model | 1066/1342 | 79.4% | 174 ms 🟩 Fastest | 214 ms | $0.01543 🟨 Low | $0.020711 |
| Jev 1.14 | Decision model | 1030/1342 | 76.8% | 179 ms 🟩 Fastest | 269 ms | $0.02457 🟨 Low | $0.032974 |
| Jev 1.13 | Decision model | 1026/1342 | 76.5% | 189 ms 🟩 Fastest | 323 ms | $0.02457 🟨 Low | $0.032974 |
| Mercury Decide | Decision model | 1017/1342 | 75.8% | 238 ms 🟩 Fastest | 388 ms | $0.00696 🟩 Lowest | $0.009334 |
| Qwen3.8-Max — none, Hyper Charm | LLM reference | 967/1342 | 72.1% | 1191 ms 🟥 Slow | 1731 ms | $0.61482 🟥 Highest + ? | $0.825090 + ? quota |
| Liquid d1 | Decision model | 965/1342 | 71.9% | 206 ms 🟩 Fastest | 827 ms | $0.00577 🟩 Lowest | $0.007748 |
| Cloudflare Clef | Decision model | 936/1342 | 69.7% | 268 ms 🟨 Fast | 417 ms | $0.01759 🟨 Low | $0.023611 |
| Perplexity Decider Flash v1.2 | Decision model | 923/1342 | 68.8% | 159 ms 🟩 Fastest | 231 ms | $0.00341 🟩 Lowest + ? | $0.004570 + ? |
| Microsoft-Decision-1 | Decision model | 921/1342 | 68.6% | 283 ms 🟨 Fast | 566 ms | $0.01224 🟨 Low | $0.016422 |
| Drex v2.0 | Decision model | 915/1342 | 68.2% | 232 ms 🟩 Fastest | 755 ms | $0.01666 🟨 Low + ? | $0.022359 + ? |
| Cloudflare Clef Flash | Decision model | 860/1342 | 64.1% | 245 ms 🟩 Fastest | 353 ms | $0.00880 🟩 Lowest | $0.011806 |
| Cloudflare Clef Omni | Decision model | 860/1342 | 64.1% | 241 ms 🟩 Fastest | 400 ms | $0.06151 🟥 Highest + ? | $0.082547 + ? |
| Drex v1.5 | Decision model | 853/1342 | 63.6% | 203 ms 🟩 Fastest | 649 ms | $0.01116 🟨 Low | $0.014976 |
| Kev 4B | Decision model | 822/1342 | 61.3% | 225 ms 🟩 Fastest | 377 ms | $0.01172 🟨 Low | $0.015725 |
| Luna 6 Decisions | Decision model | 758/1342 | 56.5% | 254 ms 🟨 Fast | 527 ms | $0.03584 🟧 Mid + ? | $0.048097 + ? |
| Tev1 4B experimental (OpenRouter native adapter) | Decision model | 751/1342 | 56.0% | 198 ms 🟩 Fastest | 253 ms | $0.01566 🟨 Low | $0.021011 |
| ScaleDown Classify-1 | Decision model | 550/1342 | 41.0% | 268 ms 🟨 Fast | 362 ms | $0.02139 🟨 Low | $0.028703 |
| Solar Decide Flash | Decision model | 538/1342 | 40.1% | 540 ms 🟧 Moderate | 747 ms | $0.03020 🟧 Mid + ? | $0.040532 + ? |

*d3-turbo and Amos currently provide free public access. No monetary charge was reported; their metered cost fields are null and no numeric price point is plotted. This is not a guarantee of free production capacity.*

## Reading the speed and cost colors

The squares and labels use fixed descriptive bands, not relative ranks or statistical significance. Speed uses the full-bank first-attempt median. Cost uses known or accounted dollars per 1,000 questions, normalized from each actual 1,342-question run including permitted recoveries.

| Band | Median response time | Known/accounted cost per 1,000 |
|---|---|---|
| Green | 🟩 Fastest: ≤250 ms | 🟩 Lowest: ≤$0.010 |
| Yellow | 🟨 Fast: >250 to ≤500 ms | 🟨 Low: >$0.010 to ≤$0.025 |
| Orange | 🟧 Moderate: >500 to ≤1,000 ms | 🟧 Mid: >$0.025 to ≤$0.050 |
| Red | 🟥 Slow: >1,000 ms | 🟥 Highest: >$0.050 |
| Gray | ⬜ Unknown: unavailable | ⬜ Unknown: unavailable |

Bands use unrounded measurements; displayed numbers can round to a boundary. `+ ?` means additional charges were not reported. In those cells, the cost band describes only the known lower bound, not a complete cost or a guaranteed price advantage. The website also underlines these incomplete costs in amber. Text labels remain visible without color.

## October 20 additions

| October 20 addition | Correct /1342 | Average (mean) | Median | p95 | Actual 1342-question cost |
| --- | --- | --- | --- | --- | --- |
| d3-turbo | 1106/1342 (82.4%) | 182 ms | 165 ms | 298 ms | Free public access* |
| Amos 1 Large | 1074/1342 (80.0%) | 306 ms | 311 ms | 360 ms | Free public access* |
| kettei-fat | 1066/1342 (79.4%) | 179 ms | 174 ms | 214 ms | $0.020711 |

All three completed 1342 first attempts, without failures, recoveries or probability warnings. Rate-limit waits are excluded from response times.

## Three additions, the same leading group

d3-turbo scored 1106/1342 (82.4%), fourth among the 23 specialized decision models. Span remains first at 1127, followed by Perplexity Decider at 1120 and Nimble Max at 1115. Amos Large scored 1074 (80.0%), sixth; kettei-fat scored 1066 (79.4%), seventh. These are observed scores on this developing bank, not a general intelligence ordering.

## Strong rule following does not imply strong state tracking

d3-turbo and kettei-fat each answered all 46 if-then questions correctly; Amos answered 44. Checking required conditions produced 51/52, 49/52 and 50/52 respectively. On step-by-step procedures—applying each ordered edit to the current state—the scores were 20/48, 16/48 and 16/48. Span scored 33/48. All three newcomers returned valid decisions; their unsuccessful procedure answers were wrong choices, not formatting failures.

## Knowledge tracking and exact counting separate the newcomers

On tracking what others know, d3-turbo scored 47/50, Amos 46/50 and kettei-fat 43/50, versus Span 41/50. These tasks ask, for example, where an observer will look after an object moved while they were absent. Exact truth counting—how many supplied claims are true—gave d3-turbo 35/71, Amos 37/71 and kettei-fat 19/71, versus Span 46/71. A similar overall score can conceal a large difference on one operation.

## kettei-fat has a different profile from its neighboring scores

kettei-fat scored 45/50 on causal intervention, which asks what changes when a specified cause is forced to a new value; d3-turbo scored 38/50 and Amos 36/50. It also scored 56/58 on exceptions and priority rules and 43/43 on choosing authoritative current records. Its 19/71 exact truth-counting score is 26.8%, against a 20% random-choice baseline. The category profile is more useful than treating its 79.4% overall as one uniform ability.

## Scores near the Sonnet reference, at shorter response times

Sonnet's separately constrained, no-thinking reference scored 1070/1342 (79.7%). d3-turbo answered 36 more correctly, Amos four more and kettei-fat four fewer. Their medians were 165, 311 and 174 ms, versus Sonnet's 1506 ms. These small Amos/Sonnet/kettei score gaps do not establish a reliable ordering. Sol remains the highest-scoring LLM reference at 1143/1342 (85.2%).

## Fast responses, separate public-access and metered prices

The October 20 mean / median / p95 times were d3-turbo 182/165/298 ms, Amos 306/311/360 ms and kettei-fat 179/174/214 ms. All 4026 first attempts returned usable decisions, with no recoveries or probability-format warnings. d3-turbo and Amos used currently free public endpoints; no monetary charge was reported, so they are not plotted as a metered production price of zero. Sqwish reported $0.02071056 for all 1342 questions ($0.01543 per 1000). Its 30-request/minute starter limit stretched batch duration, not the measured response time. Different providers, dates, hardware and admission limits remain confounds.

## New image-capable candidates, not new image scores

Current catalogs or author documentation declare image input for 16 of the 23 decision models, including Span-02, both Perplexity Deciders, both Liquid models and all three newcomers. The separate image benchmark has not changed. Text accuracy and latency do not establish image accuracy or image cost; the capability review records sources and distinguishes declared support from tested performance.

## Decision models alongside high-end LLMs

Respan Span-02 scored 1127/1342 (84.0%). The highest-scoring LLM reference was GPT-6 Sol — no reasoning: 1143/1342 (85.2%), a gap of 16 decisions. These are the same questions, facts and option order, with no tools or iterative repair. This measures System 1-style decision performance, not unrestricted reasoning or general intelligence.

## Sol and Span are close overall, with different strengths

Sol scored 1143/1342 (85.2%), versus Span’s 1127 (84.0%). On the original 1136 questions, Sol scored 1014 and Span 1011; on the added 206, Sol scored 129 and Span 116. Sol answered 45/46 forward conditionals and 52/52 necessary-condition questions; Span answered 32/46 and 44/52. Span answered 33/48 sequential procedures and 55/74 truth-teller questions, versus Sol 18/48 and 38/74.

## Speed and cost separate otherwise nearby scores

Sol’s median was 1023 ms, versus Span’s 206 ms: 5.0 times longer. Their recorded full-bank costs were $0.848294 and $0.00474628, a 179-fold difference. Span’s p95 was 2157 ms, versus Sol’s 1546 ms; the median advantage did not extend to that tail measure. These are route measurements, not controlled hardware comparisons.

## Sonnet needs a constrained decision format

Sonnet’s JSON-choice run scored 1070/1342 (79.7%), at a 1506 ms median and $1.923908 for the bank. All 1342 outputs were valid and reported zero thinking tokens. In the separate bare-ID trial, 84 of 110 outputs were unusable explanations or truncated text. That trial is not pooled into this score. Sonnet scored 45/46 forward conditionals, 15/48 sequential procedures and 30/71 exact truth-counting questions.

## Qwen: decision accuracy and account limits

Qwen3.8-Max delivered 967/1342 (72.1%); 1317 first attempts returned usable decisions, with 73.4% accuracy among those responses. There were 25 first-attempt provider/transport failures, retained in the primary score. It scored 38/46 on following if-then rules, 11/48 on step-by-step procedures and 30/74 on truth-teller consistency. Its median was 1191 ms and p95 1731 ms. Hyper Charm’s hourly limit produced some rejected requests; those are not labelled wrong model choices. Its cost is a prepaid-quota valuation, not additional cash billing. The requested none setting is documented in Hyper’s catalog, but the route does not report reasoning-token counts.

## What the comparison supports

Span’s 84.0% sits between Sol’s 85.2% and Sonnet’s 79.7% on these immediate decisions, with much lower recorded cost and a shorter median response. The Qwen row adds a further reference point. Scores and error profiles differ by category. This is a selected reference group, not an exhaustive ranking of every LLM that can disable reasoning. Models that require thinking are outside this comparison. New eight-question categories remain coarse diagnostic samples, not reliability guarantees.

## What this measures

One decision from supplied information, with five choices. No requested thinking budget, tools, explanation or iterative repair. This is System 1-style decision performance, not a comparison of unrestricted reasoning, writing or agentic work. The ranking uses every first attempt; provider failures count as unsuccessful delivered decisions and are not called wrong reasoning answers.

## Span leads the decision models

Span scored 1,127/1,342 (84.0%), Perplexity 1,120 (83.5%) and Nimble Max 1,115 (83.1%). The gaps are 7 and 12 answers. They are too small to establish a general intelligence ordering. Equal weighting of the 31 category percentages also puts Span first: 82.4%, versus Perplexity’s 79.4% and Nimble’s 79.0%. The main score remains question-weighted, so large categories contribute more questions.

## Typical speed and tail speed tell different stories

Span’s median was 206 ms, with a 2.16-second p95. Perplexity’s median was 249 ms and p95 332 ms; Nimble’s were 235 and 329 ms. Span combines a short typical response with a much longer response-time tail. Its recorded cost is $0.00354 per 1,000 questions, versus $0.00700 plus one unreported attempt cost for Perplexity and approximately $0.02763 for Nimble. Span has the lowest metered cost among routes with complete charge accounting. The new free public endpoints are a separate access category. All pooled medians are below two seconds. The exclusion policy uses median, not p95.

## Sequential state updates and truth counting remain discriminating

Sequential procedures require applying ordered edits to the current state, such as reversing a row, swapping positions and moving an item. Span scored 33/48, Nimble 19/48, Perplexity 14/48 and Jev 1.14 7/48. For exact truth counting, which asks how many claims are true under the supplied facts, the same routes scored 46/71, 39/71, 43/71 and 28/71. Strong performance here still includes many wrong answers.

## The decision-model leader is not strongest in every function

Forward conditionals ask what follows when facts activate chains of rules. Jev 1.14 scored 46/46, Perplexity and Nimble each 45/46, and Span 32/46. On truth-teller consistency, where whole statements must match each speaker’s type, Perplexity scored 58/74, Span 55/74 and Nimble 53/74. On one-to-one assignments, Perplexity scored 65/67 and Span 63/67; on belief tracking, Jev 1.13 scored 47/50 and Span 41/50. Belief tracking distinguishes what observers know from what actually happened.

## Uncertainty and system constraints change the functional picture

Across the six uncertainty, strategy and system categories, Span scored 34/48, Perplexity 26/48, Nimble 25/48 and Jev 1.14 26/48. Span’s largest visible advantage is worst-case choices without supplied probabilities: 8/8, versus Perplexity 3/8, Nimble 4/8 and Jev 1.14 2/8. These require a worst-case action or policy, not an invented average. In information-flow security, Perplexity, Nimble and Jev 1.14 each scored 6/8, versus Span’s 5/8. Each category has eight questions. One answer changes its score by 12.5 percentage points; these are diagnostic profiles, not reliability guarantees.

## Jev, Luna and a lower-cost native alternative

Jev 1.14 scored 1,030/1,342 (76.8%), Jev 1.13 1,026 (76.5%), and Luna Decisions 758 (56.5%). The Jev versions differ by 4 correct decisions overall. Assignments favor 1.14, 57/67 versus 54/67; causal intervention favors 1.13, 42/50 versus 38/50. The update is not a uniform improvement across functions. Mercury Decide scored 1,017 (75.8%), with a 238 ms median and $0.00696 per 1,000 at the captured prices. It scored 34/52 on swaps and 55/58 on priority rules, but 28/52 on necessary conditions, versus Jev 1.14’s 48/52. This is the native Mercury Decide route, not regular Mercury 2.5. The earlier LLM cohort lacks expanded coverage; the new reference group has complete matched coverage.

## Category scores and explanations

The 31 categories are grouped below so the labels and values remain readable. These are reading groups, not new scored categories. All 26 routes remain in overall-score order. Every cell shows **correct / questions and percentage**. Darker blue means higher accuracy on a fixed 0-100% scale; uniform random guessing averages 20%. Different category sizes mean that percentages alone do not show how much evidence is available.

[Open the color-coded, selectable tables](https://etsabary.github.io/system-1-decision-benchmark/report.html#functions), with a pinned model-name column and individual category rankings.

### Rules and evidence

Which facts meet a rule, which conclusions follow, and when is the evidence insufficient?

| Category | Questions | What it tests and a simple example |
| --- | --- | --- |
| Lookup and filtering (F01) | 43 | Select records that meet stated conditions Example: Which listed request is both signed and marked urgent? |
| Following if-then rules (F02) | 46 | Apply an implication from its trigger Example: If an active badge grants entry and this badge is active, what follows? |
| Checking required conditions (F03) | 52 | Reason backward from a missing required condition Example: Every approved request needs a valid ticket; can one without a ticket be approved? |
| Combining AND, OR and NOT (F04) | 54 | Track combinations such as both, either and exactly one Example: Which choice satisfies exactly one of two stated conditions? |
| All, some, none and sets (F05) | 49 | Track all, some, none and overlapping groups Example: All teal tokens are marked; no marked token is blank; which relation follows? |
| Enough evidence or a conflict? (F11) | 41 | Determine whether facts force an answer or contradict one another Example: Is a proposed arrangement determined, impossible or still underdetermined? |

![Rules and evidence: all 26 routes, named categories, correct counts and percentages](direct_additions_2026-10-20/rules.png)

[Full-size SVG](direct_additions_2026-10-20/rules.svg) · [Color-coded table and category rankings](https://etsabary.github.io/system-1-decision-benchmark/report.html#group-rules)

### Ordering, schedules and assignments

Can the model combine comparisons, fit a schedule, assign unique partners and apply tie-break rules?

| Category | Questions | What it tests and a simple example |
| --- | --- | --- |
| Ordering by comparisons (F06) | 40 | Combine ordered comparisons Example: A is taller than B and B than C; how do A and C compare? |
| Scheduling under constraints (F07) | 76 | Fit events around order and exclusion rules Example: Which timetable puts one meeting before another without overlapping a break? |
| One-to-one assignments (F08) | 67 | Give each item a unique partner while satisfying clues Example: Assign three people different desks using location restrictions. |
| Comparing time intervals (F14) | 42 | Compare starts, ends and overlapping periods Example: Which interval overlaps a specified event without containing it? |
| Ranking with tie-break rules (F22) | 51 | Rank candidates using explicit tie-break rules Example: Rank by priority first, then age when priorities tie. |

![Ordering, schedules and assignments: all 26 routes, named categories, correct counts and percentages](direct_additions_2026-10-20/ordering.png)

[Full-size SVG](direct_additions_2026-10-20/ordering.svg) · [Color-coded table and category rankings](https://etsabary.github.io/system-1-decision-benchmark/report.html#group-ordering)

### Claims, changing state and perspectives

Can the model count true statements, update a changing situation and separate what different observers know?

| Category | Questions | What it tests and a simple example |
| --- | --- | --- |
| Counting exactly true claims (F09) | 71 | Count precisely how many statements hold Example: Under the supplied facts, how many of six claims are true? |
| Truth-tellers and liars (F10) | 74 | Find a consistent pattern of truthful and false statements Example: Which assignment of honest and dishonest speakers fits their claims? |
| Tracking swaps (F12) | 52 | Update locations after repeated exchanges Example: A red token starts in box A; several box contents are swapped; where does it end? |
| Following step-by-step procedures (F13) | 48 | Apply each ordered edit to the current state Example: Toggle one flag, swap two values, then conditionally reset another flag. |
| Tracking position and direction (F15) | 49 | Update position or direction from described movement Example: Follow successive turns and moves, then identify the final direction. |
| Resolving names and references (F16) | 50 | Resolve chains of names, roles and references Example: Identify the mentor of the colleague named in a nested description. |
| Tracking what others know (F17) | 50 | Distinguish what different observers witnessed Example: An object moves while one observer is absent; where will that observer look? |

![Claims, changing state and perspectives: all 26 routes, named categories, correct counts and percentages](direct_additions_2026-10-20/state.png)

[Full-size SVG](direct_additions_2026-10-20/state.svg) · [Color-coded table and category rankings](https://etsabary.github.io/system-1-decision-benchmark/report.html#group-state)

### Causes, plans and exceptions

Which actions work, which consequences change, and which rule or source controls when information conflicts?

| Category | Questions | What it tests and a simple example |
| --- | --- | --- |
| Changing a cause (F18) | 50 | Recompute consequences of changing a specified input Example: Force a switch off while holding other inputs fixed; which lamp now lights? |
| Exceptions and priority rules (F19) | 58 | Apply a rule, its exception and stated precedence Example: A badge permits entry unless a higher-priority suspension applies. |
| Planning valid action sequences (F20) | 43 | Choose an action sequence whose requirements are met Example: Obtain a key before opening a locked door, with limited moves available. |
| Following directed connections (F21) | 43 | Follow arrows in their permitted direction Example: Can node A reach node D through the listed directed links? |
| Finding rule violations (F23) | 52 | Find a case that violates a stated rule Example: Which listed record disproves the claim that every approved item is signed? |
| Choosing authoritative current records (F24) | 43 | Select the valid source rather than an outdated conflicting one Example: Two records disagree; which controls under the stated authority and date policy? |
| Diagnosing faults from evidence (F25) | 50 | Match observed symptoms to explicit fault rules Example: Which fault is consistent with the supplied test results? |

![Causes, plans and exceptions: all 26 routes, named categories, correct counts and percentages](direct_additions_2026-10-20/causes.png)

[Full-size SVG](direct_additions_2026-10-20/causes.svg) · [Color-coded table and category rankings](https://etsabary.github.io/system-1-decision-benchmark/report.html#group-causes)

### Risk, strategy and system behavior

These decisions involve uncertain outcomes, another actor, overlapping operations or possible information leaks.

**Worst-case choices without probabilities** means choosing under a specified worst-case loss or regret rule when the likelihoods of possible situations are not supplied. There is no probability distribution to average over. Each of these six categories has eight questions, so one answer changes its score by 12.5 percentage points.

| Category | Questions | What it tests and a simple example |
| --- | --- | --- |
| Risk with supplied probabilities (F26) | 8 | Choose the action with the lowest probability-weighted cost, using the supplied likelihoods and costs. Example: Which action minimizes the expected cost of a possible delay? |
| Is extra information worth its cost? (F27) | 8 | Decide whether paying for a test before choosing an action reduces the probability-weighted cost enough to cover the test price. Example: Should you buy a sensor reading before choosing an action, or is acting without the extra information cheaper overall? |
| Worst-case choices without probabilities (F28) | 8 | Follow the stated worst-case rule when likelihoods are not supplied. Minimize either the largest possible loss or the largest regret (extra loss compared with the best action for each situation), as the question specifies. Do not invent probabilities. Example: A route costs 4 in either situation; another costs 1 or 9. With no probabilities and a smallest-worst-case-cost rule, which route should be chosen? |
| Anticipating another decision-maker (F29) | 8 | Choose an action while accounting for the specified choices or payoff-maximizing response of another decision-maker. Example: Which first move gives the best result after the other player chooses their own best reply? |
| Checking overlapping operations (F30) | 8 | Decide whether overlapping operations and their reported results can fit a permitted one-at-a-time order that respects the specified timing and object rules. Example: Two processes read and change the same stored value. Could their reported results fit an allowed one-at-a-time order? |
| Detecting secret-information leaks (F31) | 8 | Check whether changing a protected secret can change an observable result in a way the stated policy forbids. Example: If public inputs stay the same, could public output distinguish two secret values that the policy says must remain indistinguishable? |

![Risk, strategy and system behavior: all 26 routes, named categories, correct counts and percentages](direct_additions_2026-10-20/uncertainty.png)

[Full-size SVG](direct_additions_2026-10-20/uncertainty.svg) · [Color-coded table and category rankings](https://etsabary.github.io/system-1-decision-benchmark/report.html#group-uncertainty)

Counts are exact; displayed percentages are rounded. A perfect result on a small sample is not a reliability guarantee. [Download the full category matrix](direct_additions_2026-10-20/category_scores.csv).

## Questions, statistics and method

All 1342 question inputs are unchanged and remain available without answers: [CSV](consolidated_2026-10-19/questions_1342.csv), [exact native JSONL](consolidated_2026-10-19/questions_1342.jsonl), [readable text](consolidated_2026-10-19/questions_1342.txt).

Current exports: [model CSV](direct_additions_2026-10-20/model_statistics.csv), [named-category CSV](direct_additions_2026-10-20/category_scores.csv), [aggregate JSON](direct_additions_2026-10-20/statistics.json), [sanitized audit receipt](direct_additions_2026-10-20/audit_receipt.json), [manifest](direct_additions_2026-10-20/manifest.json), [plain-text findings](direct_additions_2026-10-20/report.txt).

[Request failures and output compliance](OUTPUT_COMPLIANCE.md) · [Image capability review](IMAGE_CAPABILITIES.md) · [Earlier 1136-question comparison](REFERENCE_1136.md) · [Separate image benchmark](https://github.com/etsabary/visual-decision-benchmark).

The full comparison covers 26 routes × 1342 questions = 34,892 first attempts: 23 specialized decision models and three separately labelled high-end LLM references. The same 1342 inputs, facts and five choices retain their tested order. No existing model was rerun or removed for this update. There are 35,058 selected HTTP attempts, including 166 permitted recoveries; the three October 20 runs account for 4026 first attempts and zero recoveries.

Primary scores and latency use all first attempts. A valid wrong choice is never retried. One recovery is permitted only for transport failures or HTTP 408/429/5xx; its cost is included and its response cannot replace the first attempt in the ranking. Provider failures are unsuccessful delivered decisions, not classified as wrong reasoning choices.

Median and p95 are computed from individual first-attempt times, never averages of stage medians. Timing runs from a fresh HTTPS connection through the complete response body, not time to first token. Deliberate admission, rate-limit and retry waits are excluded. The mean is also available for the three new runs. p95 is an interpolated 95th percentile, not the mean of the slowest 5%.

The October 20 additions use direct provider APIs. Amos was paced below its public 60-request/minute cap. Sqwish starter access used one active request and 2.1-second start spacing after an account-limit amendment; the first 54 successful attempts remain included. Its response latency is not batch throughput. d3-turbo used up to two in flight. Previous routes, dates, loads and quantiles are unchanged. Different protocols, hosting hardware and account conditions are not controlled away.

Among the earlier 20 decision routes, Nimble uses Bespoke directly and the others use OpenRouter with pinned providers and no fallback. Sol and Sonnet use OpenRouter; Qwen uses Hyper Charm. Sonnet requires the separately labelled JSON-choice grammar; its stopped bare-ID trial remains outside the scored comparison. Qwen requests reasoning_effort=none but has no reasoning-token telemetry. Tev1 is a decision-specialized generative model using a native adapter, not a claimed nongenerative architecture.

All three new responses named the requested model and reported zero output tokens. The hosted names do not attest immutable weights or reveal internal implementation. No explanation generation, tool use, agentic iteration or answer-dependent repair was requested. This measures System 1-style choices, not unrestricted reasoning or general intelligence.

Costs per 1000 are actual selected-run costs divided by 1342 and multiplied by 1000. Probe charges are separate. Sqwish charges come from every returned receipt and match the captured $0.06 per million input tokens; its exact full-bank charge is $0.02071056. d3-turbo and Amos used currently free public access, with no API-reported monetary charge; their metered price fields are null, not fabricated zeros. They have no cost-axis numeric point. Starter credit does not make Sqwish free.

Earlier captured charges and usage-times-tariff accounting remain unchanged. + ? means additional unreported charges, not zero. Nimble retains its recorded mixed tariffs; Hyper Charm Qwen is a prepaid-quota valuation, not a cash invoice. Verification subscriptions are outside model-inference accounting. The total is not an independently reconciled financial invoice.

This is a developing benchmark with dependent variants and uneven category sizes, not 1342 independent observations or a pristine held-out evaluation. The 37 author-development cases retain their permanent exclusion from a future held-out scored release and their separate 1305-case diagnostic. The complete developmental ranking remains 1342 questions for every route. Small score gaps do not establish a general intelligence ordering.

The construction combines the corrected 1136-question bank, 200 verified expansion questions and six additional truth-teller questions into one score. The 31 categories and their question weights are unchanged. Each of F26–F31 has eight questions, so one answer changes a category score by 12.5 percentage points. Display groups are reading aids, not additional scored categories.

All 206 expansion questions have current-revision blind Sol xhigh and different-model Opus or Argon checks, supplemented by exact computational evidence. The original bank received a targeted difficult-item audit, not independent external verification of every original question. Two retired ambiguous procedure questions are absent; their verified replacements appear once.

All question inputs remain available without answer keys. Aggregate scores, categories, usage and costs are published; answer keys, item-level correctness, certificates, verifier responses, raw account data and credentials are not. Publication validators check consistency and privacy; public aggregates cannot reproduce private-key scoring or raw-latency pooling. The dated audit receipt binds the private evidence checks.

Sixteen earlier regular-LLM configurations have only 1136-question coverage and are not extrapolated. Solar Decide remains excluded for latency; the distinct Solar Decide Flash remains included. No older published row was removed. The separate image benchmark is unchanged; documented image support is not an image score.

## Offline publication checks

Run `python3 validate_direct_release.py`, `python3 repo_identity.py` and `python3 -m unittest discover -p "test_*.py"` with `requirements-reports.txt` and `python-dotenv` installed. These checks make no inference calls. Earlier dated releases and seals remain available unchanged.
