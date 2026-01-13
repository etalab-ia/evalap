---
id: 108
name: "Comparing Albert-API models v11-12-2025 (with sysprompt)"
date: 2025-12-11T20:06:52.533324
description: ""
tags: []
---

# Experiment Set: Comparing Albert-API models v11-12-2025 (with sysprompt) (ID: 108)

Comparing albert models on MFS-AIA datasets (with sysprompt)

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: mistral-medium-latest

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model             | generation_time   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| openweight-large  | 1.68 ± 0.02       | 6.14 ± 0.08     | 0.38 ± 0.02       | 60.11 ± 1.14           |              28.59 | 37.82 ± 1.49    |
| openweight-small  | 0.29 ± 0.02       | 5.09 ± 0.0      | 0.14 ± 0.02       | 60.62 ± 4.29           |              28.59 | 30.55 ± 2.47    |
| albert-small      | 3.73 ± 3.89       | 3.55 ± 0.02     | 0.1 ± 0.02        | 51.7 ± 6.09            |              28.59 | 34.3 ± 4.52     |
| albert-large      | 0.93 ± 0.18       | 5.33 ± 0.03     | 0.03 ± 0.02       | 28.54 ± 0.92           |              28.59 | 18.74 ± 0.49    |
| openweight-medium | 0.45 ± 0.05       | 5.45 ± 0.02     | 0.03 ± 0.02       | 27.46 ± 1.2            |              28.59 | 17.93 ± 0.58    |


**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: mistral-medium-latest

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model             | generation_time   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt | output_length   |
|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|:----------------|
| openweight-large  | 1.74 ± 0.11       | 6.86 ± 0.09     | 0.46 ± 0.04       | 95.62 ± 5.48           |               37.9 | 56.85 ± 2.5     |
| openweight-small  | 0.53 ± 0.09       | 6.67 ± 0.47     | 0.32 ± 0.02       | 77.13 ± 2.72           |               37.9 | 38.13 ± 1.96    |
| openweight-medium | 0.69 ± 0.04       | 6.44 ± 0.11     | 0.18 ± 0.0        | 39.32 ± 0.45           |               37.9 | 26.22 ± 0.13    |
| albert-large      | 1.35 ± 0.2        | 6.47 ± 0.09     | 0.17 ± 0.02       | 41.45 ± 4.04           |               37.9 | 27.72 ± 2.28    |
| albert-small      | 14.03 ± 8.88      | 4.78 ± 0.67     | 0.13 ± 0.07       | 70.76 ± 4.26           |               37.9 | 50.38 ± 3.01    |



## Set Overview

|   Id | Name                                                         | Dataset           | Model             | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------------------------------------------------|:------------------|:------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1674 | Comparing Albert-API models v11-12-2025 (with sysprompt)__0  | MFS_questions_v01 | openweight-small  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1675 | Comparing Albert-API models v11-12-2025 (with sysprompt)__1  | MFS_questions_v01 | openweight-small  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1676 | Comparing Albert-API models v11-12-2025 (with sysprompt)__2  | MFS_questions_v01 | openweight-medium | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1677 | Comparing Albert-API models v11-12-2025 (with sysprompt)__3  | MFS_questions_v01 | openweight-medium | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1678 | Comparing Albert-API models v11-12-2025 (with sysprompt)__4  | MFS_questions_v01 | openweight-large  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1679 | Comparing Albert-API models v11-12-2025 (with sysprompt)__5  | MFS_questions_v01 | openweight-large  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1680 | Comparing Albert-API models v11-12-2025 (with sysprompt)__6  | MFS_questions_v01 | albert-small      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1681 | Comparing Albert-API models v11-12-2025 (with sysprompt)__7  | MFS_questions_v01 | albert-small      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1682 | Comparing Albert-API models v11-12-2025 (with sysprompt)__8  | MFS_questions_v01 | albert-large      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1683 | Comparing Albert-API models v11-12-2025 (with sysprompt)__9  | MFS_questions_v01 | albert-large      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        39 |            39 |
| 1684 | Comparing Albert-API models v11-12-2025 (with sysprompt)__10 | Assistant IA - QA | openweight-small  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1685 | Comparing Albert-API models v11-12-2025 (with sysprompt)__11 | Assistant IA - QA | openweight-small  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1686 | Comparing Albert-API models v11-12-2025 (with sysprompt)__12 | Assistant IA - QA | openweight-medium | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1687 | Comparing Albert-API models v11-12-2025 (with sysprompt)__13 | Assistant IA - QA | openweight-medium | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1688 | Comparing Albert-API models v11-12-2025 (with sysprompt)__14 | Assistant IA - QA | openweight-large  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1689 | Comparing Albert-API models v11-12-2025 (with sysprompt)__15 | Assistant IA - QA | openweight-large  | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1690 | Comparing Albert-API models v11-12-2025 (with sysprompt)__16 | Assistant IA - QA | albert-small      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1691 | Comparing Albert-API models v11-12-2025 (with sysprompt)__17 | Assistant IA - QA | albert-small      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1692 | Comparing Albert-API models v11-12-2025 (with sysprompt)__18 | Assistant IA - QA | albert-large      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |
| 1693 | Comparing Albert-API models v11-12-2025 (with sysprompt)__19 | Assistant IA - QA | albert-large      | {'temperature': 0.2, 'sys_prompt': '543c'} | finished | 2025-12-11T20:06:52.533324 |        46 |            46 |


## Details by Experiment

- [Experiment 1674](details/experiment_1674.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__0
- [Experiment 1675](details/experiment_1675.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__1
- [Experiment 1676](details/experiment_1676.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__2
- [Experiment 1677](details/experiment_1677.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__3
- [Experiment 1678](details/experiment_1678.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__4
- [Experiment 1679](details/experiment_1679.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__5
- [Experiment 1680](details/experiment_1680.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__6
- [Experiment 1681](details/experiment_1681.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__7
- [Experiment 1682](details/experiment_1682.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__8
- [Experiment 1683](details/experiment_1683.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__9
- [Experiment 1684](details/experiment_1684.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__10
- [Experiment 1685](details/experiment_1685.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__11
- [Experiment 1686](details/experiment_1686.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__12
- [Experiment 1687](details/experiment_1687.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__13
- [Experiment 1688](details/experiment_1688.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__14
- [Experiment 1689](details/experiment_1689.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__15
- [Experiment 1690](details/experiment_1690.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__16
- [Experiment 1691](details/experiment_1691.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__17
- [Experiment 1692](details/experiment_1692.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__18
- [Experiment 1693](details/experiment_1693.md) - Comparing Albert-API models v11-12-2025 (with sysprompt)__19
