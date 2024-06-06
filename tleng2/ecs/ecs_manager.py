from .world import World


class WorldsManager:
    """
    The ECS manager of tleng2
    """
    def __init__(self) -> None:
        self.scenes: list[World] = []

