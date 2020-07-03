from webshop.bot.main import start_bot, app


if __name__ == "__main__":
    start_bot()
    app.run(port=5000, debug=True)
