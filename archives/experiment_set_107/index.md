---
id: 107
name: "Comparing Albert-API models v11-12-2025"
date: 2025-12-11T19:30:34.093055
description: ""
tags: []
---

# Experiment Set: Comparing Albert-API models v11-12-2025 (ID: 107)

Comparing albert models on MFS-AIA datasets

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: mistral-medium-latest

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model             | generation_time   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| openweight-large  | 13.32 ± 0.14      | 6.62 ± 0.02     | 0.67 ± 0.0        | 1532.93 ± 3.44         |              12.59 | 890.07 ± 1.78   |
| openweight-small  | 6.01 ± 0.75       | 6.29 ± 0.14     | 0.65 ± 0.03       | 1094.67 ± 32.65        |              12.59 | 595.84 ± 21.2   |
| albert-large      | 12.76 ± 0.15      | 6.63 ± 0.37     | 0.63 ± 0.03       | 409.09 ± 3.81          |              12.59 | 242.57 ± 4.06   |
| openweight-medium | 6.37 ± 0.03       | 6.64 ± 0.26     | 0.6 ± 0.05        | 420.42 ± 5.46          |              12.59 | 249.72 ± 2.12   |
| albert-small      | 5.95 ± 0.23       | 4.1 ± 0.17      | 0.23 ± 0.05       | 316.1 ± 9.42           |              12.59 | 230.24 ± 5.1    |


**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: mistral-medium-latest

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model             | generation_time   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| openweight-small  | 8.06 ± 0.78       | 7.5 ± 0.05      | 0.85 ± 0.0        | 1504.79 ± 2.54         |               21.9 | 827.47 ± 0.42   |
| openweight-large  | 18.28 ± 0.87      | 7.63 ± 0.24     | 0.83 ± 0.05       | 2311.38 ± 15.74        |               21.9 | 1340.09 ± 2.67  |
| openweight-medium | 9.38 ± 0.0        | 7.33 ± 0.07     | 0.76 ± 0.02       | 554.85 ± 7.8           |               21.9 | 325.5 ± 1.03    |
| albert-large      | 18.74 ± 4.71      | 7.28 ± 0.0      | 0.73 ± 0.02       | 544.14 ± 5.09          |               21.9 | 322.56 ± 0.51   |
| albert-small      | 7.28 ± 0.44       | 5.38 ± 0.11     | 0.28 ± 0.0        | 413.38 ± 1.38          |               21.9 | 301.97 ± 2.07   |



## Set Overview

|   Id | Name                                        | Dataset           | Model             | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------------------|:------------------|:------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1654 | Comparing Albert-API models v11-12-2025__0  | MFS_questions_v01 | openweight-small  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1655 | Comparing Albert-API models v11-12-2025__1  | MFS_questions_v01 | openweight-small  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1656 | Comparing Albert-API models v11-12-2025__2  | MFS_questions_v01 | openweight-medium | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1657 | Comparing Albert-API models v11-12-2025__3  | MFS_questions_v01 | openweight-medium | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1658 | Comparing Albert-API models v11-12-2025__4  | MFS_questions_v01 | openweight-large  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1659 | Comparing Albert-API models v11-12-2025__5  | MFS_questions_v01 | openweight-large  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1660 | Comparing Albert-API models v11-12-2025__6  | MFS_questions_v01 | albert-small      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1661 | Comparing Albert-API models v11-12-2025__7  | MFS_questions_v01 | albert-small      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1662 | Comparing Albert-API models v11-12-2025__8  | MFS_questions_v01 | albert-large      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1663 | Comparing Albert-API models v11-12-2025__9  | MFS_questions_v01 | albert-large      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        39 |            39 |
| 1664 | Comparing Albert-API models v11-12-2025__10 | Assistant IA - QA | openweight-small  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1665 | Comparing Albert-API models v11-12-2025__11 | Assistant IA - QA | openweight-small  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1666 | Comparing Albert-API models v11-12-2025__12 | Assistant IA - QA | openweight-medium | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1667 | Comparing Albert-API models v11-12-2025__13 | Assistant IA - QA | openweight-medium | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1668 | Comparing Albert-API models v11-12-2025__14 | Assistant IA - QA | openweight-large  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1669 | Comparing Albert-API models v11-12-2025__15 | Assistant IA - QA | openweight-large  | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1670 | Comparing Albert-API models v11-12-2025__16 | Assistant IA - QA | albert-small      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1671 | Comparing Albert-API models v11-12-2025__17 | Assistant IA - QA | albert-small      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1672 | Comparing Albert-API models v11-12-2025__18 | Assistant IA - QA | albert-large      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |
| 1673 | Comparing Albert-API models v11-12-2025__19 | Assistant IA - QA | albert-large      | {'temperature': 0.2} | finished | 2025-12-11T19:30:34.093055 |        46 |            46 |


## Details by Experiment

- [Experiment 1654](details/experiment_1654.md) - Comparing Albert-API models v11-12-2025__0
- [Experiment 1655](details/experiment_1655.md) - Comparing Albert-API models v11-12-2025__1
- [Experiment 1656](details/experiment_1656.md) - Comparing Albert-API models v11-12-2025__2
- [Experiment 1657](details/experiment_1657.md) - Comparing Albert-API models v11-12-2025__3
- [Experiment 1658](details/experiment_1658.md) - Comparing Albert-API models v11-12-2025__4
- [Experiment 1659](details/experiment_1659.md) - Comparing Albert-API models v11-12-2025__5
- [Experiment 1660](details/experiment_1660.md) - Comparing Albert-API models v11-12-2025__6
- [Experiment 1661](details/experiment_1661.md) - Comparing Albert-API models v11-12-2025__7
- [Experiment 1662](details/experiment_1662.md) - Comparing Albert-API models v11-12-2025__8
- [Experiment 1663](details/experiment_1663.md) - Comparing Albert-API models v11-12-2025__9
- [Experiment 1664](details/experiment_1664.md) - Comparing Albert-API models v11-12-2025__10
- [Experiment 1665](details/experiment_1665.md) - Comparing Albert-API models v11-12-2025__11
- [Experiment 1666](details/experiment_1666.md) - Comparing Albert-API models v11-12-2025__12
- [Experiment 1667](details/experiment_1667.md) - Comparing Albert-API models v11-12-2025__13
- [Experiment 1668](details/experiment_1668.md) - Comparing Albert-API models v11-12-2025__14
- [Experiment 1669](details/experiment_1669.md) - Comparing Albert-API models v11-12-2025__15
- [Experiment 1670](details/experiment_1670.md) - Comparing Albert-API models v11-12-2025__16
- [Experiment 1671](details/experiment_1671.md) - Comparing Albert-API models v11-12-2025__17
- [Experiment 1672](details/experiment_1672.md) - Comparing Albert-API models v11-12-2025__18
- [Experiment 1673](details/experiment_1673.md) - Comparing Albert-API models v11-12-2025__19
