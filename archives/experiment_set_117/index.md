---
id: 117
name: "MediaTech's Service Public & Travail Emploi Chunking Evaluation V1"
date: 2026-01-08T10:04:11.072672
description: ""
tags: []
---

# Experiment Set: MediaTech's Service Public & Travail Emploi Chunking Evaluation V1 (ID: 117)

Evaluation of severals chunking strategies for MediaTech's Service Public & Travail Emploi datasets.

**Finished**: 99%

## Scores

**Dataset**: MFS_good_dataset (Size: 142)

**Judge model**: openai/gpt-oss-120b

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model         | contextual_precision   | contextual_recall   | contextual_relevancy   | faithfulness   | judge_notator   |
|:--------------|:-----------------------|:--------------------|:-----------------------|:---------------|:----------------|
| 1024_ov100    | 0.84 ± 0.01            | 0.62 ± 0.02         | 0.58 ± 0.01            | 0.97 ± 0.01    | 5.31 ± 0.01     |
| 1024_ov0      | 0.81 ± 0.01            | 0.62 ± 0.01         | 0.58 ± 0.01            | 0.97 ± 0.0     | 5.28 ± 0.05     |
| 512_ov50      | 0.83 ± 0.01            | 0.61 ± 0.01         | 0.59 ± 0.02            | 0.97 ± 0.01    | 5.19 ± 0.01     |
| 1500_ov20_len | 0.84 ± 0.01            | 0.6 ± 0.02          | 0.6 ± 0.02             | 0.98 ± 0.0     | 5.09 ± 0.02     |
| 1500_ov0_len  | 0.84 ± 0.01            | 0.59 ± 0.01         | 0.6 ± 0.01             | 0.98 ± 0.01    | 5.03 ± 0.06     |
| 512_ov0       | 0.78 ± 0.02            | 0.57 ± 0.01         | 0.57 ± 0.02            | 0.98 ± 0.01    | 5.0 ± 0.04      |
| 256_ov0       | 0.81 ± 0.0             | 0.54 ± 0.01         | 0.62 ± 0.02            | 0.99 ± 0.01    | 4.73 ± 0.03     |
| 256_ov25      | 0.73 ± 0.01            | 0.5 ± 0.0           | 0.54 ± 0.01            | 0.98 ± 0.0     | 4.31 ± 0.03     |


**Support**: the numbers of item on which the metrics is computed (total items = 142)

| model         | contextual_precision_support   | contextual_recall_support   | contextual_relevancy_support   | faithfulness_support   |   judge_notator_support |
|:--------------|:-------------------------------|:----------------------------|:-------------------------------|:-----------------------|------------------------:|
| 1024_ov100    | 141.33 ± 1.15                  | 142.0 ± 0.0                 | 140.67 ± 0.58                  | 142.0 ± 0.0            |                     142 |
| 1024_ov0      | 141.67 ± 0.58                  | 141.67 ± 0.58               | 141.0 ± 1.0                    | 142.0 ± 0.0            |                     142 |
| 512_ov50      | 141.33 ± 1.15                  | 141.0 ± 0.0                 | 140.33 ± 0.58                  | 142.0 ± 0.0            |                     142 |
| 1500_ov20_len | 142.0 ± 0.0                    | 141.67 ± 0.58               | 141.33 ± 0.58                  | 142.0 ± 0.0            |                     142 |
| 1500_ov0_len  | 142.0 ± 0.0                    | 141.67 ± 0.58               | 140.67 ± 0.58                  | 141.67 ± 0.58          |                     142 |
| 512_ov0       | 142.0 ± 0.0                    | 141.67 ± 0.58               | 141.67 ± 0.58                  | 141.33 ± 0.58          |                     142 |
| 256_ov0       | 141.0 ± 1.0                    | 141.67 ± 0.58               | 141.33 ± 0.58                  | 141.67 ± 0.58          |                     142 |
| 256_ov25      | 142.0 ± 0.0                    | 141.67 ± 0.58               | 141.67 ± 0.58                  | 141.33 ± 0.58          |                     142 |



## Set Overview

|   Id | Name                                                                   | Dataset          | Model         | Model params   | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------------------------------------------------------|:-----------------|:--------------|:---------------|:---------|:---------------------------|----------:|--------------:|
| 1873 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__0  | MFS_good_dataset | 1500_ov0_len  | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1874 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__1  | MFS_good_dataset | 1500_ov0_len  | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1875 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__2  | MFS_good_dataset | 1500_ov0_len  | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1876 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__3  | MFS_good_dataset | 1500_ov20_len | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1877 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__4  | MFS_good_dataset | 1500_ov20_len | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1878 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__5  | MFS_good_dataset | 1500_ov20_len | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1879 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__6  | MFS_good_dataset | 256_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1880 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__7  | MFS_good_dataset | 256_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1881 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__8  | MFS_good_dataset | 256_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1882 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__9  | MFS_good_dataset | 256_ov25      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1883 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__10 | MFS_good_dataset | 256_ov25      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1884 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__11 | MFS_good_dataset | 256_ov25      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1885 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__12 | MFS_good_dataset | 512_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1886 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__13 | MFS_good_dataset | 512_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1887 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__14 | MFS_good_dataset | 512_ov0       | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1888 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__15 | MFS_good_dataset | 512_ov50      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1889 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__16 | MFS_good_dataset | 512_ov50      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1890 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__17 | MFS_good_dataset | 512_ov50      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1891 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__18 | MFS_good_dataset | 1024_ov0      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1892 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__19 | MFS_good_dataset | 1024_ov0      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1893 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__20 | MFS_good_dataset | 1024_ov0      | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1894 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__21 | MFS_good_dataset | 1024_ov100    | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1895 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__22 | MFS_good_dataset | 1024_ov100    | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |
| 1896 | MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__23 | MFS_good_dataset | 1024_ov100    | {}             | finished | 2026-01-08T10:04:11.072672 |       142 |           142 |


## Details by Experiment

- [Experiment 1873](details/experiment_1873.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__0
- [Experiment 1874](details/experiment_1874.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__1
- [Experiment 1875](details/experiment_1875.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__2
- [Experiment 1876](details/experiment_1876.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__3
- [Experiment 1877](details/experiment_1877.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__4
- [Experiment 1878](details/experiment_1878.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__5
- [Experiment 1879](details/experiment_1879.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__6
- [Experiment 1880](details/experiment_1880.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__7
- [Experiment 1881](details/experiment_1881.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__8
- [Experiment 1882](details/experiment_1882.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__9
- [Experiment 1883](details/experiment_1883.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__10
- [Experiment 1884](details/experiment_1884.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__11
- [Experiment 1885](details/experiment_1885.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__12
- [Experiment 1886](details/experiment_1886.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__13
- [Experiment 1887](details/experiment_1887.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__14
- [Experiment 1888](details/experiment_1888.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__15
- [Experiment 1889](details/experiment_1889.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__16
- [Experiment 1890](details/experiment_1890.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__17
- [Experiment 1891](details/experiment_1891.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__18
- [Experiment 1892](details/experiment_1892.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__19
- [Experiment 1893](details/experiment_1893.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__20
- [Experiment 1894](details/experiment_1894.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__21
- [Experiment 1895](details/experiment_1895.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__22
- [Experiment 1896](details/experiment_1896.md) - MediaTech's Service Public & Travail Emploi Chunking Evaluation V1__23
