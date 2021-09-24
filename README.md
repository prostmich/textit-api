# TextIT API Client

This is an asynchronous __unofficial__ client library Python TextIT API for working with Russian texts from [Ego AI](http://ego-ai.tech).

This library is in beta testing. It means that critical errors and security issues may occur during operation, which may be fixed in the next updates.



## Installation

Install this library in a [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. virtualenv is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

### Mac/Linux

```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install git+https://github.com/prostmich/textit-api.git
```

### Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install git+https://github.com/prostmich/textit-api.git
```

## Supported Python Versions

Python 3.6, 3.7, 3.8, and 3.9 are fully supported. This library may work on later versions of 3, but I do not currently run tests against those versions.

## Unsupported Python Versions

Python < 3.6

## Example
Setting the word "ананас" to the dative plural

```Python
import asyncio
from textit import TextIT
from textit.types.word import WordCase, WordNumber


async def task():
    api = TextIT()
    response = await api.set_form(
        "ананас", case=WordCase.DATIVE, number=WordNumber.PLURAL
    )
    print(response.word)  # ананасам
    await api.session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(task())
```

Batch processing
```Python
import asyncio
from textit import TextIT
from textit.types.word import WordPart, WordNumber


async def task():
    api = TextIT()
    text = "яблоко, персик, груша"
    for word in text.split(", "):
        await api.set_form(
            word, part=WordPart.NOUN, number=WordNumber.PLURAL, immediately=False
        )
    responses = await api.send_request()
    result = ", ".join([response.word for response in responses])
    print(result)  # яблоки, персики, груши
    await api.session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(task())
```

## Documentation

You can find the official documentation on the [website](https://textit.ego-ai.tech/api/1.0/help) 

## Third Party Libraries and Dependencies

The following libraries will be installed when you install the client library:
* [aiohttp](https://github.com/aio-libs/aiohttp)

## Contributing
For technical issues particular to this module, please [report the issue](https://github.com/prostmich/textit-api/issues) on this GitHub repository.

New features, as well as bug fixes, by sending a pull request is always welcomed.

