H/W
Pin Connection
1.MCP3008 VDD   -> 5V      (Pin  2)
2.MCP3008 VREF  -> 5V      (Pin  2)
3.MCP3008 AGND  -> GND     (Pin  6)
4.MCP3008 CLK   -> SPI_CLK (Pin 23)
5.MCP3008 DOUT  -> SPI_MISO(Pin 21)
6.MCP3008 DIN   -> SPI_MOSI(Pin 19)
7.MCP3008 CS    -> GPIO25  (Pin 22)
8.MCP3008 DGND  -> GND     (Pin  6)



S/W
1. SPI Setting
  sudo raspi-config
  select 8
  SPI OK select -> reboot

2. sudo nano /etc/modprobe.d/raspi-blacklist.conf
   add #
   #blacklist spi-bcm2708

3. gpio load spi
     if you can not execute command
     http://www.raplay.org/?p=4918 or wiringpi.com 

4. simple code link
     http://cafe.naver.com/openrt/494
     https://app.box.com/s/o21oqt127f1bvnn8swh2pmp48y2nbsm7
