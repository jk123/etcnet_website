# ETCNET_TEMPLATE

Tämä dokumentti toimii teknisenä määrittelynä verkkosivuston rakentamiseen.

Toteutus: Single File HTML5 (Kaikki yhdessä tiedostossa)

1 Sivuston Rakenne ja Toiminnallisuus

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

Kohde: Sisäänkirjautuminen (Client Area), Linkki: https://hosting.etcnet.fi/whmcs/index.php?rp=/login


Footer (Alatunniste)
Sivuston alatunnisteessa tulee näkyä lakisääteiset tiedot selkeästi:

*   Linkit: Tietosuojaseloste, Palveluehdot, ei blogia.

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
