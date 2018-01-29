from faker import Faker
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','User_MTV.settings')

import django
# Import settings
django.setup()
from User_App.models import User

fakegen = Faker()


def populate(N = 5):
    for entry in range(N):

        fake_first_name = fakegen.first_name()
        fake_last_name = fakegen.last_name()
        fake_email = fakegen.email()

        user = User.objects.get_or_create(first_name = fake_first_name, last_name = fake_last_name, email = fake_email)[0]


if __name__ == '__main__':
    print('Populating User List')
    populate(30)
    print('Done Populating!')
