# Werkwijze voor nieuwe geanimeerde personages

Bijgewerkt: 27 november 2026  
Status: bindende werkwijze voor nieuwe personageproeven; geen nieuwe figuren gegenereerd bij het vastleggen van dit document.

## Doel

Een nieuw personage moet passen in de bestaande Pensioen Ontdekt-stijl én betrouwbaar werken met de bestaande animaties. Een afbeelding is pas geschikt als zowel het uiterlijk als de technische beweging is beoordeeld.

Deze werkwijze geldt zodra een chat vraagt om een nieuw personage, avatar, portret of een nieuwe variant van een bestaande figuur. De assistent leest eerst `PROJECT_STATUS.md` en dit document, haalt de daar genoemde beeldreferenties op en volgt de stappen in volgorde.

## Vaste beeldreferentie uit de eerste geslaagde ronde

De projecthistorie wijst naar [Vier personages in transparante sprite sheet.webp](https://chatgpt.com/library?file_id=libfile_7c1d877c434c8191b3d387b367ed1f0c&account_id=personal) als de bestaande sprite sheet die bij de eerste geslaagde generatie als directe referentie is gebruikt. Haal deze afbeelding bij een nieuwe personageopdracht op uit de Library en voeg haar rechtstreeks toe als beeldcontext. Controleer daarnaast de actuele productie-assets in het project; gebruik een bestaande productiefiguur als aanvullende maat- en animatiereferentie.

Gebruik de sprite sheet als stijl- en houdingstemplate, niet als bewijs dat elk figuur daarin productiegeschikt is. Gebruik geen conceptvellen, mislukte animatieproeven of niet-goedgekeurde nieuwe figuren als gouden referentie. Als deze Library-afbeelding niet toegankelijk is, of niet te rijmen is met de actuele productie-assets, stop en meld welke referentie ontbreekt voordat generatie begint.

## Wat bekend is over de eerste geslaagde generatie

In de beschikbare projectnotities staat dat de eerste geslaagde ronde een bestaande, goedgekeurde sprite sheet als directe beeldreferentie gebruikte. De nieuwe figuren zijn daarbij naast bestaande figuren beoordeeld op illustratiestijl, houding en proporties. Een tekstbeschrijving alleen bleek minder betrouwbaar voor stijlconsistentie.

De oorspronkelijke exacte prompt, referentiebestanden en numerieke gezichtsmaten zijn niet teruggevonden. Daarom presenteert dit document geen nieuwe maatvoering als historische afspraak. De beeldmaten hieronder zijn controlegrenzen voor toekomstige proeven en worden aan een goedgekeurde referentie gekoppeld.

## Vaste uitgangspunten

- Gebruik minimaal één goedgekeurd bestaand volledig personage als directe beeldreferentie in de beeldgenerator. Gebruik bij voorkeur de goedgekeurde sprite sheet of de naast elkaar beoordeelde bronfiguren. Een tekstprompt alleen is niet genoeg.
- De referentie bepaalt stijl, materiaalgevoel, gezichtsvorm, oogstijl, lijnwerk, lichtval, kleurverwerking, pose, camerastandpunt, lichaamsverhoudingen en schaal. Behoud die kenmerken; wijzig alleen de gevraagde identiteit, huidskleur, haar, hoofdbedekking of kleding.
- Maak per proef precies één volledig figuur. Geen groep, contact sheet of set van varianten in dezelfde generatie: die bemoeilijken een eerlijke maat- en animatiecontrole.
- Houd het figuur frontaal, volledig zichtbaar van kruin tot schoenzool, rechtop, met ontspannen armen langs het lichaam, symmetrische gewichtsverdeling en een vriendelijke, gesloten of zeer subtiele glimlach.
- Gebruik dezelfde canvasverhouding, transparante achtergrond, voetlijn, schaal en optische middellijn als de gekozen gouden referentie. Geen achtergrond, vloer, slagschaduw, gloed, randhalo, tekst, accessoires die niet zijn gevraagd of afgesneden lichaamsdelen.
- Vermijd karikaturen, nationale klederdracht en overdreven etnische kenmerken. Een identiteit wordt herkenbaar gemaakt met beperkte, natuurlijke verschillen; verander de bestaande tekenstijl niet.
- Als de goedgekeurde referentie niet beschikbaar is in de chat of via de projectbestanden, stop dan en vraag om die referentie. Genereer niet op basis van alleen tekst.

## Technische maatvoering

### Canvas, schaal en uitlijning

- De bestaande full-body assets zijn 560 pixels hoog. Behoud voor nieuwe full-body bronafbeeldingen die hoogte en dezelfde canvasverhouding als de gekozen goedgekeurde bron.
- Meet op de bronafbeelding, niet op een screenshot of verkleinde chatweergave. Bewaar de meetpunten als fracties van canvasbreedte en -hoogte, zodat dezelfde waarden op andere weergaveschalen controleerbaar zijn.
- Voeten staan op dezelfde basislijn als de referentie (maximaal 2 bronpixels verschil bij 560 px hoogte). De lichaamsmiddellijn wijkt maximaal 1% van de canvasbreedte af.
- Kruin, kin, schouderlijn, heupen, knieën en schoenzolen vallen binnen ±5% van hun positie ten opzichte van de totale figuurhoogte uit de referentie. Hoofd-breedte/-hoogte en schouderbreedte wijken maximaal ±5% af, tenzij Mike vooraf een bewuste ontwerpafwijking goedkeurt.
- Houd rondom het lichaam voldoende transparante ruimte voor de bestaande uitsnede. Geen lichaamsdeel raakt of kruist de canvasrand.

Deze toleranties zijn voorgestelde kwaliteitsgrenzen. Bij een goedgekeurde referentie met een aantoonbaar andere canvasmaat worden zij proportioneel omgerekend.

### Ogen en knipperen

- Gebruik geen universele oogradius of één vaste maat voor ieder personage. De ogen verschillen per gezicht; meet elk oog afzonderlijk op de nieuwe bron.
- Leg voor linker- en rechteroog vast: middelpunt (x,y), breedte, hoogte, kanteling en begrenzingsvak. Meet ook de afstand tussen de ogen en de afstand tot wenkbrauwen.
- De knipperlaag wordt vanuit die ankers gemaakt en naar de ooghoek en gezichtshoek van dat specifieke oog getransformeerd. Zij moet het oogwit, de iris, pupil en eventuele wimpers volledig bedekken, met alleen een kleine marge van circa 2% van de oogbreedte.
- De gesloten ooglijn volgt de breedte en kanteling van het open oog. Er mag geen stukje open oog zichtbaar blijven; de huidmaskers mogen niet als grote ovale vlekken zichtbaar zijn.
- Plaats het knippermasker en de gesloten ooglijn op dezelfde schaal en coördinaten als de bronfiguur. Koppel geen maat over van een ander personage zonder de ankers opnieuw te meten.

### Glimlach en neutrale mond

- Gebruik één en hetzelfde goedgekeurde gezicht als basis voor de glimlach en neutrale mond. Maak geen tweede gezicht en verschuif geen gezichtsonderdelen.
- Meet het mondmiddelpunt, de mondbreedte, hoogte, kanteling en het bounding box op de bronafbeelding. Bewaar deze ankers per personage.
- De glimlach blijft compact genoeg om binnen dat mondgebied te passen: geen brede tandrijke grijns, geen mondhoeken buiten het gemeten mondvak en geen glimlach die de wangvorm of neus bedekt.
- De neutrale variant is een kleine mondpatch die exact op dezelfde coördinaten en schaal past. De patch bevat geen neus, kin of grote delen van de wangen. Hij bedekt de tanden en glimlach volledig zonder zichtbare rechthoek, rand, smeer, kleurverschil of achtergebleven glimlachlijn.
- Maak glimlach- en neutrale toestand vanuit dezelfde afbeelding en transformeer ze met dezelfde ankers. Controleer beide overgangen heen en terug.

### Nek en eventuele hoofdbeweging

- De huidige standaardanimatie gebruikt knipperen en ademen; een hoofdbeweging hoort niet stilzwijgend bij de standaardset.
- Als de opdracht expliciet een lichte hoofdbeweging vraagt, plan die vóór de generatie. Maak hoofd en romp dan als afzonderlijk uitlijnbare lagen met overlap onder de kin/kraag, een duidelijke rotatiepivot bij de nek en voldoende getekende nek-/kraagruimte om bij een kleine rotatie geen gat of witte naad te tonen.
- Bij een hoofddoek of ander kledingstuk dat doorloopt over nek en romp moet de laagindeling de bedekking intact houden. Vereis geen zichtbare of onbedekte nek.
- Test de beoogde maximale draaiing met de echte lagen; een losse nek in de prompt zonder scheidbare lagen of pivot geldt niet als technische voorbereiding.

## Verplichte proefstappen

1. **Referentie vastzetten.** Noteer de exacte goedgekeurde bronafbeelding(en), assetversie en beoogde animaties. Gebruik deze bestanden rechtstreeks als referentie.
2. **Eén ontwerp genereren.** Maak één full-body proef volgens de vaste uitgangspunten. Genereer nog geen mond- of oogvarianten.
3. **Statische maatcontrole.** Leg de canvasmaat, voetlijn, middellijn, hoofdmaat, schouderlijn, oogankers en mondankers vast. Vergelijk het figuur naast de referentie op dezelfde afbeeldingshoogte.
4. **Animatielagen maken.** Maak voor alleen dit figuur de oogknippering en glimlach/neutrale mond met de bovenstaande ankers. Voeg een hoofd-/neklagen alleen toe wanneer die beweging expliciet deel uitmaakt van de opdracht.
5. **In de echte scène testen.** Gebruik dezelfde schaal en rendercode als de website. Bekijk meerdere cycli: open ogen → dicht → open; glimlach → neutraal → glimlach. Controleer op scheve plaatsing, lekkende originele pixels, huidvlekken, witte naden, flikkering, abrupte schaalverandering en verkeerd uitgelijnde gezichtskenmerken. Controleer ook de HTML-preview in de bedoelde browser; de preview moet de assets correct laden met de afgesproken relatieve paden of ingebedde assets.
6. **Eerst beoordelen, dan pas uitbreiden.** Deel de proef met Mike en wacht op expliciet akkoord. Pas na akkoord worden asset, ankers en werkwijze als goedgekeurde basis vastgelegd. Een tweede personage of batch wordt pas daarna gemaakt met die goedgekeurde proef én de oorspronkelijke gouden referentie als beeldcontext.
7. **Voor publicatie.** Herhaal de echte-scène controle voor alle relevante expressies en schermroutes. Publiceer niets zonder aparte expliciete publicatieopdracht en een goedgekeurde preview.

Een mislukte controle betekent terug naar de betreffende ontwerp- of ankerstap. De maat van een oog- of mondlaag niet op gevoel verschuiven om een fout te verbergen.

## Herbruikbare prompttemplate

Gebruik de goedgekeurde referentieafbeelding als directe input/context; vul alleen de blokhaken in:

> Maak één nieuw volledig personage voor Pensioen Ontdekt, met de bijgevoegde goedgekeurde personageafbeelding als leidende stijl-, pose-, schaal- en proportiereferentie. Behoud dezelfde zachte, verzorgde 3D-cartoonillustratie, gezichtsstijl, oogverhouding, contouren, materiaalweergave, lichtval, frontale camera, volledige lichaamslengte, ontspannen rechte houding, armpositie, voetlijn, canvasverhouding en transparante achtergrond. Maak alleen deze gevraagde wijziging: [identiteits-/uiterlijke kenmerken]. Kleding: [kleding]. Houd gelaatstrekken natuurlijk en subtiel; geen stereotype, nationale klederdracht of overdrijving. Geef een vriendelijke gesloten of heel subtiele glimlach met een compacte mond die later door een kleine neutrale mondpatch vervangen kan worden. Eén persoon, symmetrisch recht van voren, van kruin tot schoenzolen zichtbaar. Geen achtergrond, schaduw, gloed, randhalo, tekst, extra persoon, extra voorwerp of afgesneden lichaamsdeel. Verander de referentiestijl en lichaamsproporties niet.

De prompt vervangt de visuele referentie niet. Als de beeldgenerator de referentie niet daadwerkelijk kan ontvangen, wordt er niet gegenereerd.

## Registratie per goedgekeurd personage

Bewaar samen met het goedgekeurde bronbestand:

- unieke personage-ID en versienummer;
- gebruikte gouden referentie en bronassetversie;
- broncanvas en uiteindelijke weergaveschaal;
- voetenbasislijn en lichaamsmiddellijn;
- hoofd- en schoudermaten;
- aparte linker- en rechteroogankers;
- mondankers en glimlach/neutraal-patchafmetingen;
- eventuele hoofd-/romplagen en rotatiepivot;
- resultaat van de scènecontrole en goedkeuringsdatum.

Zo kan de volgende chat de juiste bestanden en metingen ophalen in plaats van de generatie opnieuw uit alleen een beschrijving af te leiden.
