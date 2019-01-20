class Task():
    """docstring for Task."""
    def __init__(self, title, driver_id, vehicle_id, start_time, estimated_end_time, destination, status):
        self.title = title
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.start_time = start_time
        self.estimated_end_time = estimated_end_time
        self.destination = destination
        self.status = status

    def getDict(self):
        return {'title': self.title, 'driver_id': self.driver_id,
        'vehicle_id': self.vehicle_id, 'start_time': self.start_time,
        'estimated_end_time': self.estimated_end_time, 'destination': self.destination,
        'status': self.status}
