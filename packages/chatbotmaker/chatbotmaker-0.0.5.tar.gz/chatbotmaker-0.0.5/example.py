# app imports
from flask import Flask, request
from chatbotmaker import Bot, Dispatcher, Database
from chatbotmaker.defaults.facebook import FacebookMessenger, facebook_route


dispatcher_config = {
    'actions': {
        'welcome': {
            'func': lambda user, user_input: (
                user.send_message('Im in welcome state'),
                user.change_state('home')
            )
        },
        'home': {
            'func': lambda user, user_input: (
                user.send_message('Im in home state'),
                user.change_state('welcome')
            )
        },
    }
}
FACEBOOK_CHECK_TOKEN = 'VERIFY_TOKEN'
FACEBOOK_AUTH_TOKEN = 'EAAKnsCzlM7wBAM0waYVmDwMFMg1s6GMDoDCXSV1ZADQ9xxhzonZAKhHmJ8TZBhN58IKd9cUlAprdc1lBPFhXmRQTmBv8aNZAq6ko2wVTwF0xxOKDkwrD2iRKeQEVzjCk2J6eNAfCzkD2uQ4rGv96QwZC24p8sZC2GrS4uv25WNgQZDZD'
messenger = FacebookMessenger(FACEBOOK_AUTH_TOKEN)
dispatcher = Dispatcher(dispatcher_config)
database = Database({'sqlalchemy.url': 'sqlite:///foo.db'})
bot = Bot({}, messenger, dispatcher, database)
app = Flask(__name__)


@app.route('/bot', methods=['GET', 'POST'])
def ngn_bot():
    return facebook_route(request, FACEBOOK_CHECK_TOKEN, bot)


@app.route('/bot_debug', methods=['GET'])
def ngn_bot_debug():
    if request.method == 'GET':
        user_id = request.args.get("user")
        user_input = request.args.get("message")
        return bot.user_handle(user_id, user_input)
    return "Message ignored"


app.run()
