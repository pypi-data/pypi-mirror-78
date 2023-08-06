from random import randint
from re import findall

def create_key():
    key = ""
    for i in range(50):
        key = key + str(randint(1,9))
    return key

def cipher(message,key):
    if "0" in key:
        raise InvalidKey("Key must be type string with 50 integers and must not contain 0.")
    if not isinstance(key, str):
        raise InvalidKey("Key must be type string with 50 integers and must not contain 0. ")

    if len(key) != 50:
        raise InvalidKey("Key must be type string with 50 integers and must not contain 0.  ")

    key = [i for i in key]
    x = []
    for letter in message:
        letter = str(ord(letter))
        x.append(letter)
    message = x

    ki = 0
    oi = 1
    y = oi

    for i in range(len(message)):
        if not oi:
            message[i] = str(int(message[i]) + int(key[ki]))
        else:
            message[i] = str(int(message[i]) - int(key[ki]))
        ki = ki + 1
        oi = oi + 1

        if ki + 1 == len(key):
            ki = 0
        if oi > 1:
            oi = 0

    x = []
    for letter in message:
        if len(letter) == 1:
            letter = "00" + letter
        elif len(letter) == 2:
            letter = "0" + letter
        x.append(letter)

    message = "".join(x)
    return str(y) + str(message)


def decipher(code,key):
    if not isinstance(key, str):
        raise InvalidCode("Key received was corrupted.")

    if len(key) != 50:
        raise InvalidCode("Key received was corrupted.")

    if str(code[0]) != "0" and str(code[0]) != "1":
        raise InvalidCode("Code received was corrupted.")

    y = code[0]
    code = code[1:]
    origin = code
    code = findall("...",code)

    if "".join(code) != origin:
        raise InvalidCode("Code received was corrupted.")

    key = [i for i in key]
    y = y
    ki = 0
    for i in range(len(code)):
        if not str(y) == "1":
            code[i] = chr(
                    int(int(code[i]) - int(key[ki]))
                )
        else:
            code[i] = chr(
                    int(int(code[i]) + int(key[ki]))
                )
        ki = int(ki) + 1
        y = int(y) + 1

        if ki + 1 == len(key):
            ki = 0
        if y > 1:
            y = 0
    return "".join(code)
    
def a_credits():
    print("\
=== Credits ==\n\
Thank you to the repl.it community for providing such amazing services for free.\n\
Thank you to Atticus Kuhn for pointing out safety concerns on the project.\n\
Thank you to AmazingMech2418 (https://repl.it/@AmazingMech2418), for showing me the world of cryptography.\n\
Thank you StealthHydra179 (https://repl.it/@StealthHydra179), for being the only person who cared about programming in my school.\n\
Thank you Giothecoder (https://repl.it/@Giothecoder), for being there when I needed you most.")

def changelog():
    print("=== ChangeLog ===\
0.0.1 - Cipher was added, deciphering was unfinished\
0.0.2 - Deciphering finished with lots of bugs\
0.0.3 - Atticus Kuhn pointed out a safety bug, and thus it was patched\
0.0.4 - Bugs fixes\
0.0.5 - Added Credits\
0.0.6 - AmazingMech2418 pointed out huge safety feature that should be added\
0.0.7 - Bugs fixes\
0.0.8 - Test Version\
0.0.9 - Test Version\
0.1.0 - Update 0.0.6 was revisited and implemented\
0.1.1 - Added changelog\
0.1.3 - Bug fixes\
0.1.4 - Made key generation more efficient")

class InvalidKey(Exception):
    pass

class InvalidCode(Exception):
    pass