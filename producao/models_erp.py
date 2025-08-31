# models_erp.py (VERSÃO FINAL, COMPLETA E CORRIGIDA)

from django.db import models

class Emb01(models.Model):
    """ Mapeia a tabela de Embalagens do ERP """
    embcod = models.CharField(primary_key=True, max_length=50, db_column='EmbCod')
    embnom = models.CharField(max_length=255, db_column='EmbNom')
    
    class Meta:
        managed = False
        db_table = 'emb01'

    def __str__(self):
        return self.embnom

class Ter01(models.Model):
    """ Terceiros (Clientes) - Refatorado para incluir mais detalhes """
    terdoc = models.CharField(primary_key=True, max_length=50, db_column='TerDoc', help_text="Código do Cliente no ERP")
    ternom = models.CharField(max_length=255, db_column='TerNom', help_text="Nome Fantasia")
    
    # --- NOVOS CAMPOS ADICIONADOS ---
    terraz = models.CharField(max_length=255, db_column='TerRaz', blank=True, null=True, help_text="Razão Social")
    tercpf = models.CharField(max_length=20, db_column='TerCpf', blank=True, null=True, help_text="CPF ou CNPJ")
    tercepfat = models.CharField(max_length=10, db_column='TerCepFat', blank=True, null=True, help_text="CEP de Faturamento")
    terfon1 = models.CharField(max_length=20, db_column='TerFon1', blank=True, null=True, help_text="Telefone Principal")
    terema = models.CharField(max_length=255, db_column='TerEma', blank=True, null=True, help_text="E-mail Principal")
    tercidcodf = models.CharField(max_length=50, db_column='tercidcodf', blank=True, null=True, help_text="Código da Cidade")

    class Meta:
        managed = False
        db_table = 'ter01'

    def __str__(self):
        return self.ternom

class Rep01(models.Model):
    """ Representantes """
    repdoc = models.CharField(primary_key=True, max_length=50, db_column='RepDoc')
    repnom = models.CharField(max_length=255, db_column='RepNom')
    
    class Meta:
        managed = False
        db_table = 'rep01'

    def __str__(self):
        return self.repnom

class Cid01(models.Model):
    """ Cidades """
    cidcod = models.CharField(primary_key=True, max_length=50, db_column='CidCod')
    cidnom = models.CharField(max_length=255, db_column='CidNom')
    estcod = models.CharField(max_length=2, db_column='EstCod')
    
    class Meta:
        managed = False
        db_table = 'cid01'

    def __str__(self):
        return f"{self.cidnom} - {self.estcod}"

class Opr01(models.Model):
    opracod = models.CharField(primary_key=True, max_length=50, db_column='opracod')
    opraempcod = models.CharField(max_length=10, db_column='opraempcod')
    opraprocod = models.CharField(max_length=50, db_column='opraprocod')
    opranom = models.CharField(max_length=255, db_column='opranom')
    opraagr = models.CharField(max_length=50, db_column='OprAAgr', blank=True, null=True, help_text="Código de Agrupamento")
    opradatemi = models.DateTimeField(db_column='OprADatEmi', null=True, blank=True, help_text="Data de Emissão da OP no ERP")
    oprapesjt = models.DecimalField(max_digits=19, decimal_places=4, db_column='OPRAPESCJT', null=True, blank=True, help_text="Peso da Placa")
    opraqtdcjt = models.DecimalField(max_digits=19, decimal_places=4, db_column='OPRAQTDCJT', null=True, blank=True, help_text="Qtde Placas")
    oprapesprv = models.DecimalField(max_digits=19, decimal_places=4, db_column='OPRAPESPRV', null=True, blank=True, help_text="Peso Previsto")
    opraqtdped = models.DecimalField(max_digits=19, decimal_places=4, db_column='opraqtdped')
    opraqtdprv = models.DecimalField(max_digits=19, decimal_places=4, db_column='opraqtdprv')
    opragddcod1 = models.CharField(max_length=50, db_column='opragddcod1')
    opragddcod2 = models.CharField(max_length=50, db_column='opragddcod2')
    opragddcod3 = models.CharField(max_length=50, db_column='opragddcod3')
    oprauniest = models.CharField(max_length=10, db_column='oprauniest')
    opraftmcod = models.CharField(max_length=50, db_column='opraftmcod')

    class Meta:
        managed = False
        db_table = 'opr01'


class Ftm01(models.Model):
    ftmacod = models.CharField(primary_key=True, max_length=50, db_column='ftmacod')
    ftmanom = models.CharField(max_length=255, db_column='ftmanom')
    ftmacam = models.IntegerField(db_column='FtmACam', null=True, blank=True, help_text="Número de Camadas")
    ftmamtgcod = models.CharField(max_length=50, db_column='FtmAMtgCod', blank=True, null=True, help_text="Código do Grupo de Material")
    ftmateqcod = models.CharField(max_length=50, db_column='FtmATeqCod', blank=True, null=True, help_text="Código do Equipamento")
    ftmateqemp = models.CharField(max_length=10, db_column='FtmATeqEmp', blank=True, null=True, help_text="Código da Empresa do Equipamento")

    class Meta:
        managed = False
        db_table = 'ftm01'


class Ftm02(models.Model):
    ftmacod = models.CharField(primary_key=True, max_length=50, db_column='ftmacod')
    ftmdtam = models.CharField(max_length=50, db_column='ftmdtam')
    ftmdespbru = models.DecimalField(max_digits=19, decimal_places=4, db_column='ftmdespbru')
    ftmdespaca = models.DecimalField(max_digits=19, decimal_places=4, db_column='ftmdespaca')
    ftmdren = models.DecimalField(max_digits=19, decimal_places=4, db_column='FtmDRen')
    ftmdapr = models.DecimalField(max_digits=19, decimal_places=4, db_column='FtmDApr')

    class Meta:
        managed = False
        db_table = 'ftm02'
        unique_together = (('ftmacod', 'ftmdtam'),)


class Ftm05(models.Model):
    ftmacod = models.CharField(primary_key=True, max_length=50, db_column='FtmACod')
    ftmbitm = models.IntegerField(db_column='FtmBItm', help_text="Número do Item / Camada")
    ftmbpor = models.DecimalField(max_digits=19, decimal_places=4, db_column='FtmBPor')
    ftmbfix = models.CharField(max_length=1, db_column='FtmBFix')

    class Meta:
        managed = False
        db_table = 'ftm05'
        unique_together = (('ftmacod', 'ftmbitm'),)


class Pdv02(models.Model):
    pdvempcod = models.CharField(max_length=10, db_column='pdvempcod')
    pdvcod = models.CharField(max_length=50, db_column='pdvcod')
    pdvoprcod = models.CharField(primary_key=True, max_length=50, db_column='pdvoprcod')
    pdvprocod = models.CharField(max_length=50, db_column='pdvprocod')
    pdvnompro = models.CharField(max_length=255, db_column='pdvnompro')
    pdvunicod = models.CharField(max_length=10, db_column='pdvunicod')
    pdvitmpro = models.CharField(max_length=10, db_column='pdvitmpro')
    pdvgddcod1 = models.CharField(max_length=50, db_column='pdvgddcod1')
    pdvgddcod2 = models.CharField(max_length=50, db_column='pdvgddcod2')
    pdvgddcod3 = models.CharField(max_length=50, db_column='pdvgddcod3')
    pdvterpro = models.CharField(max_length=50, db_column='pdvterpro')
    pdvoprobs = models.CharField(max_length=255, db_column='pdvBoprobs', blank=True, null=True)
    pdvqtdpro = models.DecimalField(max_digits=19, decimal_places=4, db_column='pdvqtdpro')
    pdvboriproqtd = models.DecimalField(max_digits=19, decimal_places=4, db_column='PdvBOriProQtd', help_text="Quantidade Original do Pedido")
    pdvpedcli = models.CharField(max_length=50, db_column='PdvPedCli', null=True, blank=True, help_text="Número do pedido do cliente (Ex: 006/25)")
    pdvtotitm = models.DecimalField(max_digits=19, decimal_places=4, db_column='pdvtotitm')
    pdvprvent = models.DateField(db_column='pdvprvent', null=True, blank=True, help_text="Data Previsão de Entrega")
    pdvprcven = models.DecimalField(max_digits=19, decimal_places=4, db_column='PdvPrcVen', null=True, blank=True)
    pdvemipro = models.DateField(db_column='pdvemipro', null=True, blank=True, help_text="Data de Emissão do Pedido")
    observacao_item = models.TextField(db_column='PdvBOprObs', blank=True, null=True, help_text="Observação do item no pedido de venda")

    embalagem = models.ForeignKey(
        Emb01, 
        on_delete=models.DO_NOTHING, 
        db_column='PdvEmbCod', # Nome da coluna no banco de dados do ERP
        to_field='embcod', 
        null=True, 
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'pdv02'


class Pdv01(models.Model):
    """ Cabeçalho do Pedido de Venda """
    pdvempcod = models.CharField(max_length=10, db_column='PdvEmpCod')
    pdvcod = models.CharField(primary_key=True, max_length=50, db_column='PdvCod')
    
    # --- CAMPOS MODIFICADOS E ADICIONADOS ---
    pdvrazsoc = models.CharField(max_length=255, db_column='PdvRazSoc', help_text="Nome do cliente (denormalizado no pedido)")    

    # Relacionamentos ForeignKey para facilitar as buscas
    cliente = models.ForeignKey(Ter01, on_delete=models.DO_NOTHING, db_column='PdvTerDoc', to_field='terdoc', null=True, blank=True)
    representante = models.ForeignKey(Rep01, on_delete=models.DO_NOTHING, db_column='PdvRepDoc', to_field='repdoc', null=True, blank=True)
    cidade = models.ForeignKey(Cid01, on_delete=models.DO_NOTHING, db_column='PdvLocCid', to_field='cidcod', null=True, blank=True)
    
    pdvemi = models.DateField(db_column='PdvEmi', null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'pdv01'


class Pro01(models.Model):
    procod = models.CharField(primary_key=True, max_length=50, db_column='procod')
    pronom = models.CharField(max_length=255, db_column='proNom')
    probarttam = models.CharField(max_length=50, db_column='probarttam')
    probartcod = models.DecimalField(max_digits=19, decimal_places=0, db_column='ProBArtCod', blank=True, null=True, help_text="Código de Barras do Artigo (numérico)")
    proartcodbas = models.DecimalField(max_digits=19, decimal_places=4, db_column='ProBArtCodBas', blank=True, null=True, help_text="Código do Artigo Base")
    prorprcod = models.CharField(max_length=255, db_column='prorprcod')

    # --- CAMPO ADICIONADO ---
    propesliq = models.DecimalField(
        max_digits=19, 
        decimal_places=6,  # Usando 6 casas decimais para alta precisão no peso
        db_column='ProPesLiq', 
        blank=True, 
        null=True, 
        help_text="Peso Líquido do produto (geralmente por unidade ou grosa)"
    )

    class Meta:
        managed = False
        db_table = 'pro01'

class Ftm04(models.Model):
    ftmacod = models.CharField(primary_key=True, max_length=50, db_column='FtmAcod')
    ftmeart = models.CharField(max_length=255, db_column='FtmEArt')
    ftmeobs = models.TextField(db_column='FtmEObs', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm04'
        unique_together = (('ftmacod', 'ftmeart'),)


class Ftm06(models.Model):
    ftmacod = models.CharField(primary_key=True, max_length=50, db_column='FtmAcod')
    ftmhobs = models.TextField(db_column='FtmHObs', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm06'


class Pdv06(models.Model):
    pdvempcod = models.CharField(max_length=10, db_column='pdvempcod')
    pdvcod = models.CharField(primary_key=True, max_length=50, db_column='pdvcod')
    pdvobsdet = models.TextField(db_column='PdvObsDet', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pdv06'


class Ftd02(models.Model):
    """ Proxy Model para a tabela ftd02 (Ficha Técnica de Grade - Itens) """
    gddcod = models.CharField(primary_key=True, max_length=50, db_column='GddCod')
    ftcacod = models.CharField(max_length=50, db_column='FtcACod')
    
    # --- CORREÇÃO FINAL E DEFINITIVA ---
    # Nome do campo no Django: ftditm
    # Nome da coluna no banco de dados do ERP: FtdItm
    ftditm = models.IntegerField(db_column='FtdItm', help_text="Número do Item / Camada")
    
    mtgcod = models.CharField(max_length=50, db_column='MtgCod', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftd02'
        # A chave única no Django deve usar os nomes de campo do modelo
        unique_together = (('gddcod', 'ftditm', 'mtgcod'),)


class Ftc01(models.Model):
    """ Proxy Model para a tabela ftc01 (Cabeçalho de Fórmulas) """
    ftcacod = models.CharField(primary_key=True, max_length=50, db_column='FtcACod')
    ftcanom = models.CharField(max_length=255, db_column='FtcANom')
    ftcaqtdbas = models.DecimalField(max_digits=19, decimal_places=4, db_column='FtcAQtdBas')

    class Meta:
        managed = False
        db_table = 'ftc01'


class Ftc02(models.Model):
    """ Proxy Model para a tabela ftc02 (Itens da Fórmula Química) """
    ftcacod = models.CharField(primary_key=True, max_length=50, db_column='FtcACod')
    ftcbitm = models.IntegerField(db_column='FtcBItm', help_text="Sequência do item na fórmula")
    ftcprocod = models.CharField(max_length=50, db_column='FtcBProCod')
    ftcqtd = models.DecimalField(max_digits=19, decimal_places=4, db_column='FtcBQtd')

    class Meta:
        managed = False
        db_table = 'ftc02'
        unique_together = (('ftcacod', 'ftcprocod'),)


class Teq01(models.Model):
    """ Proxy Model para a tabela teq01 (Cadastro de Equipamentos) """
    teqcod = models.CharField(primary_key=True, max_length=50, db_column='TeqCod')
    teqnom = models.CharField(max_length=255, db_column='TeqNom')
    mstcod = models.CharField(max_length=10, db_column='MstCod')

    class Meta:
        managed = False
        db_table = 'teq01'
        unique_together = (('teqcod', 'mstcod'),)


