## Regular Luna and Luna Decisions differ in ways the total score conceals


Regular Luna answered 40 more questions correctly than the historical Luna Decisions run, 727 versus 687. Its core score was also higher, 431/640 versus 401/640. They agreed on 691 of the 1,112 questions both answered, or 62.1%. Similar aggregate scores do not mean they made the same decisions.

The speed trade-off matters. The saved full-bank median was about 223 ms for Luna Decisions, compared with 942 ms for regular Luna and 534 ms for Mercury. Those are useful ballpark values, not a controlled speed comparison: the Decisions run came from earlier dates and a different request interface.


The direction of the difference depends on the function. Regular Luna did better on forward implications (32/39 versus 24/39), Boolean scope (40/48 versus 33/48), rule verification and counterexamples (44/46 versus 36/46), and source authority (37/37 versus 31/37). Luna Decisions did better on belief tracking (32/44 versus 16/44), supplied-candidate checks (32/80 versus 17/80), and correctly answering both questions after an evidence change (13/25 versus 11/25). The two services were tested on different dates and returned different identity information. These differences cannot be attributed to the decision interface alone.



## Mercury is the most interesting new cost alternative


Mercury came within 25 correct answers of regular Luna while costing $0.01321493 for the actual 1,136-question run, compared with Luna's $0.03431990. Its median complete response was 0.534 seconds, compared with 0.942 seconds for Luna. Mercury's current 80% advertised tariff discount is part of this result; the cost advantage should be checked again after that discount changes. This one short-output test does not validate a general throughput or architecture claim.


Mercury answered every sampled transitive-comparison question (34/34) and preference-ordering question (45/45), and nearly every lookup and source-authority question (36/37 in each family). It was much less dependable on exact truth counting (18/65), repeated object swaps (20/46), causal intervention (16/44), and sequential procedures (6/42). Its 61.8% total is a useful budget comparison, not a basis for accepting arbitrary decisions without checking.



## The smaller open-weight candidates expose a substantial quality cost


Qwen3-30B-A3B Instruct produced a valid numeric answer on all 1,136 questions, but only 564 were correct (49.6%). It did relatively well on preference ordering (40/45), set relations (38/43), transitive comparisons (29/34), and lookup (31/37). Scheduling (24/69), causal intervention (12/44), exact truth counting (16/65), and truth-teller consistency (14/62) remained weak. It did not outperform Mercury on aggregate accuracy, known cost or median response time in this run.


Granite 4.2 8B was fast and inexpensive, with a 0.324-second median and $0.01555172 in reported cost, but scored 478/1,136 (42.1%). Transitive comparisons (30/34), lookup (31/37), and set relations (35/43) were its better areas. Contraposition (5/46), sequential procedures (5/42), exact truth counting (12/65), and object swaps (10/46) were poor. Its post-hoc leading-ID score is almost unchanged at 479/1,136, so formatting alone does not account for the low total. Five error attempts omitted cost.


Phi-4's strict score was 428/1,136 (37.7%), but 327 first responses failed the requested output format. Many began with an answer ID and then added explanation, sometimes reaching the 16-token cap. A uniform, post-hoc leading-ID parser raises its score to 536/1,136 (47.2%). This matters: the strict result mixes decision errors with failure to honor the short-output contract. The sensitivity check uses the saved responses, adds no calls, and is not an evaluation with a larger output budget or reasoning enabled. Phi-4 remained below Mercury and regular Luna even under that more permissive reading.


Mistral NeMo was the cheapest new run at $0.009235281 reported, with two error attempts missing cost, but answered only 421/1,136 correctly (37.1%). Its stronger areas were transitive comparisons (31/34), lookup (29/37), and preference ordering (33/45). Exact truth counting (8/65), procedural execution (8/42), contraposition (10/46), and truth-teller consistency (14/62) were weak. Its leading-ID score does not improve the total.



## The two earlier budget LLMs are now evaluated on the full bank


Gemini 2.5 Flash-Lite scored 598/1,136 (52.6%), with a 0.341-second median and a reported cost of $0.03219570. It was strong on lookup (36/37), transitive comparisons (31/34), and preference ordering (38/45), but weak on causal intervention (9/44), scheduling (16/69), exact counting (14/65), and sequential procedures (7/42). It was faster than Mercury on this setup, while Mercury was more accurate and cheaper at its discounted tariff.


GPT-5.4 nano scored 464/1,136 (40.8%). All answers satisfied the numeric-ID format, so there is no formatting explanation for its low total. It cost $0.07005030, the highest amount among the eight new full runs, with a 0.683-second median. Its better areas were transitive comparisons (28/34), lookup (30/37), preference ordering (36/45), and exceptions (35/52). Contraposition (8/46), truth-teller consistency (10/62), scheduling (16/69), and exact truth counting (13/65) were weak. On this particular workload it offers no observed accuracy, median-latency or cost advantage over Mercury.



## The common hard cases remain hard


No model is dependable on sequential procedure execution: the best strict result is Qwen's 11/42 (26.2%). The best exact truth-counting result remains 24/65 (36.9%), shared by the two Jev versions. Object tracking through repeated swaps and truth-teller consistency also remain substantial weaknesses. A typed answer, a short response or a low price does not remove the need to check exact state transitions and counts.


Jev 1.14's broad advantage is clearest on bounded deductions and explicit constraints. It answered all sampled lookup, forward implication, contraposition, Boolean-scope, transitive-comparison, reachability, preference-ordering, source-authority and fault-diagnosis questions correctly. It also retained stronger performance on assignments (56/61), belief tracking (40/44), and planning with preconditions (36/37). Its 46/69 scheduling result and 6/42 procedural result show why those strengths should not be described as general reliability.


There are 26 questions that none of the eleven models answered correctly under the strict primary rules. Their IDs are saved privately for a possible later key and wording audit. That count is not evidence that their reference answers are wrong. This expansion uses the existing key unchanged and does not claim a new independent audit of it.



## What can and cannot be concluded


The eight new LLMs were tested on October 15, 2026, from 12:02 to 12:20 Toronto time. Every request went through OpenRouter, with a named backend pinned, fallback disabled, a fresh HTTPS connection, and at most two concurrent requests per model within each two-question wave. Provider hardware, quantization, default sampling and hidden checkpoint behavior are not controlled. The three historical decision-model records preserve their original dates and methods; their latency and total costs are not mixed into a new controlled speed ranking.


The new runs made 9,096 HTTP/transport attempts for 9,088 scored first requests. Eight transient first-attempt failures received one retry; seven recovered to a usable response and one remained unanswered. Across all attempts there were six HTTP 429s, one HTTP 503 and two local DNS-resolution failures. Local DNS failures should not be described as model reasoning failures. All 9,087 attempts with returned usage reported zero reasoning tokens, and no reasoning field contained a trace. Ordinary visible explanation still occurred in some responses. Reported cost totals $0.227088871; nine error attempts supplied no cost, which remains unknown rather than zero. The earlier 75-call pilot is retained separately and is not included in these full-run costs.


The first-attempt strict score is the registered primary view. Invalid format and truncation are unsuccessful in that view, rather than asserted to be wrong logical choices. Recovery and leading-ID sensitivity are reported separately. No confidence probabilities were requested from the regular LLMs, so they cannot be given the same confidence-filter analysis as the native Decisions models. The 640 core items and 496 related variants are shown separately because the full bank does not contain 1,136 independent observations.
