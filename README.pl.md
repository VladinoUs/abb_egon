# ABB Egon — integracja Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/VladinoUs/abb_egon)
![GitHub release](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Niestandardowa integracja Home Assistant dla inteligentnego systemu instalacji elektrycznej **ABB Egon**. Integracja komunikuje się bezpośrednio z lokalnym API HTTP/XML modułu komunikacyjnego ABB Egon, bez chmury i bez usług stron trzecich.

---

## Przegląd

Ta integracja umożliwia podłączenie ABB Egon do Home Assistant przez lokalną sieć lub przez dostęp zewnętrzny, jeśli urządzenie jest dostępne poprzez przekierowanie portów. Konfiguracja odbywa się przez natywny Home Assistant config flow, więc nie ma potrzeby edytowania pliku `configuration.yaml`.

### Najważniejsze funkcje

- Lokalna komunikacja HTTP/XML bez chmury.
- Konfiguracja przez interfejs Home Assistant.
- Automatyczne logowanie i odnawianie sesji.
- Regulowany interwał odpytywania w Options flow.
- Automatyczne wykrywanie dostępnych elementów urządzenia.
- Obsługa wielu typów encji.
- Wielojęzyczny interfejs użytkownika.

---

## O ABB Ego-n

Inteligentny system instalacji domowej **ABB Ego-n** został wprowadzony na rynek w 2007 roku, a ABB prezentowało go jako przystępne rozwiązanie dla nowych budynków i modernizacji.

Rozwój i dystrybucja systemu zostały zakończone w **2017** roku, a według IQinstalace ta firma przejęła później serwis, wsparcie techniczne i dostawy części zamiennych do tego systemu.

Części zamienne, serwis i wsparcie techniczne są dostępne tutaj:
- [iqinstalace.cz/elektroinstalace](http://iqinstalace.cz/elektroinstalace/)
- [viktorstrouhal@seznam.cz](mailto:viktorstrouhal@seznam.cz)

---

## Obsługiwane platformy

Integracja obecnie obsługuje te encje:

- `sensor`
- `switch`
- `light`
- `cover`
- `number`
- `button`

Dokładna liczba utworzonych encji zależy od konfiguracji i typów elementów dostępnych w konkretnej instalacji ABB Egon.

---

## Instalacja przez HACS

Jeśli używasz HACS, możesz dodać integrację jako niestandardowe repozytorium:

1. Otwórz **HACS**.
2. Przejdź do **Integrations**.
3. Otwórz menu z trzema kropkami i wybierz **Custom repositories**.
4. Dodaj adres repozytorium:
   `https://github.com/VladinoUs/abb_egon`
5. Jako typ repozytorium wybierz **Integration**.
6. Zainstaluj integrację.
7. Uruchom ponownie Home Assistant.

---

## Instalacja ręczna

Jeśli nie używasz HACS, skopiuj folder integracji ręcznie:

1. Pobierz to repozytorium z GitHub.
2. Skopiuj folder:

```text
custom_components/abb_egon
```

do folderu Home Assistant:

```text
/config/custom_components/abb_egon
```

3. Uruchom ponownie Home Assistant.

---

## Konfiguracja

Po ponownym uruchomieniu Home Assistant:

1. Otwórz **Settings** → **Devices & Services**.
2. Kliknij **Add Integration**.
3. Wyszukaj **ABB Egon**.
4. Wprowadź dane dostępu do modułu ABB Egon.

### Dostęp lokalny w sieci

```text
Host: 192.168.1.XXX
Port: 80
```

Użyj lokalnego adresu IP modułu komunikacyjnego ABB Egon w swojej sieci domowej.

### Dostęp zewnętrzny przez przekierowanie portów

Jeśli łączysz się z ABB Egon z zewnątrz przez router i NAT/port mapping, podaj publiczny adres IP lub nazwę hosta oraz port zewnętrzny ustawiony w routerze:

```text
Host: twoje-publiczne-ip-lub-domena.pl
Port: 8888
```

### Domyślne dane logowania

Jeśli nie zmieniałeś ich w systemie ABB Egon, integracja domyślnie używa tych wartości:

```text
Użytkownik: ABB
Hasło: egon
```

---

## Ustawienia

Integracja obsługuje również ustawienia użytkownika poprzez **Options flow**.

Obecnie można zmienić przede wszystkim:
- interwał odpytywania (`scan_interval`)

Po zmianie ustawień integracja zostaje automatycznie przeładowana, aby nowe wartości zaczęły działać bez ręcznej ingerencji.

---

## Bezpieczeństwo

> ⚠️ **Ważne:** Jeśli ABB Egon jest wystawiony bezpośrednio do publicznego internetu przez HTTP, komunikacja nie jest szyfrowana. Dane logowania i ruch sieciowy mogą zostać przechwycone.

Zalecane działania:
- użyj **VPN**,
- ogranicz dostęp przez reguły **firewall**,
- zezwól tylko na wybrane adresy IP,
- nie wystawiaj urządzenia bezpośrednio do internetu bez dodatkowej ochrony.

---

## O projekcie

Ten projekt to integracja społecznościowa dla użytkowników ABB Egon, którzy chcą sterować swoimi urządzeniami i monitorować je przez Home Assistant. Korzysta wyłącznie z lokalnej komunikacji i nie wymaga usług chmurowych ani kont zewnętrznych.

---

## Ważne informacje

- To nie jest oficjalny produkt ABB.
- Projekt nie jest oficjalnie wspierany przez ABB.
- Korzystasz na własną odpowiedzialność.
- Działanie może zależeć od konkretnej wersji modułu komunikacyjnego lub od sposobu wdrożenia ABB Egon.

---

## Wsparcie projektu

Ten projekt jest darmowy i open source. Jeśli oszczędził Ci czas lub ulepszył Twój smart home, możesz wesprzeć dalszy rozwój drobną wpłatą:

☕ **Postaw kawę przez Revolut:**  
[https://revolut.me/sdaddy](https://revolut.me/sdaddy)

![Revolut QR](./revolut_qr.png)

---

## Licencja

Ten projekt jest منتشرowany na licencji **MIT**.
