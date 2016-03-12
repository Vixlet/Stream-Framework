from stream_framework.default_settings import *
try:
    from stream_framework.default_settings import *
    try:
        # ignore this if we already configured settings
        pass#settings.configure()
    except RuntimeError as e:
        pass
except Exception as e:
    raise e
