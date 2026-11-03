import joblib
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

MODEL_FILE = PROJECT_DIR / "terrasense_model.pkl"
ESP32_DIR = PROJECT_DIR / "esp32"

MODEL_HEADER = ESP32_DIR / "terrasense_model.h"
ESP32_CODE = ESP32_DIR / "terrasense_esp32.ino"

# Create ESP32 folder if it does not exist
ESP32_DIR.mkdir(parents=True, exist_ok=True)

print("========================================")
print("     TERRASENSE ESP32 MODEL EXPORT")
print("========================================")

print()
print("Project folder:")
print(PROJECT_DIR)

print()
print("Loading model:")
print(MODEL_FILE)

# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_FILE)

scaler = model.named_steps["scaler"]
classifier = model.named_steps["model"]

mean = scaler.mean_
scale = scaler.scale_
coef = classifier.coef_[0]
intercept = classifier.intercept_[0]

# ============================================================
# CREATE MODEL HEADER
# ============================================================

header = f"""#ifndef TERRASENSE_MODEL_H
#define TERRASENSE_MODEL_H

#include <math.h>

// ========================================
// TERRASENSE ML MODEL
// Exported from Python
// ========================================

// StandardScaler parameters

const float TEMP_MEAN  = {mean[0]:.10f}f;
const float HUM_MEAN   = {mean[1]:.10f}f;
const float MQ135_MEAN = {mean[2]:.10f}f;

const float TEMP_SCALE  = {scale[0]:.10f}f;
const float HUM_SCALE   = {scale[1]:.10f}f;
const float MQ135_SCALE = {scale[2]:.10f}f;

// Logistic Regression coefficients

const float TEMP_COEF  = {coef[0]:.10f}f;
const float HUM_COEF   = {coef[1]:.10f}f;
const float MQ135_COEF = {coef[2]:.10f}f;

const float INTERCEPT = {intercept:.10f}f;

// Sigmoid

inline float terrasenseSigmoid(float x)
{{
    return 1.0f / (1.0f + expf(-x));
}}

// Fire probability

inline float terrasensePredict(
    float temperature,
    float humidity,
    float mq135
)
{{
    float temp =
        (temperature - TEMP_MEAN) / TEMP_SCALE;

    float hum =
        (humidity - HUM_MEAN) / HUM_SCALE;

    float mq =
        (mq135 - MQ135_MEAN) / MQ135_SCALE;

    float score =
        TEMP_COEF * temp +
        HUM_COEF * hum +
        MQ135_COEF * mq +
        INTERCEPT;

    return terrasenseSigmoid(score);
}}

#endif
"""

# Write model header
with open(MODEL_HEADER, "w", encoding="utf-8") as file:
    file.write(header)

# ============================================================
# CREATE ESP32 PROGRAM
# ============================================================

ino = r'''#include <Arduino.h>
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
'''

# Write ESP32 code
with open(ESP32_CODE, "w", encoding="utf-8") as file:
    file.write(ino)

# ============================================================
# VERIFY FILES
# ============================================================

print()
print("========================================")
print("          EXPORT SUCCESSFUL")
print("========================================")

print()
print("MODEL HEADER:")
print(MODEL_HEADER)
print("Exists:", MODEL_HEADER.exists())

print()
print("ESP32 CODE:")
print(ESP32_CODE)
print("Exists:", ESP32_CODE.exists())

print()
print("5 READINGS: ENABLED")
print("LAST 3 READINGS: USED FOR FINAL DECISION")
print("FIRE RULE: 2 OF LAST 3")
print("WEIGHTED CALCULATION: NONE")

print()
print("========================================")