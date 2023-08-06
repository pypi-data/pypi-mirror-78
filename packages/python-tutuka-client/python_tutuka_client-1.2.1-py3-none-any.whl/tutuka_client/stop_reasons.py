from types import MappingProxyType

CARD_STOP_REASONS = MappingProxyType({
    'CARD_LOST': 1,
    'CARD_STOLEN': 2,
    'PENDING_QUERY': 3,
    'CARD_CONSOLIDATION': 4,
    'CARD_INACTIVE': 5,
    'PIN_TRIES_EXCEEDED': 6,
    'SUSPECTED_FRAUD': 7,
    'CARD_REPLACED': 8,
})
