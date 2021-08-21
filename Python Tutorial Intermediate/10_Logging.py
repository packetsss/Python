import logging
'''logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %H:%M:%S")'''

'''logging.debug("This is a debug message")
logging.info("This is a info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")'''
# different messages in logging

logger = logging.getLogger(__name__)
'''logger.info("Hello from logging")'''
# lock the name of info to the file name

'''logger.propagate = False'''
# stop propagating the info while importing

logger = logging.getLogger(__name__)
stream_h = logging.StreamHandler()
file_h = logging.FileHandler("file.log")

stream_h.setLevel(logging.WARNING)
file_h.setLevel(logging.ERROR)

formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
stream_h.setFormatter(formatter)
file_h.setFormatter(formatter)

logger.addHandler(stream_h)
logger.addHandler(file_h)

'''logger.warning("Warning 1")
logger.error("Error 1")'''
# way to define logger handler

'''try:
    a = [1, 2, 3]
    val = a[4]
except IndexError as e:
    logging.error(e, exc_info=True)'''
# helpful for troubleshooting, traceback

'''import traceback
try:
    a = [1, 2, 3]
    val = a[4]
except:
    logging.error("the error is %s", traceback.format_exc())'''
# same thing

