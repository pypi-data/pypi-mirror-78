# iot.io Client
### iot.io Overview
This project aims to create a lightweight and intuitive system for connecting
IoT devices to a central server for small IoT system implementations and hobbyists.

The framework focuses on providing easy to use system of libraries so the end user does
not need to understand the protocol implementation, though this also is fairly simple.

The format of the framework is somewhat reminiscent of [Socket.IO](https://socket.io/) 
where handlers functions are defined and executed and run as events are triggered.


### Quickstart Guide (Client)
This is an example of a simple IoTClient instance which connects to a server accepting
"echo" clients ping the server every 5 seconds with a message and print the server's response.

```python
from iotio_client import IoTClient
import asyncio
import logging


# create an instance of our client
client = IoTClient("test_client", "echo", {}, logging_level=logging.DEBUG)


# define a handler for the server's response
@client.on("message")
async def test(message):
    print(message)


# define a coroutine for pinging the server at a 5 second interval
async def ping():
    # wait until the client is ready before sending a message
    await client.wait_until_ready()

    while True:
        await client.send("message", "hello")
        await asyncio.sleep(5)


# initialize the client and ping coroutine
if __name__ == "__main__":
    # run the coroutine
    client.loop.create_task(ping())

    # run the client
    client.run("localhost:5000")
```

If you would like to see the matching quickstart guide for an example
server go [here](https://github.com/dylancrockett/iot.io).

