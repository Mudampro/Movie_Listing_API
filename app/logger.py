import logging
import logging.handlers



PAPERTRAIL_HOST = 'logs2.papertrailapp.com'
PAPERTRAIL_PORT = 42044

handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[handler]
)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger



# logger.debug("This message will be recorded.")
# logger.info("This message will be recorded.")
# logger.warning("This message will be recorded.")
# logger.error("This message will be recorded.")
# logger.critical("This message will be recorded.")