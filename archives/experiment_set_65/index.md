---
id: 65
name: "albert-api-rag-mfs-v1"
date: 2025-06-28T23:54:54.633239
description: ""
tags: []
---

# Experiment Set: albert-api-rag-mfs-v1 (ID: 65)

Evaluating hybrid search on MFS dataset.

**Finished**: 99%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                 | generation_time   | judge_precision   | output_length   |
|:----------------------|:------------------|:------------------|:----------------|
| albert-large-semantic | 14.05 ± 1.84      | 0.46 ± 0.13       | 309.41 ± 31.38  |
| albert-large          | 14.78 ± 0.35      | 0.3 ± 0.05        | 363.52 ± 8.02   |


**Support**: the numbers of item on which the metrics is computed (total items = 39)

| model                 | generation_time_support   | judge_precision_support   | output_length_support   |
|:----------------------|:--------------------------|:--------------------------|:------------------------|
| albert-large-semantic | 39.0 ± 0.0                | 39.0 ± 0.0                | 39.0 ± 0.0              |
| albert-large          | 38.8 ± 0.45               | 38.8 ± 0.45               | 38.8 ± 0.45             |



## Set Overview

|   Id | Name                      | Dataset           | Model                 | Model params                                                                                                    | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------|:------------------|:----------------------|:----------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1247 | albert-api-rag-mfs-v1__0  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1248 | albert-api-rag-mfs-v1__1  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1249 | albert-api-rag-mfs-v1__2  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1250 | albert-api-rag-mfs-v1__3  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1251 | albert-api-rag-mfs-v1__4  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1252 | albert-api-rag-mfs-v1__5  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [17, 18], 'k': 10}}   | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1253 | albert-api-rag-mfs-v1__6  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [17, 18], 'k': 10}}   | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1254 | albert-api-rag-mfs-v1__7  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [17, 18], 'k': 10}}   | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1255 | albert-api-rag-mfs-v1__8  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [17, 18], 'k': 10}}   | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1256 | albert-api-rag-mfs-v1__9  | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [17, 18], 'k': 10}}   | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1257 | albert-api-rag-mfs-v1__10 | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [17, 18], 'k': 10}}     | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1258 | albert-api-rag-mfs-v1__11 | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [17, 18], 'k': 10}}     | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1259 | albert-api-rag-mfs-v1__12 | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [17, 18], 'k': 10}}     | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1260 | albert-api-rag-mfs-v1__13 | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [17, 18], 'k': 10}}     | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1261 | albert-api-rag-mfs-v1__14 | MFS_questions_v01 | albert-large-semantic | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [17, 18], 'k': 10}}     | finished | 2025-06-28T23:54:54.633239 |        39 |            39 |
| 1262 | albert-api-rag-mfs-v1__15 | MFS_questions_v01 | albert-large          | {'temperature': 0.2}                                                                                            | finished | 2025-06-29T00:26:41.214710 |        39 |            39 |
| 1263 | albert-api-rag-mfs-v1__17 | MFS_questions_v01 | albert-large          | {'temperature': 0.2}                                                                                            | finished | 2025-06-29T00:26:41.290189 |        39 |            39 |
| 1264 | albert-api-rag-mfs-v1__19 | MFS_questions_v01 | albert-large          | {'temperature': 0.2}                                                                                            | finished | 2025-06-29T00:26:41.344173 |        39 |            38 |
| 1265 | albert-api-rag-mfs-v1__21 | MFS_questions_v01 | albert-large          | {'temperature': 0.2}                                                                                            | finished | 2025-06-29T00:26:41.402320 |        39 |            39 |
| 1266 | albert-api-rag-mfs-v1__23 | MFS_questions_v01 | albert-large          | {'temperature': 0.2}                                                                                            | finished | 2025-06-29T00:26:41.457379 |        39 |            39 |


## Details by Experiment

- [Experiment 1247](details/experiment_1247.md) - albert-api-rag-mfs-v1__0
- [Experiment 1248](details/experiment_1248.md) - albert-api-rag-mfs-v1__1
- [Experiment 1249](details/experiment_1249.md) - albert-api-rag-mfs-v1__2
- [Experiment 1250](details/experiment_1250.md) - albert-api-rag-mfs-v1__3
- [Experiment 1251](details/experiment_1251.md) - albert-api-rag-mfs-v1__4
- [Experiment 1252](details/experiment_1252.md) - albert-api-rag-mfs-v1__5
- [Experiment 1253](details/experiment_1253.md) - albert-api-rag-mfs-v1__6
- [Experiment 1254](details/experiment_1254.md) - albert-api-rag-mfs-v1__7
- [Experiment 1255](details/experiment_1255.md) - albert-api-rag-mfs-v1__8
- [Experiment 1256](details/experiment_1256.md) - albert-api-rag-mfs-v1__9
- [Experiment 1257](details/experiment_1257.md) - albert-api-rag-mfs-v1__10
- [Experiment 1258](details/experiment_1258.md) - albert-api-rag-mfs-v1__11
- [Experiment 1259](details/experiment_1259.md) - albert-api-rag-mfs-v1__12
- [Experiment 1260](details/experiment_1260.md) - albert-api-rag-mfs-v1__13
- [Experiment 1261](details/experiment_1261.md) - albert-api-rag-mfs-v1__14
- [Experiment 1262](details/experiment_1262.md) - albert-api-rag-mfs-v1__15
- [Experiment 1263](details/experiment_1263.md) - albert-api-rag-mfs-v1__17
- [Experiment 1264](details/experiment_1264.md) - albert-api-rag-mfs-v1__19
- [Experiment 1265](details/experiment_1265.md) - albert-api-rag-mfs-v1__21
- [Experiment 1266](details/experiment_1266.md) - albert-api-rag-mfs-v1__23
