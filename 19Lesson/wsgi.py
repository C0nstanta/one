from webshop.bot.main import start_bot
from webshop.api.client import app


app.run(port=5000, debug=True)
start_bot()
