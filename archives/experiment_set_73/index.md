---
id: 73
name: "Albert - brut - (MFS_questions_v01) v1-10-25"
date: 2025-10-01T12:09:52.557255
description: ""
tags: []
---

# Experiment Set: Albert - brut - (MFS_questions_v01) v1-10-25 (ID: 73)

Comparing Albert Models on dataset MFS_questions_v01

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | judge_exactness   | judge_precision   | output_length   |
|:----------------------------------------------|:------------------|:------------------|:------------------|:----------------|
| gpt-5                                         | 61.65 ± 5.97      | 0.78 ± 0.05       | 0.83 ± 0.02       | 360.83 ± 11.33  |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 14.81 ± 0.16      | 0.47 ± 0.02       | 0.5 ± 0.02        | 316.45 ± 11.33  |
| Qwen/Qwen3-30B-A3B-Instruct-2507              | 17.24 ± 0.16      | 0.4 ± 0.09        | 0.45 ± 0.05       | 595.37 ± 4.91   |
| mistralai/Magistral-Small-2506                | 17.09 ± 0.92      | 0.05 ± 0.0        | 0.22 ± 0.02       | 335.26 ± 16.68  |
| meta-llama/Llama-3.1-8B-Instruct              | 6.67 ± 0.11       | 0.08 ± 0.0        | 0.1 ± 0.0         | 295.4 ± 2.59    |



## Set Overview

|   Id | Name                                       | Dataset           | Model                                         | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:-------------------------------------------|:------------------|:----------------------------------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1386 | albert_mfs_questions_v01_v1-10-25__0       | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1387 | albert_mfs_questions_v01_v1-10-25__1       | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct              | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1388 | albert_mfs_questions_v01_v1-10-25__2       | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1389 | albert_mfs_questions_v01_v1-10-25__3       | MFS_questions_v01 | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1390 | albert_mfs_questions_v01_v1-10-25__4       | MFS_questions_v01 | Qwen/Qwen3-30B-A3B-Instruct-2507              | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1391 | albert_mfs_questions_v01_v1-10-25__5       | MFS_questions_v01 | Qwen/Qwen3-30B-A3B-Instruct-2507              | {'temperature': 0.2} | finished | 2025-10-01T12:09:52.557255 |        39 |            39 |
| 1398 | Albert (MFS_questions_v01) v1-10-25__6     | MFS_questions_v01 | gpt-5                                         | {}                   | finished | 2025-10-01T12:38:40.967108 |        39 |            39 |
| 1399 | Albert (MFS_questions_v01) v1-10-25__8     | MFS_questions_v01 | gpt-5                                         | {}                   | finished | 2025-10-01T12:38:41.061891 |        39 |            39 |
| 1410 | Albert (MFS_questions_v01) v1-10-25 <3__8  | MFS_questions_v01 | mistralai/Magistral-Small-2506                | {}                   | finished | 2025-10-01T17:12:20.371850 |        39 |            39 |
| 1411 | Albert (MFS_questions_v01) v1-10-25 <3__10 | MFS_questions_v01 | mistralai/Magistral-Small-2506                | {}                   | finished | 2025-10-01T17:12:20.434855 |        39 |            39 |


## Details by Experiment

- [Experiment 1386](details/experiment_1386.md) - albert_mfs_questions_v01_v1-10-25__0
- [Experiment 1387](details/experiment_1387.md) - albert_mfs_questions_v01_v1-10-25__1
- [Experiment 1388](details/experiment_1388.md) - albert_mfs_questions_v01_v1-10-25__2
- [Experiment 1389](details/experiment_1389.md) - albert_mfs_questions_v01_v1-10-25__3
- [Experiment 1390](details/experiment_1390.md) - albert_mfs_questions_v01_v1-10-25__4
- [Experiment 1391](details/experiment_1391.md) - albert_mfs_questions_v01_v1-10-25__5
- [Experiment 1398](details/experiment_1398.md) - Albert (MFS_questions_v01) v1-10-25__6
- [Experiment 1399](details/experiment_1399.md) - Albert (MFS_questions_v01) v1-10-25__8
- [Experiment 1410](details/experiment_1410.md) - Albert (MFS_questions_v01) v1-10-25 <3__8
- [Experiment 1411](details/experiment_1411.md) - Albert (MFS_questions_v01) v1-10-25 <3__10
