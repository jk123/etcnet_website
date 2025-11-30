noTässä on täydellinen, yhden tiedoston Python-skripti, joka toteuttaa suunnitelman.
Tämä skripti:
 * Lukee paikalliset tiedostot (Markdown, CSS, Kuvat).
 * Koodaa kuvat Base64-muotoon automaattisesti.
 * Rakentaa strukturoidun promptin.
 * Lähettää pyynnön Gemini API:lle.
 * Tallentaa vastauksen valmiiksi index.html-tiedostoksi.
Esivalmistelut
Sinun tulee asentaa Googlen generatiivinen tekoälykirjasto:
pip install google-generativeai

Python-koodi (generate_site.py)
Kopioi alla oleva koodi tiedostoon. Muista vaihtaa OM_API_KEY ja varmista, että sinulla on testitiedostot (tai käytä skriptin alussa olevaa demo-tilaa).
import os
import base64
import mimetypes
import google.generativeai as genai

# --- ASETUKSET ---

# 1. Aseta Gemini API -avaimesi tähän
# (Tai suositus: lue se ympäristömuuttujasta: os.environ.get("GOOGLE_API_KEY"))
API_KEY = "SINUN_API_AVAIMESI_TÄHÄN"

# 2. Määritä lähdetiedostot
INPUT_FILES = {
    "markdown": "sisalto.md",
    "css": "tyyli.css",
    "images": ["kuva1.jpg", "logo.png"] # Listaa kuvatiedostot tähän
}

# 3. Tulostiedosto
OUTPUT_FILE = "index.html"

# 4. Valitse malli (Flash on nopea ja edullinen tähän tarkoitukseen)
MODEL_NAME = "gemini-1.5-flash" 

# --- APUFUNKTIOT ---

def setup_demo_files():
    """Luo testiaineistoa, jos tiedostoja ei ole olemassa (vain demoa varten)."""
    if not os.path.exists(INPUT_FILES["markdown"]):
        with open(INPUT_FILES["markdown"], "w", encoding="utf-8") as f:
            f.write("# Tervetuloa Gemini-sivustolle\n\nTämä sivu on generoitu automaattisesti Pythonilla.\n\n## Ominaisuudet\n* Base64 kuvat\n* Upotettu CSS\n* Yksi HTML-tiedosto")
        print(f"Luotiin demotiedosto: {INPUT_FILES['markdown']}")

    if not os.path.exists(INPUT_FILES["css"]):
        with open(INPUT_FILES["css"], "w", encoding="utf-8") as f:
            f.write("body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; } h1 { color: #2c3e50; } img { max-width: 100%; border-radius: 8px; }")
        print(f"Luotiin demotiedosto: {INPUT_FILES['css']}")
    
    # Huom: Kuvia emme voi luoda tyhjästä, skripti ohittaa puuttuvat kuvat varoituksella.

def get_base64_image(file_path):
    """Lukee kuvatiedoston ja palauttaa sen data-URI Base64 -muodossa."""
    if not os.path.exists(file_path):
        print(f"VAROITUS: Kuvaa {file_path} ei löytynyt, ohitetaan.")
        return None
    
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/png" # Oletus

    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    return f"data:{mime_type};base64,{encoded_string}"

def read_text_file(file_path):
    """Lukee tekstitiedoston sisällön."""
    if not os.path.exists(file_path):
        return f"[Tiedostoa {file_path} ei löytynyt]"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_response(text):
    """Poistaa markdown-koodimerkit (```html ... ```) vastauksesta."""
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
    # 0. Tarkista API-avain
    if API_KEY == "SINUN_API_AVAIMESI_TÄHÄN":
        print("VIRHE: Aseta API-avain koodin alkuun!")
        return

    genai.configure(api_key=API_KEY)
    
    # Luo demo-tiedostot jos niitä ei ole (voit poistaa tämän oikeassa käytössä)
    setup_demo_files()

    print("🔄 Luetaan tiedostoja ja koodataan kuvia...")

    # 1. Lue tekstisisällöt
    md_content = read_text_file(INPUT_FILES["markdown"])
    css_content = read_text_file(INPUT_FILES["css"])

    # 2. Koodaa kuvat
    image_data_prompt = ""
    for idx, img_path in enumerate(INPUT_FILES["images"]):
        b64_data = get_base64_image(img_path)
        if b64_data:
            # Luodaan selkeä ID, jota Gemini käyttää viittauksena
            image_id = f"IMAGE_{idx+1}"
            image_data_prompt += f"\n[{image_id}]: {b64_data}\n(Lähdetiedosto: {img_path})\n"

    # 3. Rakenna Prompt
    full_prompt = f"""
    Toimi asiantuntevana Front End -kehittäjänä. Tehtäväsi on luoda yksi itsenäinen (standalone) HTML5-tiedosto (index.html).

    Yhdistä seuraavat ainekset yhdeksi toimivaksi sivuksi:

    1. SISÄLTÖ (Markdown):
    Muunna tämä HTML-rakenteeksi (Semantic HTML):
    ---
    {md_content}
    ---

    2. TYYLI (CSS):
    Lisää tämä suoraan <style>-tagiin <head>-osioon:
    ---
    {css_content}
    ---

    3. KUVAT (Base64):
    Olen koodannut kuvat valmiiksi Base64-muotoon. Kun kohtaat sisällössä tarpeen kuvalle (tai jos haluat kuvittaa sivua), käytä näitä data-URI-lähteitä <img> tagin src-attribuutissa.
    
    Kuvat ovat tässä:
    {image_data_prompt}

    OHJEET:
    - Älä keksi omia kuva-URL-osoitteita. Käytä vain yllä annettuja data-URI-jonoja.
    - Sijoita kuvat loogisiin kohtiin sivulla.
    - Varmista, että tuloste on vain puhdasta HTML-koodia. Ei markdown-muotoiluja (kuten ```html), vain koodi.
    """

    print("🚀 Lähetetään pyyntö Geminille (tämä voi kestää hetken)...")

    # 4. Kutsu API:a
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(full_prompt)
        
        # 5. Käsittele ja tallenna vastaus
        final_html = clean_response(response.text)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"✅ Valmis! Sivusto tallennettu tiedostoon: {OUTPUT_FILE}")
        print(f"   Avaa tiedosto selaimessa nähdäksesi lopputuloksen.")

    except Exception as e:
        print(f"\n❌ Tapahtui virhe: {e}")

if __name__ == "__main__":
    main()

Miten tämä toimii:
 * Image ID: Skripti antaa jokaiselle kuvalle tunnisteen (esim. [IMAGE_1]). Promptissa kerrotaan Geminille: "Tässä on data kuvalle IMAGE_1. Kun rakennat HTML-koodia, laita tämä pitkä merkkijono img src -kohtaan."
 * Base64 Clientissä: Koska Python hoitaa raskaan Base64-muunnoksen, Geminin ei tarvitse "nähdä" kuvatiedostoa visuaalisesti, vaan se käsittelee sitä vain tekstijonona, joka pitää sijoittaa oikeaan paikkaan.
 * Varmistus: clean_response -funktio varmistaa, ettei tiedoston alkuun tai loppuun jää markdown-merkintöjä, jotka rikkoisivat HTML-tiedoston, jos avaat sen suoraan selaimessa.

Tämä on erittäin tärkeä parannus. API-avainten kovakoodaaminen suoraan lähdekoodiin on tietoturvariski, sillä se voi vahingossa päätyä esimerkiksi GitHubiin.
Paras ja standardinmukainen tapa on käyttää ympäristömuuttujia (Environment Variables) ja paikallisessa kehityksessä .env -tiedostoa.
Tässä on ohjeet ja päivitetty koodi.
Vaihe 1: Asenna python-dotenv
Tämä kirjasto mahdollistaa asetusten lukemisen erillisestä piilotiedostosta.
pip install python-dotenv

Vaihe 2: Luo .env -tiedosto
Luo projektisi juureen tiedosto nimeltä .env (huomaa piste alussa). Lisää avaimesi sinne:
GOOGLE_API_KEY=AIzaSyD...SinunOikeaAvainTähän...

Vaihe 3: Päivitä .gitignore (Jos käytät Gitiä)
Jos käytät versionhallintaa, varmista, että .env -tiedostoa ei koskaan lähetetä pilveen. Lisää .gitignore -tiedostoon rivi:
.env

Vaihe 4: Päivitetty Python-koodi
Tässä on koodi, joka lataa avaimen turvallisesti ympäristömuuttujista.
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


