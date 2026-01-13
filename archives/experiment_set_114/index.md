---
id: 114
name: "Comparing openweight with PatronusAI/glider"
date: 2025-12-18T14:22:53.842017
description: ""
tags: []
---

# Experiment Set: Comparing openweight with PatronusAI/glider (ID: 114)

Comparing openweight Albert-API with specific judge PatronusAI/glider

**Finished**: 87%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: PatronusAI/glider

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.0171 ± 0.0003      | 14.55 ± 0.18      | 0.0014 ± 0.0      | 9.75 ± 0.1      | 0.98 ± 0.03       | 1790.04 ± 30.7         |               38.9 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0037 ± 0.0001      | 6.6 ± 0.15        | 0.0003 ± 0.0      | 9.41 ± 0.14     | 0.95 ± 0.02       | 1401.75 ± 39.0         |               38.9 |
| Mistral small              | 0.003 ± 0.0          | 15.22 ± 3.34      | 0.0003 ± 0.0      | nan ± nan       | 0.91 ± 0.01       | 454.77 ± 3.51          |               38.9 |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                      |   energy_consumption_support |   generation_time_support |   gwp_consumption_support | judge_notator_support   | judge_precision_support   |   nb_tokens_completion_support |   nb_tokens_prompt_support |
|:---------------------------|-----------------------------:|--------------------------:|--------------------------:|:------------------------|:--------------------------|-------------------------------:|---------------------------:|
| openai/gpt-oss-120b Albert |                           39 |                        39 |                        39 | 6.75 ± 1.26             | 36.5 ± 0.58               |                             39 |                         39 |
| Qwen/Qwen3-VL-8B-Thinking  |                           39 |                        39 |                        39 | 9.25 ± 3.2              | 38.25 ± 0.5               |                             39 |                         39 |
| Mistral small              |                           39 |                        39 |                        39 | nan ± nan               | 39.0 ± 0.0                |                             39 |                         39 |


**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: PatronusAI/glider

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.0113 ± 0.0004      | 9.52 ± 0.73       | 0.0009 ± 0.0      | 9.79 ± 0.18     | 0.84 ± 0.04       | 1182.17 ± 39.29        |              29.59 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0027 ± 0.0002      | 4.71 ± 0.39       | 0.0002 ± 0.0      | 9.35 ± 0.07     | 0.81 ± 0.05       | 1030.49 ± 60.7         |              29.59 |
| Mistral small              | 0.0023 ± 0.0001      | 12.64 ± 1.6       | 0.0002 ± 0.0      | nan ± nan       | 0.73 ± 0.03       | 341.81 ± 7.57          |              29.59 |


**Support**: the numbers of item on which the metrics is computed (total items = 46)

| model                      |   energy_consumption_support |   generation_time_support |   gwp_consumption_support | judge_notator_support   | judge_precision_support   |   nb_tokens_completion_support |   nb_tokens_prompt_support |
|:---------------------------|-----------------------------:|--------------------------:|--------------------------:|:------------------------|:--------------------------|-------------------------------:|---------------------------:|
| openai/gpt-oss-120b Albert |                           46 |                        46 |                        46 | 6.0 ± 2.16              | 45.0 ± 0.82               |                             46 |                         46 |
| Qwen/Qwen3-VL-8B-Thinking  |                           46 |                        46 |                        46 | 10.5 ± 2.52             | 45.5 ± 0.58               |                             46 |                         46 |
| Mistral small              |                           46 |                        46 |                        46 | nan ± nan               | 45.75 ± 0.5               |                             46 |                         46 |



## Set Overview

|   Id | Name                                            | Dataset           | Model                      | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:------------------------------------------------|:------------------|:---------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1732 | Comparing openweight with PatronusAI/glider__0  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1733 | Comparing openweight with PatronusAI/glider__1  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1734 | Comparing openweight with PatronusAI/glider__2  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1735 | Comparing openweight with PatronusAI/glider__3  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1736 | Comparing openweight with PatronusAI/glider__4  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1737 | Comparing openweight with PatronusAI/glider__5  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1738 | Comparing openweight with PatronusAI/glider__6  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1739 | Comparing openweight with PatronusAI/glider__7  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1740 | Comparing openweight with PatronusAI/glider__8  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1741 | Comparing openweight with PatronusAI/glider__9  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1742 | Comparing openweight with PatronusAI/glider__10 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1743 | Comparing openweight with PatronusAI/glider__11 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        46 |            46 |
| 1744 | Comparing openweight with PatronusAI/glider__12 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1745 | Comparing openweight with PatronusAI/glider__13 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1746 | Comparing openweight with PatronusAI/glider__14 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1747 | Comparing openweight with PatronusAI/glider__15 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1748 | Comparing openweight with PatronusAI/glider__16 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1749 | Comparing openweight with PatronusAI/glider__17 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1750 | Comparing openweight with PatronusAI/glider__18 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1751 | Comparing openweight with PatronusAI/glider__19 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1752 | Comparing openweight with PatronusAI/glider__20 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1753 | Comparing openweight with PatronusAI/glider__21 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1754 | Comparing openweight with PatronusAI/glider__22 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |
| 1755 | Comparing openweight with PatronusAI/glider__23 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T14:22:53.842017 |        39 |            39 |


## Details by Experiment

- [Experiment 1732](details/experiment_1732.md) - Comparing openweight with PatronusAI/glider__0
- [Experiment 1733](details/experiment_1733.md) - Comparing openweight with PatronusAI/glider__1
- [Experiment 1734](details/experiment_1734.md) - Comparing openweight with PatronusAI/glider__2
- [Experiment 1735](details/experiment_1735.md) - Comparing openweight with PatronusAI/glider__3
- [Experiment 1736](details/experiment_1736.md) - Comparing openweight with PatronusAI/glider__4
- [Experiment 1737](details/experiment_1737.md) - Comparing openweight with PatronusAI/glider__5
- [Experiment 1738](details/experiment_1738.md) - Comparing openweight with PatronusAI/glider__6
- [Experiment 1739](details/experiment_1739.md) - Comparing openweight with PatronusAI/glider__7
- [Experiment 1740](details/experiment_1740.md) - Comparing openweight with PatronusAI/glider__8
- [Experiment 1741](details/experiment_1741.md) - Comparing openweight with PatronusAI/glider__9
- [Experiment 1742](details/experiment_1742.md) - Comparing openweight with PatronusAI/glider__10
- [Experiment 1743](details/experiment_1743.md) - Comparing openweight with PatronusAI/glider__11
- [Experiment 1744](details/experiment_1744.md) - Comparing openweight with PatronusAI/glider__12
- [Experiment 1745](details/experiment_1745.md) - Comparing openweight with PatronusAI/glider__13
- [Experiment 1746](details/experiment_1746.md) - Comparing openweight with PatronusAI/glider__14
- [Experiment 1747](details/experiment_1747.md) - Comparing openweight with PatronusAI/glider__15
- [Experiment 1748](details/experiment_1748.md) - Comparing openweight with PatronusAI/glider__16
- [Experiment 1749](details/experiment_1749.md) - Comparing openweight with PatronusAI/glider__17
- [Experiment 1750](details/experiment_1750.md) - Comparing openweight with PatronusAI/glider__18
- [Experiment 1751](details/experiment_1751.md) - Comparing openweight with PatronusAI/glider__19
- [Experiment 1752](details/experiment_1752.md) - Comparing openweight with PatronusAI/glider__20
- [Experiment 1753](details/experiment_1753.md) - Comparing openweight with PatronusAI/glider__21
- [Experiment 1754](details/experiment_1754.md) - Comparing openweight with PatronusAI/glider__22
- [Experiment 1755](details/experiment_1755.md) - Comparing openweight with PatronusAI/glider__23
