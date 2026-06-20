# this file is translating tamil text to english , imported into whisper.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
TAMIL = "tam_Taml"
ENGLISH = "eng_Latn"
def translatetoenglish(text: str) -> str:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    tokenizer.src_lang = TAMIL
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(ENGLISH)
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=200
    )
    result = tokenizer.decode(
        translated_tokens[0],
        skip_special_tokens=True
    )
    return result
if __name__ == "__main__":
    sample = "வணக்கம்"
    print("English:", translatetoenglish(sample))