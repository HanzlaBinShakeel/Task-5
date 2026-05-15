"""
CLI and Streamlit interface for the empathetic mental health support chatbot.
"""

from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_DIR = Path(__file__).parent / "model"
BASE_MODEL = "distilgpt2"

SYSTEM_PREFIX = (
    "You are a gentle, empathetic mental wellness companion. "
    "Offer supportive, non-judgmental responses. "
    "Do not diagnose or replace professional therapy.\n"
)

WELLNESS_FALLBACKS = {
    "stress": (
        "That sounds really hard, and it makes sense you feel pressured. "
        "Try breaking things into small steps and give yourself short breaks. You are doing your best."
    ),
    "anxious": (
        "I'm sorry you are going through this. Anxiety can feel overwhelming. "
        "Slow breathing and talking to someone you trust may help. You are not alone."
    ),
    "anxiety": (
        "I'm sorry you are going through this. Anxiety can feel overwhelming. "
        "Slow breathing and talking to someone you trust may help. You are not alone."
    ),
    "sleep": (
        "Lack of sleep can make everything feel harder. A calm bedtime routine may help. "
        "If this continues, reaching out to a health professional is a caring step."
    ),
    "lonely": (
        "Feeling lonely is painful, and your feelings are valid. "
        "Even a small connection today — a message or a walk — can help a little."
    ),
    "sad": (
        "I'm sorry you feel this way. Sadness can be heavy. Be gentle with yourself today, "
        "and consider talking to someone you trust if it stays with you."
    ),
    "exam": (
        "Exam stress is very common. Prepare in small blocks, rest, and remember one result "
        "does not define your worth. You have handled hard things before."
    ),
}


def _fallback_reply(message: str) -> str | None:
    m = message.lower()
    for key, text in WELLNESS_FALLBACKS.items():
        if key in m:
            return text
    return None


class EmpatheticBot:
    def __init__(self, model_path: Path | None = None):
        path = model_path or MODEL_DIR
        if path.exists() and (path / "config.json").exists():
            print(f"Loading fine-tuned model from {path}")
            self.tokenizer = AutoTokenizer.from_pretrained(str(path))
            self.model = AutoModelForCausalLM.from_pretrained(str(path))
        else:
            print("Fine-tuned weights not found — using base DistilGPT2.")
            print("Run: python train_empathetic.py")
            self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
            self.model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def reply(self, user_message: str, max_new_tokens: int = 60) -> str:
        fallback = _fallback_reply(user_message)
        if fallback:
            return fallback

        prompt = f"User: {user_message}\nSupportive friend:"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        full = self.tokenizer.decode(out[0], skip_special_tokens=True)
        if "Supportive friend:" in full:
            text = full.split("Supportive friend:")[-1].strip()
        else:
            text = full[len(prompt) :].strip()
        # Use fallback if model output is too short or repetitive
        if len(text) < 25 or text.count("When you") > 1:
            return _fallback_reply(user_message) or (
                "I hear that this is difficult for you. Your feelings matter, "
                "and it is okay to take things one step at a time."
            )
        return text


def run_cli():
    bot = EmpatheticBot()
    print("Mental Wellness Support Chat (type 'quit' to exit)")
    print("Note: This is not professional therapy.\n")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in {"quit", "exit", "q"}:
            break
        print(f"Friend: {bot.reply(msg)}\n")


if __name__ == "__main__":
    run_cli()
