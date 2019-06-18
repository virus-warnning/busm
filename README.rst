The package busm means bring up Samuel. It has some decorators to help you get
stdout of function execution through Email, Telegram and Line Notify.
"Bring up samuel" is from Holy Bible 1 Samuel 28:11.

套件 busm 是 "召喚撒母耳" 的意四，裡面有一組 decorators 可以幫你透過 Email, Telegram 和
Line Notify 等方式取得函數執行過程的 stdout 訊息。
召喚撒母耳這句話出自聖經撒母耳記上 28 章第 11 節，其實就是觀落陰的意思啦。

Quick Start
------------


.. code:: bash

    pip install busm


.. code:: python

    import busm

    @busm.through_email
    def foo_email():
        print('foo_email() executed.')

    @busm.through_telegram
    def foo_telegram():
        print('foo_telegram() executed.')

    @busm.through_line
    def foo_line():
        print('foo_line() executed.')

    if __name__ == '__main__':
        foo_email()
        foo_telegram()
        foo_line()

.. code:: bash

    python foo.py


~/.busm.json

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
