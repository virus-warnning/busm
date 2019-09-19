import time

import busm

@busm.through_email
def thefuck_one():
    print('Test Email')
    time.sleep(0)

@busm.through_telegram
def thefuck_two():
    print('Test Telegram')
    time.sleep(0)

@busm.through_line
def thefuck_three():
    print('Test Line')
    time.sleep(0)

@busm.through_telegram(subject='...')
def thefuck_four():
    print('Test Telegram')
    time.sleep(0)
    a = 1 / 0

if __name__ == '__main__':
    #thefuck_one()
    #thefuck_two()
    #thefuck_three()
    thefuck_four()
