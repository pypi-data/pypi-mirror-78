LVL2H = (
    object(),  # ~ reserved for unused level
    'Error',
    'Warning',
    'Info',
    'Debug-info'
)

LVL2MSG = (
    object(),  # ~ reserved for unused level
    '🔥 **ERROR** in',
    '⚠️ **Warning** in',
    'ℹ️ **Info** from',
    'Debug-info from',
)

LVL_ALIAS = {
    '1': 1, 'error': 1, 'err': 1, 'e': 1,
    '2': 2, 'warning': 2, 'warn': 2, 'w': 2,
    '3': 3, 'info': 3, 'i': 3,
    '4': 4, 'debug': 4, 'd': 4,
}
