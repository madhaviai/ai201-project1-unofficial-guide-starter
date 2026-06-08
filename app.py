import gradio as gr

from src.query import ask


def handle_query(question: str):
    if not question.strip():
        return "Enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="CS 482 Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide — CS 482 Applied Algorithms")
    gr.Markdown("Ask about exams, projects, grading, and professor tips. Answers are grounded in retrieved documents.")
    inp = gr.Textbox(label="Your question", placeholder="How does the professor grade DP questions?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
