from transformers import T5Tokenizer, T5ForConditionalGeneration

MODEL_NAME = "t5-small"

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def summarize_text(text):
    """
    Summarize text using T5-small.
    """
    text = "summarize: " + text

    inputs = tokenizer.encode(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    summary_ids = model.generate(
        inputs,
        max_length=150,
        min_length=40,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
