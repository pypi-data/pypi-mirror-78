# ChatBotMaker

This project aims to automate plateform messaging where the plateform support
message forwarding.

## Description

This module is based around a bot class in which you inject the necessary code
/ objects:
- Messenger (An object that sends message or event back)
- Dispatcher (An object that contains all the logic rule)
- Database (An object that allows database interaction)

## General Idea

User are in **states** and define what action should be executed.

A state is composed of 3 event and 1 input event (or main event):
- func(user, user\_input): **main** function called with the user's input
- enter\_func(user): called **every** time before the user sends text in its
current state
- pre\_func(user): called when entering a state (ie. during change\_state)
- post\_func(user): called when exiting a state (ie. during change\_state)

![Internal shema](img/inner_shema.png)

### Components

#### Messenger

You can create your own messenger class that should inherit the
**chatbotmaker.Messenger** class.  
It must implement a send(user\_id: str, message:str)
method and can implement other optional methods.

#### Dispatcher

The dispatcher recieves your config as a dictionnary in the following format:

<pre>
{  
  'actions': {  
    'handle_name': {  
        'enter_func': lambda user: user.send_message('Hi there every time'),  
        'pref_func': lambda user: user.send_message('Hi there'),  
        'func': lambda user, user_input: user.change_state('home'),  
        'post_func': lambda user: user.send_message('You are redirected'),  
    },  
    'home': {  
        'pref_func': lambda user: user.send_message('Welcome back!'),  
        'func': 'lambda user, user_input: user.change_state(user_input)',  
    },  
    'input': {  
        'func': 'lambda user, user_input: (  
                    user.store_argument('input', user_input),  
                    user.change_state('home'),  
                )',  
    },  
    'help': Dispatcher.DEFAULT,
  }  
}
</pre>

###### DEFAULT

You can associate function by their name to make the binding process easier.
You must name your functions with {key}\_{handle\_name} (eg: func\_help,
pre\_func\_help, post\_func\_help). You then must pass the binding table
dictionary to the Dispatcher constructor alongside the config
**\_\_init\_\_(self, config, env=None)** . This generally are locals() or
globals().

###### How does it work?

The user is the orm User class to whom we add some method (redirect failing
attribute calls):
- send\_message(message: str)
- change\_state(state: str)
- get\_argument(name: str)
- store\_argument(name: str, value: str)
- self.messenger, self.dispatcher, self.database (the one onjected in the bot)


#### Database

The given database database follows the following architecture:
- users:
  - id = Column(Integer, primary\_key=True)
  - fb\_id = Column(String)
  - state = Column(String)
  - arguments = relationship('Argument', back\_populates='user', lazy='dynamic')
- arguments:
  - id = Column(Integer, primary\_key=True)
  - name = Column(String)
  - value = Column(String)
  - user\_id = Column(Integer, ForeignKey('users.id'))
  - user = relationship('User', uselist=False, back\_populates='arguments')

The database expects a config (sqlachemy.config) object to initialize the
database. You can postpone the database creation using create\_database=False,
add your own ORM classes using the database.base attribute and construct the
database using database.create_database().

###### Custom tables / ORM classes

You can add custom tables (thus ORM classes) by potponing the final creation of
the database (ie create_database=False) and using the database **base** object
to identify your custom tables.

In case you want to create relationships with default classes, it is possible.
You can input in the database constructor **user_rs** and **arg_rs**, list of
tuple (name, relationship_object).


## Usage

### Default components
To avoid re-inventing the wheel, some "common" components have already been
coded. They are in chatbotmaker.default.

#### Facebook
- FacebookMessenger(authentication\_token)
- facebook\_route(request, facebook\_check\_token, bot)
  - this flask routing should be called directly from the routing function

#### Dev

We have the dev file containing:
- DevMessenger()  # prints everythin in console

## Installation

Using PIP since its a pip module repository:
``` bash
42sh$ : pip install chatbotmaker
```

## Contributing

Do no hesitate to make a pull request or launch a discussion. I am looking
foreward to expand the default capabilites.

## Authors and acknowledgment

Author:
> Dominique MICHEL <dominique.michel@epita.fr>

## Status

The project has reached its first final phase. Now there will be:
- need to think about the design and facilitate user-database integration
  - Good work done here, maybe allow any orm engiine ine the future
- need of tests (why not make a CI pipeline)
  - tests must tests more the content of the calls
  - github ci pipeline is so confusing coming from gitlab :o

Once the backend is functional and robust, i aim to make a frontend plateform
to allow non-programming people to create bots too.
