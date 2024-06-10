from .system import System


class Schedule:
    """
    Something like a system manager.
    """
    def __init__(self) -> None:
        self.system_schedule: list[System] = []
    

    def add_systems(self, *systems) -> None: 
        for system in systems:
            self.system_schedule.append(system)
        
        self.system_schedule.sort(key=lambda syst: syst.priority, reverse=True)

    
    def init_systems(self, world) -> None:
        for system in self.system_schedule:
            system.change_world(world)


    def update(self) -> None:
        for system in self.system_schedule:
            system.update()