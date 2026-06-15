# ABB Egon — Home Assistant integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/VladinoUs/abb_egon)
![GitHub release](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A custom Home Assistant integration for the **ABB Egon** smart electrical installation system. The integration communicates directly with the local HTTP/XML API of the ABB Egon communication module, without cloud services or third-party dependencies.

---

## Overview

This integration allows ABB Egon to be connected to Home Assistant over a local network or through external access if the device is available via port forwarding. Configuration is done through the native Home Assistant config flow, so there is no need to edit `configuration.yaml`.

### Key features

- Local HTTP/XML API communication without cloud access.
- Configuration through the Home Assistant UI.
- Automatic login and session renewal.
- Adjustable polling interval through the Options flow.
- Automatic discovery of available device elements.
- Support for multiple entity types.
- Multi-language user interface.

---

## About ABB Ego-n

The **ABB Ego-n** home electrical installation system was introduced on the market in 2007 and ABB presented it as an affordable solution for both new builds and renovations.

Development and distribution of the system ended in **2017**, and according to IQinstalace, that company later took over service, technical support, and spare part supply for the system.

Spare parts, service, and technical support can be found here:
- [iqinstalace.cz/elektroinstalace](http://iqinstalace.cz/elektroinstalace/)
- [viktorstrouhal@seznam.cz](mailto:viktorstrouhal@seznam.cz)

---

## Supported platforms

The integration currently supports these entities:

- `sensor`
- `switch`
- `light`
- `cover`
- `number`
- `button`

The exact number of created entities depends on the configuration and the available elements in a specific ABB Egon installation.

---

## Installation via HACS

If you use HACS, you can add the integration as a custom repository:

1. Open **HACS**.
2. Go to **Integrations**.
3. Open the three-dot menu and select **Custom repositories**.
4. Add the repository URL:
   `https://github.com/VladinoUs/abb_egon`
5. Select **Integration** as the repository type.
6. Install the integration.
7. Restart Home Assistant.

---

## Manual installation

If you do not use HACS, copy the integration folder manually:

1. Download this repository from GitHub.
2. Copy the folder:

```text
custom_components/abb_egon
```

into your Home Assistant folder:

```text
/config/custom_components/abb_egon
```

3. Restart Home Assistant.

---

## Configuration

After restarting Home Assistant:

1. Open **Settings** → **Devices & Services**.
2. Click **Add Integration**.
3. Search for **ABB Egon**.
4. Enter the ABB Egon module credentials.

### Local network access

```text
Host: 192.168.1.XXX
Port: 80
```

Use the local IP address of the ABB Egon communication module in your home network.

### External access via port forwarding

If you access ABB Egon from outside through a router and NAT/port mapping, enter the public IP address or hostname and the external port configured in your router:

```text
Host: your-public-ip-or-domain.com
Port: 8888
```

### Default credentials

If you have not changed them in the ABB Egon system, the integration assumes these default values:

```text
Username: ABB
Password: egon
```

---

## Settings

The integration also supports user settings through the **Options flow**.

Currently the main adjustable setting is:
- polling interval (`scan_interval`)

After changing the settings, the integration reloads automatically so the new values take effect without manual intervention.

---

## Security

> ⚠️ **Important:** If ABB Egon is exposed directly to the public internet over HTTP, the communication is not encrypted. Login credentials and traffic may be intercepted.

Recommended measures:
- use a **VPN**,
- restrict access with **firewall rules**,
- allow access only from selected IP addresses,
- avoid exposing the device directly to the internet without additional protection.

---

## About the project

This project is a community integration for ABB Egon users who want to control and monitor their devices through Home Assistant. It uses local communication only and does not require cloud services or external accounts.

---

## Important information

- This is not an official ABB product.
- The project is not officially supported by ABB.
- Use at your own risk.
- Functionality may depend on the specific communication module version or the way ABB Egon is deployed.

---

## Support the project

This project is free and open source. If it saved you time or improved your smart home, you can support further development with a small contribution:

☕ **Buy me a coffee via Revolut:**  
[https://revolut.me/sdaddy](https://revolut.me/sdaddy)

![Revolut QR](revolut_qr.jpg)

---

## License

This project is distributed under the **MIT** license.