import yaml
import pprint
import json
from django.core.management.base import BaseCommand

from ...schemas import SchemaGenerator


class Command(BaseCommand):
    help = "Generates Open API schema for project."

    def add_arguments(self, parser):
        parser.add_argument('--title', dest="title", default='', type=str)
        parser.add_argument('--url', dest="url", default=None, type=str)
        parser.add_argument('--description', dest="description", default=None, type=str)
        parser.add_argument('--urlconf', dest="urlconf", default=None, type=str)


    def handle(self, *args, **options):
        generator = SchemaGenerator(
            url=options['url'],
            title=options['title'],
            description=options['description'],
            urlconf=options['urlconf'],
        )

        schema = generator.get_schema()
        with open('schema.yaml', 'w') as yml:
            yaml.dump(schema, yml, allow_unicode=True)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(schema)
        # self.stdout.write(nice)
        # print(json.dumps(schema, indent=4, sort_keys=True))
        # self.stdout.write(schema)
        # renderer.render(schema)
        # print(output)
        # self.stdout.write(output.decode())
