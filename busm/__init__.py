"""
blah blah ...
"""

from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime
import io
import json
import logging
import os
import re
import shutil
import smtplib
import sys
import time
import threading

import requests

VERSION = '0.8.0'
hinted = False

def load_config(channel):
    global hinted

    conf_path = os.path.expanduser('~/.busm.json')
    if not os.path.isfile(conf_path):
        tmpl_path = os.path.dirname(__file__) + '/conf/busm.json'
        shutil.copy(tmpl_path, conf_path)

    with open(conf_path, 'r') as f_conf:
        conf = json.load(f_conf)[channel]
        if channel == 'smtp' and \
           conf['from_email'] != 'someone@gmail.com':
            return conf
        if channel == 'telegram' and \
           conf['token'] != '123456789:-----------------------------------':
            return conf
        if channel == 'line' and conf['token'] != '':
            return conf

    if not hinted:
        print('-' * 65)
        print('  Please change fundog config file (~/.busm.json) to enable.')
        print('-' * 65)
        os.system('open -t ~/.busm.json') # TODO: Limit Darwin only.
        hinted = True

def gl_pre_task(state):
    state['conf'] = load_config(state['channel'])
    if state['conf'] is not None:
        state['begin'] = time.time()
        sys.stdout = io.StringIO()

def gl_post_task(state):
    if state['conf'] is not None:
        # Retrive stdout.
        sys.stdout.seek(0)
        state['stdout'] = sys.stdout.read().strip()
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        # Retrive execution time.
        state['elapsed'] = time.time() - state['begin']

        # Default subject
        if state['subject'] == '':
            state['subject'] = '{}() executed.'.format(state['func'].__name__)

        # Send to target channel
        if state['channel'] == 'telegram':
            telegram_send_message(state['conf'], state['subject'], state['stdout'], state['elapsed'])
        elif state['channel'] == 'line':
            line_send_message(state['conf'], state['subject'], state['stdout'], state['elapsed'])
        elif state['channel'] == 'smtp':
            smtp_send_message(state['conf'], state['subject'], state['stdout'], state['elapsed'], state['debug'])

def telegram_send_message(conf, subject, detail, extime=-1):
    if extime == -1:
        message = '*{}*\n```\n{}\n```'.format(subject, detail)
    else:
        message = '*{}* ({:.2f}s)\n```\n{}\n```'.format(subject, extime, detail)

    api = 'https://api.telegram.org/bot{}/sendMessage'.format(conf['token'])
    params = {
        'chat_id': conf['master'],
        'text': message,
        'parse_mode': 'markdown',
        'disable_web_page_preview': False
    }

    sent = False
    retry = -1
    while not sent and retry < 3:
        resp = requests.post(api, data=params)
        if resp.status_code != 200:
            retry += 1
        else:
            sent = True

def line_send_message(conf, subject, detail, extime=-1):
    if extime == -1:
        message = '{}\n{}'.format(subject, detail)
    else:
        message = '{} ({:.2f}s)\n{}'.format(subject, extime, detail)

    api = 'https://notify-api.line.me/api/notify'
    params = {
        'message': message
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(conf['token'])
    }

    sent = False
    retry = -1
    while not sent and retry < 3:
        resp = requests.post(api, data=params, headers=headers)
        if resp.status_code != 200:
            retry += 1
        else:
            sent = True

def smtp_send_message(conf, subject, detail, extime=-1, debug=False):
    # Compose email
    if extime == -1:
        contents = re.sub(r'\s+\| ', '\n', '''
            | <p>STDOUT:</p>
            | <pre style="border:1px solid #aaa; border-radius:5px; background:#e7e7e7; padding:10px;">
            | {}
            | </pre>
            | <p style="color: #d0d0d0;">Sent by busm {}</p>
            ''') \
            .format(detail, VERSION)
    else:
        contents = re.sub(r'\s+\| ', '\n', '''
            | <p>STDOUT:</p>
            | <pre style="border:1px solid #aaa; border-radius:5px; background:#e7e7e7; padding:10px;">
            | {}
            | </pre>
            | <ul style="padding: 5px">
            | <li>Execution time: {:.2f}</li>
            | </ul>
            | <p style="color: #d0d0d0;">Sent by busm {}</p>
            ''') \
            .format(detail, extime, VERSION)

    msg = MIMEText(contents, 'html', 'utf-8')
    msg['Subject'] = Header(subject)
    msg['From'] = '{} <{}>'.format(Header(conf['from_name']).encode(), conf['from_email'])
    msg['To'] = '{} <{}>'.format(Header(conf['to_name']).encode(), conf['to_email'])
    smtp_message = msg.as_string()

    # Send email
    try:
        with smtplib.SMTP(conf['host'], conf['port'], timeout=30) as smtp:
            if debug == True:
                smtp.set_debuglevel(2)
            smtp.starttls()
            smtp.login(conf['user'], conf['pass'])
            smtp.sendmail(conf['from_email'], conf['to_email'], smtp_message)
    except Exception as ex:
        print('Failed to send email.')
        print(ex)

def through_smtp(func=None, subject='', debug=False):
    """
    @busm.through_smtp
    """

    state = {
        'begin': 0,
        'conf': None,
        'func': None,
        'subject': subject,
        'debug': debug,
        'channel': 'smtp'
    }

    # @busm.through_smtp
    def func_wrapper(*args):
        nonlocal state
        gl_pre_task(state)
        try:
            fret = state['func'](*args)
        except Exception as ex:
            print(ex)
            fret = None
        gl_post_task(state)
        return fret

    # @busm.through_smtp(subject='...')
    def deco_wrapper(func):
        nonlocal state
        state['func'] = func
        return func_wrapper

    if callable(func):
        state['func'] = func
        return func_wrapper
    else:
        return deco_wrapper

    return deco_wrapper if func is None else func_wrapper

def through_telegram(func=None, subject=''):
    """
    @busm.through_telegram
    """

    state = {
        'begin': 0,
        'conf': None,
        'func': None,
        'subject': subject,
        'channel': 'telegram'
    }

    # @busm.through_telegram
    def func_wrapper(*args):
        nonlocal state
        gl_pre_task(state)
        try:
            fret = state['func'](*args)
        except Exception as ex:
            print(ex)
            fret = None
        gl_post_task(state)
        return fret

    # @busm.through_telegram(subject='...')
    def deco_wrapper(func):
        nonlocal state
        state['func'] = func
        return func_wrapper

    if callable(func):
        state['func'] = func
        return func_wrapper
    else:
        return deco_wrapper

def through_line(func=None, subject=''):
    """
    @busm.through_line
    """

    state = {
        'begin': 0,
        'conf': None,
        'func': None,
        'subject': subject,
        'channel': 'line'
    }

    # @busm.through_line
    def func_wrapper(*args):
        nonlocal state
        gl_pre_task(state)
        try:
            fret = state['func'](*args)
        except Exception as ex:
            print(ex)
            fret = None
        gl_post_task(state)
        return fret

    # @busm.through_line(subject='...')
    def deco_wrapper(func):
        nonlocal state
        state['func'] = func
        return func_wrapper

    if callable(func):
        state['func'] = func
        return func_wrapper
    else:
        return deco_wrapper

class TelegramHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.conf = load_config('telegram')
        self.collected = ''
        self.last_logging = -1
        self.send_later = None
        self.lock = threading.Lock()

    def handle(self, record):
        detail = '\n[%s] %s\nAt: %s:%d\nMessage: %s' % (
            datetime.now().strftime('%H:%M:%S'),
            record.levelname,
            record.filename,
            record.lineno,
            record.msg
        )
        t = time.time()
        threading.Thread(target=self.append, args=(t,detail)).start()

    def append(self, timing, detail):
        with self.lock:
            self.last_logging = timing
            self.collected += detail
            if self.send_later is None:
                self.send_later = threading.Thread(target=self.send)
                self.send_later.start()

    def send(self):
        secs_ago = time.time() - self.last_logging
        while secs_ago < 1:
            time.sleep(1 - secs_ago)
            secs_ago = time.time() - self.last_logging

        with self.lock:
            telegram_send_message(self.conf, '', self.collected.strip())
            self.collected = ''
            self.last_logging = -1
            self.send_later = None
