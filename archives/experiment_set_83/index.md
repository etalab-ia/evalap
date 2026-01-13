---
id: 83
name: "Compare Open Weight Models 31th"
date: 2025-10-31T15:45:42.793753
description: ""
tags: []
---

# Experiment Set: Compare Open Weight Models 31th (ID: 83)

Comparing open weight models

**Finished**: 90%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:----------------|
| mistral-medium-2508                           | 9.5 ± 1.08        | 0.62 ± 0.02       | 517.64 ± 19.54  |
| gpt-oss-120b-RAG                              | 21.32 ± 0.26      | 0.59 ± 0.0        | 864.84 ± 10.07  |
| openai/gpt-oss-120b                           | 20.99 ± 0.51      | 0.58 ± 0.02       | 844.25 ± 0.42   |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 11.34 ± 0.81      | 0.51 ± 0.02       | 243.76 ± 2.21   |
| openai/gpt-oss-20b                            | 33.23 ± 8.29      | 0.4 ± 0.05        | 509.82 ± 13.76  |
| Qwen/Qwen3-VL-8B-Thinking                     | 133.12 ± 28.15    | 0.26 ± 0.02       | 360.72 ± 11.55  |
| nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | 6.9 ± 0.78        | 0.25 ± 0.05       | 284.9 ± 2.94    |
| Qwen/Qwen3-VL-4B-Instruct                     | 80.63 ± 37.76     | 0.11 ± 0.0        | 591.64 ± 3.64   |
| meta-llama/Llama-3.1-8B-Instruct              | 5.17 ± 0.12       | 0.09 ± 0.03       | 235.35 ± 4.86   |
| Groq/Llama-3-Groq-8B-Tool-Use                 | 0.72 ± 0.03       | 0.02 ± 0.0        | 45.46 ± 0.37    |
| mistralai/Magistral-Small-2509                | nan ± nan         | nan ± nan         | nan ± nan       |


**Support**: the numbers of item on which the metrics is computed (total items = 46)

| model                                         | generation_time_support   | judge_precision_support   | output_length_support   |
|:----------------------------------------------|:--------------------------|:--------------------------|:------------------------|
| mistral-medium-2508                           | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| gpt-oss-120b-RAG                              | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| openai/gpt-oss-120b                           | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| openai/gpt-oss-20b                            | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| Qwen/Qwen3-VL-8B-Thinking                     | 44.0 ± 1.41               | 44.0 ± 1.41               | 44.0 ± 1.41             |
| nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| Qwen/Qwen3-VL-4B-Instruct                     | 44.0 ± 1.41               | 44.0 ± 1.41               | 44.0 ± 1.41             |
| meta-llama/Llama-3.1-8B-Instruct              | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| Groq/Llama-3-Groq-8B-Tool-Use                 | 46.0 ± 0.0                | 46.0 ± 0.0                | 46.0 ± 0.0              |
| mistralai/Magistral-Small-2509                | nan ± nan                 | nan ± nan                 | nan ± nan               |


**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_precision   | output_length    |
|:----------------------------------------------|:------------------|:------------------|:-----------------|
| mistral-medium-2508                           | 14.06 ± 2.3       | 0.73 ± 0.05       | 656.35 ± 12.35   |
| openai/gpt-oss-120b                           | 34.92 ± 7.47      | 0.71 ± 0.02       | 1302.47 ± 4.08   |
| gpt-oss-120b-RAG                              | 31.69 ± 1.74      | 0.58 ± 0.02       | 1308.55 ± 108.77 |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 15.76 ± 0.63      | 0.44 ± 0.04       | 319.74 ± 3.23    |
| openai/gpt-oss-20b                            | 47.73 ± 5.89      | 0.37 ± 0.05       | 750.28 ± 23.93   |
| Qwen/Qwen3-VL-8B-Thinking                     | 142.41 ± 3.3      | 0.27 ± 0.05       | 475.87 ± 11.46   |
| nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | 5.17 ± 0.71       | 0.23 ± 0.07       | 279.27 ± 1.61    |
| Qwen/Qwen3-VL-4B-Instruct                     | 57.7 ± 12.59      | 0.2 ± 0.0         | 664.27 ± 66.45   |
| meta-llama/Llama-3.1-8B-Instruct              | 6.5 ± 0.24        | 0.1 ± 0.0         | 301.87 ± 13.09   |
| Groq/Llama-3-Groq-8B-Tool-Use                 | 0.94 ± 0.02       | 0.06 ± 0.02       | 62.62 ± 1.31     |
| mistralai/Magistral-Small-2509                | nan ± nan         | nan ± nan         | nan ± nan        |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         |   generation_time_support |   judge_precision_support |   output_length_support |
|:----------------------------------------------|--------------------------:|--------------------------:|------------------------:|
| mistral-medium-2508                           |                        39 |                        39 |                      39 |
| openai/gpt-oss-120b                           |                        39 |                        39 |                      39 |
| gpt-oss-120b-RAG                              |                        39 |                        39 |                      39 |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 |                        39 |                        39 |                      39 |
| openai/gpt-oss-20b                            |                        39 |                        39 |                      39 |
| Qwen/Qwen3-VL-8B-Thinking                     |                        39 |                        39 |                      39 |
| nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     |                        39 |                        39 |                      39 |
| Qwen/Qwen3-VL-4B-Instruct                     |                        35 |                        35 |                      35 |
| meta-llama/Llama-3.1-8B-Instruct              |                        39 |                        39 |                      39 |
| Groq/Llama-3-Groq-8B-Tool-Use                 |                        39 |                        39 |                      39 |
| mistralai/Magistral-Small-2509                |                       nan |                       nan |                     nan |



## Set Overview

|   Id | Name                                | Dataset           | Model                                         | Model params                                                                                                       | Status          | Created at                 |   Num try |   Num success |
|-----:|:------------------------------------|:------------------|:----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|:----------------|:---------------------------|----------:|--------------:|
| 1460 | Compare Open Weight Models 31th__0  | MFS_questions_v01 | gpt-oss-120b-RAG                              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [783, 784, 785], 'k': 10}} | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1461 | Compare Open Weight Models 31th__1  | MFS_questions_v01 | gpt-oss-120b-RAG                              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [783, 784, 785], 'k': 10}} | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1462 | Compare Open Weight Models 31th__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1463 | Compare Open Weight Models 31th__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1464 | Compare Open Weight Models 31th__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1465 | Compare Open Weight Models 31th__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1466 | Compare Open Weight Models 31th__6  | MFS_questions_v01 | openai/gpt-oss-120b                           | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1467 | Compare Open Weight Models 31th__7  | MFS_questions_v01 | openai/gpt-oss-120b                           | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        39 |            39 |
| 1468 | Compare Open Weight Models 31th__8  | Assistant IA - QA | gpt-oss-120b-RAG                              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [783, 784, 785], 'k': 10}} | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1469 | Compare Open Weight Models 31th__9  | Assistant IA - QA | gpt-oss-120b-RAG                              | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [783, 784, 785], 'k': 10}} | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1470 | Compare Open Weight Models 31th__10 | Assistant IA - QA | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1471 | Compare Open Weight Models 31th__11 | Assistant IA - QA | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1472 | Compare Open Weight Models 31th__12 | Assistant IA - QA | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1473 | Compare Open Weight Models 31th__13 | Assistant IA - QA | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1474 | Compare Open Weight Models 31th__14 | Assistant IA - QA | openai/gpt-oss-120b                           | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1475 | Compare Open Weight Models 31th__15 | Assistant IA - QA | openai/gpt-oss-120b                           | {'temperature': 0.2}                                                                                               | finished        | 2025-10-31T15:45:42.793753 |        46 |            46 |
| 1542 | Compare Open Weight Models 31th__32 | MFS_questions_v01 | nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T16:13:38.437346 |        39 |            39 |
| 1543 | Compare Open Weight Models 31th__34 | MFS_questions_v01 | nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T16:13:38.550790 |        39 |            39 |
| 1544 | Compare Open Weight Models 31th__36 | Assistant IA - QA | nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T16:13:38.621183 |        46 |            46 |
| 1545 | Compare Open Weight Models 31th__38 | Assistant IA - QA | nvidia/Llama-4-Scout-17B-16E-Instruct-FP8     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T16:13:38.688061 |        46 |            46 |
| 1550 | Compare Open Weight Models 31th__40 | MFS_questions_v01 | mistral-medium-2508                           | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T17:04:20.083436 |        39 |            39 |
| 1551 | Compare Open Weight Models 31th__42 | MFS_questions_v01 | mistral-medium-2508                           | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T17:04:20.177843 |        39 |            39 |
| 1552 | Compare Open Weight Models 31th__44 | Assistant IA - QA | mistral-medium-2508                           | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T17:04:20.310415 |        46 |            46 |
| 1553 | Compare Open Weight Models 31th__46 | Assistant IA - QA | mistral-medium-2508                           | {'temperature': 0.2}                                                                                               | finished        | 2025-11-13T17:04:20.418754 |        46 |            46 |
| 1566 | Compare Open Weight Models 31th__48 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2}                                                                                               | running_metrics | 2025-11-14T10:42:22.863338 |        39 |            38 |
| 1567 | Compare Open Weight Models 31th__50 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-14T10:42:22.972446 |        39 |            39 |
| 1568 | Compare Open Weight Models 31th__52 | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-14T10:42:23.049272 |        46 |            45 |
| 1569 | Compare Open Weight Models 31th__54 | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking                     | {'temperature': 0.2}                                                                                               | running_metrics | 2025-11-14T10:42:23.116603 |        46 |            43 |
| 1570 | Compare Open Weight Models 31th__56 | MFS_questions_v01 | mistralai/Magistral-Small-2509                | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:07:18.394496 |        39 |             0 |
| 1571 | Compare Open Weight Models 31th__58 | MFS_questions_v01 | mistralai/Magistral-Small-2509                | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:07:18.510929 |        39 |             0 |
| 1572 | Compare Open Weight Models 31th__60 | Assistant IA - QA | mistralai/Magistral-Small-2509                | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:07:18.588684 |        46 |             0 |
| 1573 | Compare Open Weight Models 31th__62 | Assistant IA - QA | mistralai/Magistral-Small-2509                | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:07:18.656210 |        46 |             0 |
| 1574 | Compare Open Weight Models 31th__64 | MFS_questions_v01 | Groq/Llama-3-Groq-8B-Tool-Use                 | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:45:33.849411 |        39 |            39 |
| 1575 | Compare Open Weight Models 31th__66 | MFS_questions_v01 | Groq/Llama-3-Groq-8B-Tool-Use                 | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:45:33.952680 |        39 |            39 |
| 1576 | Compare Open Weight Models 31th__68 | Assistant IA - QA | Groq/Llama-3-Groq-8B-Tool-Use                 | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:45:34.015209 |        46 |            46 |
| 1577 | Compare Open Weight Models 31th__70 | Assistant IA - QA | Groq/Llama-3-Groq-8B-Tool-Use                 | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T10:45:34.082618 |        46 |            46 |
| 1578 | Compare Open Weight Models 31th__72 | MFS_questions_v01 | Qwen/Qwen3-VL-4B-Instruct                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T11:32:45.765198 |        39 |            35 |
| 1579 | Compare Open Weight Models 31th__74 | MFS_questions_v01 | Qwen/Qwen3-VL-4B-Instruct                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T11:32:45.846744 |        39 |            35 |
| 1580 | Compare Open Weight Models 31th__76 | Assistant IA - QA | Qwen/Qwen3-VL-4B-Instruct                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T11:32:45.908254 |        46 |            45 |
| 1581 | Compare Open Weight Models 31th__78 | Assistant IA - QA | Qwen/Qwen3-VL-4B-Instruct                     | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T11:32:45.973374 |        46 |            43 |
| 1582 | Compare Open Weight Models 31th__80 | MFS_questions_v01 | openai/gpt-oss-20b                            | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T16:59:30.105226 |        39 |            39 |
| 1583 | Compare Open Weight Models 31th__82 | MFS_questions_v01 | openai/gpt-oss-20b                            | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T16:59:30.189610 |        39 |            39 |
| 1584 | Compare Open Weight Models 31th__84 | Assistant IA - QA | openai/gpt-oss-20b                            | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T16:59:30.257223 |        46 |            46 |
| 1585 | Compare Open Weight Models 31th__86 | Assistant IA - QA | openai/gpt-oss-20b                            | {'temperature': 0.2}                                                                                               | finished        | 2025-11-18T16:59:30.321441 |        46 |            46 |


## Details by Experiment

- [Experiment 1460](details/experiment_1460.md) - Compare Open Weight Models 31th__0
- [Experiment 1461](details/experiment_1461.md) - Compare Open Weight Models 31th__1
- [Experiment 1462](details/experiment_1462.md) - Compare Open Weight Models 31th__2
- [Experiment 1463](details/experiment_1463.md) - Compare Open Weight Models 31th__3
- [Experiment 1464](details/experiment_1464.md) - Compare Open Weight Models 31th__4
- [Experiment 1465](details/experiment_1465.md) - Compare Open Weight Models 31th__5
- [Experiment 1466](details/experiment_1466.md) - Compare Open Weight Models 31th__6
- [Experiment 1467](details/experiment_1467.md) - Compare Open Weight Models 31th__7
- [Experiment 1468](details/experiment_1468.md) - Compare Open Weight Models 31th__8
- [Experiment 1469](details/experiment_1469.md) - Compare Open Weight Models 31th__9
- [Experiment 1470](details/experiment_1470.md) - Compare Open Weight Models 31th__10
- [Experiment 1471](details/experiment_1471.md) - Compare Open Weight Models 31th__11
- [Experiment 1472](details/experiment_1472.md) - Compare Open Weight Models 31th__12
- [Experiment 1473](details/experiment_1473.md) - Compare Open Weight Models 31th__13
- [Experiment 1474](details/experiment_1474.md) - Compare Open Weight Models 31th__14
- [Experiment 1475](details/experiment_1475.md) - Compare Open Weight Models 31th__15
- [Experiment 1542](details/experiment_1542.md) - Compare Open Weight Models 31th__32
- [Experiment 1543](details/experiment_1543.md) - Compare Open Weight Models 31th__34
- [Experiment 1544](details/experiment_1544.md) - Compare Open Weight Models 31th__36
- [Experiment 1545](details/experiment_1545.md) - Compare Open Weight Models 31th__38
- [Experiment 1550](details/experiment_1550.md) - Compare Open Weight Models 31th__40
- [Experiment 1551](details/experiment_1551.md) - Compare Open Weight Models 31th__42
- [Experiment 1552](details/experiment_1552.md) - Compare Open Weight Models 31th__44
- [Experiment 1553](details/experiment_1553.md) - Compare Open Weight Models 31th__46
- [Experiment 1566](details/experiment_1566.md) - Compare Open Weight Models 31th__48
- [Experiment 1567](details/experiment_1567.md) - Compare Open Weight Models 31th__50
- [Experiment 1568](details/experiment_1568.md) - Compare Open Weight Models 31th__52
- [Experiment 1569](details/experiment_1569.md) - Compare Open Weight Models 31th__54
- [Experiment 1570](details/experiment_1570.md) - Compare Open Weight Models 31th__56
- [Experiment 1571](details/experiment_1571.md) - Compare Open Weight Models 31th__58
- [Experiment 1572](details/experiment_1572.md) - Compare Open Weight Models 31th__60
- [Experiment 1573](details/experiment_1573.md) - Compare Open Weight Models 31th__62
- [Experiment 1574](details/experiment_1574.md) - Compare Open Weight Models 31th__64
- [Experiment 1575](details/experiment_1575.md) - Compare Open Weight Models 31th__66
- [Experiment 1576](details/experiment_1576.md) - Compare Open Weight Models 31th__68
- [Experiment 1577](details/experiment_1577.md) - Compare Open Weight Models 31th__70
- [Experiment 1578](details/experiment_1578.md) - Compare Open Weight Models 31th__72
- [Experiment 1579](details/experiment_1579.md) - Compare Open Weight Models 31th__74
- [Experiment 1580](details/experiment_1580.md) - Compare Open Weight Models 31th__76
- [Experiment 1581](details/experiment_1581.md) - Compare Open Weight Models 31th__78
- [Experiment 1582](details/experiment_1582.md) - Compare Open Weight Models 31th__80
- [Experiment 1583](details/experiment_1583.md) - Compare Open Weight Models 31th__82
- [Experiment 1584](details/experiment_1584.md) - Compare Open Weight Models 31th__84
- [Experiment 1585](details/experiment_1585.md) - Compare Open Weight Models 31th__86
