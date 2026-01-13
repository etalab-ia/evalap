---
id: 115
name: "Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B"
date: 2025-12-18T15:38:02.218822
description: ""
tags: []
---

# Experiment Set: Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B (ID: 115)

Comparing openweight Albert-API with specific judge AtlaAI/Selene-1-Mini-Llama-3.1-8B

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: AtlaAI/Selene-1-Mini-Llama-3.1-8B

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.017 ± 0.0006       | 13.78 ± 0.75      | 0.0014 ± 0.0      | 7.91 ± 0.04     | 0.21 ± 0.03       | 1780.77 ± 62.47        |               38.9 |
| Mistral small              | 0.0029 ± 0.0         | 10.93 ± 0.26      | 0.0003 ± 0.0      | 7.77 ± 0.1      | 0.19 ± 0.04       | 453.78 ± 8.64          |               38.9 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0037 ± 0.0002      | 6.51 ± 0.34       | 0.0003 ± 0.0      | 7.88 ± 0.08     | 0.15 ± 0.06       | 1389.65 ± 67.8         |               38.9 |


**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: AtlaAI/Selene-1-Mini-Llama-3.1-8B

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                      | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   |   nb_tokens_prompt |
|:---------------------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|-------------------:|
| openai/gpt-oss-120b Albert | 0.0113 ± 0.0002      | 9.56 ± 0.17       | 0.001 ± 0.0       | 7.66 ± 0.11     | 0.19 ± 0.02       | 1186.32 ± 20.73        |              29.59 |
| Qwen/Qwen3-VL-8B-Thinking  | 0.0028 ± 0.0001      | 4.8 ± 0.19        | 0.0002 ± 0.0      | 7.67 ± 0.13     | 0.18 ± 0.03       | 1036.54 ± 35.74        |              29.59 |
| Mistral small              | 0.0022 ± 0.0001      | 7.86 ± 0.46       | 0.0002 ± 0.0      | 7.57 ± 0.12     | 0.16 ± 0.03       | 342.87 ± 9.86          |              29.59 |



## Set Overview

|   Id | Name                                                            | Dataset           | Model                      | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:----------------------------------------------------------------|:------------------|:---------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1760 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__0  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1761 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__1  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1762 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__2  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1763 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__3  | Assistant IA - QA | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1764 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__4  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1765 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__5  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1766 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__6  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1767 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__7  | Assistant IA - QA | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1768 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__8  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1769 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__9  | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1770 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__10 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1771 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__11 | Assistant IA - QA | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        46 |            46 |
| 1772 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__12 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1773 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__13 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1774 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__14 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1775 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__15 | MFS_questions_v01 | Qwen/Qwen3-VL-8B-Thinking  | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1776 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__16 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1777 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__17 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1778 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__18 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1779 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__19 | MFS_questions_v01 | Mistral small              | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1780 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__20 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1781 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__21 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1782 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__22 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |
| 1783 | Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__23 | MFS_questions_v01 | openai/gpt-oss-120b Albert | {'temperature': 0.2, 'sys_prompt': 'c9f3'} | finished | 2025-12-18T15:38:02.218822 |        39 |            39 |


## Details by Experiment

- [Experiment 1760](details/experiment_1760.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__0
- [Experiment 1761](details/experiment_1761.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__1
- [Experiment 1762](details/experiment_1762.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__2
- [Experiment 1763](details/experiment_1763.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__3
- [Experiment 1764](details/experiment_1764.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__4
- [Experiment 1765](details/experiment_1765.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__5
- [Experiment 1766](details/experiment_1766.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__6
- [Experiment 1767](details/experiment_1767.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__7
- [Experiment 1768](details/experiment_1768.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__8
- [Experiment 1769](details/experiment_1769.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__9
- [Experiment 1770](details/experiment_1770.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__10
- [Experiment 1771](details/experiment_1771.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__11
- [Experiment 1772](details/experiment_1772.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__12
- [Experiment 1773](details/experiment_1773.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__13
- [Experiment 1774](details/experiment_1774.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__14
- [Experiment 1775](details/experiment_1775.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__15
- [Experiment 1776](details/experiment_1776.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__16
- [Experiment 1777](details/experiment_1777.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__17
- [Experiment 1778](details/experiment_1778.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__18
- [Experiment 1779](details/experiment_1779.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__19
- [Experiment 1780](details/experiment_1780.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__20
- [Experiment 1781](details/experiment_1781.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__21
- [Experiment 1782](details/experiment_1782.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__22
- [Experiment 1783](details/experiment_1783.md) - Comparing openweight with AtlaAI/Selene-1-Mini-Llama-3.1-8B__23
