---
id: 29
name: "NousResearch/Meta-Llama-3-8B-Instruct_mfs"
date: 2025-04-04T14:02:57.704454
description: ""
tags: []
---

# Experiment Set: NousResearch/Meta-Llama-3-8B-Instruct_mfs (ID: 29)

Experiment set for NousResearch/Meta-Llama-3-8B-Instruct_mfs

**Finished**: 97%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                 | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:--------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| NousResearch/Meta-Llama-3-8B-Instruct | 0.77 ± 0.02        | 3.54 ± 0.04       | 0.01 ± 0.02       | 3.42 ± 0.14     | 305.35 ± 5.46   |
| NousResearch/Meta-Llama-3.1-8B        | 0.6 ± nan          | 13.69 ± nan       | 0.05 ± nan        | 1.87 ± nan      | 1127.67 ± nan   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                 | answer_relevancy_support   | generation_time_support   | judge_exactness_support   | judge_notator_support   | output_length_support   |
|:--------------------------------------|:---------------------------|:--------------------------|:--------------------------|:------------------------|:------------------------|
| NousResearch/Meta-Llama-3-8B-Instruct | 38.5 ± 1.0                 | 37.75 ± 2.5               | 37.75 ± 2.5               | 37.75 ± 2.5             | 37.75 ± 2.5             |
| NousResearch/Meta-Llama-3.1-8B        | 39.0 ± nan                 | 39.0 ± nan                | 39.0 ± nan                | 39.0 ± nan              | 39.0 ± nan              |



## Set Overview

|   Id | Name                                         | Dataset           | Model                                 | Model params   | Status          | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------------------|:------------------|:--------------------------------------|:---------------|:----------------|:---------------------------|----------:|--------------:|
|  575 | mfs_nousresearch__0                          | MFS_questions_v01 | NousResearch/Meta-Llama-3.1-8B        | {}             | finished        | 2025-04-04T14:02:57.704454 |        39 |            39 |
|  576 | NousResearch/Meta-Llama-3-8B-Instruct_mfs__1 | MFS_questions_v01 | NousResearch/Meta-Llama-3-8B-Instruct | {}             | finished        | 2025-04-04T15:37:56.874343 |        39 |            39 |
|  577 | NousResearch/Meta-Llama-3-8B-Instruct_mfs__3 | MFS_questions_v01 | NousResearch/Meta-Llama-3-8B-Instruct | {}             | finished        | 2025-04-04T15:37:59.239339 |        39 |            39 |
|  578 | NousResearch/Meta-Llama-3-8B-Instruct_mfs__5 | MFS_questions_v01 | NousResearch/Meta-Llama-3-8B-Instruct | {}             | finished        | 2025-04-04T15:38:01.068381 |        39 |            39 |
|  579 | NousResearch/Meta-Llama-3-8B-Instruct_mfs__7 | MFS_questions_v01 | NousResearch/Meta-Llama-3-8B-Instruct | {}             | running_metrics | 2025-04-04T15:38:02.616130 |        39 |            39 |


## Details by Experiment

- [Experiment 575](details/experiment_575.md) - mfs_nousresearch__0
- [Experiment 576](details/experiment_576.md) - NousResearch/Meta-Llama-3-8B-Instruct_mfs__1
- [Experiment 577](details/experiment_577.md) - NousResearch/Meta-Llama-3-8B-Instruct_mfs__3
- [Experiment 578](details/experiment_578.md) - NousResearch/Meta-Llama-3-8B-Instruct_mfs__5
- [Experiment 579](details/experiment_579.md) - NousResearch/Meta-Llama-3-8B-Instruct_mfs__7
