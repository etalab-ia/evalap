---
id: 67
name: "baseline_model_assIA"
date: 2025-08-07T13:10:50.190282
description: ""
tags: []
---

# Experiment Set: baseline_model_assIA (ID: 67)

Baseline evaluation for Assistant IA dataset

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model               | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |   nb_tool_calls |
|:--------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|----------------:|
| openai/gpt-oss-120b | 0.019 ± 0.0004       | 21.51 ± 0.63      | 0.0113 ± 0.0002   | 5.28 ± 0.08     | 0.5 ± 0.03        | 1455.98 ± 32.31        |              12.59 |               0 |
| albert-large        | 0.0043 ± 0.0         | 11.74 ± 0.13      | 0.0004 ± 0.0      | 5.61 ± 0.12     | 0.39 ± 0.03       | 415.72 ± 4.18          |              12.59 |               0 |
| openai/gpt-oss-20b  | 0.0112 ± 0.0006      | 36.75 ± 13.21     | 0.0067 ± 0.0003   | 4.58 ± 0.16     | 0.35 ± 0.04       | 821.1 ± 37.89          |              12.59 |               0 |
| albert-small        | 0.001 ± 0.0          | 5.02 ± 0.12       | 0.0001 ± 0.0      | 3.19 ± 0.12     | 0.09 ± 0.0        | 316.69 ± 7.41          |              12.59 |               0 |



## Set Overview

|   Id | Name                     | Dataset           | Model               | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------------|:------------------|:--------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1277 | baseline_model_assIA__0  | Assistant IA - QA | albert-large        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1278 | baseline_model_assIA__1  | Assistant IA - QA | albert-large        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1279 | baseline_model_assIA__2  | Assistant IA - QA | albert-large        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1280 | baseline_model_assIA__3  | Assistant IA - QA | albert-large        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1281 | baseline_model_assIA__4  | Assistant IA - QA | albert-large        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1282 | baseline_model_assIA__5  | Assistant IA - QA | albert-small        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1283 | baseline_model_assIA__6  | Assistant IA - QA | albert-small        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1284 | baseline_model_assIA__7  | Assistant IA - QA | albert-small        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1285 | baseline_model_assIA__8  | Assistant IA - QA | albert-small        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1286 | baseline_model_assIA__9  | Assistant IA - QA | albert-small        | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1287 | baseline_model_assIA__10 | Assistant IA - QA | openai/gpt-oss-120b | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1288 | baseline_model_assIA__11 | Assistant IA - QA | openai/gpt-oss-120b | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1289 | baseline_model_assIA__12 | Assistant IA - QA | openai/gpt-oss-120b | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1290 | baseline_model_assIA__13 | Assistant IA - QA | openai/gpt-oss-120b | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1291 | baseline_model_assIA__14 | Assistant IA - QA | openai/gpt-oss-120b | {'temperature': 0.2} | finished | 2025-08-07T13:10:50.190282 |        46 |            46 |
| 1339 | baseline_model_assIA__15 | Assistant IA - QA | openai/gpt-oss-20b  | {'temperature': 0.2} | finished | 2025-08-08T14:09:03.324839 |        46 |            46 |
| 1340 | baseline_model_assIA__17 | Assistant IA - QA | openai/gpt-oss-20b  | {'temperature': 0.2} | finished | 2025-08-08T14:09:03.452966 |        46 |            46 |
| 1341 | baseline_model_assIA__19 | Assistant IA - QA | openai/gpt-oss-20b  | {'temperature': 0.2} | finished | 2025-08-08T14:09:03.516387 |        46 |            46 |
| 1342 | baseline_model_assIA__21 | Assistant IA - QA | openai/gpt-oss-20b  | {'temperature': 0.2} | finished | 2025-08-08T14:09:03.579106 |        46 |            46 |
| 1343 | baseline_model_assIA__23 | Assistant IA - QA | openai/gpt-oss-20b  | {'temperature': 0.2} | finished | 2025-08-08T14:09:03.639657 |        46 |            46 |


## Details by Experiment

- [Experiment 1277](details/experiment_1277.md) - baseline_model_assIA__0
- [Experiment 1278](details/experiment_1278.md) - baseline_model_assIA__1
- [Experiment 1279](details/experiment_1279.md) - baseline_model_assIA__2
- [Experiment 1280](details/experiment_1280.md) - baseline_model_assIA__3
- [Experiment 1281](details/experiment_1281.md) - baseline_model_assIA__4
- [Experiment 1282](details/experiment_1282.md) - baseline_model_assIA__5
- [Experiment 1283](details/experiment_1283.md) - baseline_model_assIA__6
- [Experiment 1284](details/experiment_1284.md) - baseline_model_assIA__7
- [Experiment 1285](details/experiment_1285.md) - baseline_model_assIA__8
- [Experiment 1286](details/experiment_1286.md) - baseline_model_assIA__9
- [Experiment 1287](details/experiment_1287.md) - baseline_model_assIA__10
- [Experiment 1288](details/experiment_1288.md) - baseline_model_assIA__11
- [Experiment 1289](details/experiment_1289.md) - baseline_model_assIA__12
- [Experiment 1290](details/experiment_1290.md) - baseline_model_assIA__13
- [Experiment 1291](details/experiment_1291.md) - baseline_model_assIA__14
- [Experiment 1339](details/experiment_1339.md) - baseline_model_assIA__15
- [Experiment 1340](details/experiment_1340.md) - baseline_model_assIA__17
- [Experiment 1341](details/experiment_1341.md) - baseline_model_assIA__19
- [Experiment 1342](details/experiment_1342.md) - baseline_model_assIA__21
- [Experiment 1343](details/experiment_1343.md) - baseline_model_assIA__23
