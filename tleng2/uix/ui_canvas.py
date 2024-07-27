from .layout import BoxLayout
from ..ecs import *
from ..components.renderable import Renderable, RenderableComp


class UICanvas:
    def __init__(self, 
            *elements,
            layout=BoxLayout('VERTICAL'),
            theme=...
        ) -> None:
        """
        layout: stores the elements,
                stores the position of the elements
        """
        self.layout = layout
        self.theme = theme
        self.elements_types: set = set()

        for element in elements:
            self.elements_types.add(type(element))

        self.layout.append_widgets(*elements)


class UICanvasSystem(System):
    """
    Draws the UI to the window 
    """
    def update(self):
        ui_canvas = self.world.fast_query(
            UICanvas,
            RenderableComp
        )






