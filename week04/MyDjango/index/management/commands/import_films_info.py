import csv
from django.core.management import BaseCommand
from index.models import Films

class Command(BaseCommand):
    help = '从csv文件中导入电影星级和评级信息'
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
    
    def handle(self, *args, **options):
        path = options['path']
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                films = Films.objects.create(
                    stars = row[0], 
                    comments = row[1],
                )
        # print(films)