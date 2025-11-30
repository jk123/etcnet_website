import os
import glob
import base64
import mimetypes
import google.generativeai as genai
from pathlib import Path

# --- ASETUKSET ---
# Määritä kansio, jossa lähdetiedostot ovat (css, js, kuvat, md, jne.)
SOURCE_FOLDER = "projektin_tiedostot"
OUTPUT_FILENAME = "index.html"

# Käytetään Flash-mallia sen suuren konteksti-ikkunan vuoksi (tärkeää Base64-kuville)
MODEL_NAME = "gemini-1.5-flash"

def setup_api():
    """Hakee API-avaimen turvallisesti ympäristömuuttujasta."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\nVIRHE: API-avain puuttuu.")
        print("Aseta se Fedorassa komennolla: export GOOGLE_API_KEY='sinun_avaimesi'")
        exit(1)
    genai.configure(api_key=api_key)

def get_mime_type(filepath):
    """Päättelee tiedoston MIME-tyypin."""
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type or "application/octet-stream"

def encode_file_to_base64(filepath):
    """Lukee binääritiedoston (kuva) ja muuntaa sen base64-merkkijonoksi."""
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def read_text_file(filepath):
    """Lukee tekstitiedoston sisällön."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Jos ei ole utf-8, oletetaan binääriksi ja palautetaan None käsiteltäväksi muualla
        return None

def collect_project_files():
    """Kerää tiedostot ja valmistelee ne promptia varten."""
    files_data = []
    
    # Etsitään kaikki tiedostot alikansiosta
    search_path = os.path.join(SOURCE_FOLDER, "**", "*.*")
    # recursive=True vaatii python 3.5+
    all_files = glob.glob(search_path, recursive=True)

    if not all_files:
        print(f"Ei tiedostoja kansiossa '{SOURCE_FOLDER}'. Luo kansio ja lisää sinne materiaalia.")
        exit()

    print(f"Luetaan {len(all_files)} tiedostoa kansiosta '{SOURCE_FOLDER}'...")

    prompt_parts = [
        "Olet taitava Frontend-kehittäjä ja automaatioinsinööri.",
        "Tehtäväsi on yhdistää seuraavat tiedostot ja resurssit YHDEKSI ainoaksi HTML5-tiedostoksi (index.html).",
        "VAATIMUKSET:",
        "1. Kaikki CSS on oltava <style>-tageissa.",
        "2. Kaikki Javascript on oltava <script>-tageissa.",
        "3. Kaikki kuvat ja media (png, jpg, webp) ON UPOTETTAVA base64-muodossa suoraan <img> tagien src-attribuutteihin.",
        "4. Markdown-tiedostot (MD) tulee muuntaa HTML-muotoon ja asettaa sivun sisällöksi loogiseen järjestykseen.",
        "5. JSON/XML-datan voit hyödyntää sisällön rakentamisessa tai visualisoinnissa.",
        "6. Älä lyhennä koodia tai Base64-merkkijonoja. Tulosta koko tiedosto toimivana.",
        "7. Lisää moderni ja responsiivinen CSS-tyylittely, jos lähdetiedostoissa ei ole tyylejä.",
        "\nTässä ovat lähdetiedostot:\n"
    ]

    for filepath in all_files:
        filename = os.path.basename(filepath)
        mime_type = get_mime_type(filepath)
        
        print(f"  - Käsitellään: {filename} ({mime_type})")

        # Tarkistetaan onko tekstiä vai binääriä
        text_content = read_text_file(filepath)

        if text_content is not None:
            # Tekstitiedostot (koodi, md, json, xml)
            prompt_parts.append(f"\n--- TIEDOSTO: {filename} (Tyyppi: {mime_type}) ---\n{text_content}\n")
        else:
            # Binääritiedostot (kuvat, fontit)
            b64_string = encode_file_to_base64(filepath)
            prompt_parts.append(f"\n--- TIEDOSTO: {filename} (Tyyppi: {mime_type}) ---\n")
            prompt_parts.append(f"Tämä on binääritiedosto. Käytä seuraavaa Base64-dataa upotukseen:\ndata:{mime_type};base64,{b64_string}\n")

    prompt_parts.append("\n\nLuo nyt lopullinen index.html tiedosto. Vastaa pelkällä koodilla ilman markdown-blokkeja (```html).")
    return prompt_parts

def main():
    setup_api()
    
    # 1. Kerää aineisto
    prompt_content = collect_project_files()
    
    # 2. Lähetä Geminiin
    print("Lähetetään aineistoa Geminille (tämä voi kestää hetken riippuen kuvien määrästä)...")
    model = genai.GenerativeModel(MODEL_NAME)
    
    # Yhdistetään prompt listasta stringiksi
    full_prompt = "\n".join(prompt_content)
    
    try:
        response = model.generate_content(full_prompt)
        
        # 3. Käsittele vastaus
        html_content = response.text
        
        # Siivotaan mahdolliset markdown-merkinnät jos Gemini ne kuitenkin laittoi
        html_content = html_content.replace("```html", "").replace("```", "")
        
        # 4. Tallenna
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\nValmis! Tiedosto tallennettu nimellä: {OUTPUT_FILENAME}")
        print("Voit avata sen selaimessa.")

    except Exception as e:
        print(f"\nVirhe generoinnissa: {e}")

if __name__ == "__main__":
    main()

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
