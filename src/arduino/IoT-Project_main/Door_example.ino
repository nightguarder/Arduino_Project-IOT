#include <Wire.h>
#include <Arduino_LSM6DSOX.h>

#define INT_MODE true         // Run in interrupt mode.
bool INT_FLAG = false;        // Set true on interrupt.

LSM6DSOX lsm;

void imu_int_handler() {
    INT_FLAG = true;
}

void setup() {
    if (INT_MODE) {
        pinMode(24, INPUT);
        attachInterrupt(digitalPinToInterrupt(24), imu_int_handler, RISING);
    }
    Wire.begin();
    lsm.begin();
    lsm.configure_mlc("lsm6dsox_vibration_monitoring.ucf", LSM6DSOX_ODR_26_HZ, LSM6DSOX_ODR_26_HZ, LSM6DSOX_FS_2000_DPS, LSM6DSOX_FS_4_G);
    Serial.begin(9600);
    Serial.println("MLC configured...");
}

void loop() {
    if (INT_MODE) {
        if (INT_FLAG) {
            INT_FLAG = false;
            switch (lsm.read_mlc_output()) {
                case 0:
                    Serial.println("no vibration");
                    break;
                case 1:
                    Serial.println("low vibration");
                    break;
                case 2:
                    Serial.println("high vibration");
                    break;
            }
        }
    } else {
        int output = lsm.read_mlc_output();
        if (output != -1) {
            switch (output) {
