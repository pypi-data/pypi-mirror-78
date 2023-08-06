name = "ada_core"


from ada_core.setLogging import AdaLoggingConfig


AdaLoggingConfig.setLogConfig()

import logging

logger = logging.getLogger(__name__)

logger.info("The logging config for ada_core has setup, logger name started with 'ada_core.' will be taken")