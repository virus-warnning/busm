import logging
import logging.config
import time
import sys
import json
import os
import threading
import yaml
import busm

def load_config(config_path):
    cfg = { 'version': 1.0 }

    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            if config_path.endswith('yaml'):
                cfg = yaml.load(f, Loader=yaml.SafeLoader)
            if config_path.endswith('json'):
                cfg = json.load(f)

    return cfg

def by_yaml():
    cfg = load_config('busm/conf/logging.yaml')
    logging.config.dictConfig(cfg)
    logger = logging.getLogger('busm')
    # These two messages would be sent in a code block.
    logger.error('This is an error. [by_yaml()]')
    logger.warning('That is a warning. [by_yaml()]')
    time.sleep(1.5)
    # These two messages would be sent in another code block.
    logger.error('This is another error. [by_yaml()]')
    logger.warning('That is another warning. [by_yaml()]')

def by_json():
    cfg = load_config('busm/conf/logging.json')
    logging.config.dictConfig(cfg)
    logger = logging.getLogger('busm')
    # These two messages would be sent in a code block.
    logger.error('This is an error. [by_json()]')
    logger.warning('That is a warning. [by_json()]')
    time.sleep(1.5)
    # These two messages would be sent in another code block.
    logger.error('This is another error. [by_json()]')
    logger.warning('That is another warning. [by_json()]')

def programmatically():
    tlh = busm.TelegramHandler()
    logger = logging.getLogger()
    logger.addHandler(tlh)
    # These two messages would be sent in a code block.
    logger.error('This is an error. [programmatically()]')
    logger.warning('That is a warning. [programmatically()]')
    time.sleep(1)
    # These two messages would be sent in another code block.
    logger.error('This is another error. [programmatically()]')
    logger.warning('That is another warning. [programmatically()]')
    logger.removeHandler(tlh)

def main():
    programmatically()
    time.sleep(1.5)
    by_json()
    time.sleep(1.5)
    by_yaml()

if __name__ == '__main__':
    main()
