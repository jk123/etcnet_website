# WHMCS Teeman Määrittely: "Etcnet Solar"

Tämä dokumentti määrittelee visuaalisen ilmeen Etcetera Networks (Etcnet) asiakasportaalille (WHMCS). Teema perustuu "Independent Solar Hosting" -brändi-ilmeeseen.

## 1. Yleiset Asetukset (Base Settings)

*   **Pohjakehys:** Bootstrap 5.
*   **Muotokieli:** Pyöristetyt kulmat (Rounded), pehmeät varjot, minimalistinen, luonnonläheinen.
*   **CSS Framework Referenssi:** Tailwind CSS (Stone / Amber -paletti).

---

## 2. Väripaletti (Color Palette)

Teema käyttää `Stone` (kivi) ja `Amber` (meripihka) sävyjä.

### Ensisijaiset Värit (Primary Colors)
Käytetään painikkeissa, linkeissä ja korostuksissa.

| Nimi | Tailwind | HEX Koodi | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Brand Primary** | `amber-600` | `#d97706` | Pääpainikkeet (Primary Buttons), aktiiviset linkit |
| **Brand Hover** | `amber-700` | `#b45309` | Painikkeiden hover-tila |
| **Brand Light** | `amber-400` | `#fbbf24` | Ikonit tummalla taustalla, pienet korostukset |
| **Selection** | `amber-200` | `#fde68a` | Tekstin valintaväri (Selection) |

### Taustavärit (Backgrounds)

| Nimi | Tailwind | HEX Koodi | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Body Background** | `stone-50` | `#fafaf9` | Sivun päätausta (light mode) |
| **Card Background** | `white` | `#ffffff` | Sisältölaatikot, paneelit |
| **Dark Header** | `stone-900` | `#1c1917` | Yläpalkki (Navbar), Footer, Hero-alueet |
| **Dark Alt** | `stone-800` | `#292524` | Mobiilivalikko, Footerin erottimet |

### Typografiavärit (Text Colors)

| Nimi | Tailwind | HEX Koodi | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Text Main** | `stone-900` | `#1c1917` | Otsikot, leipäteksti (tumma) |
| **Text Muted** | `stone-600` | `#57534e` | Aputekstit, kuvaukset |
| **Text Inverse** | `stone-100` | `#f5f5f4` | Teksti tummalla pohjalla (Header/Footer) |

### Statusvärit (WHMCS Alerts)

| Nimi | HEX Koodi | Käyttökohde |
| :--- | :--- | :--- |
| **Success** | `#10b981` (Emerald-500) | Palvelu aktiivinen, maksettu |
| **Warning** | `#f59e0b` (Amber-500) | Lasku erääntymässä |
| **Danger** | `#ef4444` (Red-500) | Palvelu suljettu, virhe |
| **Info** | `#3b82f6` (Blue-500) | Yleiset ilmoitukset |

---

## 3. Typografia (Typography)

Käytössä on kaksi fonttia. `Merriweather` tuo arvokkuutta otsikoihin, `Inter` selkeyttä käyttöliittymään.

**Google Fonts Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Inter:wght@300;400;500;600&display=swap');
```

### Otsikot (Headings H1-H6)
*   **Font Family:** `'Merriweather', serif`
*   **Weight:** 700 (Bold) tai 400 (Regular)
*   **Color:** `#1c1917` (Stone-900)
*   **Tyyli:** Moderni Serif

### Leipäteksti & UI (Body & UI)
*   **Font Family:** `'Inter', sans-serif`
*   **Weight:** 300 (Light), 400 (Regular), 500 (Medium)
*   **Base Size:** 16px
*   **Line Height:** 1.5

---

## 4. Komponentit (UI Components)

### Painikkeet (Buttons)
WHMCS `.btn-primary` ja `.btn-action` tyylit.

*   **Muoto (Border Radius):** `9999px` (Täysi pilleri / Full rounded)
*   **Padding:** `0.75rem 1.5rem` (Väljät)
*   **Font:** Inter, font-weight 500
*   **CSS Esimerkki:**
    ```css
    .btn-primary {
        background-color: #d97706;
        border-color: #d97706;
        border-radius: 9999px;
        color: white;
        transition: all 0.3s ease;
    }
    .btn-primary:hover {
        background-color: #b45309;
        transform: scale(1.05); /* Pieni suurennus */
        box-shadow: 0 10px 15px -3px rgba(180, 83, 9, 0.3);
    }
    ```

### Kortit ja Paneelit (Cards & Panels)
WHMCS "Client Area Home Panels" ja tuotelistaukset.

*   **Tausta:** Valkoinen (`#ffffff`)
*   **Reuna:** 1px solid `#e7e5e4` (Stone-200)
*   **Border Radius:** `1.5rem` (24px) – Tämä on tärkeä osa brändiä.
*   **Varjo (Shadow):** `0 1px 2px 0 rgba(0, 0, 0, 0.05)` (Hienovarainen)
*   **Hover-efekti:** Nousee hieman ylös ja varjo syvenee.

### Navigaatio (Navbar)
*   **Tausta:** `#1c1917` (Stone-900)
*   **Korkeus:** 80px
*   **Linkit:** `#f5f5f4` (Stone-100), Hover: `#fbbf24` (Amber-400)
*   **Logo:** Teksti "Etcetera Networks" fontilla Merriweather, Bold.

### Kirjautumissivu (Login Page)
*   **Layout:** Keskitetty kortti (Card).
*   **Tausta:** Kuva auringonlaskusta (overlay opacity 60% stone-900).
*   **Kortti:** Valkoinen, vahvasti pyöristetty (`rounded-3xl`), varjostettu.

---

## 5. Grafiikat ja Ikonit (Assets)

### Ikonit
Käytä **Feather Icons** tai **Lucide React** tyylisiä SVG-ikoneita (stroke-width 2, rounded ends).
*   Älä käytä täytettyjä (solid) FontAwesome-ikoneita oletuksena, vaan "light" tai "regular" versioita, jos mahdollista.
*   Väri ikoneissa: `#d97706` (Amber-600) tai `#57534e` (Stone-600).

### Taustakuva (Hero & Login)
*   **Lähde:** Unsplash (Sunset / Nordic nature).
*   **Esimerkki:** `https://images.unsplash.com/photo-1472120435266-53113306b2a8`
*   **Käsittely:** Kuvan päälle aina tumma gradientti (`from-stone-900/90 to-amber-900/40`), jotta valkoinen teksti on luettavaa.

---

## 6. WHMCS Template Muutokset (Six / Twenty-One Theme)

Tärkeimmät CSS-ylikirjoitukset (Custom CSS):

1.  **Header:** Muuta taustaväri mustaksi (stone-900).
2.  **Sidebar:** Muuta tausta vaaleaksi (stone-50) tai valkoiseksi (white) pyöristetyillä kulmilla.
3.  **Body:** Aseta taustaväriksi `#fafaf9`.
4.  **Panel:** Lisää `border-radius: 24px;` kaikkiin `.panel` ja `.card` elementteihin.
5.  **Fonts:** Pakota otsikot käyttämään Merriweather-fonttia.

```css
/* Quick CSS Snippet for WHMCS */
body {
    background-color: #fafaf9;
    font-family: 'Inter', sans-serif;
    color: #1c1917;
}
h1, h2, h3, h4 {
    font-family: 'Merriweather', serif;
    font-weight: 700;
}
.navbar {
    background-color: #1c1917 !important;
}
.btn-primary {
    background-color: #d97706;
    border-color: #d97706;
    border-radius: 50px;
}
.card, .panel {
    border-radius: 24px;
    border: 1px solid #e7e5e4;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```
