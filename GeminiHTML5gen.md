Tässä on Python-skripti, joka toimii pyytämänäsi "rakentajana". Se lukee määritellystä kansiosta kaiken sisällön (koodit, tekstit, kuvat), muuntaa ne sopivaan muotoon ja pyytää Geminiä koostamaan niistä yhden itsenäisen index.html-tiedoston.
Olen huomioinut Linux-ympäristön ohjeistuksessa.
gemini_web_builder.py
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

Käyttöohjeet (Fedora)
 * Asenna tarvittava kirjasto:
   Avaa terminaali ja suorita:
   pip install google-generativeai

 * Valmistele kansiorakenne:
   Luo skriptin viereen kansio nimeltä projektin_tiedostot.
   Laita sinne kaikki verkkosivusi palaset:
   * logo.png
   * tekstit.md
   * data.json
   * tyylit.css (jos on, muuten Gemini keksii ne)
 * Aseta API-avain (Turvallinen tapa):
   Älä kirjoita avainta koodiin. Aseta se ympäristömuuttujaksi Fedoran terminaalissa ennen skriptin ajoa:
   export GOOGLE_API_KEY="AIzaSy..."

 * Aja skripti:
   python gemini_web_builder.py

Miten tämä toimii:
 * Lukeminen: Skripti lukee kaiken datan. Tekstitiedostot luetaan tekstinä, kuvat ja muut mediat muutetaan Pythonissa valmiiksi Base64-merkkijonoiksi.
 * Promptaus: Skripti rakentaa Geminille valtavan kehotteen, jossa sanotaan: "Tässä on kuva logo.png base64-muodossa [MERKKIJONO]. Upota tämä HTML-koodiin img-tagin sisään."
 * Malli: Käytän gemini-1.5-flash -mallia. Tämä on kriittistä, koska kuvien Base64-muunnos vie valtavasti tilaa (tokeneita). Flash-mallin 1 miljoonan tokenin konteksti-ikkuna riittää hyvin jopa useille kuville.
 * Tulostus: Gemini palauttaa yhden tiedoston tekstinä, joka tallennetaan index.html-nimellä.
