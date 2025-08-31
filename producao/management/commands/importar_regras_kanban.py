from django.core.management.base import BaseCommand
from producao.models import RegraKanban

# Cole a lista completa de artigos e materiais aqui.
# Exemplo com alguns itens:
KANBAN_DATA = [
    {'artigo': '10.004', 'material': 'PEROLADO'},
    {'artigo': '10.005', 'material': 'PEROLADO'},
    {'artigo': '10.023', 'material': 'PEROLADO'},
    {'artigo': '10.035', 'material': 'PEROLADO'},
    {'artigo': '10.082', 'material': 'CRISTAL'},
    # ... adicione todos os outros 180+ itens aqui
]

class Command(BaseCommand):
    help = 'Popula a tabela RegraKanban com os dados iniciais de artigo/material.'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando a importação de regras do Kanban...')
        regras_criadas = 0
        regras_existentes = 0

        for item in KANBAN_DATA:
            _, created = RegraKanban.objects.get_or_create(
                artigo=item['artigo'].strip(),
                material=item['material'].strip().upper()
            )
            if created:
                regras_criadas += 1
            else:
                regras_existentes += 1

        self.stdout.write(self.style.SUCCESS(f'\nImportação concluída!'))
        self.stdout.write(f'{regras_criadas} novas regras foram criadas.')
        self.stdout.write(f'{regras_existentes} regras já existiam.')