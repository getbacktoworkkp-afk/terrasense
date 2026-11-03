#ifndef TERRASENSE_MODEL_H
#define TERRASENSE_MODEL_H

#include <math.h>

// ========================================
// TERRASENSE ML MODEL
// Exported from Python
// ========================================

// StandardScaler parameters

const float TEMP_MEAN  = 69.1307461233f;
const float HUM_MEAN   = 15.4565079140f;
const float MQ135_MEAN = 3339.8330383646f;

const float TEMP_SCALE  = 7.8312701335f;
const float HUM_SCALE   = 2.7376630156f;
const float MQ135_SCALE = 309.6961135354f;

// Logistic Regression coefficients

const float TEMP_COEF  = 2.1327299924f;
const float HUM_COEF   = -2.6503728692f;
const float MQ135_COEF = 4.6151102108f;

const float INTERCEPT = 0.5217690458f;

// Sigmoid

inline float terrasenseSigmoid(float x)
{
    return 1.0f / (1.0f + expf(-x));
}

// Fire probability

inline float terrasensePredict(
    float temperature,
    float humidity,
    float mq135
)
{
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
}

#endif
