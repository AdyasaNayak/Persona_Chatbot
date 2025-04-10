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


sample_responses = get_sample_responses("hitesh_transcript_clean.txt")
system_prompt = build_system_prompt(sample_responses)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"
)


st.set_page_config(page_title="Hitesh Choudhary AI", page_icon="🤖")
st.title("Hitesh Choudhary Chatbot ☕")

if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun() 


if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        system_instruction=system_prompt
    )


example_prompts = [
    "How do I start learning full-stack development?",
    "Sir DSA tough lagti hai, kaise seekha jaye ?",
    "Backend vs frontend: kya choose karun?",
    "How to become a DevOps engineer?",
    "Sir GenAI ka course kab launch kar rahe ho ?",
    "Sir how to be consistent ?"
]

st.markdown("### 💡 Example Prompts")
selected_example = st.selectbox("Pick a question or type your own below 👇", [""] + example_prompts)


user_input = st.text_input("Ask Hitesh Sir something", value=selected_example if selected_example else "", key="user_prompt")


if st.button("Send") and user_input:
    with st.spinner("Thinking... chai ke saath response leke aate hain..."):
        response = st.session_state.chat.send_message(user_input)
        st.write(f"🤖 Hitesh Bot: {response.text}")
        save_conversation(user_input, response.text)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

 

for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑‍💻 You:** {message}")
    else:
        st.markdown(f"**🤖 Hitesh Bot:** {message}")