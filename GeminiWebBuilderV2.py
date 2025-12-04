import os
import base64
import io
import re
import google.generativeai as genai
from pathlib import Path
from PIL import Image  # Vaatii: pip install Pillow

# --- ASETUKSET ---
SOURCE_DIR = Path('.')
OUTPUT_FILENAME = 'index.html'

# Tiedostotyypit
TEXT_EXTENSIONS = {'.html', '.css', '.js', '.json', '.xml', '.md', '.txt'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.bmp'}

# Kuvien optimointiasetukset
MAX_DIMENSION = (1024, 1024)  # Kuvat pienennetään mahtumaan tähän (leveys, korkeus)
WEBP_QUALITY = 80             # 0-100. 80 on hyvä tasapaino laadun ja koon välillä.

def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("VIRHE: GOOGLE_API_KEY ympäristömuuttuja puuttuu.")
        exit(1)
    return api_key

def optimize_image_to_base64(filepath):
    """
    Lukee kuvan, pienentää sen, muuntaa WebP:ksi ja palauttaa Base64-stringinä.
    """
    try:
        filename = filepath.name
        original_size = filepath.stat().st_size
        
        # Erikoiskäsittely SVG:lle (vektori -> ei voi muuntaa pikseleiksi samalla tavalla)
        if filepath.suffix.lower() == '.svg':
            with open(filepath, "rb") as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                return f"data:image/svg+xml;base64,{b64}"

        with Image.open(filepath) as img:
            # 1. Muunnetaan RGBA:ksi (säilyttää läpinäkyvyyden)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 2. Pienennetään kuva (Thumbnail säilyttää kuvasuhteen)
            img.thumbnail(MAX_DIMENSION, Image.Resampling.LANCZOS)

            # 3. Tallennetaan muistiin WebP-muodossa
            buffer = io.BytesIO()
            # method=6 on hitain mutta tehokkain pakkaus
            img.save(buffer, format="WEBP", quality=WEBP_QUALITY, method=6)
            
            img_bytes = buffer.getvalue()
            b64_string = base64.b64encode(img_bytes).decode('utf-8').replace("\n", "")
            
            # Tulostetaan statistiikkaa
            new_size = len(b64_string)
            reduction = (1 - (new_size / original_size)) * 100
            print(f"  [OPTI] {filename}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB (Säästö: {reduction:.1f}%)")
            
            return f"data:image/webp;base64,{b64_string}"

    except Exception as e:
        print(f"  VIRHE kuvan {filepath.name} käsittelyssä: {e}")
        return None

def read_text_context():
    """Lukee kaikki tekstipohjaiset lähdetiedostot yhteen stringiin."""
    buffer = []
    exclusions = {OUTPUT_FILENAME, "bundler.py", "bundler_v2.py"}
    
    # Etsitään kaikki tiedostot nykyisestä hakemistosta
    for file_path in SOURCE_DIR.iterdir():
        if file_path.is_file() and file_path.name not in exclusions:
            if file_path.suffix.lower() in TEXT_EXTENSIONS:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    buffer.append(f"--- FILE: {file_path.name} ---\n{content}\n")
                except Exception as e:
                    print(f"  VAROITUS: Ei voitu lukea {file_path.name}: {e}")
    
    return "\n".join(buffer)

def main():
    print("--- Gemini Web Builder v2 (Optimized) ---")
    genai.configure(api_key=get_api_key())
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash') # Käytetään uusinta jos mahdollista
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')

    # 1. Kerää tiedostot
    text_context = read_text_context()
    
    # Luodaan sanakirja kuville: "kuva.jpg" -> Path-objekti
    image_map = {}
    for f in SOURCE_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
            image_map[f.name] = f

    if not text_context:
        print("Ei tekstisisältöä lähdehakemistossa.")
        return

    # 2. Generoi prompt
    img_list_str = "\n".join([f"- {name}" for name in image_map.keys()])
    
    prompt = f"""
Olet Senior Frontend Developer. Tehtäväsi on koodata Single File Website (index.html).

LÄHDEMATERIAALI:
{text_context}

SAATAVILLA OLEVAT KUVAT:
{img_list_str}

OHJEET:
1. Yhdistä kaikki CSS `<style>`-tagiin ja JS `<script>`-tagiin HTML:n sisään.
2. Luo moderni, responsiivinen HTML5-rakenne.
3. **KUVAT:** - Käytä vain listassa mainittuja kuvia.
   - `src`-attribuutin ON OLTAVA tarkalleen muodossa: `%%TIEDOSTONIMI%%`
   - Esimerkki: `<img src="%%logo.png%%" alt="Logo">`
   - Älä yritä keksiä kuvia, joita ei ole listassa.
4. Palauta vain puhdas HTML-koodi.
"""

    print("Pyydetään HTML-rakennetta Geminiltä...")
    
    try:
        response = model.generate_content(prompt)
        html_content = response.text
        
        # Markdown-siivous
        html_content = html_content.replace("```html", "").replace("```", "").strip()
        
        print("HTML saatu. Aloitetaan kuvien injektointi...")

        # 3. Etsi paikkamerkit ja korvaa kuvilla
        # Regex löytää kaikki %%jotain.jpg%% kohdat
        placeholders = set(re.findall(r'%%(.*?)%%', html_content))
        
        for filename in placeholders:
            # Etsitään tiedostoa mapista (tarkka nimi)
            if filename in image_map:
                file_path = image_map[filename]
                print(f"Käsitellään: {filename}")
                
                optimized_b64 = optimize_image_to_base64(file_path)
                
                if optimized_b64:
                    html_content = html_content.replace(f"%%{filename}%%", optimized_b64)
            else:
                print(f"  VAROITUS: Gemini pyysi kuvaa '{filename}', jota ei löydy hakemistosta.")

        # 4. Tallenna
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"\nVALMIS! Tiedosto luotu: {OUTPUT_FILENAME}")
        print(f"Tiedoston koko: {os.path.getsize(OUTPUT_FILENAME)/1024:.1f} KB")

    except Exception as e:
        print(f"\nKRITINEN VIRHE: {e}")

if __name__ == "__main__":
    main()
