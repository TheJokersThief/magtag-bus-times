class Trip:
    def __init__(
        self,
        trip_id: str,
        route: str,
        route_type: str,
        headsign: str,
        direction: str,
        stop_id: str,
        dueTime: str,
        dueInSeconds: int,
        source: str,
    ) -> None:
        self.trip_id = trip_id
        self.route = route
        self.route_type = route_type
        self.headsign = headsign
        self.direction = direction
        self.stop_id = stop_id
        self.dueTime = dueTime
        self.dueInSeconds = dueInSeconds
        self.source = source

    def __str__(self) -> str:
        mins = self.dueInSeconds // 60
        secs = self.dueInSeconds - (mins * 60)
        return f"{self.route} {self.dueTime} ({mins}min {secs}sec) [{self.source}]"
