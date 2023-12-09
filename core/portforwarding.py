"""
https://github.com/westhecool/python-portforwarding
A simple library to manage port forwards on your router using UPnP.
"""

import upnpy
from upnpy.ssdp.SSDPRequest import SSDPRequest

class PortForwarding:
	def __init__(self):
		# try to find the first service that has "AddPortMapping"
		self._service = False
		upnp = upnpy.UPnP()
		print(upnp.discover())
		device = upnp.discover(ST='urn:schemas-upnp-org:device:InternetGatewayDevice:1')[0] # get the "InternetGatewayDevice"
		for service in device.get_services():
			for a in service.get_actions():
				if a.name == 'AddPortMapping':
					self._service = service
					break
			if self._service:
				break
	def AddPortForward(self, port, ip, protocal, description, InternalPort=None, LeaseDuration=0):
		if not InternalPort:
			InternalPort = port
		return self._service.AddPortMappinga(
 			NewRemoteHost='',
			NewExternalPort=port,
			NewProtocol=protocal,
			NewInternalPort=InternalPort,
			NewInternalClient=ip,
			NewEnabled=1,
	 		NewPortMappingDescription=description,
			NewLeaseDuration=LeaseDuration
		)
	def DeletePortForward(self, port, protocal):
		return self._service.DeletePortMapping(
			NewRemoteHost='',
            NewExternalPort=port,
        	NewProtocol=protocal,
		)
	def GetPortForward(self, id=0):
		return self._service.GetGenericPortMappingEntry(NewPortMappingIndex=id)
	def ListPortForwards(self):
		stop = False
		i = 0
		data = []
		while not stop:
			try:
				data.append(self.GetPortForward(i))
			except upnpy.exceptions.SOAPError: # hopeing for "SpecifiedArrayIndexInvalid" to know that we are at the end of the list
				stop = True
			i = i + 1
		return data
	def GetPublicIP(self):
		return self._service.GetExternalIPAddress()['NewExternalIPAddress']
