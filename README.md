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
- tunnuksen luominen onnistuu
- kirjautuminen onnistuu
- tietokannassa kokoelmat ja julkaisut
- kokoelman lisääminen ei toimi vielä
- levyn lisääminen ei toimi vielä

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
