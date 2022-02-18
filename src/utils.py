import random
import string


def random_string(length=(10, 30), letters=True, numbers=True):
    """
    Return random string

    :param length: length to randint from
    :param letters: attach letter in output
    :param numbers: attach number in output
    :return: string object ~ 'asdfg53423qfe'
    """
    output = ''
    if letters:
        output += string.ascii_letters
    if numbers:
        output += string.digits
    return ''.join(random.choice(output) for _ in range(random.randint(length[0], length[1])))
