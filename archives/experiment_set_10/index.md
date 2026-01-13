---
id: 10
name: "mfs_variability_v2"
date: 2025-02-28T10:22:35.021009
description: ""
tags: []
---

# Experiment Set: mfs_variability_v2 (ID: 10)

Comparing some models variability.

**Finished**: 100%

## Scores

**Dataset**: MFS_questions_v01 (Size: 39)

**Judge model**: gpt-4o

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                       | answer_relevancy   | generation_time   | judge_exactness   | judge_notator   | output_length   |
|:--------------------------------------------|:-------------------|:------------------|:------------------|:----------------|:----------------|
| AgentPublic/llama3-instruct-guillaumetell   | 0.78 ± 0.03        | 5.5 ± 0.57        | 0.13 ± 0.03       | 5.28 ± 0.18     | 133.25 ± 4.23   |
| neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | 0.89 ± 0.02        | 16.82 ± 2.18      | 0.07 ± 0.04       | 4.77 ± 0.12     | 266.96 ± 6.42   |
| google/gemma-2-9b-it                        | 0.77 ± 0.03        | 31.3 ± 24.96      | 0.05 ± 0.02       | 4.37 ± 0.18     | 229.9 ± 5.37    |
| meta-llama/Llama-3.3-70B-Instruct           | 0.85 ± 0.02        | 12.27 ± 0.3       | 0.04 ± 0.02       | 4.34 ± 0.13     | 339.05 ± 5.16   |
| meta-llama/Llama-3.1-8B-Instruct            | 0.8 ± 0.04         | 7.51 ± 7.38       | 0.05 ± 0.03       | 4.27 ± 0.68     | 212.47 ± 85.75  |
| meta-llama/Llama-3.2-3B-Instruct            | 0.74 ± 0.04        | 2.48 ± 0.05       | 0.0 ± 0.0         | 2.88 ± 0.09     | 320.4 ± 5.5     |



## Set Overview

|   Id | Name                   | Dataset           | Model                                       | Model params                                             | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------------|:------------------|:--------------------------------------------|:---------------------------------------------------------|:---------|:---------------------------|----------:|--------------:|
|  202 | mfs_variability_v2__0  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  203 | mfs_variability_v2__1  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  204 | mfs_variability_v2__2  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  205 | mfs_variability_v2__3  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  206 | mfs_variability_v2__4  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  207 | mfs_variability_v2__5  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  208 | mfs_variability_v2__6  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  209 | mfs_variability_v2__7  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  210 | mfs_variability_v2__8  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  211 | mfs_variability_v2__9  | MFS_questions_v01 | google/gemma-2-9b-it                        | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  212 | mfs_variability_v2__10 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  213 | mfs_variability_v2__11 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  214 | mfs_variability_v2__12 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  215 | mfs_variability_v2__13 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  216 | mfs_variability_v2__14 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  217 | mfs_variability_v2__15 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  218 | mfs_variability_v2__16 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  219 | mfs_variability_v2__17 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  220 | mfs_variability_v2__18 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  221 | mfs_variability_v2__19 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  222 | mfs_variability_v2__20 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  223 | mfs_variability_v2__21 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  224 | mfs_variability_v2__22 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  225 | mfs_variability_v2__23 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  226 | mfs_variability_v2__24 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  227 | mfs_variability_v2__25 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  228 | mfs_variability_v2__26 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  229 | mfs_variability_v2__27 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  230 | mfs_variability_v2__28 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  231 | mfs_variability_v2__29 | MFS_questions_v01 | meta-llama/Llama-3.2-3B-Instruct            | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  232 | mfs_variability_v2__30 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  233 | mfs_variability_v2__31 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  234 | mfs_variability_v2__32 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  235 | mfs_variability_v2__33 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  236 | mfs_variability_v2__34 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  237 | mfs_variability_v2__35 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  238 | mfs_variability_v2__36 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  239 | mfs_variability_v2__37 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  240 | mfs_variability_v2__38 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  241 | mfs_variability_v2__39 | MFS_questions_v01 | neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8 | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  242 | mfs_variability_v2__40 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  243 | mfs_variability_v2__41 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  244 | mfs_variability_v2__42 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  245 | mfs_variability_v2__43 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  246 | mfs_variability_v2__44 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  247 | mfs_variability_v2__45 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  248 | mfs_variability_v2__46 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  249 | mfs_variability_v2__47 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  250 | mfs_variability_v2__48 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  251 | mfs_variability_v2__49 | MFS_questions_v01 | meta-llama/Llama-3.3-70B-Instruct           | {'temperature': 0.2}                                     | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  252 | mfs_variability_v2__50 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  253 | mfs_variability_v2__51 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  254 | mfs_variability_v2__52 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  255 | mfs_variability_v2__53 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  256 | mfs_variability_v2__54 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  257 | mfs_variability_v2__55 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  258 | mfs_variability_v2__56 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  259 | mfs_variability_v2__57 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  260 | mfs_variability_v2__58 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  261 | mfs_variability_v2__59 | MFS_questions_v01 | meta-llama/Llama-3.1-8B-Instruct            | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  262 | mfs_variability_v2__60 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  263 | mfs_variability_v2__61 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  264 | mfs_variability_v2__62 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  265 | mfs_variability_v2__63 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  266 | mfs_variability_v2__64 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  267 | mfs_variability_v2__65 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  268 | mfs_variability_v2__66 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  269 | mfs_variability_v2__67 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  270 | mfs_variability_v2__68 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |
|  271 | mfs_variability_v2__69 | MFS_questions_v01 | AgentPublic/llama3-instruct-guillaumetell   | {'temperature': 0.2, 'rag': {'mode': 'rag', 'limit': 7}} | finished | 2025-02-28T10:22:35.021009 |        39 |            39 |


## Details by Experiment

- [Experiment 202](details/experiment_202.md) - mfs_variability_v2__0
- [Experiment 203](details/experiment_203.md) - mfs_variability_v2__1
- [Experiment 204](details/experiment_204.md) - mfs_variability_v2__2
- [Experiment 205](details/experiment_205.md) - mfs_variability_v2__3
- [Experiment 206](details/experiment_206.md) - mfs_variability_v2__4
- [Experiment 207](details/experiment_207.md) - mfs_variability_v2__5
- [Experiment 208](details/experiment_208.md) - mfs_variability_v2__6
- [Experiment 209](details/experiment_209.md) - mfs_variability_v2__7
- [Experiment 210](details/experiment_210.md) - mfs_variability_v2__8
- [Experiment 211](details/experiment_211.md) - mfs_variability_v2__9
- [Experiment 212](details/experiment_212.md) - mfs_variability_v2__10
- [Experiment 213](details/experiment_213.md) - mfs_variability_v2__11
- [Experiment 214](details/experiment_214.md) - mfs_variability_v2__12
- [Experiment 215](details/experiment_215.md) - mfs_variability_v2__13
- [Experiment 216](details/experiment_216.md) - mfs_variability_v2__14
- [Experiment 217](details/experiment_217.md) - mfs_variability_v2__15
- [Experiment 218](details/experiment_218.md) - mfs_variability_v2__16
- [Experiment 219](details/experiment_219.md) - mfs_variability_v2__17
- [Experiment 220](details/experiment_220.md) - mfs_variability_v2__18
- [Experiment 221](details/experiment_221.md) - mfs_variability_v2__19
- [Experiment 222](details/experiment_222.md) - mfs_variability_v2__20
- [Experiment 223](details/experiment_223.md) - mfs_variability_v2__21
- [Experiment 224](details/experiment_224.md) - mfs_variability_v2__22
- [Experiment 225](details/experiment_225.md) - mfs_variability_v2__23
- [Experiment 226](details/experiment_226.md) - mfs_variability_v2__24
- [Experiment 227](details/experiment_227.md) - mfs_variability_v2__25
- [Experiment 228](details/experiment_228.md) - mfs_variability_v2__26
- [Experiment 229](details/experiment_229.md) - mfs_variability_v2__27
- [Experiment 230](details/experiment_230.md) - mfs_variability_v2__28
- [Experiment 231](details/experiment_231.md) - mfs_variability_v2__29
- [Experiment 232](details/experiment_232.md) - mfs_variability_v2__30
- [Experiment 233](details/experiment_233.md) - mfs_variability_v2__31
- [Experiment 234](details/experiment_234.md) - mfs_variability_v2__32
- [Experiment 235](details/experiment_235.md) - mfs_variability_v2__33
- [Experiment 236](details/experiment_236.md) - mfs_variability_v2__34
- [Experiment 237](details/experiment_237.md) - mfs_variability_v2__35
- [Experiment 238](details/experiment_238.md) - mfs_variability_v2__36
- [Experiment 239](details/experiment_239.md) - mfs_variability_v2__37
- [Experiment 240](details/experiment_240.md) - mfs_variability_v2__38
- [Experiment 241](details/experiment_241.md) - mfs_variability_v2__39
- [Experiment 242](details/experiment_242.md) - mfs_variability_v2__40
- [Experiment 243](details/experiment_243.md) - mfs_variability_v2__41
- [Experiment 244](details/experiment_244.md) - mfs_variability_v2__42
- [Experiment 245](details/experiment_245.md) - mfs_variability_v2__43
- [Experiment 246](details/experiment_246.md) - mfs_variability_v2__44
- [Experiment 247](details/experiment_247.md) - mfs_variability_v2__45
- [Experiment 248](details/experiment_248.md) - mfs_variability_v2__46
- [Experiment 249](details/experiment_249.md) - mfs_variability_v2__47
- [Experiment 250](details/experiment_250.md) - mfs_variability_v2__48
- [Experiment 251](details/experiment_251.md) - mfs_variability_v2__49
- [Experiment 252](details/experiment_252.md) - mfs_variability_v2__50
- [Experiment 253](details/experiment_253.md) - mfs_variability_v2__51
- [Experiment 254](details/experiment_254.md) - mfs_variability_v2__52
- [Experiment 255](details/experiment_255.md) - mfs_variability_v2__53
- [Experiment 256](details/experiment_256.md) - mfs_variability_v2__54
- [Experiment 257](details/experiment_257.md) - mfs_variability_v2__55
- [Experiment 258](details/experiment_258.md) - mfs_variability_v2__56
- [Experiment 259](details/experiment_259.md) - mfs_variability_v2__57
- [Experiment 260](details/experiment_260.md) - mfs_variability_v2__58
- [Experiment 261](details/experiment_261.md) - mfs_variability_v2__59
- [Experiment 262](details/experiment_262.md) - mfs_variability_v2__60
- [Experiment 263](details/experiment_263.md) - mfs_variability_v2__61
- [Experiment 264](details/experiment_264.md) - mfs_variability_v2__62
- [Experiment 265](details/experiment_265.md) - mfs_variability_v2__63
- [Experiment 266](details/experiment_266.md) - mfs_variability_v2__64
- [Experiment 267](details/experiment_267.md) - mfs_variability_v2__65
- [Experiment 268](details/experiment_268.md) - mfs_variability_v2__66
- [Experiment 269](details/experiment_269.md) - mfs_variability_v2__67
- [Experiment 270](details/experiment_270.md) - mfs_variability_v2__68
- [Experiment 271](details/experiment_271.md) - mfs_variability_v2__69
