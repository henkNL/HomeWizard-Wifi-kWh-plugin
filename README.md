# HomeWizard-Wifi-kWh-plugin
A Python plugin for Domoticz that creates several devices for the HomeWizard Wifi (1 phase) kWh meter.

![HomeWizard Wi-Fi P1 meter](https://www.homewizard.nl/media/catalog/product/cache/e5430b9fa526b8a06edfa3b86f08b1c3/i/m/image_13_.png)

The [HomeWizard Wi-Fi kWh meter](https://www.homewizard.nl/homewizard-wi-fi-kwh-meter) is a small device that can be build  into the circuit breaker box in your home. By default it sends all of its data to the HomeWizard servers but thanks to its local API you can read the device locally too. With this plugin you can use Domoticz to read the meter and store the data without using your internet connection.

# Devices

The plugin creates a total of 2 devices:

1. An energy meter that shows your current power usage and daily power draw
2. A Wi-Fi signal strength meter that shows the current signal strength from the Wi-Fi P1 meter

# Installation and setup
1. Clone repository into your domoticz plugins folder
```bash
cd domoticz/plugins
git clone https://github.com/henkNL/HomeWizard-Wifi-kWh-plugin.git HomeWizard-Wifi-kWh
```

2. Restart your Domoticz service with:

```bash
sudo service domoticz.sh restart
```
3. Make sure that "Accept new Hardware Devices" is enabled in Domoticz settings
4. Now go to **Setup**, **Hardware** in your Domoticz interface. There you add
**HomeWizard Wi-Fi kWh Meter - 1 phase**.

Make sure you enter all the required fields.

# Plugin update

1. Go to plugin folder and pull new version
```
cd domoticz/plugins/HomeWizard-Wifi-kWh
git pull
```
2. Restart your Domoticz service with:

```bash
sudo service domoticz.sh restart
```

# Configuration

The configuration is pretty self explaining. You just need the IP address of your Wi-Fi kWh meter. Make sure the IP address is static DHCP so it won't change over time.

| Configuration	| Explanation |
|--|--|
| IP address	| The IP address of the Wi-Fi P1 meter |
| Port | The port on which to connect (80 is default) |
| Data interval	| The interval for the data devices to be refreshed |
| Debug	| Used by the developer to test stuff |

Thanks to [Eraser3 ](https://github.com/Eraser3/HomeWizard-Wifi-p1-plugin)!

