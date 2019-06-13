import time

import fundog

@fundog.watch_by_email
def thefuck_one():
    print('The fuck #1')
    time.sleep(0)

@fundog.watch_by_email(subject='The fuck #2 is done.')
def thefuck_two():
    print('The fuck #2')
    time.sleep(0)

if __name__ == '__main__':
    thefuck_one()
    thefuck_two()
