from enum import StrEnum, auto

class OrderStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    CANCELLED = auto()


ALLOWED_STATUS_TRANSITIONS = {

    OrderStatus.PENDING: [
        OrderStatus.CANCELLED,
        OrderStatus.PROCESSING
    ],

    OrderStatus.PROCESSING: [
        OrderStatus.COMPLETED,
        OrderStatus.CANCELLED
    ],

    OrderStatus.COMPLETED: [
    ],

    OrderStatus.CANCELLED: [
    ]
}
