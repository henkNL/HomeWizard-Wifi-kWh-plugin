# HomeWizard-Wifi-kWh-plugin
A Python plugin for Domoticz that creates several devices for the HomeWizard Wifi kWh meter

HomeWizard Wi-Fi kWh meter

The HomeWizard Wi-Fi kWh meter is a small device that can be build  into the circuit breaker box in your home. By default it sends all of its data to the HomeWizard servers but thanks to its local API you can read the device locally too. With this plugin you can use Domoticz to read the meter and store the data without using your internet connection.

**Devices**
The plugin creates a total of 2 devices. Some may not be usefull for everyone but you can safely ignore those.

An energy meter that shows your daily power draw (and feed back on the grid)
An energy meter that shows your current power usage
A Wi-Fi signal strength meter that shows the current signal strength from the Wi-Fi P1 meter

**Configuration**
The configuration is pretty self explaining. You just need the IP address of your Wi-Fi kWh meter. Make sure the IP address is static DHCP so it won't change over time.

**Configuration	Explanation**
IP address	The IP address of the Wi-Fi P1 meter
Port	The port on which to connect (80 is default) -> Not necessary in the next release
Data interval	The interval for the data devices to be refreshed
Debug	Used by the developer to test stuff
