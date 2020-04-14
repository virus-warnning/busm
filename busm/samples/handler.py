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
            cfg = yaml.load(f, Loader=yaml.SafeLoader)
    return cfg

def sample_yaml():
    cfg = load_config('busm/conf/logging.yaml')
    logging.config.dictConfig(cfg)
    logger = logging.getLogger('busm')

    # These two messages would be in the 1st bubble.
    logger.error('This is an error.')
    logger.warning('That is a warning.')
    time.sleep(1.5)

    # This message would be in the 2nd bubble with formatting.
    template = 'The %s is %dcm, which length is %.2f times than normal state.'
    logger.error(template, 'dick', 30, 1.67)
    time.sleep(1.5)

    # These two messages would be in the 1st bubble.
    logger.info('This message must be in 1st bubble.')
    logger.info('$')
    logger.info('This message must be in 2nd bubble.')
    logger.info('$')

if __name__ == '__main__':
    sample_yaml()
