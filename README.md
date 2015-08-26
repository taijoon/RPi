# RPi
TJ Test Code

SPI_SPEED folder 
	: MAX 4K SPEED Test

RPi2 setting tip
	wifi setting path = /etc/network/interface
	
	add code in interface
	auto wlan0
	allow-hotplug wlan0
	iface wlan0 inet dhcp
	wpa-ssid "ssid name"
	wpa-psk "password"
