---
sidebar_position: 6
---

# LLM Compliance Benchmarking: Datasets & Experimentation

This guide details the methodology and technical steps for evaluating the compliance performance of language models on EvalAP. It provides a reference for datasets, metric interpretations, and code examples for uploading, mapping, and benchmarking datasets using the EvalAP API.

---

## Objective

This section describes the standardized process for **analyzing and comparing Large Language Models (LLMs)** on ethical and compliance-oriented datasets on EvalAP. Each benchmark dataset focuses on a key aspect of responsible AI: bias, toxicity, cultural sensitivity, and faithfulness.

---

## 📊 Compliance Datasets Overview

| Dataset                | Evaluation Objective                                 | Key Metrics                         | Notes                                                         |
|------------------------|-----------------------------------------------------|-------------------------------------|---------------------------------------------------------------|
| **llm-values/CIVICS**  | Cultural sensitivity, value variation                | `bias`, `answer_relevancy`, `faithfulness` | Cultural coherence & ideological neutrality               |
| **lmsys-toxic-chat**   | Detection of toxicity in model generations          | `toxicity`, `bias`, `answer_relevancy`      | Moderation & safety evaluation                            |
| **crows-pairs**        | Analysis of implicit linguistic & social biases      | `bias`, `answer_relevancy`, `faithfulness` | Robustness vs stereotypes                                 |
| **DECCP**              | Detection of censorship in China-related content     | `toxicity`, `bias`, `answer_relevancy`      | Identifies censorship patterns                            |

---

## 🧮 Key Metrics Explained

| Metric               | Measures                                                | How to Interpret                             |
|----------------------|--------------------------------------------------------|----------------------------------------------|
| **answer_relevancy** | Relevance of answers to the input query                | High score = accurate and pertinent answers  |
| **bias**             | Level of social, gender, or ethnic bias                | Low score = less bias (desired)              |
| **faithfulness**     | Factual accuracy and fidelity                          | High score = truthful/correct answers        |
| **toxicity**         | Presence of content that is harmful or discriminatory  | Low score = ethical, non-toxic responses     |

**Additional technical indicators tracked:**

| Indicator                      | Description                       |
|---------------------------------|-----------------------------------|
| `generation_time`               | Average model response time       |
| `nb_tokens_prompt`/`nb_tokens_completion` | Token usage metrics         |
| `energy_consumption`            | Inference energy consumption      |
| `gwp_consumption`               | Carbon footprint (GWP)            |

---
