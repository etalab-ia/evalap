---
id: 68
name: "albert-api-rag-mfs-v3"
date: 2025-08-08T00:19:43.207127
description: ""
tags: []
---

# Experiment Set: albert-api-rag-mfs-v3 (ID: 68)

Evaluating hybrid search on MFS dataset.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                            | generation_time   | judge_precision   | output_length   |
|:---------------------------------|:------------------|:------------------|:----------------|
| albert-large-semantic-qdrant     | 17.47 ± 1.17      | 0.67 ± 0.04       | 338.65 ± 2.86   |
| albert-large-semantic-elastic    | 17.0 ± 0.52       | 0.66 ± 0.05       | 339.15 ± 1.31   |
| albert-large-hybrid-elastic      | 18.45 ± 1.21      | 0.63 ± 0.03       | 334.65 ± 5.31   |
| albert-large-hybrid-web-elastic  | 24.63 ± 1.96      | 0.63 ± 0.01       | 311.96 ± 5.47   |
| albert-large-semantic-web-qdrant | 23.77 ± 2.45      | 0.61 ± 0.03       | 307.49 ± 5.51   |
| albert-large-dry-3.2             | 15.54 ± 0.43      | 0.48 ± 0.03       | 319.35 ± 6.68   |
| albert-large-lexical-elastic     | 16.9 ± 0.79       | 0.48 ± 0.02       | 314.19 ± 10.35  |
| albert-large-dry-3.1             | 15.86 ± 0.71      | 0.46 ± 0.04       | 322.22 ± 6.98   |



## Set Overview

|   Id | Name                      | Dataset           | Model                            | Model params                                                                                                    | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------|:------------------|:---------------------------------|:----------------------------------------------------------------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1293 | albert-api-rag-mfs-v2__0  | MFS_questions_v01 | albert-large-semantic-qdrant     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1294 | albert-api-rag-mfs-v2__1  | MFS_questions_v01 | albert-large-semantic-qdrant     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1295 | albert-api-rag-mfs-v2__2  | MFS_questions_v01 | albert-large-semantic-qdrant     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1296 | albert-api-rag-mfs-v2__3  | MFS_questions_v01 | albert-large-semantic-qdrant     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1297 | albert-api-rag-mfs-v2__4  | MFS_questions_v01 | albert-large-semantic-qdrant     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [784, 785], 'k': 10}} | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1298 | albert-api-rag-mfs-v2__5  | MFS_questions_v01 | albert-large-semantic-elastic    | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [20, 21], 'k': 10}}   | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1299 | albert-api-rag-mfs-v2__6  | MFS_questions_v01 | albert-large-semantic-elastic    | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [20, 21], 'k': 10}}   | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1300 | albert-api-rag-mfs-v2__7  | MFS_questions_v01 | albert-large-semantic-elastic    | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [20, 21], 'k': 10}}   | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1301 | albert-api-rag-mfs-v2__8  | MFS_questions_v01 | albert-large-semantic-elastic    | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [20, 21], 'k': 10}}   | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1302 | albert-api-rag-mfs-v2__9  | MFS_questions_v01 | albert-large-semantic-elastic    | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'collections': [20, 21], 'k': 10}}   | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1303 | albert-api-rag-mfs-v2__10 | MFS_questions_v01 | albert-large-lexical-elastic     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'lexical', 'collections': [20, 21], 'k': 10}}    | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1304 | albert-api-rag-mfs-v2__11 | MFS_questions_v01 | albert-large-lexical-elastic     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'lexical', 'collections': [20, 21], 'k': 10}}    | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1305 | albert-api-rag-mfs-v2__12 | MFS_questions_v01 | albert-large-lexical-elastic     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'lexical', 'collections': [20, 21], 'k': 10}}    | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1306 | albert-api-rag-mfs-v2__13 | MFS_questions_v01 | albert-large-lexical-elastic     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'lexical', 'collections': [20, 21], 'k': 10}}    | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1307 | albert-api-rag-mfs-v2__14 | MFS_questions_v01 | albert-large-lexical-elastic     | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'lexical', 'collections': [20, 21], 'k': 10}}    | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1308 | albert-api-rag-mfs-v2__15 | MFS_questions_v01 | albert-large-hybrid-elastic      | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [20, 21], 'k': 10}}     | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1309 | albert-api-rag-mfs-v2__16 | MFS_questions_v01 | albert-large-hybrid-elastic      | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [20, 21], 'k': 10}}     | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1310 | albert-api-rag-mfs-v2__17 | MFS_questions_v01 | albert-large-hybrid-elastic      | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [20, 21], 'k': 10}}     | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1311 | albert-api-rag-mfs-v2__18 | MFS_questions_v01 | albert-large-hybrid-elastic      | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [20, 21], 'k': 10}}     | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1312 | albert-api-rag-mfs-v2__19 | MFS_questions_v01 | albert-large-hybrid-elastic      | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'collections': [20, 21], 'k': 10}}     | finished | 2025-08-08T00:19:43.207127 |        39 |            39 |
| 1329 | albert-api-rag-mfs-v2__20 | MFS_questions_v01 | albert-large-dry-3.2             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.591662 |        39 |            39 |
| 1330 | albert-api-rag-mfs-v2__22 | MFS_questions_v01 | albert-large-dry-3.2             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.697824 |        39 |            39 |
| 1331 | albert-api-rag-mfs-v2__24 | MFS_questions_v01 | albert-large-dry-3.2             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.763870 |        39 |            39 |
| 1332 | albert-api-rag-mfs-v2__26 | MFS_questions_v01 | albert-large-dry-3.2             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.817642 |        39 |            39 |
| 1333 | albert-api-rag-mfs-v2__28 | MFS_questions_v01 | albert-large-dry-3.2             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.873693 |        39 |            39 |
| 1334 | albert-api-rag-mfs-v2__30 | MFS_questions_v01 | albert-large-dry-3.1             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.930376 |        39 |            39 |
| 1335 | albert-api-rag-mfs-v2__32 | MFS_questions_v01 | albert-large-dry-3.1             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:56.984122 |        39 |            39 |
| 1336 | albert-api-rag-mfs-v2__34 | MFS_questions_v01 | albert-large-dry-3.1             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:57.037269 |        39 |            39 |
| 1337 | albert-api-rag-mfs-v2__36 | MFS_questions_v01 | albert-large-dry-3.1             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:57.090415 |        39 |            39 |
| 1338 | albert-api-rag-mfs-v2__38 | MFS_questions_v01 | albert-large-dry-3.1             | {'temperature': 0.2}                                                                                            | finished | 2025-08-08T13:07:57.143765 |        39 |            39 |
| 1349 | albert-api-rag-mfs-v3__30 | MFS_questions_v01 | albert-large-hybrid-web-elastic  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'web_search': True, 'k': 10}}          | finished | 2025-08-13T15:27:15.600059 |        39 |            39 |
| 1350 | albert-api-rag-mfs-v3__32 | MFS_questions_v01 | albert-large-hybrid-web-elastic  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'web_search': True, 'k': 10}}          | finished | 2025-08-13T15:27:15.699106 |        39 |            39 |
| 1351 | albert-api-rag-mfs-v3__34 | MFS_questions_v01 | albert-large-hybrid-web-elastic  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'web_search': True, 'k': 10}}          | finished | 2025-08-13T15:27:15.758279 |        39 |            39 |
| 1352 | albert-api-rag-mfs-v3__36 | MFS_questions_v01 | albert-large-hybrid-web-elastic  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'web_search': True, 'k': 10}}          | finished | 2025-08-13T15:27:15.813647 |        39 |            39 |
| 1353 | albert-api-rag-mfs-v3__38 | MFS_questions_v01 | albert-large-hybrid-web-elastic  | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'hybrid', 'web_search': True, 'k': 10}}          | finished | 2025-08-13T15:27:15.868291 |        39 |            39 |
| 1354 | albert-api-rag-mfs-v3__40 | MFS_questions_v01 | albert-large-semantic-web-qdrant | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'web_search': True, 'k': 10}}        | finished | 2025-08-13T15:27:16.140769 |        39 |            39 |
| 1355 | albert-api-rag-mfs-v3__42 | MFS_questions_v01 | albert-large-semantic-web-qdrant | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'web_search': True, 'k': 10}}        | finished | 2025-08-13T15:27:16.194491 |        39 |            39 |
| 1356 | albert-api-rag-mfs-v3__44 | MFS_questions_v01 | albert-large-semantic-web-qdrant | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'web_search': True, 'k': 10}}        | finished | 2025-08-13T15:27:16.247926 |        39 |            39 |
| 1357 | albert-api-rag-mfs-v3__46 | MFS_questions_v01 | albert-large-semantic-web-qdrant | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'web_search': True, 'k': 10}}        | finished | 2025-08-13T15:27:16.300386 |        39 |            39 |
| 1358 | albert-api-rag-mfs-v3__48 | MFS_questions_v01 | albert-large-semantic-web-qdrant | {'temperature': 0.2, 'search': True, 'search_args': {'method': 'semantic', 'web_search': True, 'k': 10}}        | finished | 2025-08-13T15:27:16.353085 |        39 |            39 |


## Details by Experiment

- [Experiment 1293](details/experiment_1293.md) - albert-api-rag-mfs-v2__0
- [Experiment 1294](details/experiment_1294.md) - albert-api-rag-mfs-v2__1
- [Experiment 1295](details/experiment_1295.md) - albert-api-rag-mfs-v2__2
- [Experiment 1296](details/experiment_1296.md) - albert-api-rag-mfs-v2__3
- [Experiment 1297](details/experiment_1297.md) - albert-api-rag-mfs-v2__4
- [Experiment 1298](details/experiment_1298.md) - albert-api-rag-mfs-v2__5
- [Experiment 1299](details/experiment_1299.md) - albert-api-rag-mfs-v2__6
- [Experiment 1300](details/experiment_1300.md) - albert-api-rag-mfs-v2__7
- [Experiment 1301](details/experiment_1301.md) - albert-api-rag-mfs-v2__8
- [Experiment 1302](details/experiment_1302.md) - albert-api-rag-mfs-v2__9
- [Experiment 1303](details/experiment_1303.md) - albert-api-rag-mfs-v2__10
- [Experiment 1304](details/experiment_1304.md) - albert-api-rag-mfs-v2__11
- [Experiment 1305](details/experiment_1305.md) - albert-api-rag-mfs-v2__12
- [Experiment 1306](details/experiment_1306.md) - albert-api-rag-mfs-v2__13
- [Experiment 1307](details/experiment_1307.md) - albert-api-rag-mfs-v2__14
- [Experiment 1308](details/experiment_1308.md) - albert-api-rag-mfs-v2__15
- [Experiment 1309](details/experiment_1309.md) - albert-api-rag-mfs-v2__16
- [Experiment 1310](details/experiment_1310.md) - albert-api-rag-mfs-v2__17
- [Experiment 1311](details/experiment_1311.md) - albert-api-rag-mfs-v2__18
- [Experiment 1312](details/experiment_1312.md) - albert-api-rag-mfs-v2__19
- [Experiment 1329](details/experiment_1329.md) - albert-api-rag-mfs-v2__20
- [Experiment 1330](details/experiment_1330.md) - albert-api-rag-mfs-v2__22
- [Experiment 1331](details/experiment_1331.md) - albert-api-rag-mfs-v2__24
- [Experiment 1332](details/experiment_1332.md) - albert-api-rag-mfs-v2__26
- [Experiment 1333](details/experiment_1333.md) - albert-api-rag-mfs-v2__28
- [Experiment 1334](details/experiment_1334.md) - albert-api-rag-mfs-v2__30
- [Experiment 1335](details/experiment_1335.md) - albert-api-rag-mfs-v2__32
- [Experiment 1336](details/experiment_1336.md) - albert-api-rag-mfs-v2__34
- [Experiment 1337](details/experiment_1337.md) - albert-api-rag-mfs-v2__36
- [Experiment 1338](details/experiment_1338.md) - albert-api-rag-mfs-v2__38
- [Experiment 1349](details/experiment_1349.md) - albert-api-rag-mfs-v3__30
- [Experiment 1350](details/experiment_1350.md) - albert-api-rag-mfs-v3__32
- [Experiment 1351](details/experiment_1351.md) - albert-api-rag-mfs-v3__34
- [Experiment 1352](details/experiment_1352.md) - albert-api-rag-mfs-v3__36
- [Experiment 1353](details/experiment_1353.md) - albert-api-rag-mfs-v3__38
- [Experiment 1354](details/experiment_1354.md) - albert-api-rag-mfs-v3__40
- [Experiment 1355](details/experiment_1355.md) - albert-api-rag-mfs-v3__42
- [Experiment 1356](details/experiment_1356.md) - albert-api-rag-mfs-v3__44
- [Experiment 1357](details/experiment_1357.md) - albert-api-rag-mfs-v3__46
- [Experiment 1358](details/experiment_1358.md) - albert-api-rag-mfs-v3__48
