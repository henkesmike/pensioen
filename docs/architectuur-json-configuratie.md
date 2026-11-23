# Architectuurafspraak: configuratie in JSON

Datum: 23 november 2026
Status: goedgekeurd ontwerpprincipe; implementatie volgt in een volgende technische iteratie.

## Besluit

Houd de programmacode zo generiek mogelijk. Bewaar duidelijke regelingafhankelijke, personage- en animatieparameters in gestructureerde JSON-bestanden, niet als verspreide vaste waarden in Python, HTML of JavaScript. Gebruik voorlopig **geen database**. Ontwerp de gegevens zodanig dat later een database als bron kan dienen zonder de animatie- en scenariologica opnieuw te ontwerpen.

Dit besluit verandert de bestaande demo niet onmiddellijk. De huidige code bevat nog ingebedde configuratie en proefwaarden; de migratie naar JSON is een afzonderlijke stap.

## Voorgestelde indeling

- `data/regelingen.json`: pensioenregelingen en hun parameters, zoals partnerpensioenpercentage en uitloopduur.
- `data/personages.json`: beschikbare personages, rollenonafhankelijke eigenschappen, verwijzingen naar illustraties, en gemeten ankers/maskers voor ogen, mond, nek en voeten.
- `data/animaties.json`: gedeelde bewegingstypen en instelbare standaarden, zoals ademhalingscyclus, intensiteit en knipperritme.

Bij groei kunnen deze bestanden per regeling of per personage worden opgesplitst zonder dat de semantiek verandert. Scenario's, fragmenten en voice-overselectie kunnen later hun eigen gegevensbestanden krijgen. Niet alles hoeft meteen geparametriseerd te worden: alleen betekenisvolle, stabiele instellingen, niet iedere tijdelijke programmeerconstante.

## Voorbeeldstructuur (illustratief, nog niet geïmplementeerd)

```json
{
  "schema_version": 1,
  "regelingen": [
    {
      "id": "regeling-a",
      "naam": "Fictieve regeling A",
      "partnerpensioen": {
        "percentage_pensioengevend_salaris": 40,
        "uitloop_maanden": 3
      }
    }
  ]
}
```

Voorbeeld voor een animatieconfiguratie:

```json
{
  "schema_version": 1,
  "animaties": {
    "ademhalen": {
      "cyclus_seconden": 3.7,
      "relatieve_intensiteit": 0.7
    }
  }
}
```

De voorbeelden zijn geen definitief schema. Definieer veldnamen en eenheden expliciet bij de implementatie. Scheid technische bewegingsinstellingen van pensioeninhoud.

## Regels voor onderhoudbaarheid en toekomstige database

1. **Stabiele ID's:** iedere regeling, elk personage en ieder herbruikbaar fragment krijgt een unieke, stabiele identificatie.
2. **Verwijzingen in plaats van duplicatie:** verwijs naar personages, illustraties, animatietypen en fragmenten met ID's of stabiele assetpaden.
3. **Vaste typen en eenheden:** onderscheid bijvoorbeeld percentagepunten (40), maanden (3), seconden (3.7) en fracties (0.7); documenteer de betekenis.
4. **Validatie:** controleer bij het inlezen verplichte velden, typen, toegestane waarden, unieke ID's en bestaande verwijzingen. Voeg bij voorkeur JSON Schema en automatische tests toe.
5. **Versiebeheer:** voeg `schema_version` toe en houd wijzigingen aan het gegevensformaat expliciet bij.
6. **Geen logica verstoppen in data:** JSON bevat waarden, keuzes en verwijzingen; berekeningen, animatiefuncties en validatieregels blijven in herbruikbare code.
7. **Één inleeslaag:** de applicatie krijgt gevalideerde configuratie via een centrale loader. Bij een latere databasewissel verandert primair deze gegevenslaag, niet de animatie-engine.
8. **Geen geheimen in JSON in GitHub of de webroot:** API-sleutels, tokens en privé-audio blijven buiten publieke bestanden.
9. **Geen onnodige complexiteit:** voorlopig geen database, beheerscherm, API of ingewikkelde abstractielaag bouwen uitsluitend voor mogelijke toekomstige behoeften.

## Migratiepad

1. Inventariseer de bestaande ingebedde parameters in Python/JavaScript/HTML.
2. Stel een minimaal JSON-schema op voor de eerstvolgende relevante wijziging.
3. Verplaats de betrokken waarden naar JSON en voeg validatie en tests toe.
4. Controleer dat alle vier fictieve regelingen en de personagecombinaties exact hetzelfde blijven werken.
5. Laat de applicatie daarna uitsluitend via een centrale inleeslaag configuratie ophalen.
6. Pas als een database functioneel nodig wordt, ontwerp tabellen/collecties en vervang de bron achter de inleeslaag. Complex geneste JSON hoeft niet letterlijk één-op-één een relationele tabel te worden.

## Afbakening

Deze afspraak is **documentatie en architectuurrichting**, geen bevestiging dat de JSON-bestanden al bestaan of dat de bestaande demo is omgebouwd. De publieke website en deployment blijven ongewijzigd.

Zie ook [technische opzet animaties](technische-opzet-animaties.md), [ontwerpprincipes personages](ontwerpprincipes-personages.md) en [projectstatus](../PROJECT_STATUS.md).
