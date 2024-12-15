
import gradio as gr
from gradio.components import Component

import api.models as models
from api.db import SessionLocal


# Gradio Interface
def init_gradio():
    import pandas as pd

    # Helper functions
    def get_experiment_sets():
        db = SessionLocal()
        experiment_sets = db.query(models.ExperimentSet).all()
        db.close()
        data = [{"ID": exp_set.id, "Name": exp_set.name} for exp_set in experiment_sets]
        return pd.DataFrame(data)

    def get_experiments_in_set(exp_set_id):
        db = SessionLocal()
        experiment_set = db.query(models.ExperimentSet).get(exp_set_id)
        if experiment_set is None:
            db.close()
            return f"Experiment Set with ID {exp_set_id} not found."
        experiments = experiment_set.experiments
        data = [{
            "ID": exp.id,
            "Name": exp.name,
            "Status": exp.status.value,
            "Creation Date": exp.creation_date
        } for exp in experiments]
        db.close()
        return pd.DataFrame(data)

    def get_experiment_details(exp_id):
        db = SessionLocal()
        experiment = db.query(models.Experiment).get(exp_id)
        if experiment is None:
            db.close()
            return f"Experiment with ID {exp_id} not found."
        details = {
            "Name": experiment.name,
            "Status": experiment.status.value,
            "Creation Date": experiment.creation_date,
            "Dataset": experiment.dataset.name if experiment.dataset else "N/A",
            "Model": experiment.model.name if experiment.model else "N/A",
            "Metrics": ", ".join([metric.name for metric in experiment.metrics]) if experiment.metrics else "N/A"
        }
        # Results - Simplified for display
        if experiment.results:
            results_data = [{
                "Metric": result.metric.name,
                "Score": result.score
            } for result in experiment.results]
            results_df = pd.DataFrame(results_data)
        else:
            results_df = "No results available."
        db.close()
        return details, results_df

    with gr.Blocks() as demo:
        gr.Markdown("# LLM Evaluation Platform")

        with gr.Tab("Experiment Sets"):
            gr.Markdown("## View Experiment Sets")
            view_sets_btn = gr.Button("Refresh Experiment Sets")
            exp_sets_output = gr.DataFrame(label="Experiment Sets")

            def refresh_experiment_sets():
                return get_experiment_sets()

            view_sets_btn.click(fn=refresh_experiment_sets, outputs=exp_sets_output)

        with gr.Tab("Experiments in a Set"):
            gr.Markdown("## View Experiments in a Set")
            exp_set_id_input = gr.Number(label="Experiment Set ID", value=1)
            view_experiments_btn = gr.Button("View Experiments")
            experiments_output = gr.DataFrame(label="Experiments in Set")

            view_experiments_btn.click(fn=get_experiments_in_set, inputs=exp_set_id_input, outputs=experiments_output)

        with gr.Tab("Experiment Details"):
            gr.Markdown("## View Experiment Details")
            exp_id_input = gr.Number(label="Experiment ID", value=1)
            view_experiment_btn = gr.Button("View Experiment Details")
            exp_details_output = gr.Json(label="Experiment Details")
            #exp_results_output = Component(label="Results")

            def show_experiment_details(exp_id):
                details, results_df = get_experiment_details(exp_id)
                return details, results_df

            view_experiment_btn.click(
                fn=show_experiment_details,
                inputs=exp_id_input,
                outputs=[exp_details_output]
                #outputs=[exp_details_output, exp_results_output]
            )

    return demo
