from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import json
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def get_sample_responses(filepath, count=5):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    return lines[:count]


def build_system_prompt(responses):
    prompt = (
        """
        You are Hitesh Choudhary, who's a passionate tech mentor and content creator.
        Tone: You generally have to speak in a mix of Hindi and English, you have to sound humble, friendly and honest at the same time. Use expressions like "bhai", "arre", "hanji kaise hain aap sabhi", "toh chaliye shuru karte hain", "chaliye", and jokes when needed but don't use them way too frequently, keep it subtle. Also make sure to take reference to chai very frequently as his online learning platform is based all on "Chai aur Code".

        Here are examples of how you talk:\n
        """
    )
    for i, r in enumerate(responses, start=1):
        prompt += f"{i}. {r}\n"
    prompt += "\nStick to this tone and vibe in all your responses."
    return prompt


def save_conversation(user_input, bot_output, filename="chat_history.json"):
    data = {"user": user_input, "hitesh_bot": bot_output}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            chat_data = json.load(f)
    else:
        chat_data = []

    chat_data.append(data)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)


GREETING = (
    "Hanji kaise hain aap sabhi! Main Hitesh hoon — chai lo, baith jao, "
    "aur puchiye jo poochna hai. Toh chaliye shuru karte hain ☕"
)


def start_persona_chat():
    # Seed the persona through chat history so the app loads without an API call.
    return model.start_chat(
        history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": [GREETING]},
        ]
    )

sample_responses = get_sample_responses("hitesh_transcript_clean.txt")
system_prompt = build_system_prompt(sample_responses)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"
)

st.set_page_config(page_title="Hitesh Choudhary AI", page_icon="🤖", layout="centered")

st.markdown(
    """
    <style>
      #MainMenu { visibility: hidden; }
      header[data-testid="stHeader"] { background: transparent; }
      .stChatMessage { padding-top: 0.4rem; padding-bottom: 0.4rem; }
      div[data-testid="stChatInput"] {
        border: 1px solid rgba(35, 79, 54, 0.4);
        border-radius: 12px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Hitesh Choudhary Chatbot ☕")
st.caption("Full-stack, DSA, career, consistency — ask anything, chai-flavored answers guaranteed.")

if "chat" not in st.session_state:
    st.session_state.chat = start_persona_chat()

if "messages" not in st.session_state:
    st.session_state.messages = [("assistant", GREETING)]


def send_message(user_input):
    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... chai ke saath response leke aate hain..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                reply = response.text
            except Exception:
                reply = (
                    "Arre, something went wrong while reaching Gemini. "
                    "Check the API key and try again bhai."
                )
                failed = True
            else:
                failed = False
        st.markdown(reply)

    st.session_state.messages.append(("assistant", reply))

    if not failed:
        save_conversation(user_input, reply)


example_prompts = [
    "How do I start learning full-stack development?",
    "Sir DSA tough lagti hai, kaise seekha jaye ?",
    "Backend vs frontend: kya choose karun?",
    "How to become a DevOps engineer?",
    "Sir GenAI ka course kab launch kar rahe ho ?",
    "Sir how to be consistent ?"
]

st.markdown("### 💡 Example Prompts")
for row_start in range(0, len(example_prompts), 2):
    columns = st.columns(2)
    for column, prompt in zip(columns, example_prompts[row_start:row_start + 2]):
        with column:
            if st.button(prompt, key=f"example_{prompt}", use_container_width=True):
                send_message(prompt)
                st.rerun()

if st.button("🧹 Clear Chat"):
    st.session_state.chat = start_persona_chat()
    st.session_state.messages = [("assistant", GREETING)]
    st.rerun()

for role, message in st.session_state.messages:
    avatar = "🧑‍💻" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

user_input = st.chat_input("Type your own question 👇")

if user_input:
    send_message(user_input)
