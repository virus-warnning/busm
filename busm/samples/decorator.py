import time
import busm

EXECUTION_TIME = 0.13

@busm.through_smtp
def smtp_sample():
    time.sleep(EXECUTION_TIME)
    print('Call smtp_sample().')

@busm.through_line
def line_sample():
    time.sleep(EXECUTION_TIME)
    print('Call line_sample().')

@busm.through_telegram
def telegram_sample1():
    time.sleep(EXECUTION_TIME)
    print('Call telegram_sample().')

@busm.through_telegram(subject='Message with subject.')
def telegram_sample2():
    time.sleep(EXECUTION_TIME)
    print('Call telegram_sample2().')

@busm.through_telegram
def telegram_exception():
    time.sleep(EXECUTION_TIME)
    print('Call telegram_exception().')
    a = 1 / 0

if __name__ == '__main__':
    smtp_sample()
    line_sample()
    telegram_sample1()
    telegram_sample2()
    telegram_exception()
