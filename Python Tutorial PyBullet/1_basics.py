import pybullet as p
import time
import pybullet_data

physics_client = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -50)
plane_id = p.loadURDF("plane.urdf")

# load car
car_id = p.loadURDF("racecar/racecar.urdf", basePosition=[0, 0, 0.03])

# set the center of mass frame (load_urdf sets base link frame) start_pos/_ornp.reset_base_position_and_orientation(box_id, start_pos, start_orientation)
for i in range(1000):
    pos, ori = p.getBasePositionAndOrientation(car_id)
    p.applyExternalForce(car_id, 0, [200, 100, 0], pos, p.WORLD_FRAME)
    p.stepSimulation()
    time.sleep(1.0 / 240.0)
cube_pos, cube_orn = p.getBasePositionAndOrientation(car_id)
print(cube_pos, cube_orn)
p.disconnect()
