from dataclasses import dataclass


@dataclass
class Trip:
    trip_id: str
    route: str
    route_type: str
    headsign: str
    direction: str
    stop_id: str
    dueTime: str
    dueInSeconds: int
    source: str

    def __str__(self) -> str:
        mins = self.dueInSeconds // 60
        secs = self.dueInSeconds - (mins * 60)
        return f"{self.route} {self.dueTime} ({mins}min {secs}sec) [{self.source}]"
