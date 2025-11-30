import os
import base64
import mimetypes
import sys
from dotenv import load_dotenv # Tuodaan dotenv
import google.generativeai as genai

# --- ASETUKSET ---

# 1. Ladataan ympäristömuuttujat .env -tiedostosta
load_dotenv()

# Haetaan API-avain turvallisesti.
# Jos avainta ei löydy, API_KEY on None.
API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Määritä lähdetiedostot
INPUT_FILES = {
    "markdown": "sisalto.md",
    "css": "tyyli.css",
    "images": ["kuva1.jpg", "logo.png"] 
}

# 3. Tulostiedosto
OUTPUT_FILE = "index.html"

# 4. Valitse malli
MODEL_NAME = "gemini-1.5-flash"

# --- APUFUNKTIOT ---

def setup_demo_files():
    """Luo testiaineistoa, jos tiedostoja ei ole olemassa."""
    if not os.path.exists(INPUT_FILES["markdown"]):
        with open(INPUT_FILES["markdown"], "w", encoding="utf-8") as f:
            f.write("# Turvallinen Gemini-generointi\n\nTämä sivu käyttää .env tiedostoa api-avaimelle.")
        print(f"Luotiin demotiedosto: {INPUT_FILES['markdown']}")

    if not os.path.exists(INPUT_FILES["css"]):
        with open(INPUT_FILES["css"], "w", encoding="utf-8") as f:
            f.write("body { font-family: sans-serif; padding: 20px; background: #f0f0f0; }")
        print(f"Luotiin demotiedosto: {INPUT_FILES['css']}")

def get_base64_image(file_path):
    """Lukee kuvatiedoston ja palauttaa sen data-URI Base64 -muodossa."""
    if not os.path.exists(file_path):
        # Hiljainen ohitus tai varoitus riippuen tarpeesta
        return None
    
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/png"

    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"Virhe kuvan {file_path} käsittelyssä: {e}")
        return None

def read_text_file(file_path):
    """Lukee tekstitiedoston sisällön."""
    if not os.path.exists(file_path):
        return f""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_response(text):
    """Poistaa markdown-koodimerkit vastauksesta."""
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text

# --- PÄÄOHJELMA ---

def main():
    # 0. Tarkistetaan, että API-avain on olemassa
    if not API_KEY:
        print("❌ VIRHE: API-avain puuttuu!")
        print("   Varmista, että olet luonut .env -tiedoston ja lisännyt sinne rivin:")
        print("   GOOGLE_API_KEY=sinun_avaimesi")
        sys.exit(1) # Lopetetaan ohjelma virhekoodilla

    # Konfiguroidaan Gemini
    genai.configure(api_key=API_KEY)
    
    setup_demo_files()

    print("🔄 Luetaan tiedostoja ja koodataan kuvia...")

    md_content = read_text_file(INPUT_FILES["markdown"])
    css_content = read_text_file(INPUT_FILES["css"])

    image_data_prompt = ""
    for idx, img_path in enumerate(INPUT_FILES["images"]):
        b64_data = get_base64_image(img_path)
        if b64_data:
            image_id = f"IMAGE_{idx+1}"
            image_data_prompt += f"\n[{image_id}]: {b64_data}\n(Lähdetiedosto: {img_path})\n"

    # Rakennetaan prompti
    full_prompt = f"""
    Toimi asiantuntevana Front End -kehittäjänä. Luo yksi itsenäinen HTML5-tiedosto (index.html).

    1. SISÄLTÖ (Markdown -> HTML):
    ---
    {md_content}
    ---

    2. TYYLI (CSS -> <style>):
    ---
    {css_content}
    ---

    3. KUVAT (Base64 -> <img src="data...">):
    Käytä näitä valmiiksi koodattuja lähteitä, kun tarvitset kuvaa sisällön perusteella:
    {image_data_prompt}

    OHJEET:
    - Tulosta vain validia HTML-koodia.
    - Ei selityksiä, ei markdown-blokkeja (```).
    """

    print("🚀 Lähetetään pyyntö Geminille...")

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(full_prompt)
        
        final_html = clean_response(response.text)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"✅ Valmis! Sivusto tallennettu: {OUTPUT_FILE}")

    except Exception as e:
        print(f"\n❌ Tapahtui virhe API-kutsussa: {e}")

if __name__ == "__main__":
    main()
