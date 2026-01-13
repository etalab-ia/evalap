---
id: 116
name: "MediaTech's LEGI Chunking Evaluation V1"
date: 2025-12-30T16:27:37.676509
description: ""
tags: []
---

# Experiment Set: MediaTech's LEGI Chunking Evaluation V1 (ID: 116)

Evaluation of severals chunking strategies for MediaTech's LEGI dataset.

**Finished**: 99%

## Scores

**Dataset**: LEGI Synthetic QA Dataset (Size: 49)

**Judge model**: openai/gpt-oss-120b

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model          | contextual_precision   | contextual_recall   | contextual_relevancy   | faithfulness   | judge_precision   |
|:---------------|:-----------------------|:--------------------|:-----------------------|:---------------|:------------------|
| 1024_ov0       | 0.83 ± 0.01            | 0.74 ± 0.02         | 0.5 ± 0.01             | 0.97 ± 0.01    | 0.1 ± 0.0         |
| 512_ov0        | 0.8 ± 0.03             | 0.68 ± 0.03         | 0.51 ± 0.03            | 0.99 ± 0.01    | 0.1 ± 0.01        |
| 1024_ov100     | 0.78 ± 0.03            | 0.73 ± 0.03         | 0.49 ± 0.02            | 0.96 ± 0.02    | 0.1 ± 0.01        |
| 1500_ov0       | 0.83 ± 0.05            | 0.72 ± 0.03         | 0.51 ± 0.03            | 0.96 ± 0.01    | 0.09 ± 0.02       |
| 5000_ov0_len   | 0.8 ± 0.01             | 0.74 ± 0.05         | 0.49 ± 0.02            | 0.99 ± 0.01    | 0.08 ± 0.0        |
| 5000_ov500_len | 0.76 ± 0.03            | 0.66 ± 0.02         | 0.51 ± 0.03            | 0.96 ± 0.02    | 0.08 ± 0.0        |
| 1500_ov100     | 0.82 ± 0.01            | 0.74 ± 0.03         | 0.51 ± 0.01            | 0.97 ± 0.01    | 0.07 ± 0.02       |
| 5000_ov250_len | 0.79 ± 0.03            | 0.75 ± 0.03         | 0.5 ± 0.03             | 0.97 ± 0.0     | 0.07 ± 0.01       |
| 512_ov50       | 0.82 ± 0.02            | 0.68 ± 0.03         | 0.51 ± 0.03            | 0.96 ± 0.01    | 0.06 ± 0.0        |
| 2048_ov100     | 0.77 ± 0.01            | 0.62 ± 0.05         | 0.5 ± 0.02             | 0.98 ± 0.02    | 0.06 ± 0.0        |
| 4096_ov0       | 0.7 ± 0.03             | 0.6 ± 0.04          | 0.52 ± 0.03            | 0.97 ± 0.02    | 0.05 ± 0.01       |
| 4096_ov100     | 0.68 ± 0.05            | 0.59 ± 0.0          | 0.49 ± 0.03            | 0.98 ± 0.01    | 0.04 ± 0.0        |
| 2048_ov0       | 0.76 ± 0.03            | 0.66 ± 0.04         | 0.47 ± 0.02            | 0.98 ± 0.03    | 0.04 ± 0.0        |
| 256_ov25       | 0.85 ± 0.01            | 0.68 ± 0.04         | 0.52 ± 0.02            | 0.97 ± 0.01    | 0.03 ± 0.01       |
| 256_ov0        | 0.86 ± 0.0             | 0.66 ± 0.01         | 0.52 ± 0.03            | 0.98 ± 0.0     | 0.02 ± 0.0        |
| 8000_ov0       | 0.66 ± 0.06            | 0.58 ± 0.01         | 0.47 ± 0.01            | 0.98 ± 0.0     | 0.02 ± 0.0        |
| 8000_ov100     | 0.64 ± 0.01            | 0.59 ± 0.02         | 0.5 ± 0.02             | 0.98 ± 0.01    | 0.02 ± 0.0        |


**Support**: the numbers of item on which the metrics is computed (total items = 49)

| model          | contextual_precision_support   | contextual_recall_support   | contextual_relevancy_support   | faithfulness_support   |   judge_precision_support |
|:---------------|:-------------------------------|:----------------------------|:-------------------------------|:-----------------------|--------------------------:|
| 1024_ov0       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 49.0 ± 0.0                     | 48.67 ± 0.58           |                        49 |
| 512_ov0        | 49.0 ± 0.0                     | 47.67 ± 1.53                | 48.33 ± 1.15                   | 49.0 ± 0.0             |                        49 |
| 1024_ov100     | 49.0 ± 0.0                     | 48.67 ± 0.58                | 48.67 ± 0.58                   | 48.67 ± 0.58           |                        49 |
| 1500_ov0       | 49.0 ± 0.0                     | 48.67 ± 0.58                | 48.67 ± 0.58                   | 48.67 ± 0.58           |                        49 |
| 5000_ov0_len   | 49.0 ± 0.0                     | 48.33 ± 0.58                | 49.0 ± 0.0                     | 49.0 ± 0.0             |                        49 |
| 5000_ov500_len | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 49.0 ± 0.0                     | 49.0 ± 0.0             |                        49 |
| 1500_ov100     | 49.0 ± 0.0                     | 48.67 ± 0.58                | 49.0 ± 0.0                     | 49.0 ± 0.0             |                        49 |
| 5000_ov250_len | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 48.67 ± 0.58                   | 49.0 ± 0.0             |                        49 |
| 512_ov50       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 49.0 ± 0.0                     | 48.67 ± 0.58           |                        49 |
| 2048_ov100     | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 48.67 ± 0.58                   | 49.0 ± 0.0             |                        49 |
| 4096_ov0       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 49.0 ± 0.0                     | 49.0 ± 0.0             |                        49 |
| 4096_ov100     | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 48.33 ± 0.58                   | 49.0 ± 0.0             |                        49 |
| 2048_ov0       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 48.67 ± 0.58                   | 49.0 ± 0.0             |                        49 |
| 256_ov25       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 49.0 ± 0.0                     | 48.67 ± 0.58           |                        49 |
| 256_ov0        | 48.67 ± 0.58                   | 49.0 ± 0.0                  | 48.67 ± 0.58                   | 49.0 ± 0.0             |                        49 |
| 8000_ov0       | 49.0 ± 0.0                     | 49.0 ± 0.0                  | 48.0 ± 1.0                     | 49.0 ± 0.0             |                        49 |
| 8000_ov100     | 48.67 ± 0.58                   | 49.0 ± 0.0                  | 48.33 ± 0.58                   | 49.0 ± 0.0             |                        49 |



## Set Overview

|   Id | Name                                        | Dataset                   | Model          | Model params   | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------------------|:--------------------------|:---------------|:---------------|:---------|:---------------------------|----------:|--------------:|
| 1822 | MediaTech's LEGI Chunking Evaluation V1__0  | LEGI Synthetic QA Dataset | 5000_ov0_len   | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1823 | MediaTech's LEGI Chunking Evaluation V1__1  | LEGI Synthetic QA Dataset | 5000_ov0_len   | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1824 | MediaTech's LEGI Chunking Evaluation V1__2  | LEGI Synthetic QA Dataset | 5000_ov0_len   | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1825 | MediaTech's LEGI Chunking Evaluation V1__3  | LEGI Synthetic QA Dataset | 5000_ov250_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1826 | MediaTech's LEGI Chunking Evaluation V1__4  | LEGI Synthetic QA Dataset | 5000_ov250_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1827 | MediaTech's LEGI Chunking Evaluation V1__5  | LEGI Synthetic QA Dataset | 5000_ov250_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1828 | MediaTech's LEGI Chunking Evaluation V1__6  | LEGI Synthetic QA Dataset | 5000_ov500_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1829 | MediaTech's LEGI Chunking Evaluation V1__7  | LEGI Synthetic QA Dataset | 5000_ov500_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1830 | MediaTech's LEGI Chunking Evaluation V1__8  | LEGI Synthetic QA Dataset | 5000_ov500_len | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1831 | MediaTech's LEGI Chunking Evaluation V1__9  | LEGI Synthetic QA Dataset | 256_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1832 | MediaTech's LEGI Chunking Evaluation V1__10 | LEGI Synthetic QA Dataset | 256_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1833 | MediaTech's LEGI Chunking Evaluation V1__11 | LEGI Synthetic QA Dataset | 256_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1834 | MediaTech's LEGI Chunking Evaluation V1__12 | LEGI Synthetic QA Dataset | 256_ov25       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1835 | MediaTech's LEGI Chunking Evaluation V1__13 | LEGI Synthetic QA Dataset | 256_ov25       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1836 | MediaTech's LEGI Chunking Evaluation V1__14 | LEGI Synthetic QA Dataset | 256_ov25       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1837 | MediaTech's LEGI Chunking Evaluation V1__15 | LEGI Synthetic QA Dataset | 512_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1838 | MediaTech's LEGI Chunking Evaluation V1__16 | LEGI Synthetic QA Dataset | 512_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1839 | MediaTech's LEGI Chunking Evaluation V1__17 | LEGI Synthetic QA Dataset | 512_ov0        | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1840 | MediaTech's LEGI Chunking Evaluation V1__18 | LEGI Synthetic QA Dataset | 512_ov50       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1841 | MediaTech's LEGI Chunking Evaluation V1__19 | LEGI Synthetic QA Dataset | 512_ov50       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1842 | MediaTech's LEGI Chunking Evaluation V1__20 | LEGI Synthetic QA Dataset | 512_ov50       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1843 | MediaTech's LEGI Chunking Evaluation V1__21 | LEGI Synthetic QA Dataset | 1024_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1844 | MediaTech's LEGI Chunking Evaluation V1__22 | LEGI Synthetic QA Dataset | 1024_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1845 | MediaTech's LEGI Chunking Evaluation V1__23 | LEGI Synthetic QA Dataset | 1024_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1846 | MediaTech's LEGI Chunking Evaluation V1__24 | LEGI Synthetic QA Dataset | 1024_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1847 | MediaTech's LEGI Chunking Evaluation V1__25 | LEGI Synthetic QA Dataset | 1024_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1848 | MediaTech's LEGI Chunking Evaluation V1__26 | LEGI Synthetic QA Dataset | 1024_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1849 | MediaTech's LEGI Chunking Evaluation V1__27 | LEGI Synthetic QA Dataset | 1500_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1850 | MediaTech's LEGI Chunking Evaluation V1__28 | LEGI Synthetic QA Dataset | 1500_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1851 | MediaTech's LEGI Chunking Evaluation V1__29 | LEGI Synthetic QA Dataset | 1500_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1852 | MediaTech's LEGI Chunking Evaluation V1__30 | LEGI Synthetic QA Dataset | 1500_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1853 | MediaTech's LEGI Chunking Evaluation V1__31 | LEGI Synthetic QA Dataset | 1500_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1854 | MediaTech's LEGI Chunking Evaluation V1__32 | LEGI Synthetic QA Dataset | 1500_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1855 | MediaTech's LEGI Chunking Evaluation V1__33 | LEGI Synthetic QA Dataset | 2048_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1856 | MediaTech's LEGI Chunking Evaluation V1__34 | LEGI Synthetic QA Dataset | 2048_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1857 | MediaTech's LEGI Chunking Evaluation V1__35 | LEGI Synthetic QA Dataset | 2048_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1858 | MediaTech's LEGI Chunking Evaluation V1__36 | LEGI Synthetic QA Dataset | 2048_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1859 | MediaTech's LEGI Chunking Evaluation V1__37 | LEGI Synthetic QA Dataset | 2048_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1860 | MediaTech's LEGI Chunking Evaluation V1__38 | LEGI Synthetic QA Dataset | 2048_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1861 | MediaTech's LEGI Chunking Evaluation V1__39 | LEGI Synthetic QA Dataset | 4096_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1862 | MediaTech's LEGI Chunking Evaluation V1__40 | LEGI Synthetic QA Dataset | 4096_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1863 | MediaTech's LEGI Chunking Evaluation V1__41 | LEGI Synthetic QA Dataset | 4096_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1864 | MediaTech's LEGI Chunking Evaluation V1__42 | LEGI Synthetic QA Dataset | 4096_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1865 | MediaTech's LEGI Chunking Evaluation V1__43 | LEGI Synthetic QA Dataset | 4096_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1866 | MediaTech's LEGI Chunking Evaluation V1__44 | LEGI Synthetic QA Dataset | 4096_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1867 | MediaTech's LEGI Chunking Evaluation V1__45 | LEGI Synthetic QA Dataset | 8000_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1868 | MediaTech's LEGI Chunking Evaluation V1__46 | LEGI Synthetic QA Dataset | 8000_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1869 | MediaTech's LEGI Chunking Evaluation V1__47 | LEGI Synthetic QA Dataset | 8000_ov0       | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1870 | MediaTech's LEGI Chunking Evaluation V1__48 | LEGI Synthetic QA Dataset | 8000_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1871 | MediaTech's LEGI Chunking Evaluation V1__49 | LEGI Synthetic QA Dataset | 8000_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |
| 1872 | MediaTech's LEGI Chunking Evaluation V1__50 | LEGI Synthetic QA Dataset | 8000_ov100     | {}             | finished | 2025-12-30T16:27:37.676509 |        49 |            49 |


## Details by Experiment

- [Experiment 1822](details/experiment_1822.md) - MediaTech's LEGI Chunking Evaluation V1__0
- [Experiment 1823](details/experiment_1823.md) - MediaTech's LEGI Chunking Evaluation V1__1
- [Experiment 1824](details/experiment_1824.md) - MediaTech's LEGI Chunking Evaluation V1__2
- [Experiment 1825](details/experiment_1825.md) - MediaTech's LEGI Chunking Evaluation V1__3
- [Experiment 1826](details/experiment_1826.md) - MediaTech's LEGI Chunking Evaluation V1__4
- [Experiment 1827](details/experiment_1827.md) - MediaTech's LEGI Chunking Evaluation V1__5
- [Experiment 1828](details/experiment_1828.md) - MediaTech's LEGI Chunking Evaluation V1__6
- [Experiment 1829](details/experiment_1829.md) - MediaTech's LEGI Chunking Evaluation V1__7
- [Experiment 1830](details/experiment_1830.md) - MediaTech's LEGI Chunking Evaluation V1__8
- [Experiment 1831](details/experiment_1831.md) - MediaTech's LEGI Chunking Evaluation V1__9
- [Experiment 1832](details/experiment_1832.md) - MediaTech's LEGI Chunking Evaluation V1__10
- [Experiment 1833](details/experiment_1833.md) - MediaTech's LEGI Chunking Evaluation V1__11
- [Experiment 1834](details/experiment_1834.md) - MediaTech's LEGI Chunking Evaluation V1__12
- [Experiment 1835](details/experiment_1835.md) - MediaTech's LEGI Chunking Evaluation V1__13
- [Experiment 1836](details/experiment_1836.md) - MediaTech's LEGI Chunking Evaluation V1__14
- [Experiment 1837](details/experiment_1837.md) - MediaTech's LEGI Chunking Evaluation V1__15
- [Experiment 1838](details/experiment_1838.md) - MediaTech's LEGI Chunking Evaluation V1__16
- [Experiment 1839](details/experiment_1839.md) - MediaTech's LEGI Chunking Evaluation V1__17
- [Experiment 1840](details/experiment_1840.md) - MediaTech's LEGI Chunking Evaluation V1__18
- [Experiment 1841](details/experiment_1841.md) - MediaTech's LEGI Chunking Evaluation V1__19
- [Experiment 1842](details/experiment_1842.md) - MediaTech's LEGI Chunking Evaluation V1__20
- [Experiment 1843](details/experiment_1843.md) - MediaTech's LEGI Chunking Evaluation V1__21
- [Experiment 1844](details/experiment_1844.md) - MediaTech's LEGI Chunking Evaluation V1__22
- [Experiment 1845](details/experiment_1845.md) - MediaTech's LEGI Chunking Evaluation V1__23
- [Experiment 1846](details/experiment_1846.md) - MediaTech's LEGI Chunking Evaluation V1__24
- [Experiment 1847](details/experiment_1847.md) - MediaTech's LEGI Chunking Evaluation V1__25
- [Experiment 1848](details/experiment_1848.md) - MediaTech's LEGI Chunking Evaluation V1__26
- [Experiment 1849](details/experiment_1849.md) - MediaTech's LEGI Chunking Evaluation V1__27
- [Experiment 1850](details/experiment_1850.md) - MediaTech's LEGI Chunking Evaluation V1__28
- [Experiment 1851](details/experiment_1851.md) - MediaTech's LEGI Chunking Evaluation V1__29
- [Experiment 1852](details/experiment_1852.md) - MediaTech's LEGI Chunking Evaluation V1__30
- [Experiment 1853](details/experiment_1853.md) - MediaTech's LEGI Chunking Evaluation V1__31
- [Experiment 1854](details/experiment_1854.md) - MediaTech's LEGI Chunking Evaluation V1__32
- [Experiment 1855](details/experiment_1855.md) - MediaTech's LEGI Chunking Evaluation V1__33
- [Experiment 1856](details/experiment_1856.md) - MediaTech's LEGI Chunking Evaluation V1__34
- [Experiment 1857](details/experiment_1857.md) - MediaTech's LEGI Chunking Evaluation V1__35
- [Experiment 1858](details/experiment_1858.md) - MediaTech's LEGI Chunking Evaluation V1__36
- [Experiment 1859](details/experiment_1859.md) - MediaTech's LEGI Chunking Evaluation V1__37
- [Experiment 1860](details/experiment_1860.md) - MediaTech's LEGI Chunking Evaluation V1__38
- [Experiment 1861](details/experiment_1861.md) - MediaTech's LEGI Chunking Evaluation V1__39
- [Experiment 1862](details/experiment_1862.md) - MediaTech's LEGI Chunking Evaluation V1__40
- [Experiment 1863](details/experiment_1863.md) - MediaTech's LEGI Chunking Evaluation V1__41
- [Experiment 1864](details/experiment_1864.md) - MediaTech's LEGI Chunking Evaluation V1__42
- [Experiment 1865](details/experiment_1865.md) - MediaTech's LEGI Chunking Evaluation V1__43
- [Experiment 1866](details/experiment_1866.md) - MediaTech's LEGI Chunking Evaluation V1__44
- [Experiment 1867](details/experiment_1867.md) - MediaTech's LEGI Chunking Evaluation V1__45
- [Experiment 1868](details/experiment_1868.md) - MediaTech's LEGI Chunking Evaluation V1__46
- [Experiment 1869](details/experiment_1869.md) - MediaTech's LEGI Chunking Evaluation V1__47
- [Experiment 1870](details/experiment_1870.md) - MediaTech's LEGI Chunking Evaluation V1__48
- [Experiment 1871](details/experiment_1871.md) - MediaTech's LEGI Chunking Evaluation V1__49
- [Experiment 1872](details/experiment_1872.md) - MediaTech's LEGI Chunking Evaluation V1__50
