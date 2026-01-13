---
id: 77
name: "analyse_prompt_test-prompt_20251006_120630"
date: 2025-10-06T12:06:30.154067
description: ""
tags: []
---

# Experiment Set: analyse_prompt_test-prompt_20251006_120630 (ID: 77)

Baseline prompt

**Finished**: 90%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model        | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   | judge_precision   | nb_tokens_completion   | nb_tokens_prompt   |
|:-------------|:---------------------|:------------------|:------------------|:----------------|:------------------|:-----------------------|:-------------------|
| albert-large | 0.0025 ± 0.0006      | 30.2 ± 5.41       | 0.0002 ± 0.0001   | 4.56 ± 0.04     | 0.21 ± 0.04       | 213.62 ± 54.58         | 3619.55 ± 6.67     |
| albert-small | 0.0007 ± 0.0001      | 14.62 ± 1.79      | 0.0001 ± 0.0      | 2.92 ± 0.24     | 0.03 ± 0.02       | 220.22 ± 26.99         | 3630.12 ± 16.65    |


**Support**: the numbers of item on which the metrics is computed (total items = 46)

| model        | energy_consumption_support   | generation_time_support   | gwp_consumption_support   | judge_notator_support   | judge_precision_support   | nb_tokens_completion_support   | nb_tokens_prompt_support   |
|:-------------|:-----------------------------|:--------------------------|:--------------------------|:------------------------|:--------------------------|:-------------------------------|:---------------------------|
| albert-large | 39.5 ± 2.12                  | 39.5 ± 2.12               | 39.5 ± 2.12               | 39.5 ± 2.12             | 39.5 ± 2.12               | 39.5 ± 2.12                    | 39.5 ± 2.12                |
| albert-small | 44.0 ± 1.41                  | 44.0 ± 1.41               | 44.0 ± 1.41               | 44.0 ± 1.41             | 44.0 ± 1.41               | 44.0 ± 1.41                    | 44.0 ± 1.41                |



## Set Overview

|   Id | Name                                          | Dataset           | Model        | Model params                                                                                                                     | Status   | Created at                 |   Num try |   Num success |
|-----:|:----------------------------------------------|:------------------|:-------------|:---------------------------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1434 | analyse_prompt_test-prompt_20251006_120630__0 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784], 'k': 10}, 'sys_prompt': '5acf'} | finished | 2025-10-06T12:06:30.154067 |        46 |            38 |
| 1435 | analyse_prompt_test-prompt_20251006_120630__1 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784], 'k': 10}, 'sys_prompt': 'c2cd'} | finished | 2025-10-06T12:06:30.154067 |        46 |            41 |
| 1436 | analyse_prompt_test-prompt_20251006_120630__2 | Assistant IA - QA | albert-small | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784], 'k': 10}, 'sys_prompt': '5acf'} | finished | 2025-10-06T12:06:30.154067 |        46 |            45 |
| 1437 | analyse_prompt_test-prompt_20251006_120630__3 | Assistant IA - QA | albert-small | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784], 'k': 10}, 'sys_prompt': 'c2cd'} | finished | 2025-10-06T12:06:30.154067 |        46 |            43 |


## Details by Experiment

- [Experiment 1434](details/experiment_1434.md) - analyse_prompt_test-prompt_20251006_120630__0
- [Experiment 1435](details/experiment_1435.md) - analyse_prompt_test-prompt_20251006_120630__1
- [Experiment 1436](details/experiment_1436.md) - analyse_prompt_test-prompt_20251006_120630__2
- [Experiment 1437](details/experiment_1437.md) - analyse_prompt_test-prompt_20251006_120630__3
