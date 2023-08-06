# Jarvis 

[![Build status](https://dev.azure.com/cubbei/JarvisCore/_apis/build/status/JarvisCore-PiP%20Publish)](https://dev.azure.com/cubbei/JarvisCore/_build/latest?definitionId=1)
[![PyPI version](https://badge.fury.io/py/jarviscore@2x.svg)](https://badge.fury.io/py/jarviscore)


This is the repository for the JarvisCore framework used to run the Jarvis the twitch bot.
You are welcome to use this library to build your own bot for twitch, please note that there is currently minimal documentation which does tend to make things a little tricky.

You are welcome to join the "[Looking for Jarvis](https://jarvis.bot/discord)" Discord server for updates and to join the community.

## Getting Started

The simplest way to get started is to create a new file, with the basic code below:

```python
from jarviscore.client import Client

jarvis = Client(nick="yourbotsname", 
    token="yourbotstoken",
    channels=["a list", "of channels", "to connect to"])
jarvis.start()
```

As an alternative, better practice would be to make use of a config file to store your settings and loading them into the bot when you start.  
Use the following code for your bot as a starter.
```python
from jarviscore.client import Client
from jarviscore import Settings

setting = Settings()

jarvis = Client(nick=setting.get_setting("nick"), 
    token=setting.get_setting("token"),
    channels=setting.get_setting("channels"))
jarvis.start()
```
Next, create a file called `config.json` and use the following template to get started
```json
{
    "name": "yourbotsname",
    "token": "yourbotstoken",
    "channels": [
        "a list", "of channels", "to connect to"
    ]
}
```
If you prefer, you may use a `config.yaml` file instead.

## Custom Modules

You can create your own custom modules and interactions for your bot using the Jarvis Core. 
Create a folder called `modules` in the same location as your bot file like so,
```
+-- root
|   |-- bot.py
|   |-- config.json
|   +-- modules
|       |-- module1.py
|       |-- module2.py
```

Then, copy the following boiler plate text to get started. This example implements a simple ping module.  
**Note:** All modules need to implement `setup()` and `teardown()`, both take `channel` as a parameter.

```python
from jarviscore import Module, Log
from jarviscore import CommandMessage

log = Log("Module:Ping", verbose="log")
class Ping(Module):

    def __init__(self, channel):
        Module.__init__(self, "Ping")
        self.channel = channel
    
    def on_command(self, data: CommandMessage):
        if "ping" == data.KEYWORD:
            self.channel.send("pong")


def setup(channel):
    channel.load_module(Ping(channel))
    log.log(f"Loaded Module Ping")

def teardown(channel):
    log.log(f"Removed Module Ping")

```