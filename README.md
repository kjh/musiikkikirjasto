# Musiikkikirjasto

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan levyjä.
- Käyttäjä pystyy lisäämään kuvia levyn tietoihin.
- Käyttäjä näkee sovellukseen lisätyt levyt.
- Käyttäjä pystyy etsimään levyjä hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät levyt.
- Käyttäjä pystyy valitsemaan levylle yhden tai useamman luokittelun (esim. median tyyppi (vinyyli, cd), musiikkigenre, levyn kunto, hintatiedot).
- Käyttäjä pystyy tekemään muistiinpanoja ym. levyistä.
- Käyttäjä voi jakaa musikkikirjaston. 

# Välipalautus 2 
- Tunnuksen luominen onnistuu
- Kirjautuminen onnistuu
- Tietokannassa kokoelmat ja julkaisut
- Kokoelman lisääminen ei toimi vielä
- Levyn lisääminen ei toimi vielä

# Välipalautus 3
- Käyttäjän tunnuksen luominen ja kirjautuminen onnistuu.
- Käyttäjä voi luoda kokoelman.
- Kokoelman julkaisun voi lisätä/muokata/poistaa.
- Tietyt toiminnot vaativat kirjatumisen. Tämä on toteutettu dekoraattorilla @helper.require_login.
- Jos käyttäjä yrittää muokata/poistaa toisen kokoelmaan kuuluvia julkaisuja, se on estetty.
- Virhetilanteiden käsittely, jos esim. kokoelmaa tai viestiä ei löydy tietokannasta.
- Lomakkeen kenttien arvojen tarkistus esim. yli 100 pitkä artistin nimi hylätään.
- Lomakkeet käyttävät text input kenttiä ja oletuskoko 40 merkkiä.
- Lomakkeiden kentät ovat pakollisia.
- Hakutoiminto lisätty. Listaa kokoelmat jotka sisältävät haetun artistin tai levyn nimen.
- Käyttäjäsivut lisätty. Sivu näyttää käyttäjän nimen, julkaisujen määrän ja vanhimman ja uusimman lisätyn julkaisun päiväyksen ja kellonajan. 

# Lopullinen palautus
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Salasana tallennetaan turvallisesti tietokantaan.
- Käyttäjä pystyy lisäämään, muokkaamaan kokoelmia.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kokoelman julkaisuja (levyjä).
- Käyttäjä näkee sovellukseen lisätyt kokoelmat ja julkaisut.
- Käyttäjä pystyy etsimään julkaisuja hakusanalla. Tietoa etsitään julkaisun nimen (title), artistin (artists) ja tagien perustella.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja (julkaisujen määrä, uusin ja vanhin julkaisu) ja käyttäjän lisäämät kokoelmat.
- Käyttäjä pystyy valitsemaan kokoelmalle useamman tagin esim. rock, pop, 2000.
- Käyttäjä pystyy muokkaamaan lisäämään ja poistamaan kokoelmaan liitettyjä tageja.
- Toisen käyttäjän kokoelmista voi tykätä (ja poistaa tykkäyksen). Kokoelman tykkäysten määrä näkyy sen tiedoissa.
- Tietyt toiminnot vaativat kirjatumisen. Tämä on toteutettu dekoraattorilla @helper.require_login.
- Jos käyttäjä yrittää muokata/poistaa toisen kokoelmia tai kokoelmaan kuuluvia julkaisuja, se on estetty.
- Virhetilanteiden käsittely, jos esim. kokoelmaa tai viestiä ei löydy tietokannasta.
- Lomakkeen kenttien arvojen tarkistus esim. yli 100 pitkä artistin nimi hylätään.
- Lomakkeet käyttävät text input kenttiä ja oletuskoko 40 merkkiä.
- Lomakkeiden kentät ovat pakollisia, jos vaaditaan arvo.
- Sivu käyttää CSS-tyylejä.
- SQL-komennossa on käytetty parametreja.
- Käytetään sivupohjia.
- Suojaudutaan CSRF-hyökkäyksiltä (julkaisut, kokoelmat, tagit ja tykkäykset).  



