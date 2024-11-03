from .world import World


class WorldsManager:
    """
    The ECS manager of tleng2
    """
    def __init__(self) -> None:
        self.worlds: dict[str, World] = {}
        self.current_world: str = ""

        self.cache_current_worlds_systems = []


    def load_worlds(self, **worlds: World) -> None: 
        self.worlds.update(worlds) 

    
    def change_world(self, new_world: str) -> None:
        self.current_world = new_world


    def run_current_world(self) -> None:
        self.worlds[self.current_world].run_schedule()

