"""
Mental Wellness Companion — modern Streamlit UI
Run: streamlit run streamlit_app.py
"""

import streamlit as st
from pathlib import Path
from chat_app import EmpatheticBot
from ui_styles import WELLNESS_CSS

st.set_page_config(
    page_title="MindCare Companion",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(WELLNESS_CSS, unsafe_allow_html=True)

MOOD_PROMPTS = {
    "😰 Stressed": "I feel really stressed about my exams.",
    "😔 Anxious": "I have been anxious and cannot sleep.",
    "😢 Sad": "I feel sad and don't know why.",
    "😓 Overwhelmed": "Work is overwhelming me lately.",
    "😔 Lonely": "I feel lonely lately.",
    "😤 Angry": "I am angry at myself today.",
}


def init_session():
    if "bot" not in st.session_state:
        with st.spinner("Loading your wellness companion..."):
            st.session_state.bot = EmpatheticBot()
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi there 💚 I'm here to listen with empathy. "
                    "Share what's on your mind — stress, anxiety, or anything weighing on you. "
                    "I'm not a therapist, but I can offer gentle support."
                ),
            }
        ]


def main():
    init_session()

    with st.sidebar:
        st.markdown("### 🎭 How are you feeling?")
        for label, prompt in MOOD_PROMPTS.items():
            if st.button(label, use_container_width=True, key=f"mood_{label}"):
                st.session_state.pending = prompt

        st.markdown("---")
        st.markdown("### ✨ Quick tips")
        st.caption("🌬️ Breathe — 4 sec in, 4 hold, 6 out")
        st.caption("📝 Journal one feeling without judgment")
        st.caption("🚶 Take a 10-minute walk")
        st.caption("💬 Message someone you trust")

        st.markdown("---")
        model_ok = (Path(__file__).parent / "model" / "config.json").exists()
        st.metric("Model", "Fine-tuned ✓" if model_ok else "Run training")
        st.caption("DevelopersHub — Task 5")

        if st.button("🗑️ New conversation", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Fresh start 💚 What's on your mind today?"}
            ]
            st.rerun()

    col_chat, col_side = st.columns([2.3, 1])

    with col_chat:
        st.markdown(
            """
            <motion-hero class="hero-banner">
                <h1>💚 MindCare Companion</h1>
                <p>Fine-tuned empathetic support for stress, anxiety & emotional wellness.
                DistilGPT2 + Hugging Face Trainer API.</p>
            </motion-hero>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <motion-disclaimer class="disclaimer-box">
            💜 <strong>You're not alone.</strong> Supportive AI only — not professional therapy.
            In crisis, contact a helpline or emergency services.
            </motion-disclaimer>
            """,
            unsafe_allow_html=True,
        )

        for msg in st.session_state.messages:
            avatar = "💚" if msg["role"] == "assistant" else "🙂"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        prompt = st.session_state.pop("pending", None) or st.chat_input(
            "Share what's on your mind..."
        )

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🙂"):
                st.markdown(prompt)
            with st.chat_message("assistant", avatar="💚"):
                with st.spinner("Listening with care..."):
                    reply = st.session_state.bot.reply(prompt)
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

    with col_side:
        st.markdown("### 🧠 About")
        st.info(
            "Fine-tuned DistilGPT2 on empathetic dialogues with gentle, "
            "non-judgmental responses."
        )
        st.markdown("**Run locally**")
        st.code("pip install -r requirements.txt\npython train_empathetic.py\nstreamlit run streamlit_app.py")
        st.markdown("**CLI chat**")
        st.code("python chat_app.py", language="bash")


if __name__ == "__main__":
    main()
