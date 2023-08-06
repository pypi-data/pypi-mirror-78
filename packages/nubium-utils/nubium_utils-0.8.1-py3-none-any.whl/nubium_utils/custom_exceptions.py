
class NoMessageError(Exception):
    """
    No message was returned when consuming from the broker
    """
    pass


class NetworkError(Exception):
    """
    Generic network errors
    """
    pass


class ConsumeMessageError(Exception):
    """
    Non-trivial errors when consuming from the broker
    """
    pass


class MessageValueException(Exception):
    """
    Represents a significant error in the value of the message
    """
    pass


class ProduceHeadersException(Exception):
    """
    Represents a significant error in the value of the message
    """
    pass


class ProducerTimeoutFailure(Exception):
    """ Exception signifying a producer failing to communicate with the broker(s). """
    def __init__(self, *args):
        if not args:
            default_message = "Producer could not reach the broker(s) when attempting to send a message."
            args = (default_message,)
        super().__init__(*args)