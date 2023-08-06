
"""absTools package main.

Launch point for command line use.

Usage:
    python -m absTools

See package README for introduction.

"""


import absTools

import logging


logger = logging.getLogger('absTools')
"""Module logger."""


def main():
    logger.error("Command line use is not implemented yet, "
                 "import absTools package and use as a library")

    # raise SystemExit(1)


if __name__ == "__main__":
    logger.info("Starting absTools")

    try:
        main()

    except Exception as e:
        logger.critical(f"Unhandled exception: {e.__class__.__name__}", exc_info=True)
        raise SystemExit(2)

    except KeyboardInterrupt:
        logger.critical("Keyboard interrupt pressed")
        raise SystemExit(3)

    except SystemExit as e:
        logger.critical("Aborting absTools")
        raise e

    else:
        logger.info("absTools Finished")
        raise SystemExit(0)

    finally:
        logger.info("absTools Closed")
