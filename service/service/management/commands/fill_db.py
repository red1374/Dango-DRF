import os
import json

from django.core.management.base import BaseCommand
from collections import defaultdict

from authors.models import Author
from users.models import Users

JSON_PATH = 'service\json'


def load_from_json(file_name):
    path_to_file = os.path.join(JSON_PATH, file_name + '.json')
    with open(path_to_file, 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_list = load_from_json('users')
        if not users_list:
            print('Empty "users.json" file!')
            return False

        Users.objects.all().delete()

        for user in users_list:
            Users.objects.create(**user)

        authors = load_from_json('authors')
        if not authors:
            print('Empty "authors.json" file!')
            return False

        Author.objects.all().delete()
        for new_author in authors:
            Author.objects.create(**new_author)

        if not Users.objects.filter(username='django'):
            Users.objects.create_superuser('django', 'support@pleshakov.org', 'geekbrains')
