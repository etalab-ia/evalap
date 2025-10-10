# Demo Notebooks

We offer several notebooks designed to demonstrate how to use the API and to provide baseline evaluation results. You can use these as inspiration to develop and propose new and original evaluation experiments.

The available notebooks are:

- **[run_experiments_demo](/notebooks/run_experiments_demo.ipynb):** (**DEPRECATED**: this notebook is fonctional, but we encourage to use experiment_set instead of "orphan" experiment when designing an evaluation, except if your intent is just to test/debug.) This notebook runs individual experiments on various large language models (LLMs) with a specified set of metrics. It aggregates and presents the results in a consolidated table, showing the mean and standard deviation for the corpus questions.

- **[run_set_repeat](/notebooks/run_set_repeat_demo.ipynb):** This notebook conducts a set of related experiments (Experiment Set) on several LLMs using a specified set of metrics and a **repetition parameter**. It aggregates and displays the results in a consolidated table, highlighting the mean and standard deviation of the experiment repetitions to illustrate model variability. This notebook also includes graphs depicting score dispersion for each model across all metrics.

- **[run_set_raglimit](/notebooks/run_set_raglimit_demo.ipynb):** This notebook conducts a series of related experiments (Experiment Set) on several retrieval-augmented generation (RAG) LLM models with a given set of metrics and performs a **grid search** on the `limit` parameters (which refers to the number of chunk limits in a RAG setting). It compiles and presents the results in a consolidated table, showing the mean results for the corpus questions.

- **[run_set_ragmetrics](/notebooks/run_set_ragmetrics_demo.ipynb):** [WIP] This notebook conducts a series of related experiments (Experiment Set) on several retrieval-augmented generation (RAG) LLM models with specialized RAG metrics. Those RAG metrics use the "retriver context" (aka the chunks) to compute the scores.

- **[run_dataset_experiences_demo](/notebooks/run_dataset_experiences_demo.ipynb):** This notebook runs individual experiments on a given dataset with a specified set of metrics. It aggregates and presents the results in a consolidated table and offers graphical visualisations.

- **[DECCP](/notebooks/deccp.ipynb)**: DECCP is a censorchip evaluation about China related questions inspired by the followinw article : https://huggingface.co/blog/leonardlin/chinese-llm-censorship-analysis

- OCR evaluation: Two notebooks that show how how to use a parquet dataset with images (marker dataset) and run an OCR evaluation on it to test some VLMs (Visual Language Model).
    - [notebooks/create_marker_dataset.ipynb](/notebooks/create_marker_dataset.ipynb)
    - [notebooks/run_ocr.ipynb](/notebooks/run_ocr.ipynb)

- **[albert-eval-brut](/notebooks/albert-raw.ipynb):** Simple evaluation of the raw Albert models.

- **[albert-evals-rag](/notebooks/run_dataset_experiences_demo.ipynb):** RAG evaluation of the Albert models.
