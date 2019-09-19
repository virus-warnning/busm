import time
import busm

@busm.through_smtp
def smtp_normal1():
    time.sleep(0.1)
    print('Call smtp_normal1().')

@busm.through_smtp(subject='It\'s a busm test.')
def smtp_normal2():
    time.sleep(0.1)
    print('Call smtp_normal2().')

@busm.through_smtp
def smtp_exception():
    time.sleep(0.1)
    print('Call smtp_exception().')
    n = 1 / 0

@busm.through_smtp(debug=True)
def smtp_debug():
    time.sleep(0.1)
    print('Call smtp_debug().')

@busm.through_line
def line_normal1():
    time.sleep(0.1)
    print('Call line_normal1().')

@busm.through_line(subject='It\'s a busm test.')
def line_normal2():
    time.sleep(0.1)
    print('Call line_normal2().')

@busm.through_line
def line_exception():
    time.sleep(0.1)
    print('Call line_exception().')
    n = 1 / 0

@busm.through_telegram
def telegram_normal1():
    time.sleep(0.1)
    print('Call telegram_normal1().')

@busm.through_telegram(subject='It\'s a busm test.')
def telegram_normal2():
    time.sleep(0.1)
    print('Call telegram_normal2().')

@busm.through_telegram
def telegram_exception():
    time.sleep(0.1)
    print('Call telegram_exception().')
    a = 1 / 0

if __name__ == '__main__':
    smtp_normal1()
    smtp_normal2()
    smtp_exception()
    smtp_debug()
    line_normal1()
    line_normal2()
    line_exception()
    telegram_normal1()
    telegram_normal2()
    telegram_exception()
