# Apex-RIR-Prediction
This project utilizes the IMU embedded on an Arduino Nano BLE Sense 33 to collect and segment rep data from an exercise in real time, which is then used to predict the reps in reserve (failure proximity) of the user. 

This System includes the following code:

1. Arduino Code - Collects real time Acceleration data using IMU, applies a 1st order High Pass Filter to cancel out drift, calculates Velocity by integrating Acceleration with time, applies the filter , then streams Velocity data to MATLAB
2. MATLAB Code - Reads real-time serial data from the Arduino, detects reps in their concentric phase (weight going up), and extracts features based on data of each rep "window".

Block Diagram: Real World / Gym -> Arduino Nano -> MATLAB -> Plots / Visual Figures -> Python Random Tree Model -> RIR Prediction

Hardware Requirements:
Arduino Nano BLE Sense 33
Arduino Container + Adhesive
USB Cable + Extension (if needed)
Laptop

Data Collection / Guide
Plug in Arduino to Laptop
Upload VelocityDataCollection code to Arduino, Note down COM port. 
Open MATLAB file and change COMPORT to match, and set recording time to much longer
RUN the MATLAB code once to ensure everything is functional
After confirming functionality, attach Arduino to ontop of Weight stack
Once ready, click RUN, then perform the set
Upon completion, Enter the SET LEVEL data into python model
