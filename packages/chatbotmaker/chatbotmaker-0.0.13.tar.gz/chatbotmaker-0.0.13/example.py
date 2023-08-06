# app imports
from flask import Flask, request
from chatbotmaker import Bot, Dispatcher, Database
from chatbotmaker.defaults.dev import DevMessenger
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
FACEBOOK_AUTH_TOKEN = 'some_token'
messenger = FacebookMessenger(FACEBOOK_AUTH_TOKEN)
# SINCE token is fake, lets use a dev-messenger (terminal printing)
messenger = DevMessenger()
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
