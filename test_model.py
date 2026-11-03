import joblib
import pandas as pd
import numpy as np

print("========================================")
print("       TERRASENSE FIRE MONITOR")
print("========================================")

model = joblib.load("terrasense_model.pkl")

print()
print("Enter 5 readings in ONE LINE")
print()
print("Format:")
print("ID:1,T:27.6,H:77.0,AQ:571;ID:2,T:28.1,H:76.0,AQ:580;ID:3,T:57.9,H:17.4,AQ:2947;ID:4,T:67.7,H:13.8,AQ:3752;ID:5,T:74.9,H:15.8,AQ:3026")
print()

text = input("Input: ")

try:
    raw_readings = text.split(";")

    if len(raw_readings) != 5:
        raise ValueError("Exactly 5 readings are required.")

    readings = []

    for reading in raw_readings:

        parts = reading.split(",")

        sensor_id = int(parts[0].split(":")[1])
        temperature = float(parts[1].split(":")[1])
        humidity = float(parts[2].split(":")[1])
        air_quality = float(parts[3].split(":")[1])

        readings.append({
            "ID": sensor_id,
            "Temperature": temperature,
            "Humidity": humidity,
            "MQ135": air_quality
        })

    # Prepare model input
    X = pd.DataFrame([
        {
            "Temperature": r["Temperature"],
            "Humidity": r["Humidity"],
            "MQ135": r["MQ135"]
        }
        for r in readings
    ])

    # Get fire probability for all 5 readings
    probabilities = model.predict_proba(X)[:, 1]

    print()
    print("----------------------------------------")
    print("INPUT OBSERVATIONS")
    print("----------------------------------------")

    for i, r in enumerate(readings):

        print(
            f"ID {r['ID']} : "
            f"T={r['Temperature']:.1f} C, "
            f"H={r['Humidity']:.1f} %, "
            f"AQ={r['MQ135']:.0f}"
        )

    print()
    print("----------------------------------------")
    print("MODEL PROBABILITIES")
    print("----------------------------------------")

    for i, probability in enumerate(probabilities):

        print(
            f"P{i+1} = {probability:.6f} "
            f"({probability * 100:.2f} %)"
        )

    # ------------------------------------------------
    # FINAL FIRE WARNING LOGIC
    # Only the LAST 3 readings are considered
    # ------------------------------------------------

    FIRE_THRESHOLD = 0.90

    last_three = probabilities[2:]

    fire_warning = any(
        probability >= FIRE_THRESHOLD
        for probability in last_three
    )

    print()
    print("----------------------------------------")
    print("FIRE WARNING ANALYSIS")
    print("----------------------------------------")

    print()
    print("Only the last 3 readings are evaluated.")

    print()
    print(f"P3 = {probabilities[2]:.6f}")
    print(f"P4 = {probabilities[3]:.6f}")
    print(f"P5 = {probabilities[4]:.6f}")

    print()
    print(f"Fire warning threshold = {FIRE_THRESHOLD:.2f}")

    print()
    print("----------------------------------------")

    if fire_warning:

        print("WARNING: FIRE DETECTED")
        print("ALARM STATUS: ON")
        print("RESULT: NOT NORMAL")

    else:

        print("NO FIRE DETECTED")
        print("ALARM STATUS: OFF")
        print("RESULT: NORMAL")

    print("----------------------------------------")
    print("========================================")

except Exception as e:

    print()
    print("----------------------------------------")
    print("ERROR")
    print("----------------------------------------")
    print(e)
    print()
    print("Use exactly 5 readings in this format:")
    print("ID:1,T:27.6,H:77.0,AQ:571;...")
