---
id: 12
name: "MMLU_Pro_140"
date: 2025-03-05T11:19:07.967701
description: ""
tags: []
---

# Experiment Set: MMLU_Pro_140 (ID: 12)

Compare DeepSearch on Rag, vannilla models on complex general dataset.

**Finished**: 81%

## Scores

**Dataset**: MMLU_Pro_140 (Size: 140)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                            |   answer_relevancy |   judge_exactness |   judge_notator |   output_length |
|:---------------------------------|-------------------:|------------------:|----------------:|----------------:|
| DeepSeek-R1-Distill-Qwen-32B     |           0.955645 |          0.425373 |         5.52985 |         6.91791 |
| deepsearch_8B(3.1)70B(3.3)_3_3_3 |           0.92381  |          0.361905 |         4.84762 |         4.47619 |
| Llama-3.3-70B-Instruct           |           0.907937 |          0.27619  |         4.64762 |         2.34286 |


**Support**: the numbers of item on which the metrics is computed (total items = 140)

| model                            |   answer_relevancy_support |   judge_exactness_support |   judge_notator_support |   output_length_support |
|:---------------------------------|---------------------------:|--------------------------:|------------------------:|------------------------:|
| DeepSeek-R1-Distill-Qwen-32B     |                        124 |                       134 |                     134 |                     134 |
| deepsearch_8B(3.1)70B(3.3)_3_3_3 |                        105 |                       105 |                     105 |                     105 |
| Llama-3.3-70B-Instruct           |                        105 |                       105 |                     105 |                     105 |



## Set Overview

|   Id | Name                             | Dataset      | Model                            | Model params   | Status          | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------|:-------------|:---------------------------------|:---------------|:----------------|:---------------------------|----------:|--------------:|
|  277 | DeepSeek-R1-Distill-Qwen-32B     | MMLU_Pro_140 | DeepSeek-R1-Distill-Qwen-32B     | {}             | running_metrics | 2025-03-05T11:22:01.936558 |       140 |           140 |
|  279 | Llama-3.3-70B-Instruct           | MMLU_Pro_140 | Llama-3.3-70B-Instruct           | {}             | running_metrics | 2025-03-05T12:21:51.543946 |       140 |           140 |
|  280 | deepsearch_8B(3.1)70B(3.3)_3_3_3 | MMLU_Pro_140 | deepsearch_8B(3.1)70B(3.3)_3_3_3 | {}             | running_metrics | 2025-03-05T14:01:59.463628 |       140 |           140 |


## Details by Experiment

- [Experiment 277](details/experiment_277.md) - DeepSeek-R1-Distill-Qwen-32B
- [Experiment 279](details/experiment_279.md) - Llama-3.3-70B-Instruct
- [Experiment 280](details/experiment_280.md) - deepsearch_8B(3.1)70B(3.3)_3_3_3
