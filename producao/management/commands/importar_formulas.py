# producao/management/commands/importar_formulas.py

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from producao.models import FormulaQuimica, ComponenteFormula
from producao.models_erp import Ftc01, Ftc02

class Command(BaseCommand):
    help = 'Importa ou atualiza as Fórmulas Químicas e seus Componentes do banco de dados do ERP (acedata).'

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Ponto de entrada principal para o comando.
        Executa a importação dos cabeçalhos e depois dos componentes.
        """
        self.stdout.write(self.style.SUCCESS('--- Iniciando a importação de Fórmulas Químicas ---'))

        formulas_criadas, formulas_atualizadas = self.importar_cabecalhos()
        componentes_criados, componentes_atualizados, componentes_ignorados = self.importar_componentes()

        self.stdout.write(self.style.SUCCESS('\n--- Resumo da Importação ---'))
        self.stdout.write(f'Fórmulas (Cabeçalhos) Criadas: {formulas_criadas}')
        self.stdout.write(f'Fórmulas (Cabeçalhos) Atualizadas: {formulas_atualizadas}')
        self.stdout.write(f'Componentes Criados: {componentes_criados}')
        self.stdout.write(f'Componentes Atualizados: {componentes_atualizados}')
        if componentes_ignorados > 0:
            self.stdout.write(self.style.WARNING(f'Componentes Ignorados (Fórmula não encontrada): {componentes_ignorados}'))
        self.stdout.write(self.style.SUCCESS('--- Importação concluída com sucesso! ---'))

    def importar_cabecalhos(self):
        """
        Importa os dados da tabela Ftc01 do ERP para o modelo FormulaQuimica.
        Esta função já está correta e não precisa de alterações.
        """
        self.stdout.write("\n1. Importando cabeçalhos das fórmulas (FTC01)...")
        criadas = 0
        atualizadas = 0
        db_alias = 'acedata'

        formulas_erp = Ftc01.objects.using(db_alias).all()

        for formula_erp in formulas_erp:
            codigo_formula_limpo = str(formula_erp.ftcacod).strip()
            if not codigo_formula_limpo:
                continue

            obj, created = FormulaQuimica.objects.update_or_create(
                codigo_formula=codigo_formula_limpo,
                defaults={
                    'nome_formula': str(formula_erp.ftcanom).strip(),
                    
                }
            )
            if created:
                criadas += 1
            else:
                atualizadas += 1
        
        self.stdout.write(self.style.SUCCESS(f"   -> Concluído: {criadas} criadas, {atualizadas} atualizadas."))
        return criadas, atualizadas

    def importar_componentes(self):
        """
        Importa os dados da tabela Ftc02 do ERP para o modelo ComponenteFormula.
        """
        self.stdout.write("\n2. Importando componentes das fórmulas (FTC02)...")
        criados = 0
        atualizados = 0
        ignorados = 0
        db_alias = 'acedata'

        # Otimização: Carrega todas as fórmulas locais para a memória de uma só vez
        self.stdout.write("   - Carregando mapa de fórmulas locais...")
        formulas_locais_map = {f.codigo_formula: f for f in FormulaQuimica.objects.all()}
        self.stdout.write(f"   - {len(formulas_locais_map)} fórmulas encontradas localmente.")

        # Busca todos os componentes do ERP
        componentes_erp = Ftc02.objects.using(db_alias).all()
        self.stdout.write(f"   - Processando {len(componentes_erp)} componentes do ERP...")

        for comp_erp in componentes_erp:
            codigo_formula_erp = str(comp_erp.ftcacod).strip()
            
            # Busca a fórmula no mapa em memória
            formula_local = formulas_locais_map.get(codigo_formula_erp)

            if formula_local:
                componente_codigo_limpo = str(comp_erp.ftcprocod).strip()
                
                # Garante que temos os dados mínimos necessários
                if not componente_codigo_limpo:
                    continue

                # --- CORREÇÃO APLICADA AQUI ---
                # A chave de identificação única de um componente é a combinação da fórmula
                # e do código do próprio componente, conforme a restrição `unique_together` do modelo.
                obj, created = ComponenteFormula.objects.update_or_create(
                    formula=formula_local,
                    componente_codigo=componente_codigo_limpo, # Usa o código do componente como parte da chave
                    defaults={
                        'item_sequencia': comp_erp.ftcbitm,
                        'componente_qtd_base': comp_erp.ftcqtd
                    }
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1
            else:
                # Se a fórmula não existe no mapa, ignora o componente
                ignorados += 1

        self.stdout.write(self.style.SUCCESS(f"   -> Concluído: {criados} criados, {atualizados} atualizados, {ignorados} ignorados."))
        return criados, atualizados, ignorados