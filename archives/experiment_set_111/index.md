---
id: 111
name: "LegalBenchRAG Evaluation v1"
date: 2025-12-12T13:18:15.439295
description: ""
tags: []
---

# Experiment Set: LegalBenchRAG Evaluation v1 (ID: 111)

A extensive RAG evaluation on the LegalBenchRAG dataset. See [complete me]

**Finished**: 14%

## Scores

**Dataset**: LegalBenchRAG (Size: 6889)

**Judge model**: mistralai/Mistral-Small-3.2-24B-Instruct-2506

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         |   judge_precision |   output_length |
|:----------------------------------------------|------------------:|----------------:|
| model_semantic_20_qwen3_lbrv5                 |              0.82 |          163.13 |
| model_hybrid_20_bgem3_lbrv5                   |              0.81 |          154.72 |
| model_semantic_20_qwen3_lbrv4.6               |              0.81 |          159.07 |
| model_semantic_20_bgem3_lbrv5                 |              0.81 |          150.22 |
| model_hybrid_20_bgem3_lbrv4.6                 |              0.8  |          153.22 |
| model_hybrid_25_bgem3_lbrv4.6                 |              0.8  |          150.42 |
| model_hybrid_7_qwen3_lbrv5                    |              0.79 |          155.07 |
| model_semantic_25_bgem3_lbrv4.6               |              0.78 |          146.2  |
| model_semantic_20_bgem3_lbrv4.6               |              0.77 |          149.82 |
| model_hybrid_14_bgem3_lbrv4.6                 |              0.76 |          151.97 |
| model_semantic_14_bgem3_lbrv4.6               |              0.75 |          149.62 |
| model_hybrid_7_qwen3_lbrv4.6                  |              0.75 |          153.46 |
| model_semantic_7_bgem3_lbrv5                  |              0.74 |          145.31 |
| model_hybrid_7_bgem3_lbrv5                    |              0.73 |          148.2  |
| model_semantic_7_bgem3_lbrv4                  |              0.68 |          141.56 |
| model_semantic_7_bgem3_lbrv4.6                |              0.68 |          141.84 |
| model_semantic_7_bgem3_lbrv4.5                |              0.68 |          142.37 |
| model_hybrid_7_bgem3_lbrv4.6                  |              0.67 |          141.21 |
| model_hybrid_7_bgem3_lbrv4.5                  |              0.67 |          143.64 |
| model_hybrid_7_bgem3_lbrv4                    |              0.66 |          143.01 |
| model_semantic_14_bgem3                       |              0.6  |          182.55 |
| model_hybrid_14_bgem3                         |              0.56 |          171.08 |
| model_semantic_14_bgem3_lbrv2                 |              0.53 |          164.33 |
| model_semantic_7_bgem3_lbrv2.5                |              0.53 |          161.51 |
| model_semantic_7_bgem3_lbrv3                  |              0.53 |          164.36 |
| model_lexical_7_bgem3_lbrv4.6                 |              0.52 |          142.39 |
| model_semantic_7_bgem3                        |              0.52 |          160.94 |
| model_semantic_7_bgem3_lbrv2                  |              0.52 |          164.33 |
| model_hybrid_7_bgem3                          |              0.49 |          147.08 |
| model_hybrid_14_bgem3_lbrv2                   |              0.48 |          148.71 |
| model_hybrid_7_bgem3_lbrv3                    |              0.48 |          148.51 |
| model_hybrid_7_bgem3_lbrv2                    |              0.48 |          148.71 |
| model_hybrid_7_bgem3_lbrv2.5                  |              0.47 |          146.67 |
| model_lexical_14_bgem3                        |              0.45 |          156.13 |
| model_lexical_7_bgem3                         |              0.38 |          127.99 |
| mistralai/Mistral-Small-3.2-24B-Instruct-2506 |              0.31 |          165.64 |



## Set Overview

|   Id | Name                            | Dataset       | Model                                         | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:--------------------------------|:--------------|:----------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1700 | LegalBenchRAG Evaluation__0     | LegalBenchRAG | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-12T13:18:15.439295 |      1000 |          1000 |
| 1701 | LegalBenchRAG Evaluation__2     | LegalBenchRAG | model_hybrid_7_bgem3                          | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T00:51:46.235472 |      1000 |          1000 |
| 1702 | LegalBenchRAG Evaluation__4     | LegalBenchRAG | model_semantic_7_bgem3                        | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T00:51:50.727967 |      1000 |          1000 |
| 1703 | LegalBenchRAG Evaluation__6     | LegalBenchRAG | model_lexical_7_bgem3                         | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T00:51:54.825474 |      1000 |          1000 |
| 1704 | LegalBenchRAG Evaluation__8     | LegalBenchRAG | model_hybrid_14_bgem3                         | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T21:03:58.945696 |      1000 |          1000 |
| 1705 | LegalBenchRAG Evaluation__10    | LegalBenchRAG | model_semantic_14_bgem3                       | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T21:04:03.595303 |      1000 |          1000 |
| 1706 | LegalBenchRAG Evaluation__12    | LegalBenchRAG | model_lexical_14_bgem3                        | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-13T21:04:07.888572 |      1000 |          1000 |
| 1756 | LegalBenchRAG Evaluation__14    | LegalBenchRAG | model_hybrid_7_bgem3_lbrv2                    | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T15:31:03.986170 |      1000 |          1000 |
| 1757 | LegalBenchRAG Evaluation__16    | LegalBenchRAG | model_semantic_7_bgem3_lbrv2                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T15:31:08.588791 |      1000 |          1000 |
| 1788 | LegalBenchRAG Evaluation__18    | LegalBenchRAG | model_hybrid_14_bgem3_lbrv2                   | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T21:11:12.266985 |      1000 |          1000 |
| 1789 | LegalBenchRAG Evaluation__20    | LegalBenchRAG | model_semantic_14_bgem3_lbrv2                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T21:11:16.771880 |      1000 |          1000 |
| 1790 | LegalBenchRAG Evaluation__22    | LegalBenchRAG | model_hybrid_7_bgem3_lbrv2.5                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T23:11:52.156017 |      1000 |          1000 |
| 1791 | LegalBenchRAG Evaluation__24    | LegalBenchRAG | model_semantic_7_bgem3_lbrv2.5                | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-18T23:11:56.549328 |      1000 |          1000 |
| 1792 | LegalBenchRAG Evaluation__26    | LegalBenchRAG | model_hybrid_7_bgem3_lbrv3                    | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T11:27:49.867673 |      1000 |          1000 |
| 1793 | LegalBenchRAG Evaluation__28    | LegalBenchRAG | model_semantic_7_bgem3_lbrv3                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T11:27:54.187536 |      1000 |          1000 |
| 1798 | LegalBenchRAG Evaluation__38    | LegalBenchRAG | model_hybrid_7_bgem3_lbrv4.5                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T15:17:24.388339 |      1000 |          1000 |
| 1799 | LegalBenchRAG Evaluation__40    | LegalBenchRAG | model_semantic_7_bgem3_lbrv4.5                | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T15:17:28.828023 |      1000 |          1000 |
| 1800 | LegalBenchRAG Evaluation__34    | LegalBenchRAG | model_hybrid_7_bgem3_lbrv4                    | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T17:47:08.633250 |      1000 |          1000 |
| 1801 | LegalBenchRAG Evaluation__36    | LegalBenchRAG | model_semantic_7_bgem3_lbrv4                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T17:47:13.331264 |      1000 |          1000 |
| 1803 | LegalBenchRAG Evaluation v1__38 | LegalBenchRAG | model_hybrid_7_bgem3_lbrv4.6                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T22:52:36.336418 |      1000 |          1000 |
| 1804 | LegalBenchRAG Evaluation v1__40 | LegalBenchRAG | model_semantic_7_bgem3_lbrv4.6                | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T22:52:41.305251 |      1000 |          1000 |
| 1805 | LegalBenchRAG Evaluation v1__42 | LegalBenchRAG | model_lexical_7_bgem3_lbrv4.6                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-19T22:52:45.868974 |      1000 |          1000 |
| 1806 | LegalBenchRAG Evaluation v1__44 | LegalBenchRAG | model_hybrid_14_bgem3_lbrv4.6                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T00:28:18.210324 |      1000 |          1000 |
| 1807 | LegalBenchRAG Evaluation v1__46 | LegalBenchRAG | model_semantic_14_bgem3_lbrv4.6               | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T00:28:22.670065 |      1000 |          1000 |
| 1808 | LegalBenchRAG Evaluation v1__48 | LegalBenchRAG | model_hybrid_20_bgem3_lbrv4.6                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T02:13:56.865098 |      1000 |          1000 |
| 1809 | LegalBenchRAG Evaluation v1__50 | LegalBenchRAG | model_semantic_20_bgem3_lbrv4.6               | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T02:14:01.491466 |      1000 |          1000 |
| 1810 | LegalBenchRAG Evaluation v1__52 | LegalBenchRAG | model_hybrid_25_bgem3_lbrv4.6                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T22:16:34.030843 |      1000 |          1000 |
| 1811 | LegalBenchRAG Evaluation v1__54 | LegalBenchRAG | model_semantic_25_bgem3_lbrv4.6               | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T22:16:38.946718 |      1000 |          1000 |
| 1812 | LegalBenchRAG Evaluation v1__56 | LegalBenchRAG | model_hybrid_7_bgem3_lbrv5                    | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T23:31:53.980357 |      1000 |          1000 |
| 1813 | LegalBenchRAG Evaluation v1__58 | LegalBenchRAG | model_semantic_7_bgem3_lbrv5                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-20T23:31:58.534245 |      1000 |          1000 |
| 1814 | LegalBenchRAG Evaluation v1__60 | LegalBenchRAG | model_hybrid_20_bgem3_lbrv5                   | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-21T01:23:36.286885 |      1000 |          1000 |
| 1815 | LegalBenchRAG Evaluation v1__62 | LegalBenchRAG | model_semantic_20_bgem3_lbrv5                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-21T01:23:40.853735 |      1000 |          1000 |
| 1816 | LegalBenchRAG Evaluation v1__64 | LegalBenchRAG | model_hybrid_7_qwen3_lbrv4.6                  | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-22T17:50:26.603304 |      1000 |          1000 |
| 1817 | LegalBenchRAG Evaluation v1__66 | LegalBenchRAG | model_semantic_20_qwen3_lbrv4.6               | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-22T17:50:31.257061 |      1000 |          1000 |
| 1818 | LegalBenchRAG Evaluation v1__68 | LegalBenchRAG | model_hybrid_7_qwen3_lbrv5                    | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-22T17:50:35.708152 |      1000 |          1000 |
| 1819 | LegalBenchRAG Evaluation v1__70 | LegalBenchRAG | model_semantic_20_qwen3_lbrv5                 | {'temperature': 0.2, 'sys_prompt': '1a83'} | finished | 2025-12-22T17:50:40.102039 |      1000 |          1000 |


## Details by Experiment

- [Experiment 1700](details/experiment_1700.md) - LegalBenchRAG Evaluation__0
- [Experiment 1701](details/experiment_1701.md) - LegalBenchRAG Evaluation__2
- [Experiment 1702](details/experiment_1702.md) - LegalBenchRAG Evaluation__4
- [Experiment 1703](details/experiment_1703.md) - LegalBenchRAG Evaluation__6
- [Experiment 1704](details/experiment_1704.md) - LegalBenchRAG Evaluation__8
- [Experiment 1705](details/experiment_1705.md) - LegalBenchRAG Evaluation__10
- [Experiment 1706](details/experiment_1706.md) - LegalBenchRAG Evaluation__12
- [Experiment 1756](details/experiment_1756.md) - LegalBenchRAG Evaluation__14
- [Experiment 1757](details/experiment_1757.md) - LegalBenchRAG Evaluation__16
- [Experiment 1788](details/experiment_1788.md) - LegalBenchRAG Evaluation__18
- [Experiment 1789](details/experiment_1789.md) - LegalBenchRAG Evaluation__20
- [Experiment 1790](details/experiment_1790.md) - LegalBenchRAG Evaluation__22
- [Experiment 1791](details/experiment_1791.md) - LegalBenchRAG Evaluation__24
- [Experiment 1792](details/experiment_1792.md) - LegalBenchRAG Evaluation__26
- [Experiment 1793](details/experiment_1793.md) - LegalBenchRAG Evaluation__28
- [Experiment 1798](details/experiment_1798.md) - LegalBenchRAG Evaluation__38
- [Experiment 1799](details/experiment_1799.md) - LegalBenchRAG Evaluation__40
- [Experiment 1800](details/experiment_1800.md) - LegalBenchRAG Evaluation__34
- [Experiment 1801](details/experiment_1801.md) - LegalBenchRAG Evaluation__36
- [Experiment 1803](details/experiment_1803.md) - LegalBenchRAG Evaluation v1__38
- [Experiment 1804](details/experiment_1804.md) - LegalBenchRAG Evaluation v1__40
- [Experiment 1805](details/experiment_1805.md) - LegalBenchRAG Evaluation v1__42
- [Experiment 1806](details/experiment_1806.md) - LegalBenchRAG Evaluation v1__44
- [Experiment 1807](details/experiment_1807.md) - LegalBenchRAG Evaluation v1__46
- [Experiment 1808](details/experiment_1808.md) - LegalBenchRAG Evaluation v1__48
- [Experiment 1809](details/experiment_1809.md) - LegalBenchRAG Evaluation v1__50
- [Experiment 1810](details/experiment_1810.md) - LegalBenchRAG Evaluation v1__52
- [Experiment 1811](details/experiment_1811.md) - LegalBenchRAG Evaluation v1__54
- [Experiment 1812](details/experiment_1812.md) - LegalBenchRAG Evaluation v1__56
- [Experiment 1813](details/experiment_1813.md) - LegalBenchRAG Evaluation v1__58
- [Experiment 1814](details/experiment_1814.md) - LegalBenchRAG Evaluation v1__60
- [Experiment 1815](details/experiment_1815.md) - LegalBenchRAG Evaluation v1__62
- [Experiment 1816](details/experiment_1816.md) - LegalBenchRAG Evaluation v1__64
- [Experiment 1817](details/experiment_1817.md) - LegalBenchRAG Evaluation v1__66
- [Experiment 1818](details/experiment_1818.md) - LegalBenchRAG Evaluation v1__68
- [Experiment 1819](details/experiment_1819.md) - LegalBenchRAG Evaluation v1__70
