from models import (People,
                    Users)


def add_people():
    person = People(name='Léo', age='27')
    print(person)
    person.save()


def update_people():
    person = People.query.filter_by(name='Edson').first()
    person.age = 33
    person.save()


def delete_people():
    person = People.query.filter_by(name='Edson').first()
    person.delete()


def search():
    person = People.query.all()
    print(person)


def add_user(login, password, active):
    user = Users(login=login, password=password, active=active)
    user.save()


def get_all_users():
    users = Users.query.all()
    print(users)

def update_user():
    users = Users.query.filter_by(login='edson').first()
    users.active = True
    users.save()

if __name__ == '__main__':
    #add_user('edson', '1234', False)
    #update_user()
    get_all_users()
