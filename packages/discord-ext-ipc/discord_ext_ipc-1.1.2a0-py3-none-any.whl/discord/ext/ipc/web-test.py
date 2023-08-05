# WEB SERVER FILE
from quart import Quart
from client import Client

app = Quart(__name__)
web_ipc = Client(secret_key="my_auth_token")

@app.route("/")
async def show_guilds():
    guild_count = await app.ipc_node.request("get_guild_count") # Make a request to get the bot's IPC get_guild_count route.

    return str(guild_count) # return the data sent to us.

@app.before_first_request
async def before():
    app.ipc_node = await web_ipc.discover() # discover IPC Servers on your network

if __name__ == "__main__":
    app.run()