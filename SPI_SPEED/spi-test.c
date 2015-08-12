#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>

#include <wiringPi.h>
#include <wiringPiSPI.h>

#define CS_MCP3208  6        // BCM_GPIO 25

#define SPI_CHANNEL 0
#define SPI_SPEED   1000000  // 1MHz


int read_mcp3208_adc(unsigned char adcChannel)
{
  unsigned char buff[3];
  int adcValue = 0;

  buff[0] = 0x06 | ((adcChannel & 0x07) >> 2);
  buff[1] = ((adcChannel & 0x07) << 6);
  buff[2] = 0x00;

  digitalWrite(CS_MCP3208, 0);  // Low : CS Active

  wiringPiSPIDataRW(SPI_CHANNEL, buff, 3);

  buff[1] = 0x0F & buff[1];
  adcValue = ( buff[1] << 8) | buff[2];

  digitalWrite(CS_MCP3208, 1);  // High : CS Inactive

  return adcValue;
}


int main (void)
{
  int adcChannel = 0;
  int adcValue   = 0;
  int Cnt = 0;
  int allCnt = 0;
  float avCnt = 0.0;
  int TCnt = 0;
  timer_t timer1, timer2;

  if(wiringPiSetup() == -1)
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror(errno));
    return 1 ;
  }

  if(wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1)
  {
    fprintf (stdout, "wiringPiSPISetup Failed: %s\n", strerror(errno));
    return 1 ;
  }

  pinMode(CS_MCP3208, OUTPUT);

  timer2 = time(NULL);
  while(1)
  {
    timer1 = time(NULL);
    if((timer1 - timer2) == 0){
      Cnt++;
    }
    else{
      if(TCnt > 0){
	allCnt += Cnt;
        //avCnt = (float)(avCnt*(TCnt-1)/TCnt)+(float)(Cnt/TCnt);
	avCnt = allCnt/TCnt;
      }
      TCnt++;

      printf("CO2 Value = %u   now=%d   avr=%.1f\n", adcValue, Cnt, avCnt);
      Cnt = 0;
      timer2 = timer1;
    }
    adcValue = read_mcp3208_adc(adcChannel);
    usleep(50);
  }

  return 0;
}
