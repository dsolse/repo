class Photo:
    def __init__(self, url: str, desc: str) -> None:
        self.url = url
        self.desc = desc


class PhotoNext:
    def __init__(self, url: str, name: str, id: int):
        self.url = url
        self.name = name
        self.id = id
