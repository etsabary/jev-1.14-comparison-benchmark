# Delivered decisions and request failures

All 29 routes retain the full 1342-question first-attempt denominator. Wrong valid decisions are separate from unusable outputs or provider failures. All 4026 new first attempts were usable, with zero recoveries.

| Model | Usable first | Wrong valid | Provider failures | Output failures | Recoveries | Eventual correct |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 Sol — no reasoning | 1342 | 199 | 0 | 0 | 0 | 1143 |
| Mammoth-1 | 1342 | 203 | 0 | 0 | 0 | 1139 |
| Drex Max | 1342 | 215 | 0 | 0 | 0 | 1127 |
| Respan Span-02 | 1342 | 215 | 0 | 0 | 0 | 1127 |
| Perplexity Decider v1.2 | 1341 | 221 | 1 | 0 | 1 | 1121 |
| Nimble v4 Max | 1342 | 227 | 0 | 0 | 0 | 1115 |
| d3-turbo | 1342 | 236 | 0 | 0 | 0 | 1106 |
| Liquid d1-ultra | 1341 | 257 | 1 | 0 | 1 | 1085 |
| Amos 1 Large | 1342 | 268 | 0 | 0 | 0 | 1074 |
| Sonnet 5.5 — no thinking, JSON-choice | 1342 | 272 | 0 | 0 | 0 | 1070 |
| kettei-fat | 1342 | 276 | 0 | 0 | 0 | 1066 |
| Jev 1.14 | 1342 | 312 | 0 | 0 | 0 | 1030 |
| Jev 1.13 | 1342 | 316 | 0 | 0 | 0 | 1026 |
| Mercury Decide | 1342 | 325 | 0 | 0 | 0 | 1017 |
| Elephant-1 | 1342 | 338 | 0 | 0 | 0 | 1004 |
| Qwen3.8-Max — none, Hyper Charm | 1317 | 350 | 25 | 0 | 23 | 971 |
| Liquid d1 | 1342 | 377 | 0 | 0 | 0 | 965 |
| Cloudflare Clef | 1342 | 406 | 0 | 0 | 0 | 936 |
| Perplexity Decider Flash v1.2 | 1286 | 363 | 56 | 0 | 56 | 940 |
| Microsoft-Decision-1 | 1342 | 421 | 0 | 0 | 0 | 921 |
| Drex v2.0 | 1302 | 387 | 40 | 0 | 40 | 933 |
| Cloudflare Clef Flash | 1342 | 482 | 0 | 0 | 0 | 860 |
| Cloudflare Clef Omni | 1341 | 481 | 1 | 0 | 1 | 861 |
| Drex v1.5 | 1342 | 489 | 0 | 0 | 0 | 853 |
| Kev 4B | 1342 | 520 | 0 | 0 | 0 | 822 |
| Luna 6 Decisions | 1300 | 542 | 42 | 0 | 42 | 761 |
| Tev1 4B experimental (OpenRouter native adapter) | 1342 | 591 | 0 | 0 | 0 | 751 |
| ScaleDown Classify-1 | 1342 | 792 | 0 | 0 | 0 | 550 |
| Solar Decide Flash | 1340 | 802 | 2 | 0 | 2 | 539 |


The separate stopped Sonnet bare-ID trial is not pooled into its complete constrained JSON-choice reference. Qwen’s original quota and transport failures remain unsuccessful first deliveries.
