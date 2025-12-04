import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from sklearn.ensemble import RandomForestRegressor

# ================== USER INPUT ==================
load_percent = float(input("Enter load percentage: "))

# ================== ARDUINO SETTINGS ==================
PORT = "COM7"
BAUD = 115200
RECORD_SECONDS = 70
CONC_THRESH = -0.05
REP_THRESH = 0.3
VELOCITY_CHANGE_THRESH = 0.1
SAMPLING_RATE = 119

# ================== EMBEDDED TRAINING DATA ==================
data = [
    [90, 0.080902, 7, 4],
    [90, 0.082081, 8, 3],
    [90, 0.072702, 9, 2],
    [90, 0.094252, 10, 1],
    [81.0, 0.36239, 2, 13.0],
    [81.0, 0.40326, 3, 12.0],
    [81.0, 0.36771, 4, 11.0],
    [81.0, 0.34297, 5, 10.0],
    [81.0, 0.3008, 6, 9.0],
    [81.0, 0.34206, 7, 8.0],
    [81.0, 0.32768, 8, 7.0],
    [81.0, 0.38284, 9, 6.0],
    [81.0, 0.33268, 10, 5.0],
    [81.0, 0.28386, 11, 4.0],
    [81.0, 0.21426, 12, 3.0],
    [81.0, 0.16019, 13, 2.0],
    [81.0, 0.14778, 14, 1.0],
    [84.0, 0.20904, 2, 7.0],
    [84.0, 0.14599, 3, 6.0],
    [84.0, 0.15647, 4, 5.0],
    [84.0, 0.17191, 5, 4.0],
    [84.0, 0.080902, 6, 3.0],
    [84.0, 0.082081, 7, 2.0],
    [84.0, 0.072702, 8, 1.0],
    [78.26, 0.42583, 3, 5.0],
    [78.26, 0.38115, 4, 4.0],
    [78.26, 0.39783, 5, 3.0],
    [78.26, 0.3415, 6, 2.0],
    [78.26, 0.38326, 7, 1.0],
    [75.0, 0.64547, 2, 9.0],
    [75.0, 0.57554, 3, 8.0],
    [75.0, 0.54587, 4, 7.0],
    [75.0, 0.40115, 5, 6.0],
    [75.0, 0.30139, 6, 5.0],
    [75.0, 0.087535, 7, 4.0],
    [75.0, 0.33221, 8, 3.0],
    [75.0, 0.083888, 9, 2.0],
    [75.0, 0.15256, 10, 1.0],
    [78.26, 0.4068, 2, 6.0],
    [78.26, 0.37102, 3, 5.0],
    [78.26, 0.35403, 4, 4.0],
    [78.26, 0.35116, 5, 3.0],
    [85.0, 0.3026, 2, 5.0],
    [85.0, 0.27808, 3, 4.0],
    [85.0, 0.27157, 4, 3.0],
    [85.0, 0.23726, 5, 2.0],
    [85.0, 0.19981, 6, 1.0],
    [85.0, 0.46208, 2, 9.0],
    [85.0, 0.44959, 3, 8.0],
    [85.0, 0.43031, 4, 7.0],
    [85.0, 0.35364, 5, 6.0],
    [85.0, 0.36179, 6, 5.0],
    [85.0, 0.18464, 7, 4.0],
    [85.0, 0.16788, 8, 3.0],
    [85.0, 0.17535, 9, 2.0],
    [85.0, 0.17181, 10, 1.0]
]

df = pd.DataFrame(data, columns=["load_percent", "mean_velocity_last_rep", "reps_completed", "actual_RIR"])

# ================== TRAIN MODEL ==================
X = df.drop("actual_RIR", axis=1)
y = df["actual_RIR"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)
print("✅ Model trained from embedded data.")

# ================== ARDUINO DATA COLLECTION ==================
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("✅ Connected to Arduino. Recording...")

t = []
vx, vy, vz, vt = [], [], [], []
vt_conc = []
rep_count = 1
prev_conc = False
rep_start = 0
rep_indices = []
idx = 0
t_start = time.time()
window_size = int(4 * SAMPLING_RATE)

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
line_conc, = ax.plot([], [], label="concentric", color="red")
ax.legend()

while time.time() - t_start < RECORD_SECONDS:
    try:
        raw = ser.readline().decode().strip()
        parts = raw.split(",")
        if len(parts) != 4:
            continue

        current_time = float(parts[0])/1e6
        vx_val = float(parts[1])
        vy_val = float(parts[2])
        vz_val = float(parts[3])
        vt_val = np.sqrt(vx_val**2 + vy_val**2 + vz_val**2)

        t.append(current_time)
        vx.append(vx_val)
        vy.append(vy_val)
        vz.append(vz_val)
        vt.append(vt_val)

        # Concentric detection
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
                    rep_indices.append((rep_start, rep_end))
                    rep_count += 1

        # Early stop on inactivity
        if len(vt) > window_size:
            recent_vt = vt[-window_size:]
            if np.max(recent_vt) - np.min(recent_vt) < VELOCITY_CHANGE_THRESH:
                print("✅ No significant motion for 4 sec. Stopping early.")
                break

        idx += 1

        # Update live plot
        if idx % 5 == 0:
            line_vx.set_data(t, vx)
            line_vy.set_data(t, vy)
            line_vz.set_data(t, vz)
            line_vt.set_data(t, vt)
            line_conc.set_data(t, vt_conc)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.001)

    except:
        continue

ser.close()
print("✅ Recording finished.")

# ================== REP ANALYSIS ==================
rep_count -= 1
avgVelocity, peakVelocity, duration = [], [], []
for start, end in rep_indices:
    avgVelocity.append(np.mean(vt[start:end]))
    peakVelocity.append(np.max(vt[start:end]))
mean_vel_last_rep = avgVelocity[-1] if avgVelocity else 0
reps_completed = rep_count
velocityLoss = ((avgVelocity[0] - avgVelocity[-1]) / avgVelocity[0] * 100) if rep_count>1 else 0

# ================== PREDICT RIR ==================
X_new = pd.DataFrame([{
    "load_percent": load_percent,
    "mean_velocity_last_rep": mean_vel_last_rep,
    "reps_completed": reps_completed
}])
predicted_rir = round(model.predict(X_new)[0])

# ================== OUTPUT ==================
print(f"\nReps completed: {reps_completed}")
print(f"Mean velocity last rep: {mean_vel_last_rep:.3f}")
print(f"Velocity loss: {velocityLoss:.1f}%")
print(f"🎯 Estimated RIR: {predicted_rir}")

# ================== FINAL PLOT ==================
plt.ioff()
plt.figure()
plt.plot(avgVelocity, label="Mean Velocity")
plt.plot(peakVelocity, label="Peak Velocity")
x = np.arange(1, rep_count+1)
if len(x)>1:
    p = np.polyfit(x, peakVelocity, 1)
    plt.plot(x, np.polyval(p, x), label="Peak Trend")
plt.title(f"Velocity Change — Loss: {velocityLoss:.1f}%")
plt.xlabel("Rep #")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()
plt.show()
