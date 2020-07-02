from webshop.bot.main import app, start_bot

if __name__ == '__main__':
    start_bot()
    app.run(port=5000, debug=True)