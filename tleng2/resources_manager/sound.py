from os import path 

class Sound:
    def __init__(self, sound_path: str) -> None:
        self.sound = path.join(sound_path)