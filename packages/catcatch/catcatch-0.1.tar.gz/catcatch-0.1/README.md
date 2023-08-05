**catcatch**

This module will help you catch exceptions in python3

**Installation**

`pip install catcatch`

**Usage**

Add @catcatch.catch decorator to your function

Example:

`@catcatch.catch`

`def function():`

`    return 1 / 0`

`print(function())  # ZeroDivisionError: division by zero`

`print(function().name)  # ZeroDivisionError`

`print(function().text)  # division by zero`
