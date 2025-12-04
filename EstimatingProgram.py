import pandas as pd
import joblib
import os

MODEL_FILE = "rir_model.pkl"

def predict_rir(load_percent, vel_last_rep, reps_completed):
    if not os.path.exists(MODEL_FILE):
        print("Model file not found. Train the model first.")
        return None

    # Load trained model
    model = joblib.load(MODEL_FILE)

    # Arrange input in same order as training columns
    X_new = pd.DataFrame([{
        "load_percent": load_percent,
        "mean_velocity_last_rep": vel_last_rep,
        "reps_completed": reps_completed,
    }])

    raw_rir = model.predict(X_new)[0]
    rounded_rir = round(raw_rir)
    print(f"✅ Predicted RIR (): {rounded_rir}")

    return rounded_rir



# -------- ENTER YOUR INPUTS HERE -------- #
predict_rir(
    load_percent=90,
    vel_last_rep=0.2,
    reps_completed = 5,

)
