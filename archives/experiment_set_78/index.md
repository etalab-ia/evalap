---
id: 78
name: "analyse_prompt_Assistant IA_20251006_175310"
date: 2025-10-06T17:53:10.112456
description: ""
tags: []
---

# Experiment Set: analyse_prompt_Assistant IA_20251006_175310 (ID: 78)

Baseline prompt

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model        | energy_consumption   | generation_time   | gwp_consumption   | judge_notator   |   judge_precision | nb_tokens_completion   | nb_tokens_prompt   |
|:-------------|:---------------------|:------------------|:------------------|:----------------|------------------:|:-----------------------|:-------------------|
| albert-large | 0.003 ± 0.0001       | 9.65 ± 0.12       | 0.0003 ± 0.0      | 5.51 ± 0.26     |              0.33 | 287.54 ± 10.94         | 1321.36 ± 11.54    |



## Set Overview

|   Id | Name                                           | Dataset           | Model        | Model params                                                                                                                     | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------------------------|:------------------|:-------------|:---------------------------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1438 | analyse_prompt_Assistant IA_20251006_175310__0 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [783], 'k': 10}, 'sys_prompt': '6bd5'} | finished | 2025-10-06T17:53:10.112456 |        46 |            46 |
| 1439 | analyse_prompt_Assistant IA_20251006_175310__1 | Assistant IA - QA | albert-large | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [783], 'k': 10}, 'sys_prompt': '4702'} | finished | 2025-10-06T17:53:10.112456 |        46 |            46 |


## Details by Experiment

- [Experiment 1438](details/experiment_1438.md) - analyse_prompt_Assistant IA_20251006_175310__0
- [Experiment 1439](details/experiment_1439.md) - analyse_prompt_Assistant IA_20251006_175310__1
