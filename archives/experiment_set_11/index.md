---
id: 11
name: "Wikipedia_Frames_150"
date: 2025-02-28T14:02:46.341013
description: ""
tags: []
---

# Experiment Set: Wikipedia_Frames_150 (ID: 11)

Compare DeepSearch on Rag, vannilla models on complex dataset.

**Finished**: 88%

## Scores

**Dataset**: WikipediaFrames_150 (Size: 150)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics

| model                                     |   answer_relevancy |   judge_exactness |   judge_notator |   output_length |
|:------------------------------------------|-------------------:|------------------:|----------------:|----------------:|
| DeepSearch-Llama3.1-8B-70Bredactor        |           0.724747 |          0.38255  |         4.7651  |         4.5906  |
| DeepSearch-Llama3.1-8B-70BRedactor(5,5,3) |           0.776228 |          0.433333 |         4.74    |         3.70667 |
| DeepSearch-Llama3.1-8B                    |           0.717989 |          0.26     |         3.66    |        26.1467  |
| deepsearch_8B(3.1)70B(3.3)-web_3_3_3      |           0.72761  |          0.265487 |         3.625   |         4.39823 |
| DeepSeek-R1-Distill-Qwen-32B              |           0.745139 |          0.275    |         3.15    |         3.42857 |
| Llama-3.3-70B-Instruct                    |           0.799845 |          0.147287 |         2.48462 |         3.75194 |


**Support**: the numbers of item on which the metrics is computed (total items = 150)

| model                                     |   answer_relevancy_support |   judge_exactness_support |   judge_notator_support |   output_length_support |
|:------------------------------------------|---------------------------:|--------------------------:|------------------------:|------------------------:|
| DeepSearch-Llama3.1-8B-70Bredactor        |                        132 |                       149 |                     149 |                     149 |
| DeepSearch-Llama3.1-8B-70BRedactor(5,5,3) |                        128 |                       150 |                     150 |                     150 |
| DeepSearch-Llama3.1-8B                    |                        150 |                       150 |                     150 |                     150 |
| deepsearch_8B(3.1)70B(3.3)-web_3_3_3      |                        112 |                       113 |                     112 |                     113 |
| DeepSeek-R1-Distill-Qwen-32B              |                        120 |                       120 |                     120 |                     119 |
| Llama-3.3-70B-Instruct                    |                        129 |                       129 |                     130 |                     129 |



## Set Overview

|   Id | Name                                 | Dataset             | Model                                     | Model params   | Status          | Created at                 |   Num try |   Num success |
|-----:|:-------------------------------------|:--------------------|:------------------------------------------|:---------------|:----------------|:---------------------------|----------:|--------------:|
|  272 | DeepSearch-Llama3.1-8B-70Bredactor   | WikipediaFrames_150 | DeepSearch-Llama3.1-8B-70Bredactor        | {}             | running_metrics | 2025-02-28T14:02:46.341013 |       150 |           150 |
|  273 | DeepSeek-R1-Distill-Qwen-32B         | WikipediaFrames_150 | DeepSeek-R1-Distill-Qwen-32B              | {}             | running_metrics | 2025-02-28T14:02:46.341013 |       150 |           150 |
|  274 | Llama-3.3-70B-Instruct               | WikipediaFrames_150 | Llama-3.3-70B-Instruct                    | {}             | running_metrics | 2025-02-28T14:02:46.341013 |       150 |           150 |
|  275 | DeepSearch-Llama3.1-8B               | WikipediaFrames_150 | DeepSearch-Llama3.1-8B                    | {}             | finished        | 2025-03-04T10:45:10.415861 |       150 |           150 |
|  276 | DeepSearch-Llama3.1-8B-70BRedactor   | WikipediaFrames_150 | DeepSearch-Llama3.1-8B-70BRedactor(5,5,3) | {}             | running_metrics | 2025-03-04T12:55:38.792059 |       150 |           150 |
|  281 | deepsearch_8B(3.1)70B(3.3)-web_3_3_3 | WikipediaFrames_150 | deepsearch_8B(3.1)70B(3.3)-web_3_3_3      | {}             | running_metrics | 2025-03-05T15:48:02.964336 |       150 |           150 |


## Details by Experiment

- [Experiment 272](details/experiment_272.md) - DeepSearch-Llama3.1-8B-70Bredactor
- [Experiment 273](details/experiment_273.md) - DeepSeek-R1-Distill-Qwen-32B
- [Experiment 274](details/experiment_274.md) - Llama-3.3-70B-Instruct
- [Experiment 275](details/experiment_275.md) - DeepSearch-Llama3.1-8B
- [Experiment 276](details/experiment_276.md) - DeepSearch-Llama3.1-8B-70BRedactor
- [Experiment 281](details/experiment_281.md) - deepsearch_8B(3.1)70B(3.3)-web_3_3_3
