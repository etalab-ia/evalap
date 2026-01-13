---
id: 60
name: "albert_OCR_v1"
date: 2025-05-05T13:02:35.537286
description: ""
tags: []
---

# Experiment Set: albert_OCR_v1 (ID: 60)

Evaluating OCR capabilities of albert on the marker datasets

**Finished**: 0%

## Scores

**Dataset**: OCR_marker_benchmark (Size: 0)

**Judge model**: No judge found

**Score**: Averaged score on experiments metrics *(aggregated on model repetition)*

| model                                         | generation_time   | ocr_v1       | output_length   |
|:----------------------------------------------|:------------------|:-------------|:----------------|
| mistralai/Mistral-Small-3.1-24B-Instruct-2503 | 35.95 ± 1.97      | 81.59 ± 0.23 | 424.21 ± 0.87   |



## Set Overview

|   Id | Name             | Dataset              | Model                                         | Model params                               | Status   | Created at                 |   Num try |   Num success |
|-----:|:-----------------|:---------------------|:----------------------------------------------|:-------------------------------------------|:---------|:---------------------------|----------:|--------------:|
| 1120 | albert_OCR_v2__0 | OCR_marker_benchmark | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2, 'sys_prompt': '1ca0'} | finished | 2025-05-05T13:02:35.537286 |      2138 |           101 |
| 1121 | albert_OCR_v2__1 | OCR_marker_benchmark | mistralai/Mistral-Small-3.1-24B-Instruct-2503 | {'temperature': 0.2}                       | finished | 2025-05-05T13:02:35.537286 |      2138 |           101 |


## Details by Experiment

- [Experiment 1120](details/experiment_1120.md) - albert_OCR_v2__0
- [Experiment 1121](details/experiment_1121.md) - albert_OCR_v2__1
