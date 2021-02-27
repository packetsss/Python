"""
Scripts to drive a triton racer car

Usage:
    manage.py (drive) [--model=<model>]
    manage.py (train) (--tub=<tub1,tub2,..tubn>) (--model=<model>) [--transfer=<model>]
    manage.py (generateconfig)
    manage.py (postprocess) (--source=<original_data_folder>) (--destination=<processed_data_folder>) [--filter] [--latency]
    manage.py (calibrate) [--steering] [--throttle] 
    manage.py (processtrack) (--tub=<data_folder>) (--output=<track_json_file>)
"""

import sys
sys.path.append('/home/haoru/Projects/TR/Triton-Racer-Sim/')
from docopt import docopt
from os import path
from TritonRacerSim.core.car import Car
from TritonRacerSim.core.datapool import DataPool
from TritonRacerSim.utils.types import ModelType

def get_joystick_by_name(joystick_name):
    from TritonRacerSim.components.controller import JoystickType, G28DrivingWheel, PS4Joystick, XBOXJoystick
    joysitck_type = JoystickType(joystick_name)
    if joysitck_type == JoystickType.PS4:
        return PS4Joystick(cfg)
    elif joysitck_type == JoystickType.G28:
        return G28DrivingWheel(cfg)
    elif joysitck_type == JoystickType.XBOX:
        return XBOXJoystick(cfg)
    else:
        raise Exception(f'Unsupported joystick type: {joysitck_type}. Could be still under development.')

def assemble_car(cfg = {}, model_path = None):
    car = Car(loop_hz=20)

    from TritonRacerSim.components.controlmultiplexer import ControlMultiplexer
    from TritonRacerSim.components.datastorage import  DataStorage
    from TritonRacerSim.components.track_data_process import LocationTracker
    from TritonRacerSim.components.driver_assistance import DriverAssistance

    # Autopilot
    if model_path is not None:
        from TritonRacerSim.components.keras_pilot import KerasPilot
        pilot = KerasPilot(cfg, model_path, ModelType(cfg['model_type']))
        if cfg['preprocessing_enabled']:
            pilot.step_inputs[0] = 'cam/processed_img'
        car.addComponent(pilot)

    # Joystick
    joystick = get_joystick_by_name(cfg['joystick_type'])
    car.addComponent(joystick)

    # Control Signal Multiplexer
    mux = ControlMultiplexer(cfg)
    car.addComponent(mux)

    # Driver Assistance
    if cfg['drive_assist_enabled']:
        assistant = DriverAssistance(cfg)
        car.addComponent(assistant)

    # Interface with donkeygym, or real car electronics
    if cfg['i_am_on_simulator']:
        from TritonRacerSim.components.gyminterface import GymInterface
        gym = GymInterface(poll_socket_sleep_time=0.01,gym_config=cfg)
        car.addComponent(gym)
    else:
        if cfg['sub_board_type'] == 'TEENSY':
            from TritonRacerSim.components.teensy import TeensyMC_Test
            teensy = TeensyMC_Test(cfg)
            car.addComponent(teensy)
        
        from TritonRacerSim.components.camera import Camera
        cam = Camera(cfg)
        car.addComponent(cam)

    #Image preprocessing
    if cfg['preprocessing_enabled']:
        from TritonRacerSim.components.img_preprocessing import ImgPreprocessing
        preprocessing = ImgPreprocessing(cfg)
        car.addComponent(preprocessing)

    # Location tracker (for mountain track)
    if cfg['use_location_tracker']:
        tracker = LocationTracker(track_data_path=cfg['track_data_file'])
        car.addComponent(tracker)

    # Data storage
    storage = DataStorage()
    if cfg['preprocessing_enabled']:
        storage.step_inputs[0] = 'cam/processed_img'
        if cfg['preproceessing_keep_original']:
            original_data_storage = DataStorage(storage_path=storage.storage_path[0:-1]+'_original/')
            car.addComponent(original_data_storage)
    car.addComponent(storage)

    return car

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['generateconfig']:
        from TritonRacerSim.core.config import generate_config
        generate_config('./myconfig.json')

    elif args['processtrack']:
        from TritonRacerSim.components.track_data_process import TrackDataProcessor
        processor = TrackDataProcessor(args['--tub'], args['--output'])
        processor.process()

    else:
        from TritonRacerSim.core.config import read_config
        cfg = read_config(path.abspath('./myconfig.json'))

        if args['drive']:
            sim_path = cfg['donkey_sim_full_path']
            if sim_path != 'remote':
                import subprocess, time
                print (f'[Launching Local Simulator] {sim_path}')
                subprocess.Popen(sim_path)
                time.sleep(3)

            model_path =None
            if args['--model']:
                model_path = path.abspath(args['--model'])
                assemble_car(cfg, model_path).start()
            else:
                assemble_car(cfg).start()

        elif args['train']:
            tub = args['--tub']
            data_paths = []
            for folder_path in tub.split(','):
                data_paths.append(path.abspath(folder_path))

            model_path = path.abspath(args['--model'])
            # assert path.exists(model_path)

            from TritonRacerSim.components.keras_train import train
            transfer_path=None
            if (args['--transfer']):
                transfer_path = args['--transfer']
            train(cfg, data_paths, model_path, transfer_path)

        elif args['calibrate']:
            from TritonRacerSim.utils.calibrate import calibrate
            calibrate(cfg, args)

        elif args['postprocess']:
            if args['--filter']:
                from TritonRacerSim.utils.post_process import post_process
                post_process(args['--source'], args['--destination'], cfg)

            elif args['--latency']:
                from TritonRacerSim.utils.post_process import shift_latency
                shift_latency(args['--source'], args['--destination'])
