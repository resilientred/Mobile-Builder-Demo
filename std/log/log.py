import logging


def configure_release(mask: str, filename: str):
    logging.basicConfig(format=mask,
                        level=logging.INFO,
                        filename=filename)


def configure_debug(mask: str):
    logging.basicConfig(format=mask,
                        level=logging.DEBUG)
