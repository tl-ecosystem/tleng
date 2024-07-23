from ..ecs import *
from ..engine.properties import RendererProperties
from ..utils.debug import debug_print
from ..components.renderable import RenderableComp


class RendererSystem(System):
    """
    Experimental Renderer
    """
    def __init__(self, priority: int = 0) -> None:
        System.__init__(self, priority)
        self._display = None
        self._window = None


    def update(self) -> None:
        # debug_print(RendererProperties.render_calls,tags=['Renderer', 'Render_calls'])
        components = self.world.single_fast_query(
            RenderableComp
        )

        
        

        
        display = RendererProperties._display



        for call in RendererProperties.render_calls:
            renderable = call
            
            debug_print(renderable, tags=["Renderer"])

            if RendererProperties._local_default_camera != None:
                ...
            else:
                ...
        