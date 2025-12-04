#include <Arduino_LSM9DS1.h>

// ------------- HPF VARS -------------
float fs = 119.0; // Sampling Rate
float fc = 0.3; // HPF Cutoff

float Ts = 1.0 / fs; // sampling period
float tau = 1.0 / (2.0 * 3.14159 * fc);
float hpf_alpha = tau / (tau + Ts);

// ------------- LPF VARS -------------
const float lpf_fc = 10.0;     // cutoff frequency (Hz)
const float dt = 1.0 / fs;
const float lpf_alpha = (2 * 3.14159 * lpf_fc * dt) / (2 * 3.14159 * lpf_fc * dt + 1);

// Butterworth vars | HPF + LPF
float ax_in_prev = 0, ay_in_prev = 0, az_in_prev = 0;
float ax_out_prev = 0, ay_out_prev = 0, az_out_prev = 0;
float ax_filtered, ay_filtered, az_filtered;

float vx_in_prev = 0, vy_in_prev = 0, vz_in_prev = 0;
float vx_out_prev = 0, vy_out_prev = 0, vz_out_prev = 0;
float vx_filtered = 0, vy_filtered = 0, vz_filtered = 0;

unsigned long lastMicros = micros();
float vx = 0, vy = 0, vz = 0;
// --------------------------------------------- // 
// ------------------FUNCTIONS------------------ // 
// --------------------------------------------- // 

float HPF_filter(float x, float &x_prev, float &y_prev) {
  float y = hpf_alpha * (y_prev + x - x_prev);
  x_prev = x;
  y_prev = y;
  return y;
}

float LPF_filter(float x, float &y_prev) {
  float y = y_prev + lpf_alpha * (x - y_prev);
  y_prev = y;
  return y;
}

void vel_reset (float &vel) {
  if (vel > 50) {
    vel = 0;
  }
}


// --------------------------------------------- // 
   // -----------------CODE------------------ // 
// --------------------------------------------- // 
void setup() {
  Serial.begin(115200);
  while (!Serial) { }
  
  if (!IMU.begin()) {
    Serial.println("IMU initialization failed!");
    while (1);
  }
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  delay(2500);
}

// --------------------------------------------- // 
  // ------------------LOOP------------------- // 
// --------------------------------------------- // 

void loop() {
  float ax, ay, az;

if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);

    unsigned long t = micros();  // timestamp in microseconds

    // ax, ay, az in g's. Convert to m/s^2:
    ax *= 9.80665;
    ay *= 9.80665;
    az *= 9.80665;

    // ACCELERATION FILTERING | HPF to remove high frequency noise
    ax_filtered = HPF_filter(ax, ax_in_prev, ax_out_prev);
    ay_filtered = HPF_filter(ay, ay_in_prev, ay_out_prev);
    az_filtered = HPF_filter(az, az_in_prev, az_out_prev);

    // VELOCITY CALCS
    vx += ax_filtered * ((t - lastMicros) * 1e-6);
    vy += ay_filtered * ((t - lastMicros) * 1e-6);
    vz += az_filtered * ((t - lastMicros) * 1e-6);
    lastMicros = t;

    // VELOCITY FILTERING
    vx_filtered = HPF_filter(vx, vx_in_prev, vx_out_prev);
    vy_filtered = HPF_filter(vy, vy_in_prev, vy_out_prev);
    vz_filtered = HPF_filter(vz, vz_in_prev, vz_out_prev);

    vel_reset(vx); vel_reset(vy); vel_reset(vz);

  
    // CSV OUTPUT --- PRINTING --- 
    Serial.print(t); Serial.print(',');
 
    Serial.print(vx_filtered); Serial.print(',');
    Serial.print(vy_filtered); Serial.print(',');
    Serial.println(vz_filtered);
  }


}
