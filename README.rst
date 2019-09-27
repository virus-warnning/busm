The package busm means bring up Samuel. It's allusion comes from Holy Bible 1 Samuel 28:11.
It help you find abnormal situations in a background process.

There are several function decorators and logging handlers inside.
These tools can send message of abnormal situations through Email, Telegram or Line Notify.

套件 busm 是 "召喚撒母耳" 的意思，典故出自聖經撒母耳記上 28 章第 11 節，其實就是觀落陰的意思。
這套件可以幫你找出背景作業的異常狀況。

裡面有一些 function decorators 和 logging handlers, 用這些工具可以把異常狀況透過
Email, Telegram, Line Notify 這些方式送出去。

Quick Start
------------

First, install the package.

.. code:: bash

    pip install busm

Then add decorators before functions you'd like to monitor.

.. code:: python

    import busm

    @busm.through_smtp
    def foo_email():
        print('It sucks!')

    @busm.through_telegram
    def foo_telegram():
        print('Segmentation fault.')

    @busm.through_line
    def foo_line():
        print('Stack overflow.')

    if __name__ == '__main__':
        foo_email()
        foo_telegram()
        foo_line()`


Run your python code.

.. code:: bash

    python foo.py

You must see the following message,
and a config file will be generated in HOME directory.

.. code:: text

    -----------------------------------------------------------------
      Please change fundog config file (~/.busm.json) to enable.
    -----------------------------------------------------------------

Edit this config file ~/.busm.json to fit for you.

.. code:: json

    {
      "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "user": "someone",
        "pass": "********",
        "from_name": "Foo",
        "from_email": "someone@gmail.com",
        "to_name": "Master",
        "to_email": "someone@gmail.com"
      },
      "telegram": {
        "token": "123456789:-----------------------------------",
        "master": "123456789"
      },
      "line-notify": {
        "token": ""
      }
    }

Run your python code again.

.. code:: bash

    python foo.py

Tada!

Visit [here](https://github.com/virus-warnning/busm/wiki) to learn more.
