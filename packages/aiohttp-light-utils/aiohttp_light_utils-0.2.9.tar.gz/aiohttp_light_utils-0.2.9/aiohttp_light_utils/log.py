import logging
from pythonjsonlogger import jsonlogger


format_str = '%(message)%(levelname)%(levelno)%(name)%(asctime)'


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['status'] = record.levelname


def get_logger():
    json_handler = logging.StreamHandler()

    formatter = CustomJsonFormatter(format_str)
    json_handler.setFormatter(formatter)

    return json_handler
