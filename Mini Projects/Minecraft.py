from ursina import mouse, camera
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grassT = load_texture("grass_block.png")
stoneT = load_texture("stone_block.png")
brickT = load_texture("brick_block.png")
dirtT = load_texture("dirt_block.png")
block_pick = 1

skyT = load_texture("skybox.png")
armT = load_texture("arm_texture.png")

punchS = Audio("punch_sound", loop=False, autoplay=False)


def update():
    global block_pick
    if held_keys["1"]:
        block_pick = 1
    if held_keys["2"]:
        block_pick = 2
    if held_keys["3"]:
        block_pick = 3
    if held_keys["4"]:
        block_pick = 4

    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), t=grassT):
        super().__init__(
            parent=scene,
            position=position,
            model='block',
            origin_y=0.5,
            texture=t,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            # highlight_color=color.lime,
            scale=0.5)

    def input(self, key):
        if self.hovered:

            if key == 'right mouse down':
                punchS.play()
                if block_pick == 1:
                    Voxel(position=self.position + mouse.normal, t=grassT)
                if block_pick == 2:
                    Voxel(position=self.position + mouse.normal, t=stoneT)
                if block_pick == 3:
                    Voxel(position=self.position + mouse.normal, t=brickT)
                if block_pick == 4:
                    Voxel(position=self.position + mouse.normal, t=dirtT)
            if key == 'left mouse down':
                punchS.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=skyT,
            scale=150,
            double_sided=True)


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="arm",
            texture=armT,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.6, -0.6))

    def active(self):
        # self.position = Vec2(0.55, -0.55)
        # self.rotation = Vec3(155, -15, 0)
        self.position = Vec2(0.5, -0.5)
        self.rotation = Vec3(160, -20, 0)

    def passive(self):
        self.position = Vec2(0.6, -0.6)
        self.rotation = Vec3(150, -10, 0)


for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()
app.run()
