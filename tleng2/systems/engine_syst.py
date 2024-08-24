from ..ecs import *
from ..components.engine import FpsComp
from ..engine.methods import EngineMethods
from ..engine.settings import GlobalSettings
# from ..engine.settings import GlobalSettings


class ClockTickSystem(System):
    def update(self):
        fps = GlobalSettings._fps
        if FpsComp in self.world.unique_components:
            fps = self.world.unique_components[FpsComp].fps
        
        EngineMethods.clock_tick_EP_dt(fps)
