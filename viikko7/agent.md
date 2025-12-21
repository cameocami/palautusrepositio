*Vibe coding with agent mode*

- Päätyikö agentti toimivaan ratkaisuun?

Ensimmäinen ratkaisu toimi päällisin puolin käyttäjälle, mutta koodin laatu oli heikkoa. Unohdin itse refaktorointi-osiossa hyödyntää erillistä pelipalvelu luokkaa. Mutta sen sijaan, että agentti olisi refaktoroinut tässä vaiheessa koodin oikein, niin se liimasi ui:n päälle oman sanakirja-olionsa, jolla se käytännössä piti kirjaa täysin samoista asoista kuin alempien tasojen luokat. 

- Miten varmistuit, että ratkaisu toimii?

Luin koodia ja testailin sovelluksen käyttöä manuaalisesti. Mitä enemmän muutoksia tein, sitä hankalampaa oli koodia seurata, joten epävarmuus kasvoi.

- Oletko ihan varma, että ratkaisu toimii oikein?
En. 

- Kuinka paljon jouduit antamaan agentille komentoja matkan varrella?
Paljon. Jouduin pyytämään agenttia erikseen refaktoroimaan ja siistimään koodia kokonaisuudessaan. Lisäksi jouduin mikromanageroimaan ja pyytämään sitä siirtämään tiettyjä metodeita luokista toisiin. Useamman kerran koko ohjelma meni rikki ja agentti turvautui siihen, että se kirjoitti koko jutun uudestaan. Lisäksi kieli ei millään pysynyt suomessa, vaan jossain vaiheessa kieli muuttui aina osin englanniksi. 

- Kuinka hyvät agentit tekemät testit olivat?
Ihan hyviä. Testit eivät menneet kovasti rikki, kun muutin voittojen määrän viidestä kolmeen. Vain testi, joka testasi juurikin tätä ominaisuutta meni rikki.

- Onko agentin tekemä koodi ymmärrettävää?
Metodit, oliot, yms. on nimetty selkeästi. Metodeista löytyy docstring-selityksiä. Mutta koodin ymmärrettävyys kärsii muuten heikosta koodin laadusta. Hankalasti identifioitavaa toisteisuutta on paljon - samoja attribuutteja haetaan useasta eri paikasta ja ristiin. 

- Miten agentti on muuttanut edellisessä tehtässä tekemääsi koodia?
Agentti tuntui aina suosivan uuden koodin kirjoittamista vanhan muokkaamisen sijaan. Herkästi se jätti luokkien metodeita käyttämättä ja liimasi päälle oman ratkaisunsa arkkitehtuurin toisessa kerroksessa.  

- Mitä uutta opit?
Opin agentin hyödyntämisestä. Silloin kun prompti tuotti muutosehdotuksen, joka oli vain yhden rivin pituinen tuntui, että osui kultasuoneen. Jossain refaktorointi tehtävissä se oli huomattavasti parempi kuin toisissa. 
