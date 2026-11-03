# TerraSense

TerraSense is an experimental AI-based wildfire monitoring prototype combining machine learning with an ESP32-oriented implementation.

The project explores fire classification using temperature, humidity, and MQ135 air-quality sensor readings.

## Features

- Temperature, humidity, and MQ135-based classification.
- Logistic Regression, Decision Tree, and Random Forest model comparison.
- Model evaluation using accuracy, classification reports, and confusion matrices.
- Export of the trained Logistic Regression model into an ESP32-compatible C++ header.
- Five-reading test sequence with a two-out-of-three fire-warning decision rule.

## Project Structure

```text
terrasense/
|-- datasets/
|   |-- terrasense_synthetic_training_data.csv
|-- esp32/
|   |-- terrasense_esp32.ino
|   |-- terrasense_model.h
|-- export.py
|-- requirements.txt
|-- terrasense_model.pkl
|-- terrasense_range_test_results.csv
|-- train_terrasense.py
|-- test.py
|-- test_model.py
|-- test_all_ranges.py
```

## Machine Learning Pipeline

The training script loads the synthetic dataset and uses Temperature, Humidity, and MQ135 as input features.

It splits the data into training and testing sets, trains three classifiers, compares their performance, and saves the best-performing model as terrasense_model.pkl.

The saved model is a scikit-learn pipeline containing feature scaling and classification.

## Installation

Requires Python 3.10 or later.

```bash
python -m venv venv
```

Activate the environment in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Train the Models

```bash
python train_terrasense.py
```

## Test Sensor Ranges

```bash
python test_all_ranges.py
```

## Test Five Sensor Readings

```bash
python test_model.py
```

The interactive test accepts five readings and evaluates the last three for its final warning decision.

## Export the Model to ESP32

```bash
python export.py
```

This generates the ESP32 model header and firmware files in the esp32 directory.

## Current Prototype Limitations

- The included training dataset is synthetic.
- Evaluation on synthetic data does not establish real-world wildfire detection accuracy.
- The current ESP32 sketch uses five hard-coded sample readings rather than live sensor acquisition.
- The ESP32 sketch uses a 0.50 probability threshold, while the Python interactive test uses 0.90 for its final warning logic.
- Real-world hardware integration and field validation are not established by this repository.

TerraSense is an experimental prototype, not a certified fire detection or safety system.

## Technologies

- Python, Pandas, NumPy, Scikit-learn, Joblib
- ESP32 and Arduino C++

## License

No open-source license has been assigned. All rights remain with their respective owners.
