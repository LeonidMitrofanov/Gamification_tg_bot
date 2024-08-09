class TribeNotFoundError(Exception):
    """Exception raised when a tribe is not found in the database."""
    def __init__(self, tribe_id: int):
        self.tribe_id = tribe_id
        self.message = f"Tribe with ID {tribe_id} not found."
        super().__init__(self.message)