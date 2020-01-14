from django.core.management.base import BaseCommand
from ...schemas import SchemaGenerator


class Command(BaseCommand):
    help = "Generates Open API schema for project."

    def add_arguments(self, parser):
        parser.add_argument('--title', dest="title", default='', type=str)
        parser.add_argument('--url', dest="url", default=None, type=str)
        parser.add_argument('--description', dest="description", default=None, type=str)
        parser.add_argument('--format', dest="format", choices=['openapi', 'openapi-json'], default='openapi', type=str)
        parser.add_argument('--urlconf', dest="urlconf", default=None, type=str)
        parser.add_argument('--generator_class', dest="generator_class", default=None, type=str)

    def handle(self, *args, **options):
        generator = SchemaGenerator(
            url=options['url'],
            title=options['title'],
            description=options['description'],
            urlconf=options['urlconf'],
        )

        # renderer = OpenAPIRenderer
        schema = generator.get_schema(request=None, public=True)
        print('schema', schema)
        # output = renderer.render(schema, renderer_context={})
        # self.stdout.write(output.decode())
