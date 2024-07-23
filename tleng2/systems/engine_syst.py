from ..ecs import *
from ..components.engine_comp import FpsComp
from ..engine.methods import EngineMethods
# from ..engine.settings import GlobalSettings


class ClockTickSystem(System):
    def update(self):
        components = self.world.single_fast_query(
            FpsComp
        )

        EngineMethods.clock_tick_EP_dt(components[0][1].fps)