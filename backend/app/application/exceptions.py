class CustomerNotFoundError(Exception):
    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(
            f"Customer '{customer_id}' was not found."
        )