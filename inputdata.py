from modeltraining import add_training_example, train_model
import pickle



# Add data
'''
#  load percentage, last rep veloctiy, mean velocity loss, Actual RIR, peak vel slope

add_training_example(82, 0.24551, 15, 47.9355,-0.028, 3)
add_training_example(68, 0.12668, 15, 53.74616,-0.017866, 2)
add_training_example(81, 0.069603, 12, 82.01379 ,-0.069783, 1)
add_training_example(81.2, 0.28363, 13, 20.972415,-0.0033755, 4)
add_training_example(79, 0.099647, 9, 52.141107,-0.020901, 3)
add_training_example(84, 0.16095, 13, 25.74086, -0.006285, 1)
add_training_example(90, 0.16016, 7, 27.698665, -0.0012756, 1)
add_training_example(86.79, 0.16814, 5, 42.28736, -0.065354, 2)
add_training_example(79, 0.1232, 8, 63.086142, -0.0330186, 2)
add_training_example(83.87, 0.3143, 10, 28.28948, -0.01695, 4)
add_training_example(76, 0.16512, 11, 49.85047, -0.017838, 2)
add_training_example(81.2, 0.21609, 9, 39.863078, -0.047029, 2)
add_training_example(86.79, 0.20467, 5, 33.249624, -0.041342, 3)
add_training_example(89, 0.067846, 4, 63.590684, -0.066687, 2)
add_training_example(90, 0.23947, 5, 10.176294, -0.015884, 3)
'''

'''
add_training_example(85, 0.22214, 4, 30.51, -0.0028319, 8)
add_training_example(85, 0.14703, 5, 54.007, -0.047015, 7)
add_training_example(85, 0.23602, 6, 26.168, -0.041505, 6)
add_training_example(85, 0.074789, 7, 76.605, -0.065001, 5)
add_training_example(85, 0.17325, 8, 45.803, -0.056099, 4)
add_training_example(85, 0.086178, 9, 73.042, -0.057535, 3)
add_training_example(85, 0.11741, 10, 63.274, -0.052391, 2)
add_training_example(85, 0.1161, 11, 63.682, -0.046751, 1)
add_training_example(85, 0.11936, 12, 62.663, -0.042491, 0)
'''

'''
add_training_example(87, 0.31148, 2, 4.5192,  -0.020408, 6)
add_training_example(87, 0.32437, 3, 0.56897, -0.019969, 5)
add_training_example(87, 0.30373, 4, 6.8965,  -0.019981, 4)
add_training_example(87, 0.20544, 5, 37.025,  -0.046006, 3)
add_training_example(87, 0.14972, 6, 54.106,  -0.069756, 2)
add_training_example(87, 0.075877, 7, 76.741, -0.084623, 1)
'''

'''
add_training_example(89, 0.1588,  2,   28.974, -0.069933, 6)
add_training_example(89, 0.1422,  3,   36.397, -0.024978, 5)
add_training_example(89, 0.14397, 4,   35.606, -0.018827, 4)
add_training_example(89, 0.17624, 5,   21.171, -0.015826, 3)
add_training_example(89, 0.17804, 6,   20.364, -0.017063, 2)
add_training_example(89, 0.14015, 7,   37.313, -0.017816, 1)
add_training_example(89, 0.12209, 8,   45.39,  -0.020802, 0)

'''

'''
add_training_example(86.79, 0.30025, 2,  -4.8574,  0.059515, 6)
add_training_example(86.79, 0.19047, 3,   33.48,  -0.064891, 5)
add_training_example(86.79, 0.15858, 4,   44.617, -0.082101, 4)
add_training_example(86.79, 0.1269,  5,   55.681, -0.083147, 3)
add_training_example(86.79, 0.14254, 6,   50.221, -0.070141, 2)
add_training_example(86.79, 0.080353,7,   71.938, -0.068669, 1)

'''
'''
add_training_example(80, 0.36239, 3,   3.055,   0.0099902, 14)

add_training_example(80, 0.36771, 5,   1.632,  -0.0090246, 12)
add_training_example(80, 0.34297, 6,   8.2521, -0.014923,  11)
add_training_example(80, 0.3008,  7,  19.532,  -0.024539,  10)
add_training_example(80, 0.34206, 8,   8.4954, -0.018924,   9)
add_training_example(80, 0.32768, 9,  12.34,   -0.019169,   8)

add_training_example(80, 0.33268,11,  11.005,  -0.013166,   6)
add_training_example(80, 0.28386,12,  24.065,  -0.016392,   5)
add_training_example(80, 0.21426,13,  42.683,  -0.023015,   4)
add_training_example(80, 0.16019,14,  57.147,  -0.031199,   3)
add_training_example(80, 0.14778,15,  60.468,  -0.035737,   2)
add_training_example(80, 0.12658,16,  66.138,  -0.038791,   1)

'''

add_training_example(90, 0.20904, 3,  -17.423,  0.029893, 8)
add_training_example(90, 0.14599, 4,   17.995, -0.045407, 7)
add_training_example(90, 0.15647, 5,   12.11,  -0.036382, 6)

add_training_example(90, 0.080902, 7,  54.556, -0.036186, 4)
add_training_example(90, 0.082081, 8,  53.893, -0.037185, 3)
add_training_example(90, 0.072702, 9,  59.162, -0.037732, 2)
add_training_example(90, 0.094252, 10, 47.056, -0.032196, 1)



# Train
train_model()


