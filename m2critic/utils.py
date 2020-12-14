"""

    m2critic.utils
    ~~~~~~~~~~~~~~~

    Utility functions.

    @author: z33k

"""
import random
import sys
import time
from typing import Union


def getdelay(base=1.5, offset=0.5) -> Union[float, int]:
    """Get random delay based on provided number.

    Keyword Arguments:
        base {float/int} -- a number to base randomizing on (default: {1.5})
        offset {float/int} -- randomizing offset (default: {1.5})
    """
    if type(base) is float and type(offset) is float:
        delay = random.uniform(base - offset, base + offset)
    elif type(base) is int and type(offset) is int:
        delay = random.randint(base - offset, base + offset)
    else:
        raise ValueError("Excpected both arguments either of type 'int' or type 'float'. "
                         + f" Got base: {type(base)}, offset: {type(offset)}")
    return delay


def countdown(secondscount: int) -> None:
    """Display countdouwn on stdout.

    Taken from:
    https://stackoverflow.com/questions/17220128/display-a-countdown-for-the-python-sleep-function

    Arguments:
        secondscount {int} -- seconds to count down
    """
    for remaining in range(secondscount, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:4d} {} remaining".format(remaining,
                                                     "second" if remaining == 1 else "seconds"))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rComplete!               \n")


def percentage(nominator: int, denominator: int, precision: int) -> str:
    """Get percentage string

    Arguments:
        nominator {int} -- a nominator
        denominator {int} -- a denominator
        precision {int} -- precision

    Returns:
        str -- percentage string
    """
    percent = round(float(nominator) / denominator * 100, precision)
    format_string = f"{{:.{precision}f}} %"
    return format_string.format(percent)
