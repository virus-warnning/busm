import time

import fundog

@fundog.watch_by_email
def thefuck_one():
    print('Test Email')
    time.sleep(0)

@fundog.watch_by_telegram
def thefuck_two():
    print('Test Telegram')
    time.sleep(0)

@fundog.watch_by_line
def thefuck_three():
    print('Test Line')
    time.sleep(0)

if __name__ == '__main__':
    thefuck_one()
    thefuck_two()
    thefuck_three()
