from dataclasses import dataclass, field


def iter_id():
    prefix = "p_"
    i = 0
    while True:
        yield f"{prefix}{i}"
        i += 1


all_portables = {}


@dataclass
class Portable:
    weight: float
    name: str = field(default=None)

    def __post_init__(self):
        if self.name is None:
            self.name = next(iter_id())
        if self.name in all_portables:
            raise ValueError(f"Portable id {self.name} already exists")
        all_portables[self.name] = self


def get_portable(name: str) -> Portable:
    return all_portables[name]


def del_portable(name: str):
    del all_portables[name]
