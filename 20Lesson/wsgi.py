from webshop.bot.main import start_bot, app


start_bot()
app.run(port=5000, debug=True)
