#include <wiringPi.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
// To manage MySQL inserts!
#include <my_global.h>
#include <mysql.h>
#include <time.h>
//
// GCC Command:
// gcc -o DHT11_TempHumi DHT11_TempHumi_new.c -L/usr/local/lib -lwiringPi -I/usr/include/mysql `mysql_config --cflags --libs`
//
#define MAX_TIME 85
#define DHT11PIN 7
#define DEVICE "RPIBIO"

int dht11_val[5]={0,0,0,0,0};

// To manage MySQL inserts!
void finish_with_error(MYSQL *con)
{
  fprintf(stderr, "%s\n", mysql_error(con));
  mysql_close(con);
  exit(1);
}
//

void dht11_read_val(MYSQL *con, char *timestamp, char *sql, char *sqlData)
{
  uint8_t lststate=HIGH;
  uint8_t counter=0;
  uint8_t j=0,i;
  float farenheit;
  for(i=0;i<5;i++)
    dht11_val[i]=0;
  pinMode(DHT11PIN,OUTPUT);
  digitalWrite(DHT11PIN,LOW);
  delay(18);
  digitalWrite(DHT11PIN,HIGH);
  delayMicroseconds(40);
  pinMode(DHT11PIN,INPUT);
  for(i=0;i<MAX_TIME;i++)
  {
    counter=0;
    while(digitalRead(DHT11PIN)==lststate){
      counter++;
      delayMicroseconds(1);
      if(counter==255)
        break;
    }
    lststate=digitalRead(DHT11PIN);
    if(counter==255)
      break;
    // top 3 transistions are ignored
    if((i>=4)&&(i%2==0)){
      dht11_val[j/8]<<=1;
      if(counter>16)
        dht11_val[j/8]|=1;
      j++;
    }
  }
  // verify cheksum and print the verified data
  if((j>=40)&&(dht11_val[4]==((dht11_val[0]+dht11_val[1]+dht11_val[2]+dht11_val[3])& 0xFF)))
  {
    //farenheit=dht11_val[2]*9./5.+32;
    //printf("Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n",dht11_val[0],dht11_val[1],dht11_val[2],dht11_val[3],farenheit);
    printf("Humidity = %d.%d %% Temperature = %d.%d *C\n",dht11_val[0],dht11_val[1],dht11_val[2],dht11_val[3]);
    // To manage MySQL inserts!

    //char timestamp[50];
    time_t now = time (0);
    strftime (timestamp, 50, "%Y-%m-%d %H:%M", localtime (&now));
    //printf ("%s\n", timestamp);

    strcpy(sql, "INSERT INTO log (temp, humi, time, device) VALUES (");
    sprintf(sqlData, "%d.%d", dht11_val[0],dht11_val[1]);
    strcat(sql, sqlData);
    strcpy(sqlData,", ");
    strcat(sql,sqlData);
    sprintf(sqlData, "%d.%d", dht11_val[2],dht11_val[3]);
    strcat(sql, sqlData);
    strcpy(sqlData,", '");
    strcat(sql,sqlData);
    sprintf(sqlData, "%s", timestamp);
    strcat(sql, sqlData);
    strcpy(sqlData,"', '");
    strcat(sql,sqlData);
    sprintf(sqlData, DEVICE);
    strcat(sql, sqlData);
    strcpy(sqlData,"'); ");
    strcat(sql,sqlData); 
    printf ("%s\n", sql);

    //if (mysql_query(con, "INSERT INTO log (temp, humi, time, device) VALUES (10.00, 37.00 , '2013-11-24 17:15:10', 'RPIBIO')")) {
    if (mysql_query(con, sql)) {
      finish_with_error(con);
    }
    //
}
  else
    printf("Invalid Data!!\n");
}

int main(void)
{
  // To manage MySQL inserts!
  MYSQL *con = mysql_init(NULL);

  char timestamp[50];
  char sql[100],sqlData[30];

  if (con == NULL)
  {
    fprintf(stderr, "mysql_init() failed\n");
    exit(1);
  }
  if (mysql_real_connect(con, "localhost", "root", "221186",
                         "DHT11", 0, NULL, 0) == NULL)
  {
    finish_with_error(con);
  }
  //
  printf("Interfacing Temperature and Humidity Sensor (DHT11) With Raspberry Pi\n");
  if(wiringPiSetup()==-1)
    exit(1);
  while(1)
  {
    dht11_read_val(con, timestamp, sql, sqlData);
    delay(3000);
  }
  return 0;
}
