import pandas as pd
import joblib

# Load trained TerraSense model
model = joblib.load("terrasense_model.pkl")

print("==============================================")
print("TERRASENSE FULL RANGE TEST")
print("==============================================")

# Values within the actual ESP32 ranges
temperatures = [55, 60, 65, 70, 75, 80, 85]
humidities = [10, 12, 15, 18, 20]
mq135_values = [2800, 3000, 3200, 3400, 3600, 3800, 3900]

results = []

# Test every combination
for temperature in temperatures:

    for humidity in humidities:

        for mq135 in mq135_values:

            sensor_data = pd.DataFrame([
                {
                    "Temperature": temperature,
                    "Humidity": humidity,
                    "MQ135": mq135
                }
            ])

            prediction = model.predict(sensor_data)[0]

            probability = model.predict_proba(sensor_data)[0][1]

            results.append({
                "Temperature": temperature,
                "Humidity": humidity,
                "MQ135": mq135,
                "Prediction": prediction,
                "Fire_Probability": probability
            })


# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Show summary
print("\nTotal combinations tested:", len(results_df))

fire_count = (results_df["Prediction"] == 1).sum()
not_fire_count = (results_df["Prediction"] == 0).sum()

print("FIRE predictions:", fire_count)
print("NOT FIRE predictions:", not_fire_count)

print("\n==============================================")
print("SAMPLE RESULTS")
print("==============================================")

print(results_df.head(20).to_string(index=False))

# Save complete results
results_df.to_csv(
    "terrasense_range_test_results.csv",
    index=False
)

print("\nComplete results saved to:")
print("terrasense_range_test_results.csv")

print("\n==============================================")
print("TEST COMPLETE")
print("==============================================")
