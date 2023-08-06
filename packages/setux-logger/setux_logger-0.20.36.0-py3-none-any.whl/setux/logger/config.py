config = {
    'formatters': {
        'stdout': {
            'format': '%(message)s'
        },
        'short': {
            'datefmt': '%H:%M',
            'format': '%(asctime)s %(levelname)-7s %(message)s'
        },
        'full': {
            'datefmt': '%H:%M:%S',
            'format': '%(levelno)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'debug': {
            'class': 'logging.FileHandler',
            'filename': '/data/log/setux_debug.log',
            'formatter': 'full',
            'level': 'DEBUG',
            'mode': 'w'
        },
        'info': {
            'class': 'logging.FileHandler',
            'filename': '/data/log/setux_info.log',
            'formatter': 'short',
            'level': 'INFO',
            'mode': 'w'
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'stdout',
            'level': 'INFO'
        },
        'root': {
            'class': 'logging.FileHandler',
            'filename': '/data/log/setux_root.log',
            'formatter': 'short',
            'level': 'ERROR',
            'mode': 'w'
        },
    },
    'loggers': {
        'setux': {
            'handlers': ['debug', 'info', 'stdout'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
    'root': {
        'handlers': ['root'], 'level': 'NOTSET'
    },
    'version': 1,
    'disable_existing_loggers': True,
 }
