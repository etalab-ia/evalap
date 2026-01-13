---
id: 33
name: "mfs_tooling_v1"
date: 2025-04-09T15:18:04.018668
description: ""
tags: []
---

# Experiment Set: mfs_tooling_v1 (ID: 33)

Evaluating tooling capabilities.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | contextual_relevancy   | faithfulness   | generation_time   | judge_exactness   | judge_notator   | nb_tool_calls   | output_length   | ragas       |
|:----------------------------------------------|:-----------------------|:---------------|:------------------|:------------------|:----------------|:----------------|:----------------|:------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 0.35 ± 0.04            | 0.94 ± 0.03    | 28.74 ± 18.0      | 0.07 ± 0.03       | 5.55 ± 0.28     | 0.16 ± 0.12     | 307.45 ± 41.09  | 0.47 ± 0.07 |
| meta-llama/Llama-3.1-8B-Instruct              | 0.44 ± 0.03            | 0.92 ± 0.02    | 5.52 ± 2.28       | 0.06 ± 0.03       | 4.43 ± 0.46     | 0.7 ± 0.46      | 179.69 ± 74.22  | 0.51 ± 0.06 |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                         | contextual_relevancy_support   | faithfulness_support   |   generation_time_support |   judge_exactness_support |   judge_notator_support |   nb_tool_calls_support |   output_length_support | ragas_support   |
|:----------------------------------------------|:-------------------------------|:-----------------------|--------------------------:|--------------------------:|------------------------:|------------------------:|------------------------:|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 9.38 ± 1.06                    | 9.38 ± 1.06            |                        39 |                        39 |                      39 |                      39 |                      39 | 5.5 ± 1.2       |
| meta-llama/Llama-3.1-8B-Instruct              | 35.0 ± 1.63                    | 35.0 ± 1.63            |                        39 |                        39 |                      39 |                      39 |                      39 | 16.9 ± 3.67     |



## Set Overview

|   Id | Name               | Dataset           | Model                                         | Model params                                                      | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------|:------------------|:----------------------------------------------|:------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  628 | mfs_tooling_v0__0  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  629 | mfs_tooling_v0__1  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  630 | mfs_tooling_v0__2  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  631 | mfs_tooling_v0__3  | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  632 | mfs_tooling_v0__4  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  633 | mfs_tooling_v0__5  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  634 | mfs_tooling_v0__6  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  635 | mfs_tooling_v0__7  | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                                              | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  640 | mfs_tooling_v0__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  641 | mfs_tooling_v0__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  642 | mfs_tooling_v0__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  643 | mfs_tooling_v0__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  648 | mfs_tooling_v0__20 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  649 | mfs_tooling_v0__21 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  650 | mfs_tooling_v0__22 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  651 | mfs_tooling_v0__23 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v2']} | finished | 2025-04-09T15:18:04.018668 |        39 |            39 |
|  652 | mfs_tooling_v0__16 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:06:10.930051 |        39 |            39 |
|  653 | mfs_tooling_v0__18 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:06:11.032059 |        39 |            39 |
|  657 | mfs_tooling_v1__18 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.158200 |        39 |            39 |
|  658 | mfs_tooling_v1__20 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.226973 |        39 |            39 |
|  659 | mfs_tooling_v1__22 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.283168 |        39 |            39 |
|  660 | mfs_tooling_v1__24 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.331802 |        39 |            39 |
|  661 | mfs_tooling_v1__26 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.381122 |        39 |            39 |
|  662 | mfs_tooling_v1__28 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.433266 |        39 |            39 |
|  663 | mfs_tooling_v1__30 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.486431 |        39 |            39 |
|  664 | mfs_tooling_v1__32 | MFS_questions_v01 | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, '_tools_': ['search_albert_collections_v1']} | finished | 2025-04-09T18:09:19.543834 |        39 |            39 |


## Details by Experiment

- [Experiment 628](details/experiment_628.md) - mfs_tooling_v0__0
- [Experiment 629](details/experiment_629.md) - mfs_tooling_v0__1
- [Experiment 630](details/experiment_630.md) - mfs_tooling_v0__2
- [Experiment 631](details/experiment_631.md) - mfs_tooling_v0__3
- [Experiment 632](details/experiment_632.md) - mfs_tooling_v0__4
- [Experiment 633](details/experiment_633.md) - mfs_tooling_v0__5
- [Experiment 634](details/experiment_634.md) - mfs_tooling_v0__6
- [Experiment 635](details/experiment_635.md) - mfs_tooling_v0__7
- [Experiment 640](details/experiment_640.md) - mfs_tooling_v0__12
- [Experiment 641](details/experiment_641.md) - mfs_tooling_v0__13
- [Experiment 642](details/experiment_642.md) - mfs_tooling_v0__14
- [Experiment 643](details/experiment_643.md) - mfs_tooling_v0__15
- [Experiment 648](details/experiment_648.md) - mfs_tooling_v0__20
- [Experiment 649](details/experiment_649.md) - mfs_tooling_v0__21
- [Experiment 650](details/experiment_650.md) - mfs_tooling_v0__22
- [Experiment 651](details/experiment_651.md) - mfs_tooling_v0__23
- [Experiment 652](details/experiment_652.md) - mfs_tooling_v0__16
- [Experiment 653](details/experiment_653.md) - mfs_tooling_v0__18
- [Experiment 657](details/experiment_657.md) - mfs_tooling_v1__18
- [Experiment 658](details/experiment_658.md) - mfs_tooling_v1__20
- [Experiment 659](details/experiment_659.md) - mfs_tooling_v1__22
- [Experiment 660](details/experiment_660.md) - mfs_tooling_v1__24
- [Experiment 661](details/experiment_661.md) - mfs_tooling_v1__26
- [Experiment 662](details/experiment_662.md) - mfs_tooling_v1__28
- [Experiment 663](details/experiment_663.md) - mfs_tooling_v1__30
- [Experiment 664](details/experiment_664.md) - mfs_tooling_v1__32
