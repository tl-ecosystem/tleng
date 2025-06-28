# Copyright (c) 2023 Theolaos

# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to 
# whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the 
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame
from pygame import Vector2
from dataclasses import dataclass
from math import cos, sin

from ..engine.settings import GlobalSettings
from ..object.area import AreaComp, VertAreaComp, VertArea
from ..object.sprite import Sprite


class MainCameraComp: ...

@dataclass
class CameraComp:
    """
    surface: entity that has `DisplayCanvasComp`
    """ 
    surface: int
    area: AreaComp


@dataclass
class VertCamera:
    surface: pygame.Surface
    vert_area: VertAreaComp


z_vec = Vector2(0, 0)

class CameraCatcher:
    cameras = {}
    default_camera_key = ''
    default_camera = None

    def __init__(self, camera_key, default_camera):
        default_key = f"camera{len(self.cameras)}"
        if camera_key != "":
            self.cameras.update({camera_key: self})
        else:
            self.cameras.update({default_key: self})

        if default_camera and camera_key != "":
            self.default_camera_key = camera_key
            self.default_camera = self
        else:
            self.default_camera_key = default_key
            self.default_camera = self

        self.name = camera_key if camera_key != "" else default_key
        print(self.cameras)


class Camera(CameraCatcher):
    '''
    Handles how the Surfaces are rendered to the screen, keeping the world positions.
    center: world position the camera is focused on (e.g., the player)
    center_screen: pixel position on the display where the camera's center appears (usually screen center)
    offset_pos: vector to translate world positions to screen positions
    angle: rotation of the camera in radians (for rotating the world around the player)
    '''
    def __init__(
            self,
            width: int = GlobalSettings._disp_res[0],
            height: int = GlobalSettings._disp_res[1],
            camera_name: str  = "",
            default_camera: bool = False
        ) -> None:
        super().__init__(
            camera_key = camera_name, 
            default_camera = default_camera
        )

        self.camera_run_setup = False

        self.vert_area = VertArea(
            width = width, 
            height = height
        )
        self.width = width
        self.height = height

        self.directions = Vector2(0,0)
        
        # World position the camera is focused on
        self.center = Vector2(0,0)
        self.topleft = Vector2(- self.width // 2, self.height // 2)

        # Pixel position on the display where the camera's center appears
        self.center_screen = Vector2(width//2, height//2)

        # Camera rotation (in radians)
        self.angle = 0.0

        self.frect = pygame.FRect(0, 0, self.vert_area.width, self.vert_area.height)
        self.target_entity = None


    def update_center(self, pos: tuple[float, float]) -> None:
        '''Set the world position the camera is focused on.'''
        self.center.x = pos[0]
        self.center.y = pos[1]
        self.topleft.x = pos[0] - self.width // 2
        self.topleft.y = pos[1] + self.height // 2


    def update_center_screen(self, pos: tuple[float, float]) -> None:
        '''Set the pixel position on the display where the camera's center appears.'''
        self.center_screen.x = pos[0]
        self.center_screen.y = pos[1]


    def set_angle(self, angle_rad: float) -> None:
        '''
        Set the camera rotation (in radians).
        '''
        self.angle = angle_rad


    def get_transform(self):
        '''
        Returns a function that transforms world coordinates to screen coordinates,
        applying translation and rotation around the camera center.
        '''
        def transform(world_pos: Vector2, center: bool = False) -> Vector2:
            # Translate so camera center is at (0,0), then rotate, then move to screen center
            rel = world_pos - self.center
            # Rotate by -self.angle (so world rotates opposite to camera)
            cos_a = cos(-self.angle)
            sin_a = sin(-self.angle)
            x = rel.x * cos_a - rel.y * sin_a
            y = rel.x * sin_a + rel.y * cos_a
            return (Vector2(x, y) + self.center_screen) if not center else self.center_screen
        return transform

    def update(self) -> None:
        ...

    def set_target(self, new_target_entity: Sprite) -> None: 
        self.target_entity = new_target_entity

class Camera_3d: 
    def __init__(self) -> None:
        ...