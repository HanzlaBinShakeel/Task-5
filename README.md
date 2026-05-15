# Task 5: Mental Health Support Chatbot (Fine-Tuned)

## Objective
Fine-tune a small LLM on **EmpatheticDialogues** for empathetic, supportive wellness conversation.

## Model & Dataset
| Item | Choice |
|------|--------|
| Base model | DistilGPT2 |
| Dataset | EmpatheticDialogues-style JSONL (`data/empathetic_train.jsonl`) |
| Training | Hugging Face `Trainer` API |

## Workflow
1. Explore dialogues in the notebook
2. Fine-tune: `python train_empathetic.py` (~1–2 min; saves to `model/`)
3. **Web UI (recommended):** `streamlit run streamlit_app.py`
4. CLI chat: `python chat_app.py`

> **Note:** The trained `model/` folder is not in GitHub (too large). Run `train_empathetic.py` after cloning.

## Key Results
- Model learns listener-style empathetic replies
- Gentle system prefix enforces supportive, non-diagnostic tone
- Fine-tuned weights saved to `model/` (gitignored — run training locally)

## Disclaimer
Not professional therapy. Crisis situations → contact a licensed counselor or helpline.

## Files
| File | Description |
|------|-------------|
| `mental_health_chatbot.ipynb` | Exploration + testing |
| `train_empathetic.py` | Fine-tuning script |
| `chat_app.py` | CLI chat interface |
| `streamlit_app.py` | Modern web UI — MindCare Companion |
| `ui_styles.py` | Custom CSS theme |

## Run
```bash
pip install -r ../requirements.txt
python train_empathetic.py
jupyter notebook mental_health_chatbot.ipynb
```
