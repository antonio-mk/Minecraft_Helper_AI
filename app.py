import gradio as gr
import os
import groq

# load API key
api_key = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
client = groq.Groq(api_key=api_key)

# define system prompt with Minecraft focus
system_prompt = """You are a Minecraft AI expert. You ONLY answer Minecraft-related questions.
If a user asks about crafting, survival, Redstone, or commands, give clear, accurate answers.
If a question is not about Minecraft, say: 'I only answer Minecraft-related questions.'"""

# function to get responses from Groqs API
def respond(message, history):
    if history is None:
        history = []  # history is initialized

    messages = [{"role": "system", "content": system_prompt}]

    # add chat history
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # add new user message
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        bot_response = f"Error: {str(e)} (Check API key & model name)"

    # update chat history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_response})

    return history, ""

# custom styling for Minecraft UI
css = f"""
@import url('https://fonts.cdnfonts.com/css/minecraft-4');
h1 {{
    text-align: center;
    font-family: 'Minecraft', sans-serif;
    color: #34eb4f;
    text-shadow: 2px 2px 0px #000;
}}
body {{
    background-image: url('https://i.pinimg.com/736x/09/6f/be/096fbe5269d2fae069305fe2742d5be5.jpg'); /* New Background */
    background-size: cover;
    font-family: 'Minecraft', sans-serif;
}}
.gradio-container {{
    max-width: 900px; /* bigger chat window */
    height: 700px; /* mkae sure main container is large enough */
    margin: auto;
    background-color: rgba(0, 0, 0, 0.8);
    padding: 20px;
    border-radius: 15px;
}}
/* Increase chat window height */
.gr-chatbot {{
    height: 600px !important;  /* force chat window to be taller */
    max-height: 80vh !important; /* responsive scaling */
    overflow-y: auto !important; /* enable scrolling */
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.gr-chatbot .chat-message {{
    animation: fadeIn 0.3s ease-in-out;
}}
button {{
    font-family: 'Minecraft', sans-serif;
    background-color: #34eb4f;
    color: black;
    border: 2px solid #000;
    padding: 8px 15px;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}}
button:hover {{
    background-color: #2aa831;
    transform: scale(1.05);
}}
"""

# create the UI layout
with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1>🟩 Minecraft Helper AI 🟩</h1>")

    chatbot = gr.Chatbot(type="messages", height=600)  # Increased chat window size
    with gr.Row():
        message = gr.Textbox(placeholder="Ask me anything about Minecraft...", scale=4, show_label=False)
        send_btn = gr.Button("Send", scale=1)

    # chatbox interactions
    message.submit(respond, inputs=[message, chatbot], outputs=[chatbot, message])
    send_btn.click(respond, inputs=[message, chatbot], outputs=[chatbot, message])

# launch
if __name__ == "__main__":
    demo.launch()
