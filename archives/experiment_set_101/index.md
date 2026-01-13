---
id: 101
name: "Assistant LASuite Tools Comparison v2"
date: 2025-12-02T14:07:16.592724
description: ""
tags: []
---

# Experiment Set: Assistant LASuite Tools Comparison v2 (ID: 101)

Generated locally via notebook and pushed to EvalAP

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4.1

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                                | answer_relevancy   | judge_exactness   | judge_notator   | judge_precision   |
|:-----------------------------------------------------|:-------------------|:------------------|:----------------|:------------------|
| Mistral Medium (No RAG)                              | 0.82 ± 0.01        | 0.61 ± 0.03       | 7.64 ± 0.12     | 0.7 ± 0.03        |
| Mistral Medium (No RAG)(no sources)                  | 0.91 ± 0.01        | 0.55 ± 0.01       | 7.37 ± 0.05     | 0.64 ± 0.0        |
| Mistral Medium (With RAG Service Public)             | 0.86 ± 0.01        | 0.59 ± 0.08       | 7.63 ± 0.17     | 0.63 ± 0.05       |
| Mistral Medium (With RAG Service Public)(no sources) | 0.93 ± 0.0         | 0.54 ± 0.0        | 7.38 ± 0.04     | 0.5 ± 0.01        |
| Mistral Medium (With WEB)(no sources)                | 0.95 ± nan         | 0.51 ± nan        | 6.72 ± nan      | 0.38 ± nan        |



## Set Overview

|   Id | Name                                      | Dataset           | Model                                                | Model params         | Status   | Created at                 |   Num try |   Num success |
|-----:|:------------------------------------------|:------------------|:-----------------------------------------------------|:---------------------|:---------|:---------------------------|----------:|--------------:|
| 1614 | Assistant LASuite Tools Comparison v2__0  | MFS_questions_v01 | Mistral Medium (No RAG)                              | {}                   | finished | 2025-12-02T14:07:16.592724 |        39 |            39 |
| 1615 | Assistant LASuite Tools Comparison v2__2  | MFS_questions_v01 | Mistral Medium (With RAG Service Public)             | {'temperature': 0.2} | finished | 2025-12-02T14:59:50.100475 |        39 |            39 |
| 1616 | Assistant LASuite Tools Comparison v2__4  | MFS_questions_v01 | Mistral Medium (No RAG)                              | {'temperature': 0.2} | finished | 2025-12-02T15:37:15.229333 |        39 |            39 |
| 1617 | Assistant LASuite Tools Comparison v2__6  | MFS_questions_v01 | Mistral Medium (With RAG Service Public)             | {'temperature': 0.2} | finished | 2025-12-02T15:42:46.285905 |        39 |            39 |
| 1618 | Assistant LASuite Tools Comparison v2__8  | MFS_questions_v01 | Mistral Medium (With RAG Service Public)             | {'temperature': 0.2} | finished | 2025-12-02T15:58:26.992117 |        39 |            39 |
| 1619 | Assistant LASuite Tools Comparison v2__10 | MFS_questions_v01 | Mistral Medium (No RAG)                              | {'temperature': 0.2} | finished | 2025-12-02T16:13:15.020137 |        39 |            39 |
| 1620 | Assistant LASuite Tools Comparison v2__12 | MFS_questions_v01 | Mistral Medium (No RAG)(no sources)                  | {'temperature': 0.2} | finished | 2025-12-02T16:40:02.031501 |        39 |            39 |
| 1621 | Assistant LASuite Tools Comparison v2__14 | MFS_questions_v01 | Mistral Medium (No RAG)(no sources)                  | {'temperature': 0.2} | finished | 2025-12-02T16:40:03.697220 |        39 |            39 |
| 1622 | Assistant LASuite Tools Comparison v2__16 | MFS_questions_v01 | Mistral Medium (No RAG)(no sources)                  | {'temperature': 0.2} | finished | 2025-12-02T16:40:05.177531 |        39 |            39 |
| 1623 | Assistant LASuite Tools Comparison v2__18 | MFS_questions_v01 | Mistral Medium (With RAG Service Public)(no sources) | {'temperature': 0.2} | finished | 2025-12-02T16:43:06.110056 |        39 |            39 |
| 1624 | Assistant LASuite Tools Comparison v2__20 | MFS_questions_v01 | Mistral Medium (With RAG Service Public)(no sources) | {'temperature': 0.2} | finished | 2025-12-02T16:43:07.624513 |        39 |            39 |
| 1625 | Assistant LASuite Tools Comparison v2__22 | MFS_questions_v01 | Mistral Medium (With RAG Service Public)(no sources) | {'temperature': 0.2} | finished | 2025-12-02T16:43:08.515160 |        39 |            39 |
| 1626 | Assistant LASuite Tools Comparison v2__24 | MFS_questions_v01 | Mistral Medium (With WEB)(no sources)                | {'temperature': 0.2} | finished | 2025-12-02T16:53:08.256253 |        39 |            39 |


## Details by Experiment

- [Experiment 1614](details/experiment_1614.md) - Assistant LASuite Tools Comparison v2__0
- [Experiment 1615](details/experiment_1615.md) - Assistant LASuite Tools Comparison v2__2
- [Experiment 1616](details/experiment_1616.md) - Assistant LASuite Tools Comparison v2__4
- [Experiment 1617](details/experiment_1617.md) - Assistant LASuite Tools Comparison v2__6
- [Experiment 1618](details/experiment_1618.md) - Assistant LASuite Tools Comparison v2__8
- [Experiment 1619](details/experiment_1619.md) - Assistant LASuite Tools Comparison v2__10
- [Experiment 1620](details/experiment_1620.md) - Assistant LASuite Tools Comparison v2__12
- [Experiment 1621](details/experiment_1621.md) - Assistant LASuite Tools Comparison v2__14
- [Experiment 1622](details/experiment_1622.md) - Assistant LASuite Tools Comparison v2__16
- [Experiment 1623](details/experiment_1623.md) - Assistant LASuite Tools Comparison v2__18
- [Experiment 1624](details/experiment_1624.md) - Assistant LASuite Tools Comparison v2__20
- [Experiment 1625](details/experiment_1625.md) - Assistant LASuite Tools Comparison v2__22
- [Experiment 1626](details/experiment_1626.md) - Assistant LASuite Tools Comparison v2__24
