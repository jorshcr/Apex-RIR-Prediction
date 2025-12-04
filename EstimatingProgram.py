import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os

# ============ USER INPUT ============
load_percent = float(input("Enter load percentage: "))

# ============ SERIAL SETTINGS ============
PORT = "COM7"
BAUD = 115200
RECORD_SECONDS = 15
INACTIVITY_LIMIT = 4      # STOP after 4 seconds of no reps
CONC_THRESH = -0.05
REP_THRESH = 0.3

MODEL_FILE = "rir_model.pkl"

# ============ LOAD MODEL ============
if not os.path.exists(MODEL_FILE):
    raise FileNotFoundError("❌ rir_model.pkl not found in this folder")

model = joblib.load(MODEL_FILE)

# ============ CONNECT TO ARDUINO ============
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("✅ Connected to Arduino. Recording...")

# ============ DATA STORAGE ============
t = []
vx, vy, vz, vt = [], [], [], []
vt_conc = []

rep_count = 1
prev_conc = False
rep_indices = []
rep_start = 0
last_rep_time = None  # ✅ FIX: track last rep end time

t_start = time.time()
idx = 0

# ============ REAL-TIME PLOT ============
plt.ion()
fig, ax = plt.subplots()
ax.set_title("Real-Time Velocity")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
ax.grid()

line_vx, = ax.plot([], [], label="vx", color="gray")
line_vy, = ax.plot([], [], label="vy", color="dimgray")
line_vz, = ax.plot([], [], label="vz", color="blue")
line_vt, = ax.plot([], [], label="vt", color="black")
line_conc, = ax.plot([], [], label="Concentric", color="red", linewidth=2)

ax.legend()
# ============ DATA COLLECTION ============
while time.time() - t_start < RECORD_SECONDS:
    try:
        raw = ser.readline().decode().strip()
        parts = raw.split(",")

        if len(parts) != 4:
            continue

        current_time = float(parts[0]) / 1e6
        vx_val = float(parts[1])
        vy_val = float(parts[2])
        vz_val = float(parts[3])
        vt_val = np.sqrt(vx_val**2 + vy_val**2 + vz_val**2)

        t.append(current_time)
        vx.append(vx_val)
        vy.append(vy_val)
        vz.append(vz_val)
        vt.append(vt_val)

        # ---- CONCENTRIC LOGIC ----
        if vz_val < CONC_THRESH:
            vt_conc.append(vt_val)

            if not prev_conc:
                rep_start = idx
                prev_conc = True
        else:
            vt_conc.append(np.nan)

            if prev_conc:
                prev_conc = False
                rep_end = idx
                duration = t[rep_end] - t[rep_start]

                if duration > REP_THRESH:
                    ax.set_title(f"Reps Completed: {rep_count}")
                    rep_indices.append((rep_start, rep_end))
                    last_rep_time = t[rep_end]   # ✅ critical line
                    rep_count += 1

                # ✅✅ STOP AFTER 4 SECONDS OF NO REPS ✅✅
            if rep_count > 2:
                if (t[-1] - last_rep_time) > INACTIVITY_LIMIT:
                    print("✅ No reps detected for 4 seconds. Stopping recording...")
                    break

        idx += 1

    
        # ---- UPDATE PLOT ----
        if idx % 5 == 0:
            line_vx.set_data(t, vx)
            line_vy.set_data(t, vy)
            line_vz.set_data(t, vz)
            line_vt.set_data(t, vt)
            line_conc.set_data(t, vt_conc)

            ax.relim()
            ax.autoscale_view()
            plt.pause(0.001)

    except Exception as e:
        continue

ser.close()
print("✅ Recording complete!")

# ============ REP ANALYSIS ============
rep_count -= 1

avgVelocity, peakVelocity, duration = [], [], []
startIdx, endIdx = [], []

for start, end in rep_indices:
    startIdx.append(start)
    endIdx.append(end)
    duration.append(t[end] - t[start])
    avgVelocity.append(np.mean(vt[start:end]))
    peakVelocity.append(np.max(vt[start:end]))

mean_vel_last_rep = avgVelocity[-1]
reps_completed = rep_count

velocityLoss = ((avgVelocity[0] - avgVelocity[-1]) / avgVelocity[0]) * 100

# ============ SUMMARY TABLE ============
repSummary = pd.DataFrame({
    "Rep #": np.arange(1, rep_count + 1),
    "Duration (s)": duration,
    "StartIdx": startIdx,
    "EndIdx": endIdx,
    "Avg Vel": avgVelocity,
    "Peak Vel": peakVelocity
})

print("\n📊 REP SUMMARY")
print(repSummary)

# ============ FINAL MODEL INPUT ============
X_new = pd.DataFrame([{
    "load_percent": load_percent,
    "mean_velocity_last_rep": mean_vel_last_rep,
    "reps_completed": reps_completed
}])

raw_rir = model.predict(X_new)[0]
predicted_rir = round(raw_rir)

# ============ RESULT ============
print("\n✅ FEATURES EXTRACTED")
print(f"Reps Completed: {reps_completed}")
print(f"Mean Velocity Last Rep: {mean_vel_last_rep:.3f}")
print(f"Velocity Loss: {velocityLoss:.2f}%")

print("\n🎯 FINAL RESULT")
print(f"Estimated RIR: {predicted_rir}")

# ============ SUMMARY PLOT ============
plt.ioff()
plt.figure()
plt.plot(avgVelocity, label="Mean Velocity")
plt.plot(peakVelocity, label="Peak Velocity")

x = np.arange(1, rep_count + 1)
p = np.polyfit(x, peakVelocity, 1)
plt.plot(x, np.polyval(p, x), label="Peak Trend")

plt.title(f"Performance Change — Vel Loss: {velocityLoss:.2f}%")
plt.xlabel("Rep #")
plt.ylabel("Velocity (m/s)")
plt.grid()
plt.legend()
plt.show()
