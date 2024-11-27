# Demo Notebooks

We offer several notebooks designed to demonstrate how to use the API and to provide baseline evaluation results. You can use these as inspiration to develop and propose new and original evaluation experiments.

The available notebooks are:

- **[run_experiments_demo](/notebooks/run_experiments_demo.ipynb):** This notebook runs individual experiments on various large language models (LLMs) with a specified set of metrics. It aggregates and presents the results in a consolidated table, showing the mean and standard deviation for the corpus questions.

- **[run_grid_repeat](/notebooks/run_grid_repeat_demo.ipynb):** This notebook conducts a set of related experiments (Experiment Set) on several LLMs using a specified set of metrics and a **repetition parameter**. It aggregates and displays the results in a consolidated table, highlighting the mean and standard deviation of the experiment repetitions to illustrate model variability. This notebook also includes graphs depicting score dispersion for each model across all metrics.

- **[run_grid_raglimit](/notebooks/run_grid_raglimit_demo.ipynb):** This notebook conducts a series of related experiments (Experiment Set) on several retrieval-augmented generation (RAG) LLM models with a given set of metrics and performs a **grid search** on the `limit` parameters (which refers to the number of chunk limits in a RAG setting). It compiles and presents the results in a consolidated table, showing the mean results for the corpus questions.

- **[run_dataset_experiences_demo](/notebooks/run_dataset_experiences_demo.ipynb):** This notebook runs individual experiments on a given dataset with a specified set of metrics. It aggregates and presents the results in a consolidated table and offers graphical visualisations.
