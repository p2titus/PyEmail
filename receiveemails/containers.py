class ID:
    id: int


class Account:
    local: str
    domain: str


class Email:
    id: ID
    sender: Account
    receivers: [(ID, Account)]
    subject: str
    body: str
    from_this: bool
