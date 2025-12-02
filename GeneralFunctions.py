import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

# 1. LOAD OR CREATE DATASET
DATA_FILE = "rir_dataset.csv"
MODEL_FILE = "rir_model.pkl"

# Create empty dataset if not_exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "load_percent",
        "mean_velocity_last_rep",
        "velocity_loss",
        "reps_completed",
        "slope",            # NEW FEATURE
        "actual_RIR"
    ])
    df.to_csv(DATA_FILE, index=False)

# Load dataset
df = pd.read_csv(DATA_FILE)

# 2. FUNCTION TO ADD NEW TRAINING DATA
def add_training_example(load_percent, vel_last_rep, vel_loss, reps, slope, actual_rir):
    global df
    new_row = {
        "load_percent": load_percent,
        "mean_velocity_last_rep": vel_last_rep,
        "velocity_loss": vel_loss,
        "reps_completed": reps,
        "slope": slope,             # NEW FEATURE
        "actual_RIR": actual_rir
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print("Added new training example.")

# 3. TRAIN OR RETRAIN MODEL
def train_model():
    global df

    if len(df) < 10:
        print("Not enough data to train yet. Need at least 10 samples.")
        return None

    X = df.drop("actual_RIR", axis=1)   # slope now included here automatically
    y = df["actual_RIR"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    print(f"Model trained. Test MAE = {mae:.3f} RIR")

    joblib.dump(model, MODEL_FILE)
    print("Model saved.")

    return model


# 4. PREDICT RIR FOR NEW WORKOUT SET
def predict_rir(load_percent, vel_last_rep, vel_loss, reps_completed, slope):
    if not os.path.exists(MODEL_FILE):
        print("Model not trained yet.")
        return None

    model = joblib.load(MODEL_FILE)

    X_new = pd.DataFrame([{
        "load_percent": load_percent,
        "mean_velocity_last_rep": vel_last_rep,
        "velocity_loss": vel_loss,
        "reps_completed": reps_completed,
        "slope": slope               # NEW FEATURE
    }])

    raw_rir = model.predict(X_new)[0]
    rounded_rir = round(raw_rir)
    print(f"✅ Predicted RIR (): {rounded_rir}")

    return rounded_rir

