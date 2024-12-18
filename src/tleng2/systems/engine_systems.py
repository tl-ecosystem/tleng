from ..ecs import *
from ..components.engine import FpsComp
from ..engine.methods import EngineMethods
from ..engine.settings import GlobalSettings
# from ..engine.settings import GlobalSettings


class ClockTickSystem(System):
    def parameters(self, world: World):
        self.world = world


    def update(self):
        fps = GlobalSettings._fps
        if FpsComp in self.world.resources:
            fps = self.world.resources[FpsComp].fps
        
        EngineMethods.clock_tick_EP_dt(fps)
