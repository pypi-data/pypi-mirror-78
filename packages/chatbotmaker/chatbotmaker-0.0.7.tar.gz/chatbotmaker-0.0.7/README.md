# ChatBotMaker

This project aims to automate plateform messaging where the plateform support
message forwarding.

## Description

This module is based around a bot class in which you inject the necessary code
/ objects:
- Messenger (An object that sends message or event back)
- Dispatcher (An object that contains all the logic rule)
- Database (An object that allows database interaction)

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
    'handle\_name': {  
        'enter_func': lambda user: user.send\_message('Hi there every time'),  
        'pref_func': lambda user: user.send\_message('Hi there'),  
        'func': lambda user, user\_input: user.change\_state('home'),  
        'post_func': lambda user: user.send\_message('You are redirected'),  
    },  
    'home': {  
        'pref_func': lambda user: user.send\_message('Welcome back!'),  
        'func': 'lambda user, user\_input: user.change\_state(user\_input)',  
    },  
    'input': {  
        'func': 'lambda user, user\_input: (  
                    user.store\_argument('input', user\_input),  
                    user.change\_state('home'),  
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
** \_\_init\_\_(self, config, env=None) ** . This generally are locals() or
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
database. You can postpone the database creation using create\_database=False),
add your own ORM classes using the database.base attribute and construct the
database using database.create_database().


## Usage

### Default components
To avoid re-inventing the wheel, some "common" components have already been
coded. They are in chatbotmaker.default.

#### Facebook
- FacebookMessenger(authentication\_token)
- facebook\_route(request, facebook\_check\_token, bot)
  - this flask routing should be called directly from the routing point

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
