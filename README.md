# ABB Egon — Home Assistant integrácia

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/VladinoUs/abb_egon)
![GitHub release](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Jazykové verzie: [Slovenčina](README.md) | [English](README.en.md) | [Deutsch](README.de.md) | [Magyar](README.hu.md) | [Polski](README.pl.md)

Vlastná integrácia pre Home Assistant pre inteligentný elektroinštalačný systém **ABB Egon**. Integrácia komunikuje priamo s lokálnym HTTP/XML API komunikačného modulu ABB Egon bez cloudu a bez služieb tretích strán [web:177][web:179].

---

## Prehľad

Táto integrácia umožňuje pripojiť ABB Egon do Home Assistanta cez lokálnu sieť alebo cez externý prístup, ak je zariadenie dostupné cez presmerovanie portov. Konfigurácia prebieha cez natívny Home Assistant config flow, takže nie je potrebné upravovať `configuration.yaml` [web:173][web:177].

### Hlavné vlastnosti

- Lokálna komunikácia cez HTTP/XML API bez cloudu.
- Konfigurácia cez Home Assistant UI.
- Automatické prihlásenie a obnova relácie.
- Nastaviteľný interval obnovovania cez Options flow.
- Automatické načítanie dostupných prvkov zo zariadenia.
- Podpora viacerých typov entít.
- Viacjazyčné používateľské rozhranie.

---

## O ABB Ego-n

Inteligentný systém domovej elektroinštalácie **ABB Ego-n** bol na trhu dostupný od roku 2007 a ABB ho prezentovalo ako prístupné riešenie pre novostavby aj rekonštrukcie [web:185][web:186].

Vývoj a distribúcia systému boli v roku **2017** ukončené a podľa IQinstalace táto spoločnosť následne prevzala servis, technickú podporu aj dodávky nových dielov pre tento systém [web:185].

Náhradné diely, servis a technickú podporu je možné nájsť napríklad tu:
- [iqinstalace.cz/elektroinstalace](http://iqinstalace.cz/elektroinstalace/) [web:185]
- [viktorstrouhal@seznam.cz](mailto:viktorstrouhal@seznam.cz) [web:185]

---

## Podporované platformy

Integrácia aktuálne podporuje tieto entity:

- `sensor`
- `switch`
- `light`
- `cover`
- `number`
- `button`

Presný počet vytvorených entít závisí od konfigurácie a typov prvkov dostupných v konkrétnej ABB Egon inštalácii.

---

## Inštalácia cez HACS

Ak používaš HACS, môžeš integráciu pridať ako vlastný repozitár:

1. Otvor **HACS**.
2. Choď do **Integrations**.
3. Otvor menu cez tri bodky a vyber **Custom repositories**.
4. Pridaj URL repozitára:
   `https://github.com/VladinoUs/abb_egon`
5. Ako typ repozitára vyber **Integration**.
6. Nainštaluj integráciu.
7. Reštartuj Home Assistant [web:173][web:184][web:179].

---

## Manuálna inštalácia

Ak HACS nepoužívaš, skopíruj priečinok integrácie ručne:

1. Stiahni tento repozitár z GitHubu.
2. Skopíruj priečinok:

```text
custom_components/abb_egon
```

do svojho Home Assistant priečinka:

```text
/config/custom_components/abb_egon
```

3. Reštartuj Home Assistant [web:177][web:176].

---

## Konfigurácia

Po reštarte Home Assistanta:

1. Otvor **Settings** → **Devices & Services**.
2. Klikni na **Add Integration**.
3. Vyhľadaj **ABB Egon**.
4. Zadaj prístupové údaje k ABB Egon modulu [web:173].

### Lokálny prístup v sieti

```text
Host: 192.168.1.XXX
Port: 80
```

Použi lokálnu IP adresu komunikačného modulu ABB Egon vo svojej domácej sieti.

### Externý prístup cez presmerovanie portov

Ak pristupuješ k ABB Egon zvonka cez router a NAT/Port Mapping, zadaj verejnú IP adresu alebo hostname a externý port nastavený v routeri:

```text
Host: tvoja-verejna-ip-alebo-domena.sk
Port: 8888
```

### Predvolené prihlasovacie údaje

Ak si ich v ABB Egon systéme nemenil, integrácia štandardne počíta s týmito hodnotami:

```text
Používateľ: ABB
Heslo: egon
```

---

## Nastavenia

Integrácia podporuje aj používateľské nastavenia cez **Options flow**.

Aktuálne je možné meniť najmä:
- interval obnovovania dát (`scan_interval`)

Po zmene nastavení sa integrácia automaticky znovu načíta, aby sa nové hodnoty prejavili bez potreby ručného zásahu [web:70].

---

## Bezpečnosť

> ⚠️ **Dôležité upozornenie:** Ak vystavíš ABB Egon priamo na verejný internet cez HTTP, komunikácia nie je šifrovaná. Prihlasovacie údaje aj prevádzka môžu byť zachytené.

Odporúčané riešenia:
- použiť **VPN**,
- obmedziť prístup cez **firewall pravidlá**,
- povoliť prístup iba z vybraných IP adries,
- nevystavovať zariadenie priamo na internet bez dodatočného zabezpečenia.

---

## O projekte

Tento projekt vznikol ako komunitná integrácia pre používateľov systému ABB Egon, ktorí chcú svoje zariadenia ovládať a monitorovať cez Home Assistant. Integrácia používa lokálnu komunikáciu a nevyžaduje cloudové služby ani externé účty.

---

## Dôležité informácie

- Toto nie je oficiálny produkt spoločnosti ABB.
- Projekt nie je oficiálne podporovaný spoločnosťou ABB.
- Používanie je na vlastné riziko.
- Funkčnosť môže závisieť od konkrétnej verzie komunikačného modulu alebo od spôsobu nasadenia ABB Egon v danej inštalácii.

---

## Podpora projektu

Tento projekt je bezplatný a open source. Ak ti ušetril čas alebo zlepšil tvoju smart domácnosť, môžeš podporiť ďalší vývoj malým príspevkom:

☕ **Pozvi ma na kávu cez Revolut:**  
[https://revolut.me/sdaddy](https://revolut.me/sdaddy)

![Revolut QR](revolut_qr.jpg)

---

## Licencia

Tento projekt je distribuovaný pod licenciou **MIT**.