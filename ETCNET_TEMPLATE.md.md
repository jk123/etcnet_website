---
created: 2025-11-27T04:47:09+02:00
modified: 2025-11-27T04:47:54+02:00
---

# ETCNET_TEMPLATE.md

---
created: 2025-11-26T23:38:49+02:00
modified: 2025-11-27T04:05:19+02:00
---

📄 Verkkosivuston Konseptisuunnitelma: Etcetera Networks
Tämä dokumentti toimii teknisenä ja sisällöllisenä määrittelynä Etcetera Networks Ab:n verkkosivuston kehitykselle.
1. Yleiskuvaus ja Yritystiedot
| Määrittely | Kuvaus |
|---|---|
| Yritys (Virallinen nimi) | Etcetera Networks Ab |
| Y-tunnus | 2974769-3 |
| Toimiala (TOL 2008) | Muu laitteisto- ja tietotekninen palvelutoiminta (62090) |
| Kotipaikka | Parainen (Toimipaikka: Nauvo) |
| Käyntiosoite | Elbacken 1 A 2, 21660 Nauvo |
| Postiosoite | Elbacken 1, 21660 Nauvo |
| Puhelin | 075 326 7910 |
| Sähköposti | info@etcnet.fi |
| Verkkosivusto | www.etcnet.fi |
| Kohderyhmä | Paikalliset yritykset, ympäristötietoiset toimijat |
| Slogan | "For a better digital everyday." (Kaikissa kieliversioissa) |
| Missio | Tehdä digitaalisesta arjesta siedettävämpää. |
| Toteutus | Single File HTML5 (Kaikki yhdessä tiedostossa) |
2. Kohderyhmä ja Arvolupaus (USP)
Arvolupauksen ydin (Core USP)
Etcetera Networks on inhimillinen, paikallinen ja ekologinen vaihtoehto suurille pilvijäteille.
Keskeiset erottuvuustekijät (Unique Selling Points)
 * Ekologisuus & Vastuullisuus
   * Energia: Palvelinhalli toimii 100 % aurinkovoimalla (seinät ja katto paneeleita).
   * Varmennus: Hoidetaan omalla akkupankilla ja varalla olevalla vesivoimalla.
   * Itämeren suojelu: Osa tuotoista lahjoitetaan Itämeren pelastamiseen. (Sitaatti: "Pisara meressäkö? Kenties, mutta tarpeeksi monta pisaraa kaivertaa jopa kiven.")
 * Inhimillisyys ja Paikallisuus
   * Ei kasvotonta tukea, vaan aitoja ihmisiä. ("Oma IT-osastosi" Nauvosta käsin.)
   * Data pysyy Suomessa, omassa hallinnassa olevassa laitesalissa.
 * Luotettavuus ja Tietoturva
   * Täysi GDPR-vaatimustenmukaisuus.
   * Säännöllinen varmuuskopiointi fyysisesti eriytettyyn sijaintiin.
3. Palvelurakenne ja Tuotteet
Sivusto esittelee ydinpalvelut selkeästi ja ohjaa tilausprosessiin.
A. Hosting & Cloud (Integraatio WHMCS:ään)
| Palvelu | Kuvaus | Alusta | Tilauslinkki (Esim.) |
|---|---|---|---|
| Webhotelli | Skaalautuvat ja luotettavat ratkaisut verkkosivuille. | Plesk | https://hosting.etcnet.fi/whmcs/index.php |
| Virtuaalipalvelimet (VPS) | Kaksi vaihtoehtoa vaativaan ja kevyeen käyttöön. | Proxmox/KVM/LXC | https://hosting.etcnet.fi/whmcs/index.php |
| -- KVM | Täysiverinen virtualisointi, täysi kontrolli. | KVM | - |
| -- LXC | Kevyt, konttipohjainen ratkaisu nopeaan käyttöönottoon. | LXC | - |
| Domainit | Rekisteröinti ja helppo hallinta. | - | https://hosting.etcnet.fi/whmcs/index.php |
B. Asiantuntijapalvelut (MSP)
| Palvelu | Kuvaus |
|---|---|
| MSP (Managed Service Provider) | Kokonaisvaltaiset ylläpitosopimukset – toimistoautomaatio ja IT-ulkoistus. |
| Sähköposti | Tietoturvallinen, GDPR-yhteensopiva ja roskapostisuojattu. |
| Infraratkaisut | Laitehankinnat, verkkoratkaisut ja konsultointi. |
4. Sivuston Rakenne ja Toiminnallisuus
Tekninen Arkkitehtuuri: Single File (Yksi tiedosto)
Sivusto rakennetaan täysin itsenäiseksi kokonaisuudeksi yhteen tiedostoon. Tämä minimoi HTTP-pyynnöt ja varmistaa sivuston toimivuuden ilman monimutkaista palvelinpuolen riippuvuutta staattisessa jakelussa.
 * Tiedoston nimi: index.html (tai kehitysvaiheessa esim. index.h jos C-header -konteksti, mutta web-käytössä index.html).
 * HTML: HTML5-runko semanttisilla tageilla.
 * CSS: Tyylit upotetaan suoraan tiedoston <head>-osioon <style>-tagien sisään (ei erillistä .css-tiedostoa).
 * JavaScript: Toiminnallisuudet (navigaatio, interaktiot) upotetaan <script>-tagien sisään ennen </body>-tagin sulkemista.
 * Grafiikka:
   * Ikonit: Inline SVG -koodina suoraan HTML-rakenteessa.
   * Kuvat: Base64-enkoodattuna merkkijonona (Data URI scheme) tai Inline SVG:nä. Ulkoisia kuvahakuja vältetään latausnopeuden ja yksityisyyden maksimoimiseksi.
Navigaatiorakenne (One-Page)
Sivuston navigaatio ohjaa pääosiin yhdellä sivulla.
 * #palvelut (Palvelut)
 * #vastuullisuus (Ekologisuus & Itämeri)
 * #yritys (Meistä / Ota yhteyttä)
 * [CTA] Kirjaudu sisään (Client Area)
Ulkoiset linkit (WHMCS-integraatio)
| Kohde | Linkki |
|---|---|
| Sisäänkirjautuminen (Client Area) | https://hosting.etcnet.fi/whmcs/index.php?rp=/login |
| Tuotehinnasto / Tilaus | https://hosting.etcnet.fi/whmcs/index.php |
Footer (Alatunniste)
Sivuston alatunnisteessa tulee näkyä lakisääteiset tiedot selkeästi:
 * Yritys: Etcetera Networks Ab
 * Y-tunnus: 2974769-3
 * Osoite: Elbacken 1, 21660 Nauvo
 * Yhteystiedot: info@etcnet.fi | 075 326 7910
 * Linkit: Tietosuojaseloste, Palveluehdot
5. Visuaalinen Ilme ja Äänensävy
Visuaalinen tyyli
 * Tyyli: Moderni, selkeä, premium.
 * Värimaailma: "Dark mode" tai saaristosta inspiroitunut paletti (syvänsininen/musta, kalliiden harmaat, kirkas aurinkopaneelien väri).
 * UX: Mobile-first, nopea latautuvuus (kevyt runko).
Copywriting (Tekstin sävy)
 * Äänensävy: Asiallinen, mutta maanläheinen ("saaristolainen").
 * Kielet: Pääkieli suomi. Slogan pidetään englanniksi.
 * Viesti: Vältetään liikaa teknistä jargonia. Korostetaan jatkuvasti hyötyjä, turvallisuutta, paikallisuutta ja ekologisuutta.
 * Esimerkki: Ei: "Toteutamme KVM-virtualisoinnin Proxmox-alustalla." Vaan: "Tarjoamme täysiverisen virtuaalipalvelimen vaativaan käyttöön – voit luottaa suomalaiseen Proxmox-pohjaiseen ratkaisuun."
6. Seuraavat vaiheet ja Toteutus
Tämä määrittely toimii ohjeena sivuston varsinaiselle toteutukselle. Etenemissuunnitelma on seuraava:
 * Koodaus (Single File Implementation):
   * Luodaan tiedosto index.html.
   * Kirjoitetaan HTML5-rakenne.
   * Lisätään CSS (Tailwind-luokat tai custom CSS) suoraan <style>-osioon.
   * Muutetaan tarvittavat logot ja kuvat Base64/SVG-muotoon ja upotetaan koodiin.
 * Tietoturva-auditointi:
   * Varmistetaan, että kaikki ulkoiset linkit (WHMCS) käyttävät HTTPS-protokollaa.
   * Tarkistetaan GDPR-vaatimusten toteutuminen (tietosuojaselosteet linkitettynä).
 * Testaus:
   * Varmistetaan toimivuus ilman verkkoyhteyttä (offline-valmius staattisille osille).
   * Testataan mobiiliskaalautuvuus.
 * Julkaisu:
   * Tiedoston siirto tuotantopalvelimelle. Koska kyseessä on yksi tiedosto, käyttöönotto on erittäin yksinkertainen.
