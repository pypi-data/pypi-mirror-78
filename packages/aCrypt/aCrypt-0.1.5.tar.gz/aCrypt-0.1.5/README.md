# aCrypt
Ciphering made easy.

## Features
- Encode a string into numbers using a secret key
- Decode encoded strings into their original form using a secret key
- Generate a valid aCrypt key

## Usage
| Usage          | Params                   | Return Value      |
| :------------- | :----------------------- | :---------------- |
| `create_key()` | `None: None`             | `int: key`        |
| `cipher()`     | `str: message, int: key` | `str: ciphered`   |
| `decipher()`   | `str: message, int: key` | `str: deciphered` |

## Examples
Lets say you have private JSON data that you need to encode:
```python
# lets imagine this is the data
data = {
    "username": "ilovecats",
    "password": "meow123"
}
```

Of course though, writing this un-encoded data can be very unsafe. So the only way to protect it is to cipher it.
```python
from json import dumps, loads
from os import getenv

data = {
    "username": "ilovecats",
    "password": "meow123"
}

# turn the JSON into a string we can encode
data = dumps(data)

# using a key we can store in our environment variables, we can cipher it
encoded_data = cipher(data, os.getenv("CIPHER_KEY")) # you can also keep the key in a variable, thought this is unsafe as users can just use the key

# voila! The data has been ciphered:
print(encoded_data)
```

And to decipher the data and use it, you can do the reverse:

```python
from json import dumps, loads
from os import getenv

# decipher the data
decoded_data = decipher(encoded_data, os.getenv("CIPHER_KEY"))

# turn the string back into json data
data = loads(decoded_data)

# now you can use it!
print("Your username is" + data.username + "!")
```

## Credits
- Thank you to the repl.it community for providing such amazing services for free.
- Thank you to Atticus Kuhn for pointing out safety concerns on the project.
- Thank you to AmazingMech2418 (https://repl.it/@AmazingMech2418), for showing me the world of cryptography.
- Thank you StealthHydra179 (https://repl.it/@StealthHydra179), for being the only person who cared about programming in my school.
- Thank you Giothecoder (https://repl.it/@Giothecoder), for being there when I needed you most.


## Change Log
- 0.0.1 - Cipher was added, deciphering was unfinished
- 0.0.2 - Deciphering finished with lots of bugs
- 0.0.3 - Atticus Kuhn pointed out a safety bug, and thus it was patched
- 0.0.4 - Bugs fixes
- 0.0.5 - Added Credits
- 0.0.6 - AmazingMech2418 pointed out huge safety feature that should be added
- 0.0.7 - Bugs fixes
- 0.0.8 - Test Version
- 0.0.9 - Test Version
- 0.1.0 - Update 0.0.6 was revisited and implemented
- 0.1.1 - Added changelog
- 0.1.3 - Bug fixes
- 0.1.4 - Made key generation more efficient
- 0.1.5 - Added examples