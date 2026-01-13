---
id: 85
name: "analyse_prompt_Prompt_no_20251104_114039"
date: 2025-11-04T11:40:39.884116
description: ""
tags: []
---

# Experiment Set: analyse_prompt_Prompt_no_20251104_114039 (ID: 85)

Baseline prompt

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model        | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   | nb_tokens_prompt   |
|:-------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|:-------------------|
| albert-large | 0.0051 ± 0.0013      | 16.43 ± 5.6       | 0.0005 ± 0.0001   | 4.43 ± 0.44     | 0.23 ± 0.01       | 474.98 ± 119.0         | 2901.34 ± 18.98    |



## Set Overview

|   Id | Name                                        | Dataset           | Model        | Model params                                                                                                                     | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------------------|:------------------|:-------------|:---------------------------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1479 | analyse_prompt_Prompt_no_20251104_114039__0 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [785], 'k': 10}, 'sys_prompt': '037a'} | finished | 2025-11-04T11:40:39.884116 |        46 |            46 |
| 1480 | analyse_prompt_Prompt_no_20251104_114039__1 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [785], 'k': 10}, 'sys_prompt': '3672'} | finished | 2025-11-04T11:40:39.884116 |        46 |            46 |
| 1481 | analyse_prompt_Prompt_no_20251104_114039__2 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [785], 'k': 10}, 'sys_prompt': 'ead2'} | finished | 2025-11-04T11:40:39.884116 |        46 |            46 |


## Details by Experiment

- [Experiment 1479](details/experiment_1479.md) - analyse_prompt_Prompt_no_20251104_114039__0
- [Experiment 1480](details/experiment_1480.md) - analyse_prompt_Prompt_no_20251104_114039__1
- [Experiment 1481](details/experiment_1481.md) - analyse_prompt_Prompt_no_20251104_114039__2
