---
created: 2025-11-27T04:47:09+02:00
modified: 2025-11-27T04:56:46+02:00
---

# ETCNET_TEMPLATE

Verkkosivuston Konseptisuunnitelma

Tämä dokumentti toimii teknisenä ja sisällöllisenä määrittelynä verkkosivuston kehitykselle.

Toteutus: Single File HTML5 (Kaikki yhdessä tiedostossa)

1 Palvelurakenne ja Tuotteet

Sivusto esittelee ydinpalvelut selkeästi ja ohjaa tilausprosessiin.

A. Hosting & Cloud (Integraatio WHMCS:ään)

Palvelu: Webhotelli, Kuvaus: Skaalautuvat ja luotettavat ratkaisut verkkosivuille., Alusta: Plesk, Tilauslinkki (Esim.): [Linkki tilausjärjestelmään]
Palvelu: Virtuaalipalvelimet (VPS), Kuvaus: Kaksi vaihtoehtoa vaativaan ja kevyeen käyttöön., Alusta: Proxmox/KVM/LXC, Tilauslinkki (Esim.): [Linkki tilausjärjestelmään]
Palvelu: -- KVM, Kuvaus: Täysiverinen virtualisointi, täysi kontrolli., Alusta: KVM, Tilauslinkki (Esim.): -
Palvelu: -- LXC, Kuvaus: Kevyt, konttipohjainen ratkaisu nopeaan käyttöönottoon., Alusta: LXC, Tilauslinkki (Esim.): -
Palvelu: Domainit, Kuvaus: Rekisteröinti ja helppo hallinta., Alusta: -, Tilauslinkki (Esim.): [Linkki tilausjärjestelmään]

B. Asiantuntijapalvelut (MSP)

Palvelu: MSP (Managed Service Provider), Kuvaus: Kokonaisvaltaiset ylläpitosopimukset – toimistoautomaatio ja IT-ulkoistus.
Palvelu: Sähköposti, Kuvaus: Tietoturvallinen, GDPR-yhteensopiva ja roskapostisuojattu.
Palvelu: Infraratkaisut, Kuvaus: Laitehankinnat, verkkoratkaisut ja konsultointi.

2 Sivuston Rakenne ja Toiminnallisuus

Tekninen Arkkitehtuuri: Single File (Yksi tiedosto)
Sivusto rakennetaan täysin itsenäiseksi kokonaisuudeksi yhteen tiedostoon. Tämä minimoi HTTP-pyynnöt ja varmistaa sivuston toimivuuden ilman monimutkaista palvelinpuolen riippuvuutta staattisessa jakelussa.

*   Tiedoston nimi: index.html (tai kehitysvaiheessa esim. index.h jos C-header -konteksti, mutta web-käytössä index.html).
*   HTML: HTML5-runko semanttisilla tageilla.
*   CSS: Tyylit upotetaan suoraan tiedoston <head>-osioon <style>-tagien sisään (ei erillistä .css-tiedostoa).
*   JavaScript: Toiminnallisuudet (navigaatio, interaktiot) upotetaan <script>-tagien sisään ennen </body>-tagin sulkemista.
*   Grafiikka:
    *   Ikonit: Inline SVG -koodina suoraan HTML-rakenteessa.
    *   Kuvat: Base64-enkoodattuna merkkijonona (Data URI scheme) tai Inline SVG:nä. Ulkoisia kuvahakuja vältetään latausnopeuden ja yksityisyyden maksimoimiseksi.

Navigaatiorakenne (One-Page)
Sivuston navigaatio ohjaa pääosiin yhdellä sivulla.

*   \#palvelut (Palvelut)
*   CTA Kirjaudu sisään (Client Area)

Ulkoiset linkit (WHMCS-integraatio)

Kohde: Sisäänkirjautuminen (Client Area), Linkki: [Sisäänkirjautumislinkki]
Kohde: Tuotehinnasto / Tilaus, Linkki: [Tilausjärjestelmän linkki]

Footer (Alatunniste)
Sivuston alatunnisteessa tulee näkyä lakisääteiset tiedot selkeästi:

*   Linkit: Tietosuojaseloste, Palveluehdot

3 Seuraavat vaiheet ja Toteutus

Tämä määrittely toimii ohjeena sivuston varsinaiselle toteutukselle. Etenemissuunnitelma on seuraava:

*   Koodaus (Single File Implementation):
    *   Luodaan tiedosto index.html.
    *   Kirjoitetaan HTML5-rakenne.
    *   Lisätään CSS (Tailwind-luokat tai custom CSS) suoraan <style>-osioon.
    *   Muutetaan tarvittavat logot ja kuvat Base64/SVG-muotoon ja upotetaan koodiin.
*   Tietoturva-auditointi:
    *   Varmistetaan, että kaikki ulkoiset linkit (WHMCS) käyttävät HTTPS-protokollaa.
    *   Tarkistetaan GDPR-vaatimusten toteutuminen (tietosuojaselosteet linkitettynä).
*   Testaus:
    *   Varmistetaan toimivuus ilman verkkoyhteyttä (offline-valmius staattisille osille).
    *   Testataan mobiiliskaalautuvuus.
*   Julkaisu:
    *   Tiedoston siirto tuotantopalvelimelle. Koska kyseessä on yksi tiedosto, käyttöönotto on erittäin yksinkertainen.
