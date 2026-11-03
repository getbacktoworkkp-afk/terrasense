import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# 1. LOAD TERRASENSE DATASET
# ==========================================

data = pd.read_csv(
    "datasets/terrasense_synthetic_training_data.csv"
)

print("Dataset loaded successfully!")
print("Total samples:", len(data))

print("\nFirst 5 samples:")
print(data.head())


# ==========================================
# 2. FEATURES AND TARGET
# ==========================================

X = data[[
    "Temperature",
    "Humidity",
    "MQ135"
]]

y = data["Fire"]


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. CREATE MODELS
# ==========================================

models = {

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            random_state=42
        ))
    ]),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        random_state=42
    )
}


# ==========================================
# 5. TRAIN AND EVALUATE
# ==========================================

results = {}

for name, model in models.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    results[name] = accuracy

    print("\nAccuracy:",
          round(accuracy * 100, 2), "%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Not Fire",
                "Fire"
            ]
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


# ==========================================
# 6. COMPARE MODELS
# ==========================================

print("\n" + "=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

for name, accuracy in results.items():

    print(
        f"{name}: "
        f"{accuracy * 100:.2f}%"
    )


# ==========================================
# 7. FIND BEST MODEL
# ==========================================

best_model_name = max(
    results,
    key=results.get
)

print("\nBest model:")
print(best_model_name)

print(
    f"Accuracy: "
    f"{results[best_model_name] * 100:.2f}%"
)

import joblib
best_model = models[best_model_name]
joblib.dump(best_model, 'terrasense_model.pkl')
print('MODEL SAVED SUCCESSFULLY!')
print('File: terrasense_model.pkl')
