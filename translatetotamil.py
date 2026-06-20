from deep_translator import GoogleTranslator
def translatetotamil(english_text: str) -> str:
    return GoogleTranslator(source="en", target="ta").translate(english_text)
if __name__ == "__main__":
    sample = "The price is 50000 rupees ."
    print("English :", sample)
    print("Tamil   :", translatetotamil(sample))