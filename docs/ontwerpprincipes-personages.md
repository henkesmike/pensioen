# Ontwerpprincipes – personages en personalisatie

Bijgewerkt: 27 november 2026  
Status: akkoord; tien selecteerbare personages, waaronder vier aanvullende ontwerpen.

## Doel

Animaties laten aansluiten bij verschillende bezoekers zonder afzonderlijke films of programmacode per doelgroep te onderhouden. De bezoeker kiest zelf twee personages; het systeem leidt uiterlijk of afkomst niet af uit persoonsgegevens.

## Vastgelegde bibliotheek

De website bevat zes eerder goedgekeurde personages en vier aanvullingen:

- een man met witte kufi en olijfgroen overhemd;
- een vrouw met mauvekleurige hijab;
- een man met een breed, generiek Aziatisch uiterlijk;
- een vrouw met een breed, generiek Aziatisch uiterlijk.

De Aziatische ontwerpen verwijzen niet nadrukkelijk naar één land of nationale klederdracht. Het doel is herkenning zonder karikatuur. Er zijn geen oudere varianten toegevoegd.

## Werkwijze voor nieuwe afbeeldingen

1. Gebruik bij het genereren de goedgekeurde bestaande personages als directe beeldreferentie/context. Alleen een tekstbeschrijving gebruiken is onvoldoende voor stijlconsistentie.
2. Houd de bestaande illustratiestijl, vriendelijke neutrale glimlach, volledige lichaamslengte, frontale houding, schaal, lichaamsverhoudingen, contouren, belichting en transparante achtergrond aan.
3. Verander uitsluitend de gevraagde kenmerken. Vermijd stereotypen, nationale kostuums en overdreven etnische kenmerken.
4. Genereer of beoordeel de figuren op dezelfde schaal naast bestaande personages. Controleer ook afzonderlijk de uitsnede, alpha-rand en ankerpunten die nodig zijn voor animatie.
5. Laat eerst de afbeeldingen beoordelen. Pas na akkoord worden ze als definitieve assets in de keuzelijst en animatiebron opgenomen.

## Technische integratie

- Houd stabiele personage-ID's aan en gebruik dezelfde ID in de portretkeuze, de partnerpensioenanimatie en de scheidingsanimatie.
- De portretten zijn 167 × 160 pixels. De transparante volledige figuren zijn 560 pixels hoog, met gemeten oog- en mondankers voor de bestaande animatielaag.
- De homepage leest de bestaande animatiebron uit een vastgepinde Git-commit en voegt de vier aanvullende figuren uit `assets/personage-overrides.json` toe. Volledige figuren en portretten worden vanaf vaste Git-commit-URL's geladen. Na wijziging van de afbeeldingen moet de overridebron naar de commit met die assets verwijzen; na wijziging van de overrides moet de homepage naar de nieuwe commit verwijzen.
- De bestaande homepage-uitrol op de VPS publiceert alleen `index.html`; daarom worden kleine portretten in die pagina opgenomen. De volledige filmbron en figuren blijven als aparte brondata beschikbaar via GitHub.
- Bewegingen en scènes werken op rollen (deelnemer en partner), niet op afkomst of een specifiek personage. Relatiecombinaties blijven onafhankelijk van de gekozen figuren.

## Grenzen

Deze set vergroot de herkenning, maar pretendeert niet elke afkomst afzonderlijk te vertegenwoordigen. Verdere varianten worden alleen toegevoegd als daar een concrete behoefte voor is en ze binnen dezelfde stijl en onderhoudbare animatie-opzet passen.
