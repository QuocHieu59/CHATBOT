# Chatbot LLM Project

Welcome to the Chatbot LLM project!

## Features

- **Model**: Llama 3.2 3B .
- **Fine-tuning**: Customizes the LLM to suit specific industries or applications.
- **Server**: t.me/Salewood_bot (API Telegram)
- **Dataset train**: https://huggingface.co/datasets/Quoc59/QA-wood-products
- **Dataset eval**: https://huggingface.co/datasets/Quoc59/Eval_QA_Wood
- **Model after finetune**: https://huggingface.co/Quoc59/llama-3.2-3b-ChatBot-woodproduct
- **Model Quantization (4 bit)**: https://huggingface.co/Quoc59/llama-3.2-3b-ChatBot-woodproduct-Q4_K_M-GGUF

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/QuocHieu59/CHATBOT/tree/main
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install LM Studio app**: add model from Huggingface to LM studio. Then run model.

---

## Usage

1. **Run the chatbot**:

   ```bash
   python src/Telechat.py
   ```

2. **Interacting with the chatbot**:

   The chatbot can be accessed via:

   - API calls Telegram with link: t.me/Salewood_bot

---

## Fine-tuning

1. **Prepare dataset**: https://huggingface.co/datasets/Quoc59/QA-wood-products

2. **Fine-tune the model**: Use Kaggle (Finetune_llama-3-2-3b.ipynp)

3. **Quantization**: Use HuggingFace API (merging-and-exporting.ipynp)

---

## Eval Chatbot

1. **dataset**: https://huggingface.co/datasets/Quoc59/Eval_QA_Wood
2. **Eval**: Use Kaggle (eval-chatbot.ipynp)
