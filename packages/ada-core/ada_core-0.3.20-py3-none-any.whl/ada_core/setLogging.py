import logging, logging.config
import yaml
import os


class AdaLoggingConfig(object):

    FULL_CONF_YAML_TEST = """
            version: 1
            disable_existing_loggers: False
            formatters:
                simple:
                    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    datefmt: '%Y-%m-%d %H:%M:%S'
            handlers:
                console:
                    class: logging.StreamHandler
                    level: DEBUG
                    formatter: simple
                    stream: ext://sys.stdout
                file:
                    class: logging.handlers.RotatingFileHandler
                    level: DEBUG
                    formatter: simple
                    filename: ada_core.log
                    maxBytes: 2097
                    backupCount: 2
            loggers:
                ada_core:
                    level: DEBUG
                    handlers: [console, file]
                    propagate: True
    """

    FULL_CONF_YAML = """
            version: 1
            disable_existing_loggers: False
            formatters:
                simple:
                    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    datefmt: '%Y-%m-%d %H:%M:%S'
            handlers:
                console:
                    class: logging.StreamHandler
                    level: DEBUG
                    formatter: simple
                    stream: ext://sys.stdout
                file:
                    class: logging.handlers.RotatingFileHandler
                    level: DEBUG
                    formatter: simple
                    filename: ada_core.log
                    maxBytes: 20976
            loggers:
                ada_core:
                    level: WARNING
                    handlers: [console]
                    propagate: True
    """

    CONSOLE_CONF_YAML = """
            version: 1
            disable_existing_loggers: False
            formatters:
                simple:
                    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    datefmt: '%Y-%m-%d %H:%M:%S'
            handlers:
                console:
                    class: logging.StreamHandler
                    level: DEBUG
                    formatter: simple
                    stream: ext://sys.stdout
            root:
                level: WARNING
                handlers: [console]
    """

    DEFAULT_LEVEL = logging.WARNING

    @ staticmethod
    def setLogConfig():
        try:
            try:
                log_dir = os.getcwd()
                logConfig = yaml.load(AdaLoggingConfig.FULL_CONF_YAML)
                logConfig["handlers"]["file"]["filename"] = os.path.join(log_dir, logConfig["handlers"]["file"]["filename"])

            except BaseException:
                logConfig = yaml.load(AdaLoggingConfig.CONSOLE_CONF_YAML)

            logging.config.dictConfig(logConfig)

        except BaseException:
            logging.basicConfig(level=AdaLoggingConfig.DEFAULT_LEVEL)

        # finally:
        #     logger = logging.getLogger(name)
        #     logger.info("The logging config for ada_core has setup, logger name started with 'ada_core.' will be taken")
        # return logger


    # @ staticmethod
    # def setLogConfig(name):
    #     try:
    #         try:
    #             log_dir = os.getcwd()
    #             logConfig = yaml.load(AdaLoggingConfig.FULL_CONF_YAML)
    #             logConfig["handlers"]["file"]["filename"] = os.path.join(log_dir, logConfig["handlers"]["file"]["filename"])
    #
    #         except BaseException:
    #             logConfig = yaml.load(AdaLoggingConfig.CONSOLE_CONF_YAML)
    #
    #         logging.config.dictConfig(logConfig)
    #
    #     except BaseException:
    #         logging.basicConfig(level=AdaLoggingConfig.DEFAULT_LEVEL)
    #
    #     finally:
    #         logger = logging.getLogger(__name__)
    #         logger.info("The logging config for ada_core has setup, logger name started with 'ada_core.' will be taken")
    #     return logger
