---
id: 113
name: "Comparing openweight with openai/gpt-oss-120b"
date: 2025-12-18T13:55:38.390142
description: ""
tags: []
---

# Experiment Set: Comparing openweight with openai/gpt-oss-120b (ID: 113)

Comparing openweight Albert-API with specific judge openai/gpt-oss-120b

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: openai/gpt-oss-120b

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.0167 ± 0.0005      | 14.46 ± 0.22      | 0.0014 ± 0.0      | 6.7 ± 0.12      | 0.26 ± 0.0        | 1747.21 ± 53.68        |               38.9 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0037 ± 0.0001      | 8.53 ± 3.07       | 0.0003 ± 0.0      | 6.96 ± 0.19     | 0.21 ± 0.03       | 1365.38 ± 32.91        |               38.9 |
| Mistral small              | 0.003 ± 0.0          | 10.97 ± 1.09      | 0.0003 ± 0.0      | 6.54 ± 0.23     | 0.16 ± 0.07       | 456.58 ± 1.12          |               38.9 |


**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: openai/gpt-oss-120b

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.0114 ± 0.0002      | 10.23 ± 0.14      | 0.001 ± 0.0       | 6.41 ± 0.17     | 0.24 ± 0.02       | 1194.73 ± 20.83        |              29.59 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0027 ± 0.0001      | 4.9 ± 0.29        | 0.0002 ± 0.0      | 5.58 ± 0.06     | 0.19 ± 0.03       | 1024.26 ± 48.3         |              29.59 |
| Mistral small              | 0.0021 ± 0.0001      | 8.54 ± 0.64       | 0.0002 ± 0.0      | 6.04 ± 0.15     | 0.11 ± 0.01       | 326.14 ± 11.73         |              29.59 |



## Set Overview

|   Id | Name                                              | Dataset           | Model                      | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------------------------|:------------------|:---------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1708 | Comparing openweight with openai/gpt-oss-120b__0  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1709 | Comparing openweight with openai/gpt-oss-120b__1  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1710 | Comparing openweight with openai/gpt-oss-120b__2  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1711 | Comparing openweight with openai/gpt-oss-120b__3  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1712 | Comparing openweight with openai/gpt-oss-120b__4  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1713 | Comparing openweight with openai/gpt-oss-120b__5  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1714 | Comparing openweight with openai/gpt-oss-120b__6  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1715 | Comparing openweight with openai/gpt-oss-120b__7  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1716 | Comparing openweight with openai/gpt-oss-120b__8  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1717 | Comparing openweight with openai/gpt-oss-120b__9  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1718 | Comparing openweight with openai/gpt-oss-120b__10 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1719 | Comparing openweight with openai/gpt-oss-120b__11 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        46 |            46 |
| 1720 | Comparing openweight with openai/gpt-oss-120b__12 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1721 | Comparing openweight with openai/gpt-oss-120b__13 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1722 | Comparing openweight with openai/gpt-oss-120b__14 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1723 | Comparing openweight with openai/gpt-oss-120b__15 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1724 | Comparing openweight with openai/gpt-oss-120b__16 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1725 | Comparing openweight with openai/gpt-oss-120b__17 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1726 | Comparing openweight with openai/gpt-oss-120b__18 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1727 | Comparing openweight with openai/gpt-oss-120b__19 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1728 | Comparing openweight with openai/gpt-oss-120b__20 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1729 | Comparing openweight with openai/gpt-oss-120b__21 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1730 | Comparing openweight with openai/gpt-oss-120b__22 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |
| 1731 | Comparing openweight with openai/gpt-oss-120b__23 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T13:55:38.390142 |        39 |            39 |


## Details by Experiment

- [Experiment 1708](details/experiment_1708.md) - Comparing openweight with openai/gpt-oss-120b__0
- [Experiment 1709](details/experiment_1709.md) - Comparing openweight with openai/gpt-oss-120b__1
- [Experiment 1710](details/experiment_1710.md) - Comparing openweight with openai/gpt-oss-120b__2
- [Experiment 1711](details/experiment_1711.md) - Comparing openweight with openai/gpt-oss-120b__3
- [Experiment 1712](details/experiment_1712.md) - Comparing openweight with openai/gpt-oss-120b__4
- [Experiment 1713](details/experiment_1713.md) - Comparing openweight with openai/gpt-oss-120b__5
- [Experiment 1714](details/experiment_1714.md) - Comparing openweight with openai/gpt-oss-120b__6
- [Experiment 1715](details/experiment_1715.md) - Comparing openweight with openai/gpt-oss-120b__7
- [Experiment 1716](details/experiment_1716.md) - Comparing openweight with openai/gpt-oss-120b__8
- [Experiment 1717](details/experiment_1717.md) - Comparing openweight with openai/gpt-oss-120b__9
- [Experiment 1718](details/experiment_1718.md) - Comparing openweight with openai/gpt-oss-120b__10
- [Experiment 1719](details/experiment_1719.md) - Comparing openweight with openai/gpt-oss-120b__11
- [Experiment 1720](details/experiment_1720.md) - Comparing openweight with openai/gpt-oss-120b__12
- [Experiment 1721](details/experiment_1721.md) - Comparing openweight with openai/gpt-oss-120b__13
- [Experiment 1722](details/experiment_1722.md) - Comparing openweight with openai/gpt-oss-120b__14
- [Experiment 1723](details/experiment_1723.md) - Comparing openweight with openai/gpt-oss-120b__15
- [Experiment 1724](details/experiment_1724.md) - Comparing openweight with openai/gpt-oss-120b__16
- [Experiment 1725](details/experiment_1725.md) - Comparing openweight with openai/gpt-oss-120b__17
- [Experiment 1726](details/experiment_1726.md) - Comparing openweight with openai/gpt-oss-120b__18
- [Experiment 1727](details/experiment_1727.md) - Comparing openweight with openai/gpt-oss-120b__19
- [Experiment 1728](details/experiment_1728.md) - Comparing openweight with openai/gpt-oss-120b__20
- [Experiment 1729](details/experiment_1729.md) - Comparing openweight with openai/gpt-oss-120b__21
- [Experiment 1730](details/experiment_1730.md) - Comparing openweight with openai/gpt-oss-120b__22
- [Experiment 1731](details/experiment_1731.md) - Comparing openweight with openai/gpt-oss-120b__23
