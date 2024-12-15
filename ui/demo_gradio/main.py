import gradio as gr

from .views import (
    datasets_view,
    experiment_sets_view,
    experiments_view,
    metrics_view,
    models_view,
)


def init_gradio():

    with gr.Blocks(css="assets/main.css") as demo:

        with gr.Row():

            with gr.Column(scale=1, min_width=200):

                # Left Navigation Menu
                with gr.Blocks():
                    gr.Markdown("## Menu")
                    nav_choice = gr.Radio(
                        choices=["Experiment Sets", "Metrics", "Models", "Datasets"],
                        value="Experiment Sets",
                        label="",
                    )

            with gr.Column(scale=5):

                content = gr.Column()

                def render_view(choice):

                    content.children = []  # Clear previous content

                    if choice == "Experiment Sets":
                        with content:
                            experiment_sets_view()
                    elif choice == "Metrics":
                        with content:
                            metrics_view()
                    elif choice == "Models":
                        with content:
                            models_view()
                    elif choice == "Datasets":
                        with content:
                            datasets_view()

                nav_choice.change(fn=render_view, inputs=nav_choice, outputs=[])

                # Initial View
                render_view(nav_choice.value)

    return demo

if __name__ == "__main__":
    demo = init_gradio()
    demo.launch()
