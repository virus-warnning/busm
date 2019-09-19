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

version = '0.8.0'
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

def telegram_send_message(conf, summary, detail):
    message = '{}\n```\n{}\n```'.format(summary, detail)

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

def line_send_message(conf, summary, detail):
    message = '{}\n{}'.format(summary, detail)

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

def through_email(func=None, subject=''):
    """
    blah blah ...
    """

    state = {
        'begin': 0,
        'conf': {},
        'func_name': ''
    }

    def pre_task():
        state['conf'] = load_config('smtp')
        if state['conf'] is not None:
            state['begin'] = time.time()
            sys.stdout = io.StringIO()

    def post_task():
        if state['conf'] is not None:
            conf = state['conf']
            elapsed = time.time() - state['begin']
            sys.stdout.seek(0)
            outstr = sys.stdout.read().rstrip()
            sys.stdout.close()
            sys.stdout = sys.__stdout__

            # Compose email
            contents = re.sub(r'\s+\| ', '\n', '''
                | <p>STDOUT:</p>
                | <pre style="border:1px solid #aaa; border-radius:5px; background:#e7e7e7; padding:10px;">
                | {}
                | </pre>
                | <ul style="padding: 5px">
                | <li>Begin at: </li>
                | <li>End at: </li>
                | <li>Time elapsed: {:.2f}</li>
                | </ul>
                | <p style="color: #d0d0d0;">Sent by fundog {}</p>
                ''') \
                .format(outstr, elapsed, version)

            msg = MIMEText(contents, 'html', 'utf-8')
            if subject == '':
                msg['Subject'] = Header('Function {}() executed.'.format(state['func_name']))
            else:
                msg['Subject'] = Header(subject)
            msg['From'] = '{} <{}>'.format(Header(conf['from_name']).encode(), conf['from_email'])
            msg['To'] = '{} <{}>'.format(Header(conf['to_name']).encode(), conf['to_email'])
            smtp_message = msg.as_string()

            # Send email
            try:
                with smtplib.SMTP(conf['host'], conf['port'], timeout=30) as smtp:
                    smtp.set_debuglevel(2)
                    smtp.starttls()
                    smtp.login(conf['user'], conf['pass'])
                    smtp.sendmail(conf['from_email'], conf['to_email'], smtp_message)
            except Exception as ex:
                print('Failed to send email.')
                print(ex)

    def func_wrapper(*args):
        pre_task()
        fret = func(*args)
        state['func_name'] = func.__name__
        post_task()
        return fret

    def deco_wrapper(func):
        def func_wrapper(*args):
            pre_task()
            fret = func(*args)
            state['func_name'] = func.__name__
            post_task()
            return fret
        return func_wrapper

    return deco_wrapper if func is None else func_wrapper

def through_telegram(func=None, subject=''):
    """
    blah blah ...
    """

    state = {
        'begin': 0,
        'conf': None,
        'func_name': ''
    }

    def pre_task():
        state['conf'] = load_config('telegram')
        if state['conf'] is not None:
            state['begin'] = time.time()
            sys.stdout = io.StringIO()

    def post_task():
        if state['conf'] is not None:
            conf = state['conf']
            elapsed = time.time() - state['begin']
            sys.stdout.seek(0)
            outstr = sys.stdout.read().strip()
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            telegram_send_message(conf, subject, outstr)

    # @busm.through_telegram
    # def foo():
    #     ...
    def func_wrapper(*args):
        pre_task()
        fret = func(*args)
        state['func_name'] = func.__name__
        post_task()
        return fret

    # @busm.through_telegram(summary='Summary')
    # def foo():
    #     ...
    def deco_wrapper(func):
        def func_wrapper(*args):
            pre_task()
            fret = func(*args)
            state['func_name'] = func.__name__
            post_task()
            return fret

    return deco_wrapper if func is None else func_wrapper

def through_line(func=None, subject=''):
    """
    blah blah ...
    """

    state = {
        'begin': 0,
        'conf': None,
        'func_name': ''
    }

    def pre_task():
        state['conf'] = load_config('line')
        if state['conf'] is not None:
            state['begin'] = time.time()
            sys.stdout = io.StringIO()

    def post_task():
        if state['conf'] is not None:
            conf = state['conf']
            elapsed = time.time() - state['begin']
            sys.stdout.seek(0)
            outstr = sys.stdout.read().strip()
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            line_send_message(conf, subject, outstr)

    def func_wrapper(*args):
        pre_task()
        fret = func(*args)
        state['func_name'] = func.__name__
        post_task()
        return fret

    def deco_wrapper(func):
        def func_wrapper(*args):
            pre_task()
            fret = func(*args)
            state['func_name'] = func.__name__
            post_task()
            return fret
        return func_wrapper

    return deco_wrapper if func is None else func_wrapper

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
