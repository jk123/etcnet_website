# Etcnet Solar – WHMCS Teemadokumentaatio

**Versio:** 1.0.0  
**Brändi:** Etcetera Networks (Independent Solar Hosting)  
**Tyyli:** Moderni, luonnonläheinen, pyöristetty (Soft UI)

Tämä dokumentti määrittelee visuaalisen ilmeen, väripaletin ja komponentit Etcnetin asiakasportaalille. Teema yhdistää vakaan luotettavuuden (kivi/stone) ja uusiutuvan energian lämmön (meripihka/amber).

---

## 1. Väripaletti (Color Palette)

Teema rakentuu `Stone` (neutraalit) ja `Amber` (korostukset) sävyjen ympärille.

### Ensisijaiset Värit (Primary Brand)
Käytetään toimintopainikkeissa, linkeissä ja aktiivisissa tiloissa.

| Väri | HEX | Tailwind | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Primary** | `#d97706` | `amber-600` | Pääpainikkeet, aktiiviset linkit, ikonit |
| **Primary Hover** | `#b45309` | `amber-700` | Painikkeiden hover-tila |
| **Primary Light** | `#fbbf24` | `amber-400` | Pienet korostukset tummalla pohjalla |

### Neutraalit & Taustat (Neutrals)
Luovat pehmeän ja silmäystävällisen pohjan.

| Väri | HEX | Tailwind | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Body Background** | `#fafaf9` | `stone-50` | Sivun päätausta |
| **Card Background** | `#ffffff` | `white` | Sisältölaatikot, paneelit |
| **Navbar / Footer** | `#1c1917` | `stone-900` | Tummmat alueet (yläpalkki, alatunniste) |
| **Border** | `#e7e5e4` | `stone-200` | Erottimet, reunukset |

### Tekstivärit (Typography Colors)

| Väri | HEX | Tailwind | Käyttökohde |
| :--- | :--- | :--- | :--- |
| **Main Text** | `#1c1917` | `stone-900` | Otsikot, leipäteksti |
| **Muted Text** | `#57534e` | `stone-600` | Aputekstit, metatiedot |
| **Inverse Text** | `#f5f5f4` | `stone-100` | Teksti tummalla pohjalla |

---

## 2. Typografia (Typography)

Teema käyttää serif- ja sans-serif-fonttien yhdistelmää luodakseen arvokkaan mutta modernin vaikutelman.

**Fonttien lataus:**
```css
@import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Inter:wght@300;400;500;600&display=swap');
