#include <Arduino.h>
#include "terrasense_model.h"

const int NUM_READINGS = 5;

const float FIRE_THRESHOLD = 0.50f;

struct SensorReading
{
    int id;
    float temperature;
    float humidity;
    float mq135;
};

// ------------------------------------------------------------
// FIVE TEST READINGS
// ------------------------------------------------------------

SensorReading readings[NUM_READINGS] =
{
    {1, 28.9f, 84.0f, 697.0f},
    {2, 28.9f, 86.0f, 703.0f},
    {3, 57.9f, 17.4f, 2947.0f},
    {4, 67.7f, 13.8f, 3752.0f},
    {5, 74.9f, 15.8f, 3026.0f}
};

void setup()
{
    Serial.begin(115200);

    delay(2000);

    Serial.println();
    Serial.println("========================================");
    Serial.println("       TERRASENSE FIRE MONITOR");
    Serial.println("========================================");

    float probabilities[NUM_READINGS];

    // --------------------------------------------------------
    // RUN MODEL ON ALL 5 READINGS
    // --------------------------------------------------------

    Serial.println();
    Serial.println("----------------------------------------");
    Serial.println("INPUT OBSERVATIONS");
    Serial.println("----------------------------------------");

    for (int i = 0; i < NUM_READINGS; i++)
    {
        probabilities[i] =
            terrasensePredict(
                readings[i].temperature,
                readings[i].humidity,
                readings[i].mq135
            );

        Serial.print("ID ");
        Serial.print(readings[i].id);

        Serial.print(" : T=");
        Serial.print(readings[i].temperature, 1);

        Serial.print(" C, H=");
        Serial.print(readings[i].humidity, 1);

        Serial.print(" %, AQ=");
        Serial.println(readings[i].mq135, 0);
    }

    // --------------------------------------------------------
    // DISPLAY PROBABILITIES
    // --------------------------------------------------------

    Serial.println();
    Serial.println("----------------------------------------");
    Serial.println("MODEL PROBABILITIES");
    Serial.println("----------------------------------------");

    for (int i = 0; i < NUM_READINGS; i++)
    {
        Serial.print("P");
        Serial.print(i + 1);
        Serial.print(" = ");

        Serial.print(probabilities[i], 6);

        Serial.print(" (");

        Serial.print(probabilities[i] * 100.0f, 2);

        Serial.println(" %)");
    }

    // --------------------------------------------------------
    // FINAL DECISION
    //
    // ONLY LAST 3 READINGS:
    //
    // P3
    // P4
    // P5
    //
    // 2 OR MORE FIRE = FIRE WARNING
    // NO WEIGHTED CALCULATION
    // --------------------------------------------------------

    int fireCount = 0;

    if (probabilities[2] >= FIRE_THRESHOLD)
    {
        fireCount++;
    }

    if (probabilities[3] >= FIRE_THRESHOLD)
    {
        fireCount++;
    }

    if (probabilities[4] >= FIRE_THRESHOLD)
    {
        fireCount++;
    }

    Serial.println();
    Serial.println("----------------------------------------");
    Serial.println("FINAL FIRE ANALYSIS");
    Serial.println("----------------------------------------");

    Serial.println();
    Serial.println("Last 3 readings are evaluated.");

    Serial.print("P3 = ");
    Serial.println(probabilities[2], 6);

    Serial.print("P4 = ");
    Serial.println(probabilities[3], 6);

    Serial.print("P5 = ");
    Serial.println(probabilities[4], 6);

    Serial.println();

    Serial.print("Threshold = ");
    Serial.println(FIRE_THRESHOLD, 2);

    Serial.print("Fire readings = ");
    Serial.print(fireCount);
    Serial.println("/3");

    Serial.println();

    // --------------------------------------------------------
    // FINAL WARNING
    // --------------------------------------------------------

    if (fireCount >= 2)
    {
        Serial.println("========================================");
        Serial.println("        WARNING: FIRE DETECTED");
        Serial.println("        ALARM STATUS: ON");
        Serial.println("        RESULT: NOT NORMAL");
        Serial.println("========================================");
    }
    else
    {
        Serial.println("========================================");
        Serial.println("        NO FIRE DETECTED");
        Serial.println("        ALARM STATUS: OFF");
        Serial.println("        RESULT: NORMAL");
        Serial.println("========================================");
    }
}

void loop()
{
}
