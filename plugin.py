##           HomeWizard Wi-Fi kWh Meter 1 phase Plugin
##
##           Author:         henkNL thanks to Eraser
##           Version:        0.0.2
##           Last modified:  16-1-2022
##
"""
<plugin key="HomeWizardWifi-kWh" name="HomeWizard Wi-Fi kWh Meter - 1 phase" author="henkNL" version="0.1" externallink="https://www.homewizard.nl/homewizard-wi-fi-kwh-meter">
    <description>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li><b>Current usage</b>: Displays the current power usage in watts. Can be negative when you are producing more power then you are using. 5 minute values are logged.</li>
            <li><b>Total electricity</b>: Shows usage and return for both tariffs. Current usage is also shown but nog logged.</li>
            <li><b>Wifi signal</b>: Shows the quality of the wifi signal.</li>
        </ul>
        <h3>Configuration</h3>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="192.168.1.254" />
        <param field="Port" label="Port" width="200px" required="true" default="80" />
        <param field="Mode1" label="Data interval" width="200px">
            <options>
                <option label="10 seconds" value="10"/>
                <option label="20 seconds" value="20"/>
                <option label="30 seconds" value="30"/>
                <option label="1 minute" value="60" default="true"/>
                <option label="2 minutes" value="120"/>
                <option label="3 minutes" value="180"/>
                <option label="4 minutes" value="240"/>
                <option label="5 minutes" value="300"/>
            </options>
        </param>
        <param field="Mode2" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import json
import urllib
import urllib.request

class BasePlugin:
    #Plugin variables
    pluginInterval = 10     #in seconds
    dataInterval = 60       #in seconds
    dataIntervalCount = 0
    switchIntervalCount = 0

#Homewizard P1 meter variables
    wifi_ssid = ""                  #: [String] Het Wi-Fi netwerk waarmee de P1 meter is verbonden
    wifi_strength = -1              #: [Number] De sterkte van het Wi-Fi signaal in %
    total_power_import_t1_kwh = -1  #: [Number] De stroom afname meterstand voor tarief 1 in kWh
    total_power_export_t1_kwh = -1  #: [Number] De stroom teruglevering meterstand voor tarief 1 in kWh
    active_power_w = -1             #: [Number] Het huidig gebruik van alle fases gecombineerd in Watt
    active_power_l1_w = -1          #: [Number] Het huidig gebruik voor fase 1 in Watt (indien van toepassing)
    
    #Calculated variables
    import_active_power_w = 0
    export_active_power_w = 0
    
    #Device ID's
    active_power_id = 101
    total_power_id = 102
    wifi_signal_id = 103
    
    def onStart(self):
        if Parameters["Mode2"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()
        
        # If data interval between 10 sec. and 5 min.
        if 10 <= int(Parameters["Mode1"]) <= 300:
            self.dataInterval = int(Parameters["Mode1"])
        else:
            # If not, set to 60 sec.
            self.dataInterval = 60
            

        # Start the heartbeat
        Domoticz.Heartbeat(self.pluginInterval)
        
        return True
        
    def onConnect(self, Status, Description):
        return True

    def onMessage(self, Data, Status, Extra):
        self.dataIntervalCount += self.pluginInterval
#        self.switchIntervalCount += self.pluginInterval
        
        if ( self.dataIntervalCount >= self.dataInterval ): 
            try:
                self.wifi_ssid = Data['wifi_ssid']
                self.wifi_strength = Data['wifi_strength']
                self.total_power_import_t1_kwh = int(Data['total_power_import_t1_kwh'] * 1000)
                self.total_power_export_t1_kwh = int(Data['total_power_export_t1_kwh'] * 1000)
                self.active_power_w = Data['active_power_w']
                self.active_power_l1_w = Data['active_power_l1_w']
                                
                if ( self.active_power_w >= 0):
                    self.import_active_power_w = self.active_power_w
                    self.export_active_power_w = 0
                else:
                    self.import_active_power_w = 0
                    self.export_active_power_w = self.active_power_w * -1
            except:
                Domoticz.Error("Failed to read response data")
                return
 
 #Elke x seconden van datainterval, afgeteld naar 0       
        if ( self.dataIntervalCount >= self.dataInterval ):
            self.dataIntervalCount = 0
#current usage aanmaken als deze niet bestaat, ander vullen met waarde          
            try:
                if ( self.active_power_id not in Devices ):
                    Domoticz.Device(Name="Current usage",  Unit=self.active_power_id, Type=243, Subtype=29).Create()
                    
                UpdateDevice(self.active_power_id, 0, numStr(self.active_power_w) + ";" + numStr(self.total_power_import_t1_kwh), True)
            except:
                Domoticz.Error("Failed to update device id " + str(self.active_power_id))
                        
            try:
               if ( self.wifi_signal_id not in Devices ):
                   Domoticz.Device(Name="Wifi signal",  Unit=self.wifi_signal_id, TypeName="Percentage").Create()
                    
               UpdateDevice(self.wifi_signal_id, 0, numStr(self.wifi_strength), True)
            except:
                Domoticz.Error("Failed to update device id " + str(self.wifi_signal_id))
                         
        return True
                    
    def onCommand(self, Unit, Command, Level, Hue):
        #Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        return True

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        #Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
        return

    def onHeartbeat(self):
        self.readMeter()
        return

    def onDisconnect(self):
        return

    def onStop(self):
        #Domoticz.Log("onStop called")
        return True

    def readMeter(self):
        try:
            APIdata = urllib.request.urlopen("http://" + Parameters["Address"] + Parameters["Port"] + "/api/v1/data").read()
        except:
            Domoticz.Error("Failed to communicate with Wi-Fi kWh meter at ip: " + Parameters["Address"] + " with port: " + Parameters["Port"] + ", check ip/port settings!")
            return False
        
        try:
            APIjson = json.loads(APIdata.decode("utf-8"))
        except:
            Domoticz.Error("Failed converting API data to JSON")
            return False
            
        try:
            self.onMessage(APIjson, "200", "")
        except:
            Domoticz.Error("onMessage failed with some error")
            return False
        
global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Status, Description):
    global _plugin
    _plugin.onConnect(Status, Description)

def onMessage(Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect():
    global _plugin
    _plugin.onDisconnect()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def numStr(s):
    try:
        return str(s).replace('.','')
    except:
        return "0"

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def UpdateDevice(Unit, nValue, sValue, AlwaysUpdate=False, SignalLevel=12):    
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if ((Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (AlwaysUpdate == True)):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), SignalLevel=SignalLevel)
            Domoticz.Debug("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
