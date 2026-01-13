---
id: 8
name: "mfs_RAG_metrics_v1"
date: 2024-12-15T14:41:26.024831
description: ""
tags: []
---

# Experiment Set: mfs_RAG_metrics_v1 (ID: 8)

Evaluation of baseline models with RAG metrics (retriever_context).

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                     | contextual_precision   | contextual_recall   | contextual_relevancy   | ragas       |
|:------------------------------------------|:-----------------------|:--------------------|:-----------------------|:------------|
| AgentPublic/llama3-instruct-8b            | 0.56 ± 0.02            | 0.68 ± 0.01         | 0.33 ± 0.01            | 0.56 ± 0.02 |
| AgentPublic/llama3-instruct-guillaumetell | 0.56 ± 0.02            | 0.68 ± 0.03         | 0.35 ± 0.0             | 0.55 ± 0.06 |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                                     |   contextual_precision_support |   contextual_recall_support |   contextual_relevancy_support | ragas_support   |
|:------------------------------------------|-------------------------------:|----------------------------:|-------------------------------:|:----------------|
| AgentPublic/llama3-instruct-8b            |                             39 |                          39 |                             39 | 23.67 ± 1.53    |
| AgentPublic/llama3-instruct-guillaumetell |                             39 |                          39 |                             39 | 19.33 ± 1.53    |



## Set Overview

|   Id | Name                     | Dataset           | Model                                     | Model params                                             | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------------|:------------------|:------------------------------------------|:---------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  148 | mfs_RAG_metrics_v1__0    | MFS_questions_v01 | AgentPublic/llama3-instruct-8b            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-15T14:41:26.024831 |        39 |            39 |
|  149 | mfs_RAG_metrics_v1__1    | MFS_questions_v01 | AgentPublic/llama3-instruct-8b            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-15T14:41:26.024831 |        39 |            39 |
|  150 | mfs_RAG_metrics_v1__2    | MFS_questions_v01 | AgentPublic/llama3-instruct-8b            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-15T14:41:26.024831 |        39 |            39 |
|  151 | mfs_GT_RAG_metrics_v1__1 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-17T15:11:48.551939 |        39 |            39 |
|  152 | mfs_GT_RAG_metrics_v1__2 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-17T15:11:48.664978 |        39 |            39 |
|  153 | mfs_GT_RAG_metrics_v1__3 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2024-12-17T15:11:48.932941 |        39 |            39 |


## Details by Experiment

- [Experiment 148](details/experiment_148.md) - mfs_RAG_metrics_v1__0
- [Experiment 149](details/experiment_149.md) - mfs_RAG_metrics_v1__1
- [Experiment 150](details/experiment_150.md) - mfs_RAG_metrics_v1__2
- [Experiment 151](details/experiment_151.md) - mfs_GT_RAG_metrics_v1__1
- [Experiment 152](details/experiment_152.md) - mfs_GT_RAG_metrics_v1__2
- [Experiment 153](details/experiment_153.md) - mfs_GT_RAG_metrics_v1__3
