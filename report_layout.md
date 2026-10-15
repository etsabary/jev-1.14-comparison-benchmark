# Eleven models on the same 1,136 text decisions

I have been intrigued by Jev because it does something different from the LLMs I usually use: it returns a typed decision with probabilities rather than a paragraph. That made it harder to place. Could it make better quick decisions than Luna, one of my favorite models? I wanted a comparison that would make its strengths and limits visible.

On these tests, the answer was clearly yes. Jev was substantially stronger than both Luna services overall. That is a finding about **System 1-style decisions**: a single answer from supplied information, without an explicit thinking budget, tools or an agentic feedback loop. Those decisions matter when a system needs to route many requests quickly and cheaply. This is not a comparison of unrestricted reasoning, writing or agentic ability.

Jev 1.14 remains the strongest overall result on this bank, with **932/1,136 correct (82.0%)**, followed by Jev 1.13 with **910 (80.1%)**. Among eight regular LLMs tested with switchable reasoning disabled, **GPT-6 Luna scored 727 (64.0%)** and **Mercury 2.5 scored 702 (61.8%)**. Mercury came close to regular Luna at lower reported cost and shorter median response time under its test-day promotional tariff.

This comparison covers **11 model services × 1,136 questions = 12,496 scored model-question cases**. It preserves three historical native Decisions results and adds eight coordinated regular-LLM runs from October 15, 2026. The new LLMs used OpenRouter, pinned backend providers, a 16-token output cap and a numeric-answer-ID-only instruction. These are short-answer decision results, not unrestricted reasoning scores.

The bank contains 640 core questions and 496 related variants, contrasts and candidate checks across 25 families. Related items are not independent observations. All models received the same underlying instructions, facts, question and five answer options in the same order; native Decisions and ordinary chat serialize that content differently.

The [original three-model report](THREE_MODEL_REFERENCE.md), [frozen original evidence](data), [eleven-model summary](expansion_2026-10-15/summary.json), and [function and load-level tables](FUNCTIONS.md) remain available. The [image benchmark](https://github.com/etsabary/visual-decision-benchmark) is separate.

![Overall and core-only accuracy across eleven services](figures/eleven_overall_accuracy.png)

## Results across the full bank

Historical rows preserve their original recorded outcomes and retry rules. New LLM rows use the first attempt as primary. Errors, refusals, non-ID output and truncation are unsuccessful; wrong valid choices remain separate.

The headline median and p95 use **all 1,136 saved outcomes for each model**, including timed failures. They give a ballpark view of the recorded services. Historical timing boundaries, dates and routes differ from the new run, so this is not a controlled eleven-way speed ranking.

{{RESULTS}}

## Actual cost of the eight new full runs

Costs cover **1,136 questions per model**, including recovery attempts. The per-1,000 column is a normalization of the same bill: reported run cost ÷ 1,136 × 1,000. It is not an additional run. The earlier 75-call pilot is separate.

{{COSTS}}

The eight new runs reported **$0.227088871 combined**. Nine error attempts omitted charges, so this is a known reported amount, not exact billing. Mercury's captured tariff had an 80% promotional discount. Its cost advantage is specific to that price. Backend hardware and quantization differ even though OpenRouter is the shared front door.

Jev 1.14's historical attempt ledger reported **$0.027183072**, with two errors omitting cost. Jev 1.13 has cost fields only for its 136 extension records ($0.003161340), not a full-bank bill. Luna Decisions' selected historical result records total $0.0395666 across 1,113 cost-reporting records; failed/retried attempts are not a complete accounting ledger here. These figures are retained with their coverage rather than presented as equivalent full-run bills.

![Actual 1136-question costs and first-attempt reply times of eight regular LLMs](figures/eleven_cost_and_speed.png)

{{ANALYSIS}}

## Where Jev 1.14 improved over 1.13

The overall text gain is modest: **22 additional correct answers, from 80.1% to 82.0%**. Some individual functions improved much more. **One-to-one assignments rose from 49/61 to 56/61**, and **verbal spatial tracking from 24/43 to 32/43**. Scheduling rose from 43/69 to 46/69, still leaving 23 errors. Exact truth counting stayed at 24/65, and sequential procedure execution moved only from 5/42 to 6/42.

The improvement was not uniform. Exceptions and priority rules fell from 48/52 to 45/52, temporal interval relations from 35/36 to 34/36, and correctly answered changed-evidence pairs from 20/25 to 19/25. Across individual questions, 1.14 corrected 56 previously unsuccessful cases and lost 34 previously correct cases; two losses were provider errors rather than wrong valid choices. This is another reason to validate an upgrade against the tasks an application actually uses.

A one-to-one assignment means giving each person, object or time slot a unique partner while respecting clues. An illustrative question is: three people need different desks; one cannot use the window desk and another must sit left of the third; which complete assignment satisfies every rule? Spatial tracking means updating a direction or position through described movements, such as following successive turns and then identifying where someone is facing. These examples explain the categories; they are not additional scored questions. The [task examples](FUNCTIONS.md) explain the remaining functions.

## Image decisions add another dimension

The separate [image benchmark](https://github.com/etsabary/visual-decision-benchmark) used 200 questions per configuration, tested on October 15, 2026. Its scores are not combined with the 1,136-question text bank. Mercury was not tested on images.

{{IMAGES}}

The image results make the value of image input concrete, while also showing where the overall winner loses. Jev scored 9/10 on conditional counting, spatial relationships and flowcharts. Conditional counting means counting only objects meeting a rule, such as red shapes inside a marked region. A flowchart question asks a model to follow the pictured branches for a supplied input and select the resulting outcome.

Luna Decisions was substantially stronger on **rotation and reflection**, at 8/10 versus Jev's 3/10: recognizing which option is the rotated or mirrored version of a pictured shape. Regular Luna was stronger on **visual rule application**, at 6/10 versus Jev's 3/10: applying a pictured transformation or legend to choose the correct next result. Both Luna services scored 7/10 on sequential visual state tracking, compared with Jev's 6/10. The text bank also has a smaller counterexample to Jev's overall lead: Qwen answered 11/42 procedural questions correctly versus Jev 1.14's 6/42, although neither result is dependable.

The release's modest text gain should be distinguished from its broader features. In the [October 14 release announcement](https://typesafe.ai/blog/jev-1-14), TypeSafe describes incremental model improvements and expects the largest gain in multilingual support. We did not test languages other than English. The release also enabled experimental image input, a bounding-box output type and longer context. Image access was enabled for 1.13 too; bounding-box output was specific to 1.14. Our image bank establishes useful behavior on the tested 1.14 OpenRouter route, not a measured vision improvement over 1.13. Bounding boxes, long-context quality and multilingual gains remain outside these tests. TypeSafe labels these added features experimental rather than production guarantees.

TypeSafe says 1.13 was already multimodal. Enabling image access to that existing model should therefore not be counted as a 1.14 model improvement. A matched 1.13 image run would be needed to measure the version-to-version vision gain.

## Accuracy across the 25 functions

The heatmap labels show correct counts; color shows the fraction correct within each family. The [full function and load tables](FUNCTIONS.md) and [family CSV](expansion_2026-10-15/family_comparison.csv) retain all denominators and results.

![Correct counts and accuracy by family for all eleven services](figures/eleven_family_accuracy.png)

## Matched diagnostic tests

Rotation and evidence-change scores use planned panel denominators, so missing answers cannot improve them. Semantic consistency is shown only among complete rotation panels; a consistent choice can still be wrong. Candidate-check scores include all 80 planned checks.

{{PANELS}}

## Output format and recovery

The leading-ID column is an explicitly **post-hoc sensitivity check**, applied uniformly to all eight saved LLM runs. It reads a numeric answer ID at the start even if an explanation follows or later output is truncated. It adds no calls and does not replace the strict primary score. A larger output budget or reasoning-enabled evaluation would be a different experiment.

{{FORMAT}}

## Historical confidence and coverage

Native Decisions models returned confidence and option probabilities. Regular LLMs were asked only for an answer ID, so an equivalent confidence-filter comparison is not available. The historical thresholds are exploratory because they were examined on the same bank.

{{CONFIDENCE}}

At ≥0.95, Jev 1.14 retained 603 questions with one error, while Luna Decisions retained 96 with no observed errors. An observed error-free subset is not a guarantee of zero future error. No LLM confidence or calibration is inferred from a short answer.

## Supporting historical speed cohorts

The main table uses each full 1,136-record bank. These older cohort views remain available to explain why familiar historical medians differ. The original Jev 1.13 1,000-question cohort measured response headers across TypeSafe direct, Experiential and OpenRouter. Its later extension measured the response body. Combining those cohorts gives a mixed-boundary median, not a new measurement. Jev 1.14 and Luna Decisions use saved response-body timings.

{{HISTORICAL_SPEEDS}}

Jev 1.13 was tested September 22 and October 14, 2026; Jev 1.14 on October 14 and 15; Luna Decisions on October 10 and 14. Dates are Toronto local dates. Luna's extension has 130 successful timings because six questions remained unanswered. The chart's left panel uses all 1,136 outcomes, matching the main table; its right panel shows successful extension records only.

![Preserved full-bank historical timings and successful shared-extension cohorts](figures/eleven_historical_speed.png)

## Model identities routes and dates

{{IDENTITIES}}

New regular LLMs generally returned aliases, not dated checkpoints. The captured [model metadata](expansion_2026-10-15/model_metadata.json) includes endpoint names and advertised snapshot hints; those are not proof of the hidden weights used for each call. An unchanged alias cannot establish an unchanged hidden checkpoint. Historical `jev-latest` records belong to the September 22 Jev 1.13 run, not a new call to that alias.

## Evidence reproduction and limits

The [questions](data/questions_1136.csv), [new request plan](expansion_2026-10-15/request_plan.jsonl), [sanitized attempts](expansion_2026-10-15/attempts.jsonl), [dispatch ledger](expansion_2026-10-15/dispatches.jsonl), [terminal outcomes](expansion_2026-10-15/results.jsonl), [frozen protocol](expansion_2026-10-15/run_manifest.json), [source audit](expansion_2026-10-15/source_audit.json) and [release checksums](expansion_2026-10-15/release_checksums.json) preserve the comparison. Provider account IDs and BYOK account flags were removed. Recorded model outputs are public; the answer key and individual correctness records remain private.

`text_models.py` reconstructs all 9,088 new payloads and validates saved responses, costs and timing arithmetic without a network connection or key. It is a portable offline verifier, not the original live executor. `score_expansion.py` reproduces all eleven accuracy scores and matched diagnostics using the external original key. Public aggregate consistency checks cannot independently establish that every reference answer is true. Shared wording or generator defects remain possible; later key corrections should be versioned and applied to every saved model response.

```bash
# Standard library only. No credentials, answer key or paid API calls.
python3 validate.py
python3 text_models.py
python3 -m unittest -v test_analysis.py test_text_models.py test_publication.py

# Reproduce accuracy with the external original key; no per-item output.
python3 score_expansion.py --answer-key /path/to/answer_key.csv

# Rebuild expanded graphics, README and Pages.
python3 -m pip install -r requirements-reports.txt
python3 plot_expansion.py
python3 build_report.py
python3 freeze_expansion_checksums.py
```

The original comparison remains in [THREE_MODEL_REFERENCE.md](THREE_MODEL_REFERENCE.md) and [commit c302581](https://github.com/etsabary/jev-1.14-comparison-benchmark/tree/c30258100569fd0b81c8db89020733f74b87e484). Its data, analysis and original figures are unchanged. `analyze.py`, `plot_results.py` and `build_reference_report.py` remain the three-model tools; the expansion has separate evidence and offline verification. The [original Jev benchmark](https://github.com/etsabary/jev-deterministic-benchmark) and [two-model extension](https://github.com/etsabary/luna-decisions-benchmark/tree/0f10c51/extension_136) remain historical references.
