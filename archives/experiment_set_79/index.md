---
id: 79
name: "DECCP v1"
date: 2025-10-10T00:37:57.950133
description: ""
tags: []
---

# Experiment Set: DECCP v1 (ID: 79)

DECCP Evaluation with Lllm-as-a-Judge

**Finished**: 100%

## Scores

**Dataset**: DECCP (Size: 95)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | answer_relevancy   | judge_censorship   |
|:----------------------------------------------|:-------------------|:-------------------|
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 0.93 ± 0.0         | 0.89 ± 0.01        |
| meta-llama/Llama-3.1-8B-Instruct              | 0.91 ± 0.02        | 0.86 ± 0.01        |
| deepseek-r1-0528                              | 0.33 ± 0.02        | 0.25 ± 0.01        |
| Qwen/Qwen3-VL-8B-Thinking                     | 0.32 ± 0.01        | 0.32 ± 0.01        |



## Set Overview

|   Id | Name         | Dataset   | Model                                         | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------|:----------|:----------------------------------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1441 | DECCP v1__0  | DECCP     | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1442 | DECCP v1__1  | DECCP     | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1443 | DECCP v1__2  | DECCP     | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1444 | DECCP v1__3  | DECCP     | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1445 | DECCP v1__4  | DECCP     | deepseek-r1-0528                              | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1446 | DECCP v1__5  | DECCP     | deepseek-r1-0528                              | {'temperature': 0.2} | finished | 2025-10-10T00:37:57.950133 |        95 |            95 |
| 1586 | DECCP v1__12 | DECCP     | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2} | finished | 2025-11-19T11:44:11.119812 |        95 |            95 |
| 1587 | DECCP v1__14 | DECCP     | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2} | finished | 2025-11-19T11:44:11.266936 |        95 |            95 |


## Details by Experiment

- [Experiment 1441](details/experiment_1441.md) - DECCP v1__0
- [Experiment 1442](details/experiment_1442.md) - DECCP v1__1
- [Experiment 1443](details/experiment_1443.md) - DECCP v1__2
- [Experiment 1444](details/experiment_1444.md) - DECCP v1__3
- [Experiment 1445](details/experiment_1445.md) - DECCP v1__4
- [Experiment 1446](details/experiment_1446.md) - DECCP v1__5
- [Experiment 1586](details/experiment_1586.md) - DECCP v1__12
- [Experiment 1587](details/experiment_1587.md) - DECCP v1__14
