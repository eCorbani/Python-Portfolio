from sqlalchemy import (create_engine,
                        Column,
                        Integer,
                        String,
                        Boolean,
                        ForeignKey,
                        CheckConstraint,
                        text)
from sqlalchemy.orm import (scoped_session,
                            sessionmaker,
                            relationship,
                            declarative_base)

engine = create_engine('sqlite:///tasks.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True, nullable=False)
    age = Column(Integer)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def __repr__(self):
        return f'<ID {self.id}> -- <Person {self.name}> -- <Age {self.age}>'


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    status = Column(String(20), CheckConstraint('status IN ("todo", "doing", "done")'))
    name = Column(String(80))
    people_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('People')

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20))
    active = Column(Boolean)

    def __repr__(self):
        return f'User: "{self.login} Active: {self.active}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
