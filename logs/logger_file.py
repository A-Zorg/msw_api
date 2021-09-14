import logging


class LogGen:
    @staticmethod
    def loggen():
        # logging.basicConfig(level=logging.INFO)
        # logging.getLogger('telethon').setLevel(logging.CRITICAL)
        logging.basicConfig(
            filename="./logs/automation.log",
            level=logging.ERROR,
            format='%(asctime)s: %(levelname)s: %(message)s: %(filename)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)

        return logger


# def logger_config():
#     logging.basicConfig(level=logging.INFO)
#     logging.getLogger('telethon').setLevel(logging.CRITICAL)
#     return LogGen.loggen()
