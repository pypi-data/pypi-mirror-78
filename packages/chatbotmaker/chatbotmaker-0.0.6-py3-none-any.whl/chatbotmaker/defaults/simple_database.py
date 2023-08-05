""" SimpleDatabase class file"""
from . import Column, Integer, String, relationship, ForeignKey,\
              declarative_base, engine_from_config, sessionmaker

class SimpleDatabase:
    """ Database representation and basic user management """

    def __init__(self, config):
        self.config = config
        self.base = declarative_base()
        # Define default tables/classes here
        self.init_default_tables()
        self.engine = engine_from_config(self.config)
        # Create database if not exists here
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

    def init_default_tables(self):
        """ Initializes the default databases """
        class User(self.base):
            """ User class """
            __tablename__ = 'users'

            id = Column(Integer, primary_key=True)
            fb_id = Column(String)
            state = Column(String)
            # Arguments (One to Many)
            arguments = relationship('Argument', back_populates='user',
                                     lazy='dynamic')

            def __init__(self, fb_id, state):
                self.fb_id = fb_id
                self.state = state

            def __repr__(self):
                return f'User: {self.fb_id}'

        self.user_class = User

        class Argument(self.base):
            """ Argument class """
            __tablename__ = 'arguments'

            id = Column(Integer, primary_key=True)
            name = Column(String)
            value = Column(String)
            # User 1-Many relationship
            user_id = Column(Integer, ForeignKey('users.id'))
            user = relationship('User', uselist=False,
                                back_populates='arguments')

        self.argument_class = Argument
