# ABB Egon — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/VladinoUs/abb_egon)
![GitHub release](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Eine benutzerdefinierte Home Assistant Integration für das intelligente Elektroinstallationssystem **ABB Egon**. Die Integration kommuniziert direkt mit der lokalen HTTP/XML-API des ABB-Egon-Kommunikationsmoduls, ohne Cloud-Dienste oder Drittanbieter.

---

## Übersicht

Diese Integration ermöglicht es, ABB Egon über ein lokales Netzwerk oder über externen Zugriff mit Home Assistant zu verbinden, wenn das Gerät per Portweiterleitung erreichbar ist. Die Konfiguration erfolgt über den nativen Home-Assistant-Config-Flow, sodass keine Änderungen an `configuration.yaml` erforderlich sind.

### Hauptfunktionen

- Lokale HTTP/XML-API-Kommunikation ohne Cloud.
- Konfiguration über die Home-Assistant-Oberfläche.
- Automatische Anmeldung und Sitzungserneuerung.
- Einstellbares Abrufintervall über den Options-Flow.
- Automatische Erkennung verfügbarer Geräteelemente.
- Unterstützung mehrerer Entitätstypen.
- Mehrsprachige Benutzeroberfläche.

---

## Über ABB Ego-n

Das intelligente Haus-Elektroinstallationssystem **ABB Ego-n** wurde im Jahr 2007 auf den Markt gebracht und von ABB als erschwingliche Lösung für Neubauten und Renovierungen vorgestellt.

Die Entwicklung und der Vertrieb des Systems wurden im Jahr **2017** eingestellt. Laut IQinstalace übernahm dieses Unternehmen anschließend Service, technischen Support und die Ersatzteilversorgung für das System.

Ersatzteile, Service und technischer Support sind hier zu finden:
- [iqinstalace.cz/elektroinstalace](http://iqinstalace.cz/elektroinstalace/)
- [viktorstrouhal@seznam.cz](mailto:viktorstrouhal@seznam.cz)

---

## Unterstützte Plattformen

Die Integration unterstützt derzeit diese Entitäten:

- `sensor`
- `switch`
- `light`
- `cover`
- `number`
- `button`

Die genaue Anzahl der erstellten Entitäten hängt von der Konfiguration und den verfügbaren Elementen in einer bestimmten ABB-Egon-Installation ab.

---

## Installation über HACS

Wenn du HACS verwendest, kannst du die Integration als benutzerdefiniertes Repository hinzufügen:

1. Öffne **HACS**.
2. Gehe zu **Integrationen**.
3. Öffne das Drei-Punkte-Menü und wähle **Custom repositories**.
4. Füge die Repository-URL hinzu:
   `https://github.com/VladinoUs/abb_egon`
5. Wähle als Repository-Typ **Integration**.
6. Installiere die Integration.
7. Starte Home Assistant neu.

---

## Manuelle Installation

Wenn du HACS nicht verwendest, kopiere den Integrationsordner manuell:

1. Lade dieses Repository von GitHub herunter.
2. Kopiere den Ordner:

```text
custom_components/abb_egon
```

in deinen Home-Assistant-Ordner:

```text
/config/custom_components/abb_egon
```

3. Starte Home Assistant neu.

---

## Konfiguration

Nach dem Neustart von Home Assistant:

1. Öffne **Einstellungen** → **Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen**.
3. Suche nach **ABB Egon**.
4. Gib die Zugangsdaten des ABB-Egon-Moduls ein.

### Lokaler Zugriff im Netzwerk

```text
Host: 192.168.1.XXX
Port: 80
```

Verwende die lokale IP-Adresse des ABB-Egon-Kommunikationsmoduls in deinem Heimnetzwerk.

### Externer Zugriff über Portweiterleitung

Wenn du ABB Egon von außen über Router und NAT/Port-Mapping erreichst, gib die öffentliche IP-Adresse oder den Hostnamen und den im Router konfigurierten externen Port ein:

```text
Host: deine-oeffentliche-ip-oder-domain.de
Port: 8888
```

### Standard-Anmeldedaten

Falls du sie im ABB-Egon-System nicht geändert hast, verwendet die Integration standardmäßig diese Werte:

```text
Benutzername: ABB
Passwort: egon
```

---

## Einstellungen

Die Integration unterstützt auch Benutzereinstellungen über den **Options-Flow**.

Derzeit kann vor allem Folgendes geändert werden:
- Abrufintervall (`scan_interval`)

Nach dem Ändern der Einstellungen wird die Integration automatisch neu geladen, damit die neuen Werte ohne manuelles Eingreifen wirksam werden.

---

## Sicherheit

> ⚠️ **Wichtig:** Wenn ABB Egon direkt über HTTP im öffentlichen Internet erreichbar ist, ist die Kommunikation nicht verschlüsselt. Anmeldedaten und Datenverkehr können abgefangen werden.

Empfohlene Maßnahmen:
- ein **VPN** verwenden,
- den Zugriff durch **Firewall-Regeln** einschränken,
- nur ausgewählte IP-Adressen zulassen,
- das Gerät nicht ohne zusätzlichen Schutz direkt ins Internet exponieren.

---

## Über das Projekt

Dieses Projekt ist eine Community-Integration für ABB-Egon-Nutzer, die ihre Geräte über Home Assistant steuern und überwachen möchten. Es verwendet nur lokale Kommunikation und benötigt weder Cloud-Dienste noch externe Konten.

---

## Wichtige Hinweise

- Dies ist kein offizielles ABB-Produkt.
- Das Projekt wird nicht offiziell von ABB unterstützt.
- Nutzung auf eigene Gefahr.
- Die Funktionalität kann von der jeweiligen Version des Kommunikationsmoduls oder von der konkreten ABB-Egon-Installation abhängen.

---

## Projekt unterstützen

Dieses Projekt ist kostenlos und Open Source. Wenn es dir Zeit gespart oder dein Smart Home verbessert hat, kannst du die weitere Entwicklung mit einer kleinen Spende unterstützen:

☕ **Einen Kaffee über Revolut spendieren:**  
[https://revolut.me/sdaddy](https://revolut.me/sdaddy)

![Revolut QR](revolut_qr.jpg)

---

## Lizenz

Dieses Projekt steht unter der **MIT**-Lizenz.