Tämä on loistava idea optimoinnin kannalta. Tehdään muutos, jossa Python-client ottaa **minkä tahansa kuvan** (JPG, PNG, jne.), muuntaa sen lennossa **läpinäkyväksi WebP-muodoksi**, koodaa sen yksiriviseksi Base64-merkkijonoksi ja upottaa lopulliseen tiedostoon.

Tämä vaatii Pythonin **Pillow (PIL)** -kuvankäsittelykirjaston.

### 1\. Asenna tarvittavat kirjastot (Fedora)

Tarvitset `Pillow`-kirjaston kuvamuunnoksiin:

```bash
pip install --upgrade google-generativeai Pillow
```

### 2\. Päivitetty koodi (`bundler_webp.py`)

Tämä skripti tekee seuraavat asiat:

1.  **Muuntaa:** Lukee kuvat, muuttaa ne `RGBA`-muotoon (läpinäkyvyys) ja pakkaa ne `WebP`-formaattiin muistissa.
2.  **Koodaa:** Tekee WebP-datasta yksirivisen Base64-stringin.
3.  **Generoi:** Pyytää Geminiä tekemään HTML-rungon paikkamerkeillä.
4.  **Bundlaa:** Ruiskuttaa optimoidun WebP-datan HTML-tiedostoon.

<!-- end list -->

````python
import os
import glob
import base64
import io
import google.generativeai as genai
from PIL import Image  # Vaatii: pip install Pillow

# --- ASETUKSET ---
SOURCE_DIR = '.'
TEXT_EXTENSIONS = ['*.html', '*.css', '*.js', '*.json', '*.xml', '*.md', '*.txt']
# Tuetut kuvaformaatit, jotka muunnetaan WebP:ksi
IMAGE_EXTENSIONS = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.svg', '*.gif', '*.bmp']
OUTPUT_FILENAME = 'index.html'

def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("VIRHE: GOOGLE_API_KEY puuttuu.")
        exit(1)
    return api_key

def convert_to_webp_base64(filepath):
    """
    1. Avaa kuvan (JPG/PNG/yms).
    2. Muuntaa sen RGBA-muotoon (varmistaa läpinäkyvyyden).
    3. Tallentaa muistiin optimoituna WebP-tiedostona.
    4. Palauttaa yksirivisen Base64-stringin.
    """
    try:
        # Avataan kuva Pillow-kirjastolla
        with Image.open(filepath) as img:
            filename = os.path.basename(filepath)
            
            # SVG-tiedostoja Pillow ei käsittele täydellisesti vektoreina, 
            # joten ne käsitellään raakana tekstinä tai base64:nä ilman muunnosta.
            if filepath.lower().endswith('.svg'):
                 with open(filepath, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                    return f"data:image/svg+xml;base64,{b64}"

            # Muunnetaan RGBA:ksi, jotta läpinäkyvyys säilyy (tai lisätään alpha-kanava)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Tallennetaan kuva muistiin (BytesIO) WebP-muodossa
            buffer = io.BytesIO()
            # lossless=True takaa laadun, quality=80 olisi tehokkaampi pakkaus
            img.save(buffer, format="WEBP", lossless=True) 
            
            # Haetaan tavut ja koodataan Base64
            img_bytes = buffer.getvalue()
            b64_string = base64.b64encode(img_bytes).decode('utf-8')
            
            # Varmistetaan yksirivisyys
            b64_string = b64_string.replace("\n", "")
            
            print(f"  -> Muunnettu WebP & Base64: {filename} (Koko: {len(b64_string)/1024:.1f} KB)")
            return f"data:image/webp;base64,{b64_string}"

    except Exception as e:
        print(f"  VIRHE kuvan {filepath} käsittelyssä: {e}")
        return None

def read_text_files():
    """Lukee tekstisisällöt."""
    content_buffer = ""
    found_files = []
    
    for ext in TEXT_EXTENSIONS:
        found_files.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
    
    exclusions = [OUTPUT_FILENAME, "bundler.py", "bundler_v2.py", "bundler_webp.py"]
    found_files = [f for f in found_files if os.path.basename(f) not in exclusions]

    for filepath in found_files:
        try:
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = f.read()
            content_buffer += f"--- FILE: {filename} ---\n{data}\n\n"
        except Exception as e:
            print(f"  VAROITUS: Ei voitu lukea {filepath}: {e}")
            
    return content_buffer

def main():
    print("--- Gemini WebP Bundler ---")
    genai.configure(api_key=get_api_key())
    
    # Valitaan malli
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')

    # 1. Kerää tiedostot
    text_context = read_text_files()
    image_paths = []
    for ext in IMAGE_EXTENSIONS:
        image_paths.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
    
    if not text_context:
        print("Ei tekstisisältöä.")
        return

    # 2. Generoi prompt
    img_list_str = "\n".join([f"- {os.path.basename(img)}" for img in image_paths])
    
    prompt = f"""
Olet Senior Web Developer. Tehtäväsi on koota materiaalista YKSI `index.html`.

LÄHDEMATERIAALI:
{text_context}

SAATAVILLA OLEVAT KUVATIEDOSTOT:
{img_list_str}

OHJEET:
1. Yhdistä CSS `<style>`-tagiin ja JS `<script>`-tagiin.
2. Luo HTML5-rakenne.
3. **KUVAT:** Käytä kuvia loogisissa paikoissa. 
   TÄRKEÄÄ: Käytä `src`-attribuutissa AINA tätä muotoa paikkamerkkinä:
   `%%TIEDOSTONIMI%%`
   
   Esimerkiksi: `<img src="%%logo.png%%" class="logo">`
   
   Älä muuta tiedostonimiä paikkamerkeissä. Python-scriptini hoitaa WebP-muunnoksen ja injektoinnin jälkikäteen.
4. Palauta vain HTML-koodi.
"""

    print("Lähetetään rakenne-pyyntö Geminille...")
    
    try:
        # Lähetetään pyyntö
        response = model.generate_content(prompt)
        html_content = response.text
        
        # Siivotaan markdown
        html_content = html_content.replace("```html", "").replace("```", "").strip()
        
        print("HTML-runko saatu. Aloitetaan WebP-muunnos ja injektointi...")

        # 3. WebP Muunnos & Injektointi
        for img_path in image_paths:
            filename = os.path.basename(img_path)
            placeholder = f"%%{filename}%%"
            
            if placeholder in html_content:
                # Tässä tapahtuu taika: Kuva luetaan, muunnetaan WebP:ksi ja koodataan
                optimized_b64 = convert_to_webp_base64(img_path)
                
                if optimized_b64:
                    html_content = html_content.replace(placeholder, optimized_b64)
            else:
                # Joskus Gemini ei käytä kaikkia kuvia, se on ok
                pass

        # 4. Tallenna
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"\nVALMIS! Tiedosto luotu: {OUTPUT_FILENAME}")

    except Exception as e:
        print(f"\nVIRHE: {e}")

if __name__ == "__main__":
    main()
````

### Mikä muuttui?

1.  **`convert_to_webp_base64` funktio:** Tämä on clientin "sydän" nyt.
      * Se tunnistaa automaattisesti, jos kuva on JPG tai PNG.
      * `img.convert('RGBA')`: Varmistaa, että alpha-kanava (läpinäkyvyys) on olemassa.
      * `img.save(buffer, format="WEBP")`: Pakkaa kuvan Googlen WebP-muotoon, joka on huomattavasti kevyempi kuin PNG mutta tukee läpinäkyvyyttä.
2.  **Yksirivisyys:** Funktio ajaa `.replace("\n", "")` varmistaakseen, että base64-string on täysin yhtenäinen pötkö, eikä riko HTML-koodia.
3.  **Toimintalogiikka:** Gemini luo edelleen "luurangon" (HTML), mutta Python tekee raskaan työn (kuvankäsittelyn) paikallisesti koneellasi. Tämä on nopeinta ja luotettavinta.

