# Demo Notebooks

We offer several notebooks designed to demonstrate how to use the API and to provide baseline evaluation results. You can use these as inspiration to develop and propose new and original evaluation experiments.

The available notebooks are:

- **[run_evals_with_crossvalidation](/notebooks/run_evals_with_crossvalidation.ipynb):** This notebook allows you to perform a series of experiments (Experiment Set) on:
    - several LLM models using a specified set of metrics and a **repetition parameter**.
    - multiple RAG-augmented generation LLM models with a given set of metrics and performs a **grid search** on the “limit” parameters (which refer to the number of block limits in an RAG parameter).
    - multiple RAG-augmented generation LLM models with specialized RAG metrics. These RAG metrics use the “search context” (aka chunks) to compute scores.

- **[run_dataset_experiences_demo](/notebooks/run_dataset_experiences_demo.ipynb):** This notebook runs individual experiments on the components of the `dataset itself`.

- **[run_your_own_llm_as_a_judge_metric](/notebooks/run_your_own_llm_as_a_judge_metric.ipynb)**: This notebook provides an example of how to use a `custom metric llm as-a-judge` (ad hoc judge). It is based on  DECCP is a censorchip evaluation about China related questions inspired by the followinw article : https://huggingface.co/blog/leonardlin/chinese-llm-censorship-analysis

- **[run_evals_compliance](/notebooks/run_evals_compliance.ipynb)**: This notebook provides an example of how to run `compliance` evaluation for your IA system (like social biais, toxicity...).

- OCR evaluation: Two notebooks that show how how to use a parquet dataset with images (marker dataset) and run an `OCR evaluation` on it to test some VLMs (Visual Language Model).
    - [create_marker_dataset.ipynb](/notebooks/create_marker_dataset.ipynb)
    - [run_evals_ocr_marker.ipynb](/notebooks/run_evals_ocr_marker.ipynb)

- **[run_an_example_of_toolings_usage](/notebooks/run_an_example_of_toolings_usage.ipynb):** An example of tooling usage.

- **[run_evals_models_raw](/notebooks/run_evals_models_raw.ipynb):** Simple evaluation of the raw Albert models.

- **[run_evals_models_with_rag](/notebooks/run_evals_models_with_rag.ipynb):** RAG evaluation of the Albert models.

- **[rd_evalap_is_your_own_ia_system](/notebooks/rd_evalap_is_your_own_ia_system.ipynb):** An exemple of `sampling dataset` usage, on LegalBenchRAG dataset.
