from datetime import datetime

import gradio as gr

from ui.utils import (
    delete_experiment_set,
    get_datasets,
    get_experiment_sets,
    get_experiments,
    get_metrics,
    get_models,
)


def experiment_sets_view():

    with gr.Column():

        gr.Markdown("# Experiment Sets")

        experiment_set_table = gr.Dataframe(
            headers=["ID", "Name", "Experiments", "Created At", "Actions"],
            datatype=["number", "str", "number", "date", "str"],
        )

        def load_experiment_sets():
            sets = get_experiment_sets()
            data = []
            for s in sets:
                data.append([
                    s['id'],
                    s['name'],
                    len(s.get('experiments', [])),
                    datetime.fromisoformat(s['creationDate']).strftime('%Y-%m-%d %H:%M'),
                    "",
                ])
            return data

        def delete_set(set_id):
            delete_experiment_set(set_id)
            return load_experiment_sets()

        experiment_set_table.value = load_experiment_sets()

        # Set up actions (Edit/Delete) - For simplicity, we'll handle only Delete in this example
        # Add buttons or other interactive elements as needed

    return experiment_set_table

def experiments_view(set_id):

    with gr.Column():

        gr.Markdown(f"## Experiments in Set {set_id}")

        experiments_table = gr.Dataframe(
            headers=["ID", "Name", "Status", "Created At"],
            datatype=["number", "str", "str", "date"],
        )

        def load_experiments():
            experiments = get_experiments(set_id)
            data = []
            for e in experiments:
                data.append([
                    e['id'],
                    e['name'],
                    e['status'],
                    datetime.fromisoformat(e['creationDate']).strftime('%Y-%m-%d %H:%M'),
                ])
            return data

        experiments_table.value = load_experiments()

    return experiments_table

def metrics_view():

    with gr.Column():

        gr.Markdown("# Metrics")

        metrics = get_metrics()

        for metric in metrics:
            with gr.Group():
                gr.Markdown(f"### {metric['name']}")
                gr.Markdown(metric.get('description', 'No description available.'))

    return

def datasets_view():

    with gr.Column():

        gr.Markdown("# Datasets")

        datasets = get_datasets()

        for dataset in datasets:
            with gr.Group():
                gr.Markdown(f"### {dataset['name']}")
                gr.Markdown(dataset.get('description', 'No description available.'))

    return

def models_view():

    with gr.Column():

        gr.Markdown("# Models")

        models = get_models()

        for model in models:
            with gr.Group():
                gr.Markdown(f"### {model['name']}")
                gr.Markdown(model.get('description', 'No description available.'))

    return
