# ABB Egon — Home Assistant integráció

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/VladinoUs/abb_egon)
![GitHub release](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Egy egyedi Home Assistant integráció a **ABB Egon** intelligens elektromos rendszerekhez. Az integráció közvetlenül a helyi HTTP/XML API-val kommunikál az ABB Egon kommunikációs modulján keresztül, felhőszolgáltatások és külső szolgáltatók nélkül.

---

## Áttekintés

Ez az integráció lehetővé teszi az ABB Egon Home Assistant rendszerhez való csatlakoztatását helyi hálózaton keresztül, vagy külső elérésen át, ha az eszköz porttovábbítással elérhető. A konfiguráció a natív Home Assistant config flow segítségével történik, ezért nincs szükség a `configuration.yaml` módosítására.

### Fő jellemzők

- Helyi HTTP/XML API kommunikáció felhő nélkül.
- Konfiguráció a Home Assistant felületén keresztül.
- Automatikus bejelentkezés és munkamenet-frissítés.
- Állítható lekérdezési időköz az Options flow segítségével.
- A rendelkezésre álló elemek automatikus felismerése.
- Többféle entitástípus támogatása.
- Többnyelvű felhasználói felület.

---

## Az ABB Ego-n rendszerről

Az **ABB Ego-n** otthoni elektromos rendszer 2007-ben jelent meg a piacon, és az ABB megfizethető megoldásként mutatta be új építésű és felújítási projektekhez egyaránt.

A rendszer fejlesztését és forgalmazását **2017**-ben megszüntették, és az IQinstalace tájékoztatása szerint ez a cég vette át a szervizt, a műszaki támogatást és az alkatrészellátást.

Pótalkatrészek, szerviz és műszaki támogatás itt található:
- [iqinstalace.cz/elektroinstalace](http://iqinstalace.cz/elektroinstalace/)
- [viktorstrouhal@seznam.cz](mailto:viktorstrouhal@seznam.cz)

---

## Támogatott platformok

Az integráció jelenleg ezeket az entitásokat támogatja:

- `sensor`
- `switch`
- `light`
- `cover`
- `number`
- `button`

A létrehozott entitások pontos száma a konfigurációtól és az adott ABB Egon telepítésben elérhető elemek típusától függ.

---

## Telepítés HACS-on keresztül

Ha HACS-ot használsz, az integrációt egyedi tárolóként is hozzáadhatod:

1. Nyisd meg a **HACS**-ot.
2. Lépj az **Integrations** részhez.
3. Nyisd meg a hárompontos menüt, és válaszd a **Custom repositories** opciót.
4. Add hozzá a tároló URL-jét:
   `https://github.com/VladinoUs/abb_egon`
5. Típusnak válaszd az **Integration**-t.
6. Telepítsd az integrációt.
7. Indítsd újra a Home Assistantot.

---

## Kézi telepítés

Ha nem használsz HACS-ot, másold át az integráció mappáját kézzel:

1. Töltsd le ezt a repozitóriumot a GitHubról.
2. Másold a következő mappát:

```text
custom_components/abb_egon
```

a Home Assistant mappádba:

```text
/config/custom_components/abb_egon
```

3. Indítsd újra a Home Assistantot.

---

## Konfiguráció

A Home Assistant újraindítása után:

1. Nyisd meg a **Settings** → **Devices & Services** menüpontot.
2. Kattints az **Add Integration** gombra.
3. Keresd meg az **ABB Egon** integrációt.
4. Add meg az ABB Egon modul hozzáférési adatait.

### Helyi hálózati elérés

```text
Host: 192.168.1.XXX
Port: 80
```

Használd az ABB Egon kommunikációs modul helyi IP-címét a saját otthoni hálózatodban.

### Külső elérés porttovábbítással

Ha az ABB Egont kívülről, routeren és NAT/port mappingen keresztül éred el, add meg a nyilvános IP-címet vagy hostnevet, valamint a routerben beállított külső portot:

```text
Host: nyilvanos-ip-vagy-domain.hu
Port: 8888
```

### Alapértelmezett bejelentkezési adatok

Ha ezeket nem változtattad meg az ABB Egon rendszerben, az integráció alapértelmezés szerint ezt használja:

```text
Felhasználónév: ABB
Jelszó: egon
```

---

## Beállítások

Az integráció támogatja a felhasználói beállításokat az **Options flow** segítségével.

Jelenleg elsősorban az alábbi állítható:
- lekérdezési időköz (`scan_interval`)

A beállítások módosítása után az integráció automatikusan újratöltődik, így az új értékek kézi beavatkozás nélkül érvénybe lépnek.

---

## Biztonság

> ⚠️ **Fontos:** Ha az ABB Egon közvetlenül, HTTP-n keresztül elérhető a nyilvános interneten, a kommunikáció nem titkosított. A bejelentkezési adatok és a forgalom elfoghatók.

Ajánlott intézkedések:
- használj **VPN-t**,
- korlátozd a hozzáférést **tűzfalszabályokkal**,
- csak kiválasztott IP-címeket engedélyezz,
- ne tedd ki az eszközt közvetlenül az internetre további védelem nélkül.

---

## A projektről

Ez a projekt egy közösségi integráció azoknak az ABB Egon felhasználóknak, akik Home Assistant segítségével szeretnék vezérelni és felügyelni eszközeiket. Csak helyi kommunikációt használ, és nem igényel felhőszolgáltatásokat vagy külső fiókokat.

---

## Fontos információk

- Ez nem hivatalos ABB termék.
- A projektet az ABB nem támogatja hivatalosan.
- Használata saját felelősségre történik.
- A működés függhet a kommunikációs modul konkrét verziójától vagy az ABB Egon telepítés módjától.

---

## A projekt támogatása

Ez a projekt ingyenes és nyílt forráskódú. Ha időt spórolt neked vagy javította az okosotthonodat, támogathatod a további fejlesztést egy kisebb hozzájárulással:

☕ **Hívj meg egy kávéra Revoluton keresztül:**  
[https://revolut.me/sdaddy](https://revolut.me/sdaddy)

![Revolut QR](https://raw.githubusercontent.com/VladinoUs/abb_egon/main/revolut_qr.png)

---

## Licenc

Ez a projekt **MIT** licenc alatt érhető el.
