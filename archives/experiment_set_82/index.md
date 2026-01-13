---
id: 82
name: "Compare albert-small with apertus-small models"
date: 2025-10-30T15:54:31.379647
description: ""
tags: []
---

# Experiment Set: Compare albert-small with apertus-small models (ID: 82)

Comparing albert-small model with apertus-small model alone, and in a RAG setting with service-public + travail-emploi sheets, on a french administration Q/A datasets

**Finished**: 100%

## Scores

**Dataset**: Assistant IA - QA (Size: 46)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                             |   generation_time |   judge_precision |   output_length |
|:----------------------------------|------------------:|------------------:|----------------:|
| meta-llama/Llama-3.1-8B-Instruct  |              8.09 |              0.13 |          234.74 |
| albert-small-rag                  |              5.37 |              0.07 |          179.96 |
| swiss-ai/Apertus-8B-Instruct-2509 |              2.2  |              0.07 |          135.43 |
| apertus-small-rag                 |              2.15 |              0.04 |          125.85 |


**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                             |   generation_time |   judge_precision |   output_length |
|:----------------------------------|------------------:|------------------:|----------------:|
| albert-small-rag                  |              8.36 |              0.41 |          259.92 |
| apertus-small-rag                 |              3.1  |              0.1  |          200.51 |
| meta-llama/Llama-3.1-8B-Instruct  |              6.79 |              0.05 |          298.03 |
| swiss-ai/Apertus-8B-Instruct-2509 |              3.26 |              0.05 |          200.36 |



## Set Overview

|   Id | Name                                               | Dataset           | Model                             | Model params                                                                                                    | Status   | Created at                 |   Num try |   Num success |
|-----:|:---------------------------------------------------|:------------------|:----------------------------------|:----------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1452 | Compare aLbert-small with albertus-small models__0 | MFS_questions_v01 | albert-small-rag                  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-10-30T15:54:31.379647 |        39 |            39 |
| 1453 | Compare aLbert-small with albertus-small models__1 | MFS_questions_v01 | apertus-small-rag                 | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished | 2025-10-30T15:54:31.379647 |        39 |            39 |
| 1454 | Compare aLbert-small with albertus-small models__2 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct  | {'temperature': 0.2}                                                                                            | finished | 2025-10-30T15:54:31.379647 |        39 |            39 |
| 1455 | Compare aLbert-small with albertus-small models__3 | MFS_questions_v01 | swiss-ai/Apertus-8B-Instruct-2509 | {'temperature': 0.2}                                                                                            | finished | 2025-10-30T15:54:31.379647 |        39 |            39 |
| 1456 | Compare aLbert-small with albertus-small models__4 | Assistant IA - QA | albert-small-rag                  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-10-30T15:54:31.379647 |        46 |            46 |
| 1457 | Compare aLbert-small with albertus-small models__5 | Assistant IA - QA | apertus-small-rag                 | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [784, 785], 'k': 10}}   | finished | 2025-10-30T15:54:31.379647 |        46 |            46 |
| 1458 | Compare aLbert-small with albertus-small models__6 | Assistant IA - QA | meta-llama/Llama-3.1-8B-Instruct  | {'temperature': 0.2}                                                                                            | finished | 2025-10-30T15:54:31.379647 |        46 |            46 |
| 1459 | Compare aLbert-small with albertus-small models__7 | Assistant IA - QA | swiss-ai/Apertus-8B-Instruct-2509 | {'temperature': 0.2}                                                                                            | finished | 2025-10-30T15:54:31.379647 |        46 |            46 |


## Details by Experiment

- [Experiment 1452](details/experiment_1452.md) - Compare aLbert-small with albertus-small models__0
- [Experiment 1453](details/experiment_1453.md) - Compare aLbert-small with albertus-small models__1
- [Experiment 1454](details/experiment_1454.md) - Compare aLbert-small with albertus-small models__2
- [Experiment 1455](details/experiment_1455.md) - Compare aLbert-small with albertus-small models__3
- [Experiment 1456](details/experiment_1456.md) - Compare aLbert-small with albertus-small models__4
- [Experiment 1457](details/experiment_1457.md) - Compare aLbert-small with albertus-small models__5
- [Experiment 1458](details/experiment_1458.md) - Compare aLbert-small with albertus-small models__6
- [Experiment 1459](details/experiment_1459.md) - Compare aLbert-small with albertus-small models__7
