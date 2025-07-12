import requests
from collections import Counter

RAPIDAPI_KEY = "36970ae23amsh9cf572a5718a6a6p10c615jsn90981362e8f9"
RAPIDAPI_HOST = "google-translate113.p.rapidapi.com"

def translate_text(text, source_lang='auto', target_lang='en'):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"

    payload = {
        "from": source_lang,
        "to": target_lang,
        "text": text
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        return result["trans"]  # ✅ The key returned by this API is 'trans'
    except Exception as e:
        print(f" Translation failed for '{text}': {e}")
        return None

def translate_and_analyze_titles(data):
    translated_titles = []

    print("\n\nTranslated Titles:")

    for item in data:
        spanish_title = item['title']
        translated = translate_text(spanish_title)
        if translated:
            translated_titles.append(translated)
            print(f"- {translated}")

    all_words = " ".join(translated_titles).lower().split()
    word_counts = Counter(all_words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    print("\n Below words repeating Twice:\n")
    if repeated_words:
        for word, count in repeated_words.items():
            print(f"- {word}: {count} times")
    else:
        print("No words repeated more than twice.")