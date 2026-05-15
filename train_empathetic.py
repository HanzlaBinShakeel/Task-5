"""
Fine-tune DistilGPT2 on empathetic dialogues using Hugging Face Trainer API.
Uses local EmpatheticDialogues-style JSONL (assignment dataset format).
Run: python train_empathetic.py
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilgpt2"
OUTPUT_DIR = Path(__file__).parent / "model"
DATA_FILE = Path(__file__).parent / "data" / "empathetic_train.jsonl"
MAX_LENGTH = 128
MAX_EPOCHS = 3


def load_local_dataset() -> Dataset:
    """Load training lines from JSONL (EmpatheticDialogues-style)."""
    texts = []
    with open(DATA_FILE, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            t = row.get("text", "").strip()
            if len(t) > 30:
                texts.append(t)
    # Repeat data for enough training steps on small model
    texts = texts * 15
    return Dataset.from_dict({"text": texts})


def main():
    print("Loading empathetic training data...")
    train = load_local_dataset()
    print(f"Training samples: {len(train)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )

    tokenized = train.map(tokenize, batched=True, remove_columns=["text"])
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=MAX_EPOCHS,
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        learning_rate=5e-5,
        warmup_steps=50,
        logging_steps=25,
        save_steps=200,
        save_total_limit=1,
        fp16=False,
        report_to="none",
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=collator,
    )

    print("Starting fine-tuning (Hugging Face Trainer)...")
    trainer.train()
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    print(f"Model saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
