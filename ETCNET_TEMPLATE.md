# ETCNET_TEMPLATE

Verkkosivuston Tekninen Määrittely: Single File -toteutus
Versio: 1.0 | Päiväys: 27.11.2025
1. Johdanto ja tavoite: 
Tämä dokumentti määrittelee tekniset vaatimukset ja toteutustavan hosting-palveluita tarjoavan verkkosivuston rakentamiseksi.
Toteutusmalli: Single File HTML5 (SPA-tyyppinen staattinen toteutus).
Tavoite: Maksimoida suorituskyky, siirrettävyys ja yksinkertaisuus sisällyttämällä kaikki resurssit yhteen tiedostoon.
2. Tekninen Arkkitehtuuri: 
Sivusto rakennetaan täysin itsenäiseksi kokonaisuudeksi ("Self-Contained"). Tämä ratkaisu minimoi HTTP-pyynnöt yhteen (1) pyyntöön ja mahdollistaa sivuston helpon jakelun ilman riippuvuuksia tiedostopoluista.
 * Tiedostoformaatti: index.html.
   * Huomio: Mikäli sivusto tarjoillaan sulautetusta järjestelmästä (esim. C/C++ -ympäristö), tiedosto voidaan konvertoida merkkijonoksi (header-tiedostoon), mutta kehitys tapahtuu HTML-muodossa.
 * HTML-runko: Moderni HTML5 semanttisilla tageilla (<header>, <main>, <section>, <footer>).
 * Tyylit (CSS):
   * Kaikki tyylit sijoitetaan <head>-osion <style>-tagien sisään.
   * Ei ulkoisia CSS-tiedostoja (<link rel="stylesheet"> kielletty).
   * Responsiivisuus toteutetaan CSS Media Queries -säännöillä (Mobile First -periaate).
 * Logiikka (JavaScript):
   * Skriptit sijoitetaan <body>-osion loppuun <script>-tagien sisään.
   * Käytetään "Vanilla JS" -ratkaisua ilman raskaita kirjastoja (kuten jQuery tai React) latausnopeuden optimoimiseksi.
 * Media ja Grafiikka:
   * Ikonit: Inline SVG -koodina suoraan HTML-rakenteessa (mahdollistaa värien muokkauksen CSS:llä).
   * Kuvat: Base64-enkoodattuna merkkijonona (Data URI) tai Inline SVG:nä.
   * Fontit: Käytetään "System Font Stack" -ratkaisua (ei ladattavia fontteja) tai base64-enkoodattua WOFF2-dataa CSS:n sisällä, jos brändifontti on välttämätön.
3. Sivuston Rakenne ja Toiminnallisuus: 
Sivusto on ns. "One-Page" -kokonaisuus, jossa navigointi tapahtuu ankkurilinkkien avulla sivun sisällä pehmeästi rullaten (Smooth Scroll).
3.1 Navigaatio ja Header: 
Yläpalkki (Sticky/Fixed), joka sisältää logon ja linkit:
 * Etusivu (ylös)
 * Palvelut (ohjaa #palvelut -osioon)
 * CTA-painike: "Kirjaudu sisään" (Client Area)
3.2 Sisältöalueet
 * Hero-osio: Pääotsikko, lyhyt esittelyteksti ja ensisijainen CTA.
 * Integraatiot: Linkitys WHMCS-järjestelmään.
3.3 Ulkoiset linkit (WHMCS)
Asiakashallintaan ohjaava liikenne toteutetaan selkeästi erottuvilla painikkeilla.
 * Kohde: Asiakassivut (Client Area)
 * URL: https://hosting.etcnet.fi/whmcs/index.php?rp=/login
 * Tietoturva: Linkeissä käytettävä attribuuttia rel="noopener noreferrer".
3.4 Footer (Alatunniste)
Selkeä ja lakisääteinen alatunniste.
 * Tiedot: Yrityksen nimi, Y-tunnus (jos soveltuu), Copyright-vuosiluku (päivittyy automaattisesti JS:llä).
 * Linkit: Tietosuojaseloste, Palveluehdot (Nämä voidaan toteuttaa joko modaali-ikkunoina samassa tiedostossa tai ankkurilinkkeinä sivun alaosaan, jotta "Single File" -lupaus säilyy).
4. Ideointi ja Lisäominaisuudet (Parantelu)
Tässä osiossa on ideoita, joilla "Single File" -konseptista saadaan vieläkin parempi:
 * Tumma tila (Dark Mode):
   * Koska CSS on samassa tiedostossa, voidaan lisätä helppo JS-kytkin ja CSS-muuttujat (:root { --bg-color: #fff }), jotka vaihtavat teeman käyttäjän järjestelmäasetusten mukaan.
 * Favicon:
   * Myös selaimen välilehden ikoni (favicon) voidaan upottaa Base64-muodossa <link rel="icon" href="data:image/x-icon;base64,..." />, jolloin yhtäkään ulkoista tiedostopyyntöä ei tapahdu.
 * Offline-tila:
   * Koska kaikki on yhdessä tiedostossa, sivusto toimii täydellisesti, vaikka käyttäjä tallentaisi sen koneelleen ja avaisi ilman nettiyhteyttä.
 * SEO (Hakukoneoptimointi):
   * Vaikka kyseessä on yksi tiedosto, <head>-osioon tulee lisätä Open Graph -tagit (OG) ja Meta Description, jotta linkki näyttää hyvältä jaettaessa sosiaalisessa mediassa.
5. Toteutussuunnitelma
Vaihe 1: Kehitys (Single File Implementation)
 * Luodaan index.html.
 * Rakennetaan DOM-rakenne (HTML).
 * Kirjoitetaan CSS (suositus: omat puhtaat CSS-luokat Tailwindin sijaan, jotta tiedostokoko pysyy pienenä ilman build-prosessia. Jos käytät Tailwindia, aja se build-prosessin läpi ja kopioi output <style>-tagiin).
 * Konvertoidaan kuvat Base64-muotoon  työkalulla ja sijoitetaan koodiin.
Vaihe 2: Optimointi ja Tietoturva
 * Minifiointi: HTML, CSS ja JS koodi ajetaan "minifier"-työkalun läpi ennen julkaisua tiedostokoon pienentämiseksi.
 * HTTPS: Varmistetaan, että hosting.etcnet.fi pakottaa HTTPS-yhteyden.
 * Linkkien tarkistus: Testataan WHMCS-linkin toimivuus ja uudelleenohjaukset.
Vaihe 3: Testaus
 * Offline-testi: Lataa sivu, katkaise verkkoyhteys, päivitä sivu (cache) tai avaa tiedosto suoraan levyltä.
 * Laitetestaus: Testaus mobiililaitteilla (iOS/Android) sekä eri selaimilla (Firefox, Chrome).
Mitä mieltä olet?
* Luodaan sivulle tämän pohjalta valmis HTML-koodirunko, jossa on perusrakenteet (Base64 placeholder-logolla ja valmiilla CSS-tyyleillä) paikoillaan.
