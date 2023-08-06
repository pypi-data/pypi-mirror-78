
"""absTools package initialization.

See package README for introduction.

"""


from absTools.miscUtils import EnvInfo, set_package_logging, LogMode, set_package_multiprocessing


# Package Name
name = "absTools"


class absToolsError(Exception):
    """Base exception class for errors in this package."""


# Set logging mode
logger = set_package_logging(LogMode.DEV, __name__)
# logger = set_package_logging(LogMode.RELEASE, __name__)
# logger = set_package_logging(LogMode.LIB, __name__)
# logger = set_package_logging(LogMode.NONE, __name__)

logger.info("absTools Starting")

# Set multiprocessing support
# MP_SUPPORT, WORKER_COUNT = set_package_multiprocessing(mode='auto', workers='auto')
# MP_SUPPORT, WORKER_COUNT = set_package_multiprocessing(mode='disable')

# Log environment info
logger.debug(f"Run Environment:\n{EnvInfo.all()}")
