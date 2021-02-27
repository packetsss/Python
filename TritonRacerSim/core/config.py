import json
import uuid
config = {
    'explanation': '''model_type: cnn_2d | cnn_2d_speed_as_feature | cnn_2d_speed_control | cnn_2d_full_house; joystick_type: ps4 | xbox | g28; sim_host: use 127.0.0.1 for local; track_data_file: used for position tracker to segment the track
    ''',
    # Camera Type
    'cam_type': 'WEBCAM', # WEBCAM | MOCK Put mock if the camera is not actually installed
    'img_w': 160, # Width after cropping
    'img_h': 120, # Height after cropping
    'image_format': 'rgb', # RGB or grey
    'cam_source': 0, # Index of camera
    'cam_resolution': [320, 240], # Resolution of open camera, check with manufacturer for resolution support

    # Image Preprocessing
    'preprocessing_enabled': False, # Enable image filtering
    'preprocessing_preview_enabled': True, # Display an OpenCV imshow window to monitor the preprocessing
    'preproceessing_keep_original': False, # Store the original image data under data/records_x_original/
    'preprocessing_contrast_enhancement_ratio': 1.0, # Enhance contrast, especially on the new robo racing league track
    'preprocessing_contrast_enhancement_offset': 125, # Ranging [0,255]. Pixels above this value will be positively boosted, vise versa, and hence enhancing the contrast of the image.
    'preprocessing_dynamic_brightness_enabled': False, # Automatically adjust the brightness of the image
    'preprocessing_brightness_baseline': 550, # Used to, for example, increase the brightness of pictures taken in the dark corners of the track
    'preprocessing_color_filter_enabled': False, # Filtering out the interested colors. Checkout Triton AI Color Filter Tutorial.
    'preprocessing_color_filter_hsvs': [((0, 0, 130),(180, 64, 255)),((25, 180, 155),(43, 255, 255))], # upper and lower bounds (HSV) of each color detection. In this case white and yellow.
    'preprocessing_color_filter_destination_channels':[0, 1], # Which channel to put the filtered layers? 0 | 1 | 2 for RGB image. Must match the number of hsv filters above.)
    'preprocessing_edge_detection_enabled': False, # Apply a canny filter for edge detection
    'preprocessing_edge_detection_threshold_a': 60, # Threshold used in OpenCV canny filter
    'preprocessing_edge_detection_threshold_b': 100,
    'preprocessing_edge_detection_destination_channel': 2, # Which channel to put the filtered layer? 0 | 1 | 2 for RGB image

    # On-board Electronics
    'sub_board_type': 'PCA9685', # PCA9685 | TEENSY | GPIO # Who is responsible for sending PWM signals to the motor and servo?
    'calibrate_max_forward_pwm': 400,
    'calibrate_zero_throttle_pwm': 370,
    'calibrate_max_reverse_pwm': 330,
    'calibrate_max_left_pwm': 430,
    'calibrate_max_right_pwm': 300,
    'calibrate_neutral_steering_pwm': 350,

    'PCA9685_esc_channel': 1, # On PCA9685, which channel is the electronic speed controller (ESC) connected to?
    'PCA9685_servo_channel': 2, # On PCA9685, which channel is the servo connected to?

    'teensy_port': '/dev/ttyACM0',
    'teensy_baudrate': 115200,
    'teensy_watchdog_trigger_time': 100, # ms before the watchdog kicks in and shut down the system
    'teensy_poll_interval': 25, # ms between each polling

    # Joystick
    'joystick_type': 'ps4', # [ ps4 | xbox | g28 | steam | switch ] Wired joysticks recommended.
    'joystick_use_bluetooth': False, # For ps4 controller: is it connected via bluetooth or wire?
    'joystick_max_throttle': 1.0, # throttle limiter (0, 1]
    'joystick_max_steering': 1.0, # steering limiter (0, 1]

    # AI boost
    'ai_launch_boost_throttle_enabled': False, # Lock throttle when switching from ai-steering to full-ai mode
    'ai_launch_boost_throttle_value': 1.0,
    'ai_launch_boost_throttle_duration': 5,

    'ai_launch_lock_steering_enabled': False, # Lock steering when switching from ai-steering to full-ai mode
    'ai_launch_lock_steering_value': 0.0,
    'ai_launch_lock_steering_duration': 3,

    'smooth_steering_enabled': False, # Consider all AI steerings above the threshold a full steering (1.0 or -1.0)
    'smooth_steering_threshold': 0.9,

    # Training
    'model_type': 'cnn_2d_speed_control', # cnn_2d | cnn_2d_speed_as_feature | cnn_2d_speed_control | cnn_2d_full_house
    'early_stop': True, # Early stop when training hasn't made any progress within the patience
    'early_stop_patience': 5,
    'max_epoch': 100, # Max epoch to train
    'batch_size': 64, # Lower it to save GPU resources, or increase it to experdite training.

    # Speed-based control params (for speed control and full house models)
    'spd_ctl_threshold': 1.1, # Allow the model to overspeed. 1.1 means 10% above predicted speed.
    'spd_ctl_reverse': True, # Apply reverse throttle when overspeed, e.g. -0.4.
    'spd_ctl_reverse_multiplier': 1.0, # How hard the car should reverse
    'spd_ctl_break': False, # WARRNING: OVERWRITES REVERSE. Apply break when overspeed, e.g. 0.3. Break will OVERRIDE any throttle value.
    'spd_ctl_break_multiplier': 1.0, # How hard the car should break
    
    # Simulator
    'i_am_on_simulator': True, # Turn this on to go to simulator. Turn this off on real cars.
    'car_name': 'TritonRacer',
    'font_size': 50,
    'racer_name': 'Triton AI',
    'bio': 'Something',
    'country': 'US',
    'body_style': 'car01',
    'body_rgb': (24, 43, 73),
    'guid': 'will_be_overwritten_when_generating_config',

    'donkey_sim_full_path': 'remote',
    'scene_name': 'roboracingleague_1',
    'sim_path': 'remote', # Does not work currently
    'sim_host': '127.0.0.1',
    'sim_port': 9091,
    'sim_latency': 0,
    
    'use_location_tracker': False, # Track which segment of track the car is on.
    'track_data_file': 'track_data/generated_track.json',

    # Driver Assistance
    'drive_assist_enabled': False, # Drive assist for simulator. Not recommanded for real cars.
    'drive_assist_limit_mode': 'steering', # speed | steering. 'speed' means limiting speed to match steering, vise versa.
    'drive_assist_limit_k': 5, # k as in y = k / x. Speed and steering are inversly proportional

}

def read_config(config_path):
    with open(config_path, 'r') as config_file:
        cfg = json.load(config_file)
    return cfg

def generate_config(config_path):
    config['guid'] = uuid.uuid1().__str__()
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)