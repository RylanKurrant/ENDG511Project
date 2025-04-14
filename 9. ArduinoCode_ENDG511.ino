#include <Wire.h>  
#include <LiquidCrystal_I2C.h>
#include "DHT20.h"  // DHT20 library (change for DHT22)

// Setups
LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT20 dht;

#define LED_TEMP 7  // Red LED (Temperature Alert)
#define LED_HUMI 8  // Blue LED (Humidity Alert)

// Default
float temperatureVal = 30.0;  // Default value
float humidityVal = 70.0;     // Default value

void setup() {
    Serial.begin(115200);
    Serial.println("DHT20 + LCD + LED Test!");

    Wire.begin();
    dht.begin();
    lcd.init(); 
    lcd.backlight();

    // LED setup
    pinMode(LED_TEMP, OUTPUT);
    pinMode(LED_HUMI, OUTPUT);
    digitalWrite(LED_TEMP, LOW);
    digitalWrite(LED_HUMI, LOW);
}
// Two loops for controlling Python value gathering and presentation and another for LCD and LED control
void loop() {
    loop1();
    loop2();
}

void loop1() {
  Serial.println("Check for input...");
    if (Serial.available() > 0) {
        String receivedData = Serial.readStringUntil('\n');  
        receivedData.trim();  

        if (receivedData.length() > 0) {  
            Serial.print("Data received: ");
            Serial.println(receivedData);

            // Debug (don't remove unless you want headache)
            Serial.print("Data has been recieved: ");
            for (int i = 0; i < receivedData.length(); i++) {
                Serial.print(receivedData[i]);
                Serial.print(" ");
            }
            Serial.println();

            // For my formatting with python
            int commaOne = receivedData.indexOf(',');
            //int commaTwo = receivedData.indexOf(',', commaOne + 1);

            if (commaOne > 0) { 
                String temperatureStr = receivedData.substring(0, commaOne);
                String humidityStr = receivedData.substring(commaOne + 1);
                //String moistureStr = receivedData.substring(commaTwo + 1);

                temperatureVal = temperatureStr.toFloat();
                humidityVal = humidityStr.toFloat();
                //moistureVal = moistureStr.toFloat();

                Serial.print("Temperature Value: "); Serial.println(temperatureVal, 3);
                Serial.print("Humidity Value: "); Serial.println(humidityVal, 3);
                //Serial.print("Moisture Value: "); Serial.println(moistureVal, 3);
            } else {
                Serial.println("Error");
            }
        }
    }
}


void loop2() {
    // Read data from the sensor
    uint8_t status = dht.read();  
    float temp = dht.getTemperature();
    float hum = dht.getHumidity();

    // Check if reading is valid
    // Setup LCD display
    if (status == 0 && !isnan(temp) && !isnan(hum)) {
        Serial.print("Humidity: ");
        Serial.print(hum);
        Serial.print(" %\t");
        Serial.print("Temperature: ");
        Serial.print(temp);
        Serial.println(" *C");
		
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Temp: ");
        lcd.print(temp);
        lcd.print(" C");

        lcd.setCursor(0, 1);
        lcd.print("Humi: ");
        lcd.print(hum);
        lcd.print(" %");

        // LED control logic
        if (temp < temperatureVal) {
            digitalWrite(LED_TEMP, HIGH); // Turn on Red LED if temp < ML value or 30°C (default)
        } else {
            digitalWrite(LED_TEMP, LOW);  // Turn off otherwise
        }

        if (hum < humidityVal) {
            digitalWrite(LED_HUMI, HIGH); // Turn on Blue LED if humidity < ML vlaue or 70% (default)
        } else {
            digitalWrite(LED_HUMI, LOW);  // Turn off otherwise
        }
    } else {
        Serial.println("Sensor error: Failed to get temperature and humidity.");
    }

    delay(2000);  // Delay before next reading
}