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

#### Nabevinding van personageproef v1 (27 november 2026)

De eerste proef met de vrouw en man gebruikte oog- en mondankers die visueel waren geschat, niet gemeten op de definitieve bronafbeelding. De HTML tekende voor beide ogen van de vrouw dezelfde soort ellips (straal 31 × 23 bronpixels) en zette het linkeroogmiddelpunt op x=459 en het rechteroog op x=558. De ogen zijn niet symmetrisch: de vorm, wimpers en kanteling verschillen. Daardoor sloot het linkermasker niet aan op de werkelijke oogrand en bleef aan de buitenzijde wit zichtbaar.

De mondoverlay was eveneens geschat (middelpunt x=512, y=285). De vervanging bestond uit een egale, radiale huidskleurvlek met daarover een lijn van 3,1 bronpixels. Bij een figuurbreedte van 500 pixels wordt die lijn ongeveer 1,5 schermpixels dik. De tint en vage patch sloten niet aantoonbaar aan op de huidtextuur en de mondlijn was op die weergaveschaal te weinig zichtbaar. De JavaScript-knoppen koppelden wel aan de neutrale stand; het probleem zat in de plaatsing en vormgeving van de overlay, niet in de knopactie.

Deze proef laat zien dat getallen uit een verkleinde chatweergave geen betrouwbare ankers zijn. Een overlay mag pas worden beoordeeld nadat de ankers uit de definitieve bron zijn gemeten en de echte HTML-weergave is gecontroleerd.

#### Aangescherpte werkwijze voor oog- en mondlagen

1. Meet uitsluitend op het definitieve bronbestand op volledige resolutie. Noteer canvasbreedte en -hoogte en bewaar elk anker als genormaliseerde positie (x/canvasbreedte, y/canvashoogte), plus de omgerekende bronpixels.
2. Meet linker- en rechteroog apart: begrenzingsvak van het volledige oog inclusief wimpers, middelpunt, breedte, hoogte en kanteling. Gebruik geen overgenomen, gespiegeld of op het oog geschat centrum of masker.
3. Teken of bewerk elk gesloten ooglid passend op de gemeten contour en hoek. Controleer in de echte HTML-preview op de uiteindelijke afbeeldingsschaal dat het oogwit, de iris, pupil en wimpers volledig verdwijnen, zonder grote huidvlekken of witte rand. Controleer beide ogen afzonderlijk én samen.
4. Meet ook het mondvak op de bron: glimlachlijn, tanden indien aanwezig, mondhoeken en middelpunt. Maak een huidgematchte zachte patch uit hetzelfde gezicht; gebruik geen uniforme kleurvlek die alleen op een gemiddelde huidskleur is gebaseerd.
5. Plaats de neutrale mondlijn binnen het gemeten mondvak. Kies de lijndikte op de uiteindelijke weergaveschaal zodat de neutrale vorm zichtbaar is, terwijl de hele glimlach en eventuele tanden verborgen blijven. Controleer dat geen smile-pixels, patchrand of kleurverschil zichtbaar blijven.
6. Open de HTML-preview in een browser en bedien afzonderlijk: glimlach/open ogen, knipperen, neutrale mond en neutrale mond met gesloten ogen. Controleer ook automatisch meerdere cycli en de overgang terug naar de glimlach. Een stand telt pas als geslaagd wanneer hij in de browser echt zichtbaar is op de beoogde grootte.
7. Sla na de controle de exacte bronmaat, ankers, masker- en patchmaten en controle-uitkomst per personage op. Bij een mislukking corrigeer eerst het gemeten anker of de overlayvorm; maskeer de fout niet met willekeurig verschuiven.

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

## Meetresultaat personageproef v2 — 27 november 2026

De v2-proef gebruikt exact dezelfde twee bronafbeeldingen als v1. De bronbestanden zijn 1024 × 1536 pixels; de SHA-256 van elk bestand is gelijk aan de afbeelding die in v1 is ingebed. De oog- en mondankers hieronder zijn afzonderlijk op die bronpixels gemeten. Bounding boxes zijn inclusief de genoemde grenspixel; de genormaliseerde centra zijn berekend als (x/1024, y/1536).

| Figuur | Kenmerk | Gemeten bronvak (x₁,y₁–x₂,y₂) | Midden in bronpixels | Genormaliseerd midden |
|---|---|---:|---:|---:|
| Vrouw | Linkeroog | (427,189)–(497,234) | (462,211.5) | (0.451172, 0.137695) |
| Vrouw | Rechteroog | (529,189)–(600,235) | (564.5,212) | (0.551270, 0.138021) |
| Vrouw | Mond | (473,278)–(555,299) | (514,288.5) | (0.501953, 0.187826) |
| Man | Linkeroog | (433,192)–(495,229) | (464,210.5) | (0.453125, 0.137044) |
| Man | Rechteroog | (529,192)–(585,229) | (557,210.5) | (0.543945, 0.137044) |
| Man | Mond | (459,277)–(576,296) | (517.5,286.5) | (0.504883, 0.186523) |

De neutrale oog- en mondtoestanden gebruiken huidkleurpatches die uit de plaatselijke kleurgradiënt van dezelfde bronfiguur zijn berekend. De oogpatches volgen de afzonderlijke oogcontouren en hebben een kleine veiligheidsmarge. De neutrale mondlijn is 5.4 bronpixels breed bij de vrouw en 5.6 bij de man; op 500 pixels figuurbreedte is dat circa 2.6–2.7 schermpixels.

**Controle-uitkomst:** de lokale HTML is bijgewerkt als v2; de figuren, scène, bediening en automatische animatiecode uit v1 zijn behouden. De gevraagde browsercontrole van glimlach, knipperen, neutrale mond, combinatie en automatische beweging kon niet worden uitgevoerd. De browser weigerde de lokale bestands-URL met deze melding: “Browser Use rejected this action due to browser security policy. Reason: The browser URL policy blocks this action. Cloud browser could not acquire authority to trigger network egress. The URL policy gate did not grant access. The requested URL protocol is not allowed. Allowed protocols: \"http:\", \"https:\".” Er is daarom geen browsermatige visuele goedkeuring; v2 blijft een onbeoordeelde preview en is niet gepubliceerd.
\n

### Follow-up: correctie naar personageproef v3 — 27 november 2026

Mike meldde dat in v2 de neutrale mond niet zichtbaar was en dat de hele figuur verdween zodra die stand werd gekozen. Code-inspectie laat zien dat de neutrale huidpatch als 1024 × 1536 PNG binnen dezelfde SVG-groep stond als de mondlijn; één groepsopaciteit bestuurde zo rasterpatch en vectorlijn tegelijk. Dit is de kwetsbare compositingconstructie en de waarschijnlijke oorzaak; de browserweergave kon niet worden geïnspecteerd om dit causaal te bevestigen.

V3 zet de basisafbeelding expliciet onderaan. De huidpatch is nu een los, bijgesneden HTML-afbeeldingslaagje; de neutrale mondlijn en gesloten ooglijnen zijn afzonderlijke SVG-paden erboven. De knop verandert alleen de zichtbaarheid van die overlaylagen. De oogmaskercontouren zijn 2% verkleind rond elk gemeten ooganker; de gesloten ooglijnen zijn ook korter gemaakt. De bronfiguren blijven ongewijzigd. V3 bevat patchuitsneden van 179 × 54 pixels voor de twee ogen en 87 × 27 pixels voor de vrouwenmond, en 157 × 44 en 117 × 25 pixels voor de mannenogen en mond.

**Controle-uitkomst v3:** HTML-structuur en laagindeling zijn statisch gecontroleerd: twee losse mondpatches, twee losse oogpatches, vectorlijnen zonder rasterafbeeldingen in de SVG en ongewijzigde bronafbeeldingen. Browsercontrole van de zichtbare neutrale stand en alle overige standen is nog niet mogelijk via de lokale file-URL: de browser staat alleen http: en https: toe. De exacte eerdere foutmelding is vastgelegd in het v2-meetresultaat hierboven. V3 is dus een structureel gecorrigeerde maar nog niet browsermatig goedgekeurde preview. Er is niets gepubliceerd.
