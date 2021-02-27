def calibrate(cfg, args):
    board = cfg['sub_board_type']
    print(f'Calibrating {board}')
    if board == 'PCA9685':
        calibrate_pca9685(cfg, args)
    elif board == 'TEENSY':
        calibrate_teensy(cfg, args)
    else: raise Exception(f'Unknown board type {board}')   

def calibrate_pca9685(cfg, args):
    pass

def calibrate_teensy(cfg, args):
    import serial
    whatToCalibrate = ''
    if args['--steering']:
        whatToCalibrate = 'Steering'
    elif args['--throttle']:
        whatToCalibrate = 'Throttle'
    else: raise Exception(f'Please specify which control to calibrate (python manage.py calibrate steering / throttle).')

    ser = serial.Serial(port=cfg['teensy_port'], baudrate=cfg['teensy_baudrate'])

    while True:
        pwm = ask_for_pwm()
        msg = f"try{whatToCalibrate}_{pwm}\n"
        ser.write(bytes(msg, 'utf-8'))

def ask_for_pwm():
    return int(input("Enter a PWM (0-4095, < 500 recommanded): "))

