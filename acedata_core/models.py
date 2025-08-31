# acedata_core/models.py (VERSÃO FINAL, COMPLETA E CORRIGIDA)

from django.db import models


# --- MODELOS BASE (Entidades Principais) ---

class Emb01(models.Model):
    """ Mapeia a tabela de Embalagens do ERP """
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)
    embcod = models.CharField(db_column='EmbCod', max_length=12)
    embempcod = models.IntegerField(db_column='EmbEmpCod')
    embdat = models.DateTimeField(db_column='EmbDat', blank=True, null=True)
    embsta = models.CharField(db_column='EmbSta', max_length=7, blank=True, null=True)
    embnom = models.CharField(db_column='EmbNom', max_length=120, blank=True, null=True)
    embabr = models.CharField(db_column='EmbAbr', max_length=15, blank=True, null=True)
    embconest = models.CharField(db_column='EmbConEst', max_length=13, blank=True, null=True)
    embgruemp = models.IntegerField(db_column='EmbGruEmp', blank=True, null=True)
    embgrucod = models.IntegerField(db_column='EmbGruCod', blank=True, null=True)
    embmaremp = models.IntegerField(db_column='EmbMarEmp', blank=True, null=True)
    embmarcod = models.IntegerField(db_column='EmbMarCod', blank=True, null=True)
    embloc = models.CharField(db_column='EmbLoc', max_length=15, blank=True, null=True)
    embempune = models.IntegerField(db_column='EmbEmpUne', blank=True, null=True)
    embuniest = models.CharField(db_column='EmbUniEst', max_length=3, blank=True, null=True)
    embempunv = models.IntegerField(db_column='EmbEmpUnv', blank=True, null=True)
    embuniven = models.CharField(db_column='EmbUniVen', max_length=3, blank=True, null=True)
    embempunc = models.IntegerField(db_column='EmbEmpUnc', blank=True, null=True)
    embunicom = models.CharField(db_column='EmbUniCom', max_length=3, blank=True, null=True)
    embtemgar = models.SmallIntegerField(db_column='EmbTemGar', blank=True, null=True)
    embtipgar = models.CharField(db_column='EmbTipGar', max_length=3, blank=True, null=True)
    embpes = models.DecimalField(db_column='EmbPes', max_digits=9, decimal_places=4, blank=True, null=True)
    embcomcus = models.CharField(db_column='EmbComCus', max_length=1, blank=True, null=True)
    embalmemp = models.IntegerField(db_column='EmbAlmEmp', blank=True, null=True)
    embalmcod = models.SmallIntegerField(db_column='EmbAlmCod', blank=True, null=True)
    embreptem = models.SmallIntegerField(db_column='EmbRepTem', blank=True, null=True)
    emblotide = models.DecimalField(db_column='EmbLotIde', max_digits=13, decimal_places=4, blank=True, null=True)
    emblotmin = models.DecimalField(db_column='EmbLotMin', max_digits=13, decimal_places=4, blank=True, null=True)
    emblotmax = models.DecimalField(db_column='EmbLotMax', max_digits=13, decimal_places=4, blank=True, null=True)
    embqtdpad = models.DecimalField(db_column='EmbQtdPad', max_digits=10, decimal_places=4, blank=True, null=True)
    embqtdmul = models.DecimalField(db_column='EmbQtdMul', max_digits=10, decimal_places=4, blank=True, null=True)
    embcollis = models.CharField(db_column='EmbColLis', max_length=1, blank=True, null=True)
    embcattip = models.CharField(db_column='EmbCatTip', max_length=1, blank=True, null=True)
    embiqqemp = models.IntegerField(db_column='EmbIqqEmp', blank=True, null=True)
    embiqqcod = models.SmallIntegerField(db_column='EmbIqqCod', blank=True, null=True)
    embfatcon = models.DecimalField(db_column='EmbFatCon', max_digits=9, decimal_places=4, blank=True, null=True)
    embfattip = models.CharField(db_column='EmbFatTip', max_length=13, blank=True, null=True)
    stpcod = models.SmallIntegerField(db_column='StpCod', blank=True, null=True)
    embvlrven = models.DecimalField(db_column='EmbVlrVen', max_digits=19, decimal_places=4, blank=True, null=True)
    embrefuniemp = models.IntegerField(db_column='EmbRefUniEmp', blank=True, null=True)
    embrefunicod = models.CharField(db_column='EmbRefUniCod', max_length=3, blank=True, null=True)
    embfabcod = models.CharField(db_column='EmbFabCod', max_length=50, blank=True, null=True)
    embori = models.CharField(db_column='EmbOri', max_length=1, blank=True, null=True)
    embras = models.CharField(db_column='EmbRas', max_length=6, blank=True, null=True)
    embcencod = models.IntegerField(db_column='EmbCenCod', blank=True, null=True)
    embcenemp = models.IntegerField(db_column='EmbCenEmp', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emb01'
        unique_together = (('mstcod', 'embcod'),)

    def __str__(self):
        return self.embnom


class Cid01(models.Model):
    """ Cidades """
    cidcod = models.IntegerField(primary_key=True, db_column='CidCod')
    cidnom = models.CharField(db_column='CidNom', max_length=30, blank=True, null=True)
    estcod = models.CharField(db_column='EstCod', max_length=2, blank=True, null=True)
    paiscod = models.IntegerField(db_column='PaisCod', blank=True, null=True)
    cidcep = models.CharField(db_column='CidCep', max_length=9, blank=True, null=True)
    cidmun = models.CharField(db_column='CidMun', max_length=5, blank=True, null=True)
    cidcodibge = models.CharField(db_column='CidCodIbge', max_length=7, blank=True, null=True)
    cidiss = models.DecimalField(db_column='CidIss', max_digits=10, decimal_places=4, blank=True, null=True)
    cidzfmalc = models.CharField(db_column='CidZfmAlc', max_length=1, blank=True, null=True)
    cidsta = models.CharField(db_column='CidSta', max_length=7, blank=True, null=True)
    cidssdseq = models.DecimalField(db_column='CidSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)
    cidlng = models.DecimalField(db_column='CidLng', max_digits=17, decimal_places=8, blank=True, null=True)
    cidlat = models.DecimalField(db_column='CidLat', max_digits=17, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cid01'

    def __str__(self):
        return f"{self.cidnom} - {self.estcod}"


# --- FAMÍLIA DE MODELOS TER (TERCEIROS) ---

class Ter01(models.Model):
    """ Terceiros (Clientes, Fornecedores, etc.) - Cabeçalho """
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)
    terdoc = models.IntegerField(db_column='TerDoc', help_text="Código do Cliente no ERP")
    tercod = models.IntegerField(db_column='TerCod', blank=True, null=True)
    tercpf = models.CharField(max_length=20, db_column='TerCpf', blank=True, null=True, help_text="CPF ou CNPJ")
    tertipdoc = models.CharField(db_column='TerTipDoc', max_length=6, blank=True, null=True)
    terdoccon = models.CharField(db_column='TerDocCon', max_length=20, blank=True, null=True)
    terdat = models.DateTimeField(db_column='TerDat', blank=True, null=True)
    tersta = models.CharField(db_column='TerSta', max_length=7, blank=True, null=True)
    tertip = models.CharField(db_column='TerTip', max_length=1, blank=True, null=True)
    ternom = models.CharField(max_length=255, db_column='TerNom', help_text="Nome Fantasia")
    terraz = models.CharField(max_length=255, db_column='TerRaz', blank=True, null=True, help_text="Razão Social")
    termod = models.CharField(db_column='TerMod', max_length=1, blank=True, null=True)
    terinstip = models.CharField(db_column='TerInsTip', max_length=6, blank=True, null=True)
    terinsest = models.CharField(db_column='TerInsEst', max_length=20, blank=True, null=True)
    terinsmun = models.CharField(db_column='TerInsMun', max_length=20, blank=True, null=True)
    terendfat = models.CharField(db_column='TerEndFat', max_length=60, blank=True, null=True)
    terfatnro = models.IntegerField(db_column='TerFatNro', blank=True, null=True)
    terfatcom = models.CharField(db_column='TerFatCom', max_length=60, blank=True, null=True)
    terbaifat = models.CharField(db_column='TerBaiFat', max_length=60, blank=True, null=True)
    tercidcodf = models.IntegerField(db_column='TerCidCodF', blank=True, null=True, help_text="Código da Cidade")
    tercepfat = models.CharField(max_length=10, db_column='TerCepFat', blank=True, null=True,
                                 help_text="CEP de Faturamento")
    tercxpfat = models.IntegerField(db_column='TerCxpFat', blank=True, null=True)
    terccpfat = models.CharField(db_column='TerCcpFat', max_length=9, blank=True, null=True)
    terfon1 = models.CharField(max_length=20, db_column='TerFon1', blank=True, null=True,
                               help_text="Telefone Principal")
    terfax1 = models.CharField(db_column='TerFax1', max_length=15, blank=True, null=True)
    terfon2 = models.CharField(db_column='TerFon2', max_length=15, blank=True, null=True)
    terfax2 = models.CharField(db_column='TerFax2', max_length=15, blank=True, null=True)
    terfon3 = models.CharField(db_column='TerFon3', max_length=15, blank=True, null=True)
    terfax3 = models.CharField(db_column='TerFax3', max_length=15, blank=True, null=True)
    terema = models.CharField(max_length=255, db_column='TerEma', blank=True, null=True, help_text="E-mail Principal")
    terhom = models.CharField(db_column='TerHom', max_length=150, blank=True, null=True)
    tercli = models.CharField(db_column='TerCli', max_length=1, blank=True, null=True)
    teralu = models.CharField(db_column='TerAlu', max_length=1, blank=True, null=True)
    terfor = models.CharField(db_column='TerFor', max_length=1, blank=True, null=True)
    terrep = models.CharField(db_column='TerRep', max_length=1, blank=True, null=True)
    tertra = models.CharField(db_column='TerTra', max_length=1, blank=True, null=True)
    tercol = models.CharField(db_column='TerCol', max_length=1, blank=True, null=True)
    tercon = models.CharField(db_column='TerCon', max_length=1, blank=True, null=True)
    tertmk = models.CharField(db_column='TerTmk', max_length=1, blank=True, null=True)
    tertmksta = models.CharField(db_column='TerTmkSta', max_length=3, blank=True, null=True)
    tericm = models.CharField(db_column='TerIcm', max_length=1, blank=True, null=True)
    terultban = models.SmallIntegerField(db_column='TerUltBan', blank=True, null=True)
    terultent = models.SmallIntegerField(db_column='TerUltEnt', blank=True, null=True)
    tercplaemp = models.IntegerField(db_column='TerCPlaEmp', blank=True, null=True)
    tercplacod = models.IntegerField(db_column='TerCPlaCod', blank=True, null=True)
    terfplaemp = models.IntegerField(db_column='TerFPlaEmp', blank=True, null=True)
    terfplacod = models.IntegerField(db_column='TerFPlaCod', blank=True, null=True)
    terenqfed = models.CharField(db_column='TerEnqFed', max_length=5, blank=True, null=True)
    terenqest = models.CharField(db_column='TerEnqEst', max_length=5, blank=True, null=True)
    terusrins = models.CharField(db_column='TerUsrIns', max_length=100, blank=True, null=True)
    terusralt = models.CharField(db_column='TerUsrAlt', max_length=100, blank=True, null=True)
    sttcod = models.SmallIntegerField(db_column='SttCod', blank=True, null=True)
    teradm = models.CharField(db_column='TerAdm', max_length=10, blank=True, null=True)
    terinssuf = models.CharField(db_column='TerInsSuf', max_length=20, blank=True, null=True)
    tersufdes = models.DecimalField(db_column='TerSufDes', max_digits=10, decimal_places=4, blank=True, null=True)
    terstaqua = models.CharField(db_column='TerStaQua', max_length=2, blank=True, null=True)
    ternas = models.DateTimeField(db_column='TerNas', blank=True, null=True)
    ternompai = models.CharField(db_column='TerNomPai', max_length=50, blank=True, null=True)
    ternommae = models.CharField(db_column='TerNomMae', max_length=50, blank=True, null=True)
    tercpfrsp = models.CharField(db_column='TerCpfRsp', max_length=20, blank=True, null=True)
    terrgrsp = models.CharField(db_column='TerRGRsp', max_length=20, blank=True, null=True)
    terape = models.CharField(db_column='TerApe', max_length=8, blank=True, null=True)
    terestciv = models.CharField(db_column='TerEstCiv', max_length=1, blank=True, null=True)
    terprof = models.CharField(db_column='TerProf', max_length=30, blank=True, null=True)
    ternac = models.CharField(db_column='TerNac', max_length=2, blank=True, null=True)
    terulticd = models.SmallIntegerField(db_column='TerUltIcd', blank=True, null=True)
    terultret = models.SmallIntegerField(db_column='TerUltRet', blank=True, null=True)
    tercodatu = models.CharField(db_column='TerCodAtu', max_length=1, blank=True, null=True)
    tercodold = models.CharField(db_column='TerCodOld', max_length=20, blank=True, null=True)
    tercodnew = models.CharField(db_column='TerCodNew', max_length=6, blank=True, null=True)
    teriseimp = models.CharField(db_column='TerIseImp', max_length=1, blank=True, null=True)
    tersincon = models.DateTimeField(db_column='TerSinCon', blank=True, null=True)
    tercodfor = models.CharField(db_column='TerCodFor', max_length=20, blank=True, null=True)
    tercodcli = models.CharField(db_column='TerCodCli', max_length=20, blank=True, null=True)
    tersufdesicm = models.CharField(db_column='TerSufDesIcm', max_length=1, blank=True, null=True)
    tersufdespis = models.CharField(db_column='TerSufDesPis', max_length=1, blank=True, null=True)
    tersufdescof = models.CharField(db_column='TerSufDesCof', max_length=1, blank=True, null=True)
    tersufdesipi = models.CharField(db_column='TerSufDesIpi', max_length=1, blank=True, null=True)
    teremaildanfe = models.CharField(db_column='TerEmailDANFE', max_length=160, blank=True, null=True)
    tervissem1 = models.CharField(db_column='TerVisSem1', max_length=1, blank=True, null=True)
    tervissem2 = models.CharField(db_column='TerVisSem2', max_length=1, blank=True, null=True)
    tervissem3 = models.CharField(db_column='TerVisSem3', max_length=1, blank=True, null=True)
    tervissem4 = models.CharField(db_column='TerVisSem4', max_length=1, blank=True, null=True)
    tervisseg = models.CharField(db_column='TerVisSeg', max_length=1, blank=True, null=True)
    tervister = models.CharField(db_column='TerVisTer', max_length=1, blank=True, null=True)
    tervisqua = models.CharField(db_column='TerVisQua', max_length=1, blank=True, null=True)
    tervisqui = models.CharField(db_column='TerVisQui', max_length=1, blank=True, null=True)
    tervissex = models.CharField(db_column='TerVisSex', max_length=1, blank=True, null=True)
    terpotven = models.DecimalField(db_column='TerPotVen', max_digits=19, decimal_places=4, blank=True, null=True)
    tervissem5 = models.CharField(db_column='TerVisSem5', max_length=1, blank=True, null=True)
    terultacr = models.DecimalField(db_column='TerUltAcr', max_digits=10, decimal_places=0, blank=True, null=True)
    terproindtot = models.CharField(db_column='TerProIndTot', max_length=1, blank=True, null=True)
    ternfeemaildanfe = models.CharField(db_column='TerNFeEmailDanfe', max_length=1, blank=True, null=True)
    ternfeemailxml1 = models.CharField(db_column='TerNFeEmailXml1', max_length=1, blank=True, null=True)
    ternfeemailxml2 = models.CharField(db_column='TerNFeEmailXml2', max_length=1, blank=True, null=True)
    ternfeemailtip = models.CharField(db_column='TerNFeEmailTip', max_length=1, blank=True, null=True)
    terponsal = models.IntegerField(db_column='TerPonSal', blank=True, null=True)
    ternatret = models.CharField(db_column='TerNatRet', max_length=2, blank=True, null=True)
    tercpfnro = models.CharField(db_column='TerCpfNro', max_length=20, blank=True, null=True)
    tertmksem1 = models.CharField(db_column='TerTmkSem1', max_length=1, blank=True, null=True)
    tertmksem2 = models.CharField(db_column='TerTmkSem2', max_length=1, blank=True, null=True)
    tertmksem3 = models.CharField(db_column='TerTmkSem3', max_length=1, blank=True, null=True)
    tertmksem4 = models.CharField(db_column='TerTmkSem4', max_length=1, blank=True, null=True)
    tertmksem5 = models.CharField(db_column='TerTmkSem5', max_length=1, blank=True, null=True)
    tertmkseg = models.CharField(db_column='TerTmkSeg', max_length=1, blank=True, null=True)
    tertmkter = models.CharField(db_column='TerTmkTer', max_length=1, blank=True, null=True)
    tertmkqua = models.CharField(db_column='TerTmkQua', max_length=1, blank=True, null=True)
    tertmkqui = models.CharField(db_column='TerTmkQui', max_length=1, blank=True, null=True)
    tertmksex = models.CharField(db_column='TerTmkSex', max_length=1, blank=True, null=True)
    terindemp = models.IntegerField(db_column='TerIndEmp', blank=True, null=True)
    terinddoc = models.IntegerField(db_column='TerIndDoc', blank=True, null=True)
    terindsta = models.CharField(db_column='TerIndSta', max_length=2, blank=True, null=True)
    terindobs = models.CharField(db_column='TerIndObs', max_length=100, blank=True, null=True)
    terindprc = models.DateTimeField(db_column='TerIndPrc', blank=True, null=True)
    terecf = models.CharField(db_column='TerEcf', max_length=1, blank=True, null=True)
    terssddoc = models.DecimalField(db_column='TerSsdDoc', max_digits=10, decimal_places=0, blank=True, null=True)
    terssdseq = models.DecimalField(db_column='TerSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)
    terfilvin = models.IntegerField(db_column='TerFilVin', blank=True, null=True)
    terempvin = models.IntegerField(db_column='TerEmpVin', blank=True, null=True)
    teravaqua = models.CharField(db_column='TerAvaQua', max_length=1, blank=True, null=True)
    terindcon = models.CharField(db_column='TerIndCon', max_length=2, blank=True, null=True)
    teroricod = models.IntegerField(db_column='TerOriCod', blank=True, null=True)
    terorimst = models.IntegerField(db_column='TerOriMst', blank=True, null=True)
    tersufdatval = models.DateTimeField(db_column='TerSufDatVal', blank=True, null=True)
    tercpfnropf = models.CharField(db_column='TerCpfNroPF', max_length=20, blank=True, null=True)
    terbolcsocod = models.CharField(db_column='TerBolCsoCod', max_length=12, blank=True, null=True)
    ternasrsp = models.DateTimeField(db_column='TerNasRsp', blank=True, null=True)
    terstadat = models.DateTimeField(db_column='TerStaDat', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter01'
        unique_together = (('terempcod', 'terdoc'),)

    def __str__(self):
        return self.ternom


class Ter02(models.Model):
    """ Terceiros (Contatos) """
    id = models.AutoField(primary_key=True)
    terempcod = models.IntegerField(db_column='TerEmpCod')
    terdoc = models.IntegerField(db_column='TerDoc')
    teritmcon = models.SmallIntegerField(db_column='TerItmCon')
    ternomcon = models.CharField(db_column='TerNomCon', max_length=30, blank=True, null=True)
    tersetcon = models.CharField(db_column='TerSetCon', max_length=15, blank=True, null=True)
    tercarcon = models.CharField(db_column='TerCarCon', max_length=15, blank=True, null=True)
    terfoncon1 = models.CharField(db_column='TerFonCon1', max_length=15, blank=True, null=True)
    terfoncon2 = models.CharField(db_column='TerFonCon2', max_length=15, blank=True, null=True)
    terfoncon3 = models.CharField(db_column='TerFonCon3', max_length=15, blank=True, null=True)
    terramcon = models.IntegerField(db_column='TerRamCon', blank=True, null=True)
    terfaxcon = models.CharField(db_column='TerFaxCon', max_length=15, blank=True, null=True)
    teremacon = models.CharField(db_column='TerEmaCon', max_length=150, blank=True, null=True)
    ternascon = models.DateTimeField(db_column='TerNasCon', blank=True, null=True)
    teranicon = models.CharField(db_column='TerAniCon', max_length=5, blank=True, null=True)
    terctccon = models.CharField(db_column='TerCtcCon', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter02'
        unique_together = (('terempcod', 'terdoc', 'teritmcon'),)


class Ter03(models.Model):
    """ Terceiros (Dados Bancários) """
    id = models.AutoField(primary_key=True)
    terempcod = models.IntegerField(db_column='TerEmpCod')
    terdoc = models.IntegerField(db_column='TerDoc')
    teritmban = models.SmallIntegerField(db_column='TerItmBan')
    terpadban = models.CharField(db_column='TerPadBan', max_length=1, blank=True, null=True)
    ternroban = models.SmallIntegerField(db_column='TerNroBan', blank=True, null=True)
    ternroage = models.CharField(db_column='TerNroAge', max_length=6, blank=True, null=True)
    ternomage = models.CharField(db_column='TerNomAge', max_length=30, blank=True, null=True)
    ternrocco = models.CharField(db_column='TerNroCco', max_length=15, blank=True, null=True)
    tertipcco = models.CharField(db_column='TerTipCco', max_length=1, blank=True, null=True)
    tertitcco = models.CharField(db_column='TerTitCco', max_length=30, blank=True, null=True)
    tertitcpf = models.CharField(db_column='TerTitCpf', max_length=20, blank=True, null=True)
    tercidcoda = models.IntegerField(db_column='TerCidCodA', blank=True, null=True)
    termodban = models.CharField(db_column='TerModBan', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter03'
        unique_together = (('terempcod', 'terdoc', 'teritmban'),)


class Ter04(models.Model):
    """ Terceiros (Endereços de Entrega) """
    id = models.AutoField(primary_key=True)
    terempcod = models.IntegerField(db_column='TerEmpCod')
    terdoc = models.IntegerField(db_column='TerDoc')
    teritment = models.SmallIntegerField(db_column='TerItmEnt')
    traemdent = models.IntegerField(db_column='TraEmdEnt', blank=True, null=True)
    tradcdent = models.IntegerField(db_column='TraDcdEnt', blank=True, null=True)
    tranomdes = models.CharField(db_column='TraNomDes', max_length=30, blank=True, null=True)
    terfrdent = models.CharField(db_column='TerFrdEnt', max_length=1, blank=True, null=True)
    traemrent = models.IntegerField(db_column='TraEmrEnt', blank=True, null=True)
    tradcrent = models.IntegerField(db_column='TraDcrEnt', blank=True, null=True)
    tranomred = models.CharField(db_column='TraNomRed', max_length=30, blank=True, null=True)
    terfrrent = models.CharField(db_column='TerFrrEnt', max_length=1, blank=True, null=True)
    terendent = models.CharField(db_column='TerEndEnt', max_length=60, blank=True, null=True)
    ternroent = models.IntegerField(db_column='TerNroEnt', blank=True, null=True)
    tercoment = models.CharField(db_column='TerComEnt', max_length=60, blank=True, null=True)
    terbaient = models.CharField(db_column='TerBaiEnt', max_length=60, blank=True, null=True)
    tercidcode = models.IntegerField(db_column='TerCidCodE', blank=True, null=True)
    tercepent = models.CharField(db_column='TerCepEnt', max_length=9, blank=True, null=True)
    tercxpent = models.IntegerField(db_column='TerCxpEnt', blank=True, null=True)
    terccpent = models.CharField(db_column='TerCcpEnt', max_length=9, blank=True, null=True)
    terrpeent = models.IntegerField(db_column='TerRpeEnt', blank=True, null=True)
    terrpdent = models.IntegerField(db_column='TerRpdEnt', blank=True, null=True)
    terrecent = models.CharField(db_column='TerRecEnt', max_length=254, blank=True, null=True)
    terfrernf = models.CharField(db_column='TerFreRnf', max_length=1, blank=True, null=True)
    terentpad = models.CharField(db_column='TerEntPad', max_length=1, blank=True, null=True)
    terfrefxa = models.SmallIntegerField(db_column='TerFreFxa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter04'
        unique_together = (('terempcod', 'terdoc', 'teritment'),)


class Ter05(models.Model):
    """ Terceiros (Endereços de Retirada) """
    id = models.AutoField(primary_key=True)
    terempcod = models.IntegerField(db_column='TerEmpCod')
    terdoc = models.IntegerField(db_column='TerDoc')
    teritmret = models.SmallIntegerField(db_column='TerItmRet')
    traemdret = models.IntegerField(db_column='TraEmdRet', blank=True, null=True)
    tradcdret = models.IntegerField(db_column='TraDcdRet', blank=True, null=True)
    terfrdret = models.CharField(db_column='TerFrdRet', max_length=1, blank=True, null=True)
    traemrret = models.IntegerField(db_column='TraEmrRet', blank=True, null=True)
    tradcrret = models.IntegerField(db_column='TraDcrRet', blank=True, null=True)
    terfrrret = models.CharField(db_column='TerFrrRet', max_length=1, blank=True, null=True)
    terendret = models.CharField(db_column='TerEndRet', max_length=60, blank=True, null=True)
    ternroret = models.IntegerField(db_column='TerNroRet', blank=True, null=True)
    tercomret = models.CharField(db_column='TerComRet', max_length=60, blank=True, null=True)
    terbairet = models.CharField(db_column='TerBaiRet', max_length=60, blank=True, null=True)
    tercidcodr = models.IntegerField(db_column='TerCidCodR', blank=True, null=True)
    tercepret = models.CharField(db_column='TerCepRet', max_length=9, blank=True, null=True)
    tercxpret = models.IntegerField(db_column='TerCxpRet', blank=True, null=True)
    terccpret = models.CharField(db_column='TerCcpRet', max_length=9, blank=True, null=True)
    terpadret = models.CharField(db_column='TerPadRet', max_length=1, blank=True, null=True)
    terhorret = models.CharField(db_column='TerHorRet', max_length=50, blank=True, null=True)
    terequret = models.CharField(db_column='TerEquRet', max_length=50, blank=True, null=True)
    terconret = models.CharField(db_column='TerConRet', max_length=30, blank=True, null=True)
    terfonret = models.CharField(db_column='TerFonRet', max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter05'
        unique_together = (('terempcod', 'terdoc', 'teritmret'),)


class Ter06(models.Model):
    """ Terceiros (Produtos/Serviços Associados) """
    id = models.AutoField(primary_key=True)
    terempcod = models.IntegerField(db_column='TerEmpCod')
    terdoc = models.IntegerField(db_column='TerDoc')
    terprocod = models.CharField(db_column='TerProCod', max_length=12)
    terembcod = models.CharField(db_column='TerEmbCod', max_length=12)
    terproemp = models.IntegerField(db_column='TerProEmp', blank=True, null=True)
    terembemp = models.IntegerField(db_column='TerEmbEmp', blank=True, null=True)
    terprocdm = models.CharField(db_column='TerProCdm', max_length=20, blank=True, null=True)
    terproucp = models.DateTimeField(db_column='TerProUcp', blank=True, null=True)
    terproeccemp = models.IntegerField(db_column='TerProEccEmp', blank=True, null=True)
    terproecccod = models.IntegerField(db_column='TerProEccCod', blank=True, null=True)
    terprocemp = models.CharField(db_column='TerProCEmp', max_length=50, blank=True, null=True)
    terprocpro = models.CharField(db_column='TerProCPro', max_length=50, blank=True, null=True)
    terprocemb = models.CharField(db_column='TerProCEmb', max_length=30, blank=True, null=True)
    terprocprc = models.DecimalField(db_column='TerProCPrc', max_digits=14, decimal_places=5, blank=True, null=True)
    terprocper = models.CharField(db_column='TerProCPer', max_length=30, blank=True, null=True)
    terpromodpor1 = models.DecimalField(db_column='TerProModPor1', max_digits=10, decimal_places=4, blank=True,
                                        null=True)
    terpromodpor2 = models.DecimalField(db_column='TerProModPor2', max_digits=10, decimal_places=4, blank=True,
                                        null=True)
    terpromodpor3 = models.DecimalField(db_column='TerProModPor3', max_digits=10, decimal_places=4, blank=True,
                                        null=True)
    terproconnro = models.CharField(db_column='TerProConNro', max_length=20, blank=True, null=True)
    terprocondat = models.DateTimeField(db_column='TerProConDat', blank=True, null=True)
    terprolicnrome = models.CharField(db_column='TerProLicNroME', max_length=20, blank=True, null=True)
    terprolicvalme = models.DateTimeField(db_column='TerProLicValME', blank=True, null=True)
    terprolicnropf = models.CharField(db_column='TerProLicNroPF', max_length=20, blank=True, null=True)
    terprolicvalpf = models.DateTimeField(db_column='TerProLicValPF', blank=True, null=True)
    terprolicnrossp = models.CharField(db_column='TerProLicNroSSP', max_length=20, blank=True, null=True)
    terprolicvalssp = models.DateTimeField(db_column='TerProLicValSSP', blank=True, null=True)
    terproprcpra = models.DecimalField(db_column='TerProPrcPra', max_digits=14, decimal_places=5, blank=True, null=True)
    terproultprc = models.DecimalField(db_column='TerProUltPrc', max_digits=14, decimal_places=5, blank=True, null=True)
    terproultqtd = models.DecimalField(db_column='TerProUltQtd', max_digits=13, decimal_places=4, blank=True, null=True)
    terproultlis = models.DecimalField(db_column='TerProUltLis', max_digits=14, decimal_places=5, blank=True, null=True)
    terprodat = models.DateTimeField(db_column='TerProDat', blank=True, null=True)
    terprolicvalib = models.DateTimeField(db_column='TerProLicValIB', blank=True, null=True)
    terprolicnroib = models.CharField(db_column='TerProLicNroIB', max_length=20, blank=True, null=True)
    terprossdseq = models.DecimalField(db_column='TerProSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ter06'
        unique_together = (('terempcod', 'terdoc', 'terprocod', 'terembcod'),)


# --- FAMÍLIA DE MODELOS REP (REPRESENTANTES) ---

class Rep01(models.Model):
    """ Representantes (Cabeçalho) """
    repempcod = models.IntegerField(db_column='RepEmpCod', primary_key=True)
    repdoc = models.IntegerField(db_column='RepDoc')
    repcod = models.IntegerField(db_column='RepCod', blank=True, null=True)
    reptipdoc = models.CharField(db_column='RepTipDoc', max_length=6, blank=True, null=True)
    repdat = models.DateTimeField(db_column='RepDat', blank=True, null=True)
    repsta = models.CharField(db_column='RepSta', max_length=7, blank=True, null=True)
    repnom = models.CharField(max_length=255, db_column='RepNom')
    repide = models.CharField(db_column='RepIde', max_length=10, blank=True, null=True)
    repraz = models.CharField(db_column='RepRaz', max_length=50, blank=True, null=True)
    reptip = models.CharField(db_column='RepTip', max_length=1, blank=True, null=True)
    rependfat = models.CharField(db_column='RepEndFat', max_length=60, blank=True, null=True)
    repnrofat = models.IntegerField(db_column='RepNroFat', blank=True, null=True)
    repcomfat = models.CharField(db_column='RepComFat', max_length=60, blank=True, null=True)
    repbaifat = models.CharField(db_column='RepBaiFat', max_length=60, blank=True, null=True)
    repcidcodf = models.IntegerField(db_column='RepCidCodF', blank=True, null=True)
    repcepfat = models.CharField(db_column='RepCepFat', max_length=9, blank=True, null=True)
    repcxpfat = models.IntegerField(db_column='RepCxpFat', blank=True, null=True)
    repccpfat = models.CharField(db_column='RepCcpFat', max_length=9, blank=True, null=True)
    repinsest = models.CharField(db_column='RepInsEst', max_length=20, blank=True, null=True)
    repinstip = models.CharField(db_column='RepInsTip', max_length=6, blank=True, null=True)
    repinsmun = models.CharField(db_column='RepInsMun', max_length=20, blank=True, null=True)
    repfon1 = models.CharField(db_column='RepFon1', max_length=15, blank=True, null=True)
    repfax1 = models.CharField(db_column='RepFax1', max_length=15, blank=True, null=True)
    repfon2 = models.CharField(db_column='RepFon2', max_length=15, blank=True, null=True)
    repfax2 = models.CharField(db_column='RepFax2', max_length=15, blank=True, null=True)
    repfon3 = models.CharField(db_column='RepFon3', max_length=15, blank=True, null=True)
    repfax3 = models.CharField(db_column='RepFax3', max_length=15, blank=True, null=True)
    repema = models.CharField(db_column='RepEma', max_length=150, blank=True, null=True)
    rephom = models.CharField(db_column='RepHom', max_length=150, blank=True, null=True)
    repmod = models.CharField(db_column='RepMod', max_length=1, blank=True, null=True)
    repareemp = models.IntegerField(db_column='RepAreEmp', blank=True, null=True)
    reparecod = models.CharField(db_column='RepAreCod', max_length=5, blank=True, null=True)
    repcalcom = models.CharField(db_column='RepCalcom', max_length=1, blank=True, null=True)
    reptplemp = models.IntegerField(db_column='RepTplEmp', blank=True, null=True)
    reptplcod = models.SmallIntegerField(db_column='RepTplCod', blank=True, null=True)
    repcpf = models.CharField(db_column='RepCpf', max_length=20, blank=True, null=True)
    repmkt = models.CharField(db_column='RepMkt', max_length=1, blank=True, null=True)
    repdvd = models.CharField(db_column='RepDvd', max_length=1, blank=True, null=True)
    repmovint = models.CharField(db_column='RepMovInt', max_length=1, blank=True, null=True)
    repultban = models.SmallIntegerField(db_column='RepUltBan', blank=True, null=True)
    repultvis = models.DecimalField(db_column='RepUltVis', max_digits=10, decimal_places=0, blank=True, null=True)
    repultapa = models.DecimalField(db_column='RepUltApa', max_digits=10, decimal_places=0, blank=True, null=True)
    repultdpa = models.DecimalField(db_column='RepUltDpa', max_digits=10, decimal_places=0, blank=True, null=True)
    repcodatu = models.CharField(db_column='RepCodAtu', max_length=1, blank=True, null=True)
    repcodold = models.CharField(db_column='RepCodOld', max_length=20, blank=True, null=True)
    repcodnew = models.CharField(db_column='RepCodNew', max_length=6, blank=True, null=True)
    repenqest = models.CharField(db_column='RepEnqEst', max_length=5, blank=True, null=True)
    repenqfed = models.CharField(db_column='RepEnqFed', max_length=5, blank=True, null=True)
    repexphis = models.CharField(db_column='RepExpHis', max_length=1, blank=True, null=True)
    sttcod = models.SmallIntegerField(db_column='SttCod', blank=True, null=True)
    repcevemp = models.IntegerField(db_column='RepCevEmp', blank=True, null=True)
    repcevcod = models.SmallIntegerField(db_column='RepCevCod', blank=True, null=True)
    repultlis = models.DecimalField(db_column='RepUltLis', max_digits=10, decimal_places=0, blank=True, null=True)
    repmemeqv = models.CharField(db_column='RepMemEqv', max_length=1, blank=True, null=True)
    repvenmod2 = models.CharField(db_column='RepVenMod2', max_length=1, blank=True, null=True)
    repvencb = models.CharField(db_column='RepVenCB', max_length=1, blank=True, null=True)
    repvisapo = models.CharField(db_column='RepVisApo', max_length=1, blank=True, null=True)
    repsinsd = models.CharField(db_column='RepSinSD', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rep01'
        unique_together = (('repempcod', 'repdoc'),)

    def __str__(self):
        return self.repnom


class Rep02(models.Model):
    """ Representantes (Contatos) """
    id = models.AutoField(primary_key=True)
    repempcod = models.IntegerField(db_column='RepEmpCod')
    repdoc = models.IntegerField(db_column='RepDoc')
    repitmcon = models.SmallIntegerField(db_column='RepItmCon')
    repnomcon = models.CharField(db_column='RepNomCon', max_length=30, blank=True, null=True)
    repsetcon = models.CharField(db_column='RepSetCon', max_length=15, blank=True, null=True)
    repcarcon = models.CharField(db_column='RepCarCon', max_length=15, blank=True, null=True)
    repfoncon = models.CharField(db_column='RepFonCon', max_length=15, blank=True, null=True)
    repramcon = models.IntegerField(db_column='RepRamCon', blank=True, null=True)
    repfaxcon = models.CharField(db_column='RepFaxCon', max_length=15, blank=True, null=True)
    repemacon = models.CharField(db_column='RepEmaCon', max_length=150, blank=True, null=True)
    repnascon = models.DateTimeField(db_column='RepNasCon', blank=True, null=True)
    repanicon = models.CharField(db_column='RepAniCon', max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rep02'
        unique_together = (('repempcod', 'repdoc', 'repitmcon'),)


class Rep03(models.Model):
    """ Representantes (Dados Bancários) """
    id = models.AutoField(primary_key=True)
    repempcod = models.IntegerField(db_column='RepEmpCod')
    repdoc = models.IntegerField(db_column='RepDoc')
    repitmban = models.SmallIntegerField(db_column='RepItmBan')
    reppadban = models.CharField(db_column='RepPadBan', max_length=1, blank=True, null=True)
    repnroban = models.SmallIntegerField(db_column='RepNroBan', blank=True, null=True)
    repnroage = models.CharField(db_column='RepNroAge', max_length=6, blank=True, null=True)
    repnomage = models.CharField(db_column='RepNomAge', max_length=30, blank=True, null=True)
    repnrocco = models.CharField(db_column='RepNroCco', max_length=15, blank=True, null=True)
    reptitcco = models.CharField(db_column='RepTitCco', max_length=30, blank=True, null=True)
    reptitcpf = models.CharField(db_column='RepTitCpf', max_length=20, blank=True, null=True)
    reptipcco = models.CharField(db_column='RepTipCco', max_length=1, blank=True, null=True)
    repcidcoda = models.IntegerField(db_column='RepCidCodA', blank=True, null=True)
    repmodban = models.CharField(db_column='RepModBan', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rep03'
        unique_together = (('repempcod', 'repdoc', 'repitmban'),)


class Rep04(models.Model):
    """ Representantes (Comissões) """
    id = models.AutoField(primary_key=True)
    repempcod = models.IntegerField(db_column='RepEmpCod')
    repdoc = models.IntegerField(db_column='RepDoc')
    repcitm = models.SmallIntegerField(db_column='RepCItm')
    repcfpgcod = models.SmallIntegerField(db_column='RepCFpgCod', blank=True, null=True)
    repcrepmstemp = models.IntegerField(db_column='RepCRepMstEmp', blank=True, null=True)
    repcrepmstdoc = models.IntegerField(db_column='RepCRepMstDoc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rep04'
        unique_together = (('repempcod', 'repdoc', 'repcitm'),)


# --- FAMÍLIA DE MODELOS PDV (PEDIDOS DE VENDA) ---

class Pdv01(models.Model):
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (PdvEmpCod, PdvFilCod, PdvPfxCod, PdvCod) found, that is not supported. The first column is selected.
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')  # Field name made lowercase.
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)  # Field name made lowercase.
    pdvcod = models.IntegerField(db_column='PdvCod')  # Field name made lowercase.
    pdvpfxemp = models.IntegerField(db_column='PdvPfxEmp', blank=True, null=True)  # Field name made lowercase.
    pdvterdoc = models.IntegerField(db_column='PdvTerDoc', blank=True, null=True)  # Field name made lowercase.
    pdvbanemp = models.IntegerField(db_column='PdvBanEmp', blank=True, null=True)  # Field name made lowercase.
    pdvbancod = models.IntegerField(db_column='PdvBanCod', blank=True, null=True)  # Field name made lowercase.
    pdvtcbcod = models.SmallIntegerField(db_column='PdvTcbCod', blank=True, null=True)  # Field name made lowercase.
    pdvfat = models.SmallIntegerField(db_column='PdvFat', blank=True, null=True)  # Field name made lowercase.
    pdvcodpocket = models.CharField(db_column='PdvCodPocket', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pdvemi = models.DateTimeField(db_column='PdvEmi', blank=True, null=True, db_comment='Data de emissao do pedido\n')  # Field name made lowercase.
    pdvdig = models.DateTimeField(db_column='PdvDig', blank=True, null=True)  # Field name made lowercase.
    pdvtip = models.CharField(db_column='PdvTip', max_length=25, blank=True, null=True)  # Field name made lowercase.
    pdvtipfre = models.CharField(db_column='PdvTipFre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvredfre = models.CharField(db_column='PdvRedFre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvteremp = models.IntegerField(db_column='PdvTerEmp', blank=True, null=True)  # Field name made lowercase.
    pdvrazsoc = models.CharField(db_column='PdvRazSoc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pdvrepemp = models.IntegerField(db_column='PdvRepEmp', blank=True, null=True)  # Field name made lowercase.
    pdvrepdoc = models.IntegerField(db_column='PdvRepDoc', blank=True, null=True, db_comment='Codigo do representante')  # Field name made lowercase.
    pdvtprcod = models.SmallIntegerField(db_column='PdvTprCod', blank=True, null=True)  # Field name made lowercase.
    pdvlcpemp = models.IntegerField(db_column='PdvLcpEmp', blank=True, null=True)  # Field name made lowercase.
    pdvlcpcod = models.IntegerField(db_column='PdvLcpCod', blank=True, null=True)  # Field name made lowercase.
    pdvnomcom = models.CharField(db_column='PdvNomCom', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pdvfeipor = models.CharField(db_column='PdvFeiPor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvcpgemp = models.IntegerField(db_column='PdvCpgEmp', blank=True, null=True)  # Field name made lowercase.
    pdvcpgcod = models.IntegerField(db_column='PdvCpgCod', blank=True, null=True)  # Field name made lowercase.
    pdvtraemp = models.IntegerField(db_column='PdvTraEmp', blank=True, null=True)  # Field name made lowercase.
    pdvtradoc = models.IntegerField(db_column='PdvTraDoc', blank=True, null=True)  # Field name made lowercase.
    pdvredemp = models.IntegerField(db_column='PdvRedEmp', blank=True, null=True)  # Field name made lowercase.
    pdvreddoc = models.IntegerField(db_column='PdvRedDoc', blank=True, null=True)  # Field name made lowercase.
    pdvtplcod = models.SmallIntegerField(db_column='PdvTplCod', blank=True, null=True)  # Field name made lowercase.
    pdvloccid = models.IntegerField(db_column='PdvLocCid', blank=True, null=True)  # Field name made lowercase.
    pdvvalfre = models.DecimalField(db_column='PdvValFre', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvalseg = models.DecimalField(db_column='PdvValSeg', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvalout = models.DecimalField(db_column='PdvValOut', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpordes = models.DecimalField(db_column='PdvPorDes', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords1 = models.DecimalField(db_column='PdvPorDs1', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords2 = models.DecimalField(db_column='PdvPorDs2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords3 = models.DecimalField(db_column='PdvPorDs3', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords4 = models.DecimalField(db_column='PdvPorDs4', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords5 = models.DecimalField(db_column='PdvPorDs5', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpords6 = models.DecimalField(db_column='PdvPorDs6', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvaldes = models.DecimalField(db_column='PdvValDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubdes = models.DecimalField(db_column='PdvSubDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmod = models.CharField(db_column='PdvMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvmod2 = models.CharField(db_column='PdvMod2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvusrmod = models.CharField(db_column='PdvUsrMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvromcar = models.IntegerField(db_column='PdvRomCar', blank=True, null=True)  # Field name made lowercase.
    pdvctvcod = models.IntegerField(db_column='PdvCtvCod', blank=True, null=True)  # Field name made lowercase.
    pdvfecemp = models.IntegerField(db_column='PdvFecEmp', blank=True, null=True)  # Field name made lowercase.
    pdvfecdoc = models.IntegerField(db_column='PdvFecDoc', blank=True, null=True)  # Field name made lowercase.
    pdvrsppgt = models.CharField(db_column='PdvRspPgt', max_length=13, blank=True, null=True)  # Field name made lowercase.
    pdvcandat = models.DateTimeField(db_column='PdvCanDat', blank=True, null=True, db_comment='data de cancelamento do pedido')  # Field name made lowercase.
    pdvfrecal = models.CharField(db_column='PdvFreCal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtotped = models.DecimalField(db_column='PdvTotPed', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfrefxa = models.SmallIntegerField(db_column='PdvFreFxa', blank=True, null=True)  # Field name made lowercase.
    pdvconfir = models.CharField(db_column='PdvConfir', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvromger = models.CharField(db_column='PdvRomGer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtransf = models.CharField(db_column='PdvTransf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvultpro = models.IntegerField(db_column='PdvUltPro', blank=True, null=True)  # Field name made lowercase.
    pdvapesbru = models.DecimalField(db_column='PdvAPesBru', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvapesliq = models.DecimalField(db_column='PdvAPesLiq', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvavolqtd = models.DecimalField(db_column='PdvAVolQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvatuflu = models.CharField(db_column='PdvAtuFlu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvatucon = models.CharField(db_column='PdvAtuCon', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvatuliv = models.CharField(db_column='PdvAtuLiv', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtotflu = models.DecimalField(db_column='PdvTotFlu', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfluabe = models.DecimalField(db_column='PdvFluAbe', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodabe = models.DecimalField(db_column='PdvModAbe', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubabe = models.DecimalField(db_column='PdvSubAbe', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpenden = models.CharField(db_column='PdvPenden', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvstatus = models.CharField(db_column='PdvStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvpvepfx = models.CharField(db_column='PdvPvePfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvpvecod = models.DecimalField(db_column='PdvPveCod', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvbloped = models.CharField(db_column='PdvBloPed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvblocod = models.CharField(db_column='PdvBloCod', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pdvblousr = models.CharField(db_column='PdvBloUsr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvblodat = models.DateTimeField(db_column='PdvBloDat', blank=True, null=True)  # Field name made lowercase.
    pdvmodtenc = models.DecimalField(db_column='PdvModTEnc', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodditm = models.DecimalField(db_column='PdvModDItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotenc = models.DecimalField(db_column='PdvTotEnc', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcanmot = models.CharField(db_column='PdvCanMot', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvcanusr = models.CharField(db_column='PdvCanUsr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvdesaux = models.DecimalField(db_column='PdvDesAux', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvdplsta = models.CharField(db_column='PdvDplSta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvdpldat = models.DateTimeField(db_column='PdvDplDat', blank=True, null=True)  # Field name made lowercase.
    pdvdplusr = models.CharField(db_column='PdvDplUsr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvemitido = models.CharField(db_column='PdvEmitido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvvlrver = models.DecimalField(db_column='PdvVlrVer', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotpro = models.DecimalField(db_column='PdvTotPro', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbasicm = models.DecimalField(db_column='PdvBasIcm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtoticm = models.DecimalField(db_column='PdvTotIcm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbasipi = models.DecimalField(db_column='PdvBasIpi', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotipi = models.DecimalField(db_column='PdvTotIpi', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotdes = models.DecimalField(db_column='PdvTotDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodpro = models.DecimalField(db_column='PdvModPro', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodbic = models.DecimalField(db_column='PdvModBic', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodvic = models.DecimalField(db_column='PdvModVic', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodbip = models.DecimalField(db_column='PdvModBip', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodvip = models.DecimalField(db_column='PdvModVip', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmoddes = models.DecimalField(db_column='PdvModDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodvaldes = models.DecimalField(db_column='PdvModValDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodfre = models.DecimalField(db_column='PdvModFre', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodout = models.DecimalField(db_column='PdvModOut', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodped = models.DecimalField(db_column='PdvModPed', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubped = models.DecimalField(db_column='PdvSubPed', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubbas = models.DecimalField(db_column='PdvSubBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubval = models.DecimalField(db_column='PdvSubVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcomvlrdes = models.DecimalField(db_column='PdvComVlrDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvlocent = models.CharField(db_column='PdvLocEnt', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pdvtotprosemacr = models.DecimalField(db_column='PdvTotProSemAcr', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvnomtra = models.CharField(db_column='PdvNomTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pdvnomred = models.CharField(db_column='PdvNomRed', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pdvlocnro = models.IntegerField(db_column='PdvLocNro', blank=True, null=True)  # Field name made lowercase.
    pdvloccom = models.CharField(db_column='PdvLocCom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pdvlocbai = models.CharField(db_column='PdvLocBai', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pdvloccep = models.CharField(db_column='PdvLocCep', max_length=9, blank=True, null=True)  # Field name made lowercase.
    pdvlocrec = models.CharField(db_column='PdvLocRec', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvhor = models.CharField(db_column='PdvHor', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvpri = models.SmallIntegerField(db_column='PdvPri', blank=True, null=True)  # Field name made lowercase.
    pdvorcger = models.CharField(db_column='PdvOrcGer', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvcontra = models.CharField(db_column='PdvContra', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvapaipfx = models.CharField(db_column='PdvAPaiPfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvapaicod = models.IntegerField(db_column='PdvAPaiCod', blank=True, null=True)  # Field name made lowercase.
    pdvobsnot = models.TextField(db_column='PdvObsNot', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pdvmsgdes = models.CharField(db_column='PdvMsgDes', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pdvobsred = models.CharField(db_column='PdvObsRed', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pdvultpar = models.SmallIntegerField(db_column='PdvUltPar', blank=True, null=True)  # Field name made lowercase.
    pdvultchq = models.SmallIntegerField(db_column='PdvUltChq', blank=True, null=True)  # Field name made lowercase.
    pdvzfmvaldes = models.DecimalField(db_column='PdvZfmValDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtipbai = models.CharField(db_column='PdvTipBai', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pdvbxaest = models.CharField(db_column='PdvBxaEst', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcpgprz = models.CharField(db_column='PdvCpgPrz', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvpdeemp = models.IntegerField(db_column='PdvPdeEmp', blank=True, null=True)  # Field name made lowercase.
    pdvpdecod = models.IntegerField(db_column='PdvPdeCod', blank=True, null=True)  # Field name made lowercase.
    pdvpdetlhcod = models.SmallIntegerField(db_column='PdvPdeTlhCod', blank=True, null=True)  # Field name made lowercase.
    pdvpdetlhscd = models.CharField(db_column='PdvPdeTlhScd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtptemp = models.IntegerField(db_column='PdvTptEmp', blank=True, null=True)  # Field name made lowercase.
    pdvtptcod = models.SmallIntegerField(db_column='PdvTptCod', blank=True, null=True)  # Field name made lowercase.
    pdvoritab = models.CharField(db_column='PdvOriTab', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvtraempzfm = models.IntegerField(db_column='PdvTraEmpZFM', blank=True, null=True)  # Field name made lowercase.
    pdvtradoczfm = models.IntegerField(db_column='PdvTraDocZFM', blank=True, null=True)  # Field name made lowercase.
    pdvtotdesitm = models.DecimalField(db_column='PdvTotDesItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdventtip = models.CharField(db_column='PdvEntTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvemailenv = models.CharField(db_column='PdvEmailEnv', max_length=1)  # Field name made lowercase.
    pdvcombloped = models.CharField(db_column='PdvComBloPed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcomblodat = models.DateTimeField(db_column='PdvComBloDat', blank=True, null=True)  # Field name made lowercase.
    pdvcomblousr = models.CharField(db_column='PdvComBloUsr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvcomblocod = models.CharField(db_column='PdvComBloCod', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pdvtraconval = models.DecimalField(db_column='PdvTraConVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvredconval = models.DecimalField(db_column='PdvRedConVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvlegtotdes = models.DecimalField(db_column='PdvLegTotDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsolting = models.CharField(db_column='PdvSolTing', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtrncod = models.DecimalField(db_column='PdvTrnCod', max_digits=12, decimal_places=0)  # Field name made lowercase.
    pdvulttrc = models.IntegerField(db_column='PdvUltTrc', blank=True, null=True)  # Field name made lowercase.
    pdvtotdescon = models.DecimalField(db_column='PdvTotDesCon', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvultcom = models.SmallIntegerField(db_column='PdvUltCom', blank=True, null=True)  # Field name made lowercase.
    pdvexpembloc = models.CharField(db_column='PdvExpEmbLoc', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pdvexpembestcod = models.CharField(db_column='PdvExpEmbEstCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvcomblotxt = models.CharField(db_column='PdvComBloTxt', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvrttemp = models.IntegerField(db_column='PdvRttEmp', blank=True, null=True)  # Field name made lowercase.
    pdvrttcod = models.IntegerField(db_column='PdvRttCod', blank=True, null=True)  # Field name made lowercase.
    pdvctcfreemp = models.IntegerField(db_column='PdvCtcFreEmp', blank=True, null=True)  # Field name made lowercase.
    pdvctcfrefil = models.IntegerField(db_column='PdvCtcFreFil', blank=True, null=True)  # Field name made lowercase.
    pdvctcfrepfx = models.CharField(db_column='PdvCtcFrePfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvctcfrecod = models.IntegerField(db_column='PdvCtcFreCod', blank=True, null=True)  # Field name made lowercase.
    pdvcpgprzmed = models.SmallIntegerField(db_column='PdvCpgPrzMed', blank=True, null=True)  # Field name made lowercase.
    pdvprcporemb = models.CharField(db_column='PdvPrcPorEmb', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvindemp = models.IntegerField(db_column='PdvIndEmp', blank=True, null=True)  # Field name made lowercase.
    pdvindcod = models.SmallIntegerField(db_column='PdvIndCod', blank=True, null=True)  # Field name made lowercase.
    pdvinddat = models.DateTimeField(db_column='PdvIndDat', blank=True, null=True)  # Field name made lowercase.
    pdvindvlr = models.DecimalField(db_column='PdvIndVlr', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvatuliviss = models.CharField(db_column='PdvAtuLivIss', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvvaldes2 = models.DecimalField(db_column='PdvValDes2', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvadatpar = models.DateTimeField(db_column='PdvADatPar', blank=True, null=True)  # Field name made lowercase.
    pdvusrins = models.CharField(db_column='PdvUsrIns', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvusralt = models.CharField(db_column='PdvUsrAlt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvindpres = models.CharField(db_column='PdvIndPres', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvbasicmpar = models.DecimalField(db_column='PdvBasIcmPar', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtoticmparo = models.DecimalField(db_column='PdvTotIcmParO', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtoticmpard = models.DecimalField(db_column='PdvTotIcmParD', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbasfcp = models.DecimalField(db_column='PdvBasFcp', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotfcp = models.DecimalField(db_column='PdvTotFcp', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvssdseq = models.DecimalField(db_column='PdvSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvgeoloc = models.CharField(db_column='PdvGeoLoc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pdvmsgssd = models.TextField(db_column='PdvMsgSsd', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pdvstatusger = models.SmallIntegerField(db_column='PdvStatusGer', blank=True, null=True)  # Field name made lowercase.
    pdvempenro = models.CharField(db_column='PdvEmpeNro', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pdvcodintegracao1 = models.IntegerField(db_column='PdvCodIntegracao1', blank=True, null=True)  # Field name made lowercase.
    pdvfatadto = models.CharField(db_column='PdvFatAdto', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvfatpar = models.CharField(db_column='PdvFatPar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvvaloutise = models.DecimalField(db_column='PdvValOutIse', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfreiseicm = models.CharField(db_column='PdvFreIseIcm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvtoticmdif = models.DecimalField(db_column='PdvTotIcmDif', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    intvencod = models.IntegerField(db_column='IntVenCod', blank=True, null=True)  # Field name made lowercase.
    intvenfil = models.IntegerField(db_column='IntVenFil', blank=True, null=True)  # Field name made lowercase.
    intvenemp = models.IntegerField(db_column='IntVenEmp', blank=True, null=True)  # Field name made lowercase.
    pdvfreiseipi = models.CharField(db_column='PdvFreIseIpi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcodmarpla = models.CharField(db_column='PdvCodMarPla', max_length=500, blank=True, null=True)  # Field name made lowercase.
    pdvrecdoc = models.IntegerField(db_column='PdvRecDoc', blank=True, null=True)  # Field name made lowercase.
    pdvrecmst = models.IntegerField(db_column='PdvRecMst', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PDV01'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod'),)


class Pdv02(models.Model):
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (PdvEmpCod, PdvFilCod, PdvPfxCod, PdvCod, PdvItmPro) found, that is not supported. The first column is selected.
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')  # Field name made lowercase.
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)  # Field name made lowercase.
    pdvcod = models.IntegerField(db_column='PdvCod')  # Field name made lowercase.
    pdvitmpro = models.IntegerField(db_column='PdvItmPro')  # Field name made lowercase.
    pdvproemp = models.IntegerField(db_column='PdvProEmp', blank=True, null=True)  # Field name made lowercase.
    pdvprocod = models.CharField(db_column='PdvProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvuniemp = models.IntegerField(db_column='PdvUniEmp', blank=True, null=True)  # Field name made lowercase.
    pdvunicod = models.CharField(db_column='PdvUniCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvuniest = models.CharField(db_column='PdvUniEst', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvuniven = models.CharField(db_column='PdvUniVen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvnompro = models.CharField(db_column='PdvNomPro', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvmodnom = models.CharField(db_column='PdvModNom', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvfatcon = models.DecimalField(db_column='PdvFatCon', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtipfat = models.CharField(db_column='PdvTipFat', max_length=13, blank=True, null=True)  # Field name made lowercase.
    pdvqtdpro = models.DecimalField(db_column='PdvQtdPro', max_digits=13, decimal_places=4, blank=True, null=True, db_comment='Quantidade de itens faturado, ')  # Field name made lowercase.
    pdvqtdrea = models.DecimalField(db_column='PdvQtdRea', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvencpro = models.DecimalField(db_column='PdvEncPro', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvprcpro = models.DecimalField(db_column='PdvPrcPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvprcven = models.DecimalField(db_column='PdvPrcVen', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvlisdat = models.DateTimeField(db_column='PdvLisDat', blank=True, null=True)  # Field name made lowercase.
    pdvprclis = models.DecimalField(db_column='PdvPrcLis', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvicmpro = models.DecimalField(db_column='PdvIcmPro', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmred = models.DecimalField(db_column='PdvIcmRed', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmsub = models.DecimalField(db_column='PdvIcmSub', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmint = models.DecimalField(db_column='PdvIcmInt', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsitpro = models.CharField(db_column='PdvSitPro', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvdespro = models.DecimalField(db_column='PdvDesPro', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvdesuni = models.DecimalField(db_column='PdvDesUni', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvalmemp = models.IntegerField(db_column='PdvAlmEmp', blank=True, null=True)  # Field name made lowercase.
    pdvalmcod = models.SmallIntegerField(db_column='PdvAlmCod', blank=True, null=True)  # Field name made lowercase.
    pdvcfoemp = models.IntegerField(db_column='PdvCfoEmp', blank=True, null=True)  # Field name made lowercase.
    pdvcfocod = models.CharField(db_column='PdvCfoCod', max_length=7, blank=True, null=True)  # Field name made lowercase.
    pdvdatent = models.DateTimeField(db_column='PdvDatEnt', blank=True, null=True, db_comment='Data que foi faturado o pedido')  # Field name made lowercase.
    pdvprzent = models.SmallIntegerField(db_column='PdvPrzEnt', blank=True, null=True)  # Field name made lowercase.
    pdvprvent = models.DateTimeField(db_column='PdvPrvEnt', blank=True, null=True, db_comment='Data de previsao de entrega')  # Field name made lowercase.
    pdvprvsai = models.DateTimeField(db_column='PdvPrvSai', blank=True, null=True)  # Field name made lowercase.
    pdvnfsser = models.CharField(db_column='PdvNfsSer', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvnfsnro = models.IntegerField(db_column='PdvNfsNro', blank=True, null=True, db_comment='Numero da nota fiscal de saida')  # Field name made lowercase.
    pdvipisus = models.CharField(db_column='PdvIpiSus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvipipro = models.DecimalField(db_column='PdvIpiPro', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvipiapu = models.CharField(db_column='PdvIpiApu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvembcod = models.CharField(db_column='PdvEmbCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvembqtd = models.DecimalField(db_column='PdvEmbQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvembcap = models.DecimalField(db_column='PdvEmbCap', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvembmul = models.DecimalField(db_column='PdvEmbMul', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpedcli = models.CharField(db_column='PdvPedCli', max_length=15, blank=True, null=True, db_comment='Numero da ordem e compra do cl')  # Field name made lowercase.
    pdvemicli = models.DateTimeField(db_column='PdvEmiCli', blank=True, null=True)  # Field name made lowercase.
    pdvmodprc = models.DecimalField(db_column='PdvModPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodlis = models.DecimalField(db_column='PdvModLis', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodpor1 = models.DecimalField(db_column='PdvModPor1', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodpor2 = models.DecimalField(db_column='PdvModPor2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodpor3 = models.DecimalField(db_column='PdvModPor3', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtipven = models.CharField(db_column='PdvTipVen', max_length=16, blank=True, null=True)  # Field name made lowercase.
    pdvconfer = models.CharField(db_column='PdvConfer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvconini = models.CharField(db_column='PdvConIni', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvoprprg = models.CharField(db_column='PdvOprPrg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvoprpfx = models.CharField(db_column='PdvOprPfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvoprcod = models.IntegerField(db_column='PdvOprCod', blank=True, null=True)  # Field name made lowercase.
    pdvcomnom = models.CharField(db_column='PdvComNom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pdvpfxent = models.CharField(db_column='PdvPfxEnt', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvnroent = models.DecimalField(db_column='PdvNroEnt', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvgddemp1 = models.IntegerField(db_column='PdvGddEmp1', blank=True, null=True)  # Field name made lowercase.
    pdvgddgdr1 = models.CharField(db_column='PdvGddGdr1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvgddcod1 = models.CharField(db_column='PdvGddCod1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvgddemp2 = models.IntegerField(db_column='PdvGddEmp2', blank=True, null=True)  # Field name made lowercase.
    pdvgddgdr2 = models.CharField(db_column='PdvGddGdr2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvgddcod2 = models.CharField(db_column='PdvGddCod2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvgddemp3 = models.IntegerField(db_column='PdvGddEmp3', blank=True, null=True)  # Field name made lowercase.
    pdvgddgdr3 = models.CharField(db_column='PdvGddGdr3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvgddcod3 = models.CharField(db_column='PdvGddCod3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvlocest = models.CharField(db_column='PdvLocEst', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pdvbtplemp = models.IntegerField(db_column='PdvBTplEmp', blank=True, null=True)  # Field name made lowercase.
    pdvbtplcod = models.SmallIntegerField(db_column='PdvBTplCod', blank=True, null=True)  # Field name made lowercase.
    pdvbtipmov = models.CharField(db_column='PdvBTipMov', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvnrolot = models.CharField(db_column='PdvNroLot', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pdvblotfin = models.CharField(db_column='PdvBLotFin', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pdvbcomvlrdes = models.DecimalField(db_column='PdvBComVlrDes', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbcomvlrmod = models.DecimalField(db_column='PdvBComVlrMod', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbpronomdet = models.TextField(db_column='PdvBProNomDet', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pdvbvlrtot = models.DecimalField(db_column='PdvBVlrTot', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbicmdesvlr = models.DecimalField(db_column='PdvBIcmDesVlr', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbremqtd = models.DecimalField(db_column='PdvBRemQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvemipro = models.DateTimeField(db_column='PdvEmiPro', blank=True, null=True)  # Field name made lowercase.
    pdvdigpro = models.DateTimeField(db_column='PdvDigPro', blank=True, null=True)  # Field name made lowercase.
    pdvpeccxa = models.SmallIntegerField(db_column='PdvPecCxa', blank=True, null=True)  # Field name made lowercase.
    pdvpespro = models.DecimalField(db_column='PdvPesPro', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpesbru = models.DecimalField(db_column='PdvPesBru', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpesgal = models.DecimalField(db_column='PdvPesGal', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotpes = models.DecimalField(db_column='PdvTotPes', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotgal = models.DecimalField(db_column='PdvTotGal', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmbas = models.DecimalField(db_column='PdvIcmBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmval = models.DecimalField(db_column='PdvIcmVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvipibas = models.DecimalField(db_column='PdvIpiBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvipival = models.DecimalField(db_column='PdvIpiVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodliq = models.DecimalField(db_column='PdvModLiq', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodenc = models.DecimalField(db_column='PdvModEnc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvdi = models.DecimalField(db_column='PdvModVdi', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvdr = models.DecimalField(db_column='PdvModVdr', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvfr = models.DecimalField(db_column='PdvModVfr', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvsg = models.DecimalField(db_column='PdvModVsg', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvod = models.DecimalField(db_column='PdvModVod', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvmodvpr = models.DecimalField(db_column='PdvModVpr', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmoditm = models.DecimalField(db_column='PdvModItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubprc = models.DecimalField(db_column='PdvSubPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubliq = models.DecimalField(db_column='PdvSubLiq', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubitm = models.DecimalField(db_column='PdvSubItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubenc = models.DecimalField(db_column='PdvSubEnc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubvdi = models.DecimalField(db_column='PdvSubVdi', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubvdr = models.DecimalField(db_column='PdvSubVdr', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubvpr = models.DecimalField(db_column='PdvSubVpr', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvdrpro = models.DecimalField(db_column='PdvVdrPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvvfrpro = models.DecimalField(db_column='PdvVfrPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvvsgpro = models.DecimalField(db_column='PdvVsgPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvvodpro = models.DecimalField(db_column='PdvVodPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcondat = models.DateTimeField(db_column='PdvConDat', blank=True, null=True)  # Field name made lowercase.
    pdvlibdat1 = models.DateTimeField(db_column='PdvLibDat1', blank=True, null=True)  # Field name made lowercase.
    pdvlibdat3 = models.DateTimeField(db_column='PdvLibDat3', blank=True, null=True)  # Field name made lowercase.
    pdvprvpro = models.DateTimeField(db_column='PdvPrvPro', blank=True, null=True)  # Field name made lowercase.
    pdvterpro = models.IntegerField(db_column='PdvTerPro', blank=True, null=True)  # Field name made lowercase.
    pdvproblo = models.CharField(db_column='PdvProBlo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvencuni = models.DecimalField(db_column='PdvEncUni', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvencval = models.DecimalField(db_column='PdvEncVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvprcliq = models.DecimalField(db_column='PdvPrcLiq', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvdesval = models.DecimalField(db_column='PdvDesVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvalpro = models.DecimalField(db_column='PdvValPro', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotitm = models.DecimalField(db_column='PdvTotItm', max_digits=19, decimal_places=4, blank=True, null=True, db_comment='Valor total faturado do item, ')  # Field name made lowercase.
    pdvsubvfr = models.DecimalField(db_column='PdvSubVfr', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbsubbas = models.DecimalField(db_column='PdvBSubBas', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbsubval = models.DecimalField(db_column='PdvBSubVal', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvboprobs = models.CharField(db_column='PdvBOprObs', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvboritab = models.CharField(db_column='PdvBOriTab', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvboriid = models.DecimalField(db_column='PdvBOriId', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvboriproqtd = models.DecimalField(db_column='PdvBOriProQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbpaiemp = models.IntegerField(db_column='PdvBPaiEmp', blank=True, null=True)  # Field name made lowercase.
    pdvbpaifil = models.IntegerField(db_column='PdvBPaiFil', blank=True, null=True)  # Field name made lowercase.
    pdvbpaipfx = models.CharField(db_column='PdvBPaiPfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvbpaicod = models.IntegerField(db_column='PdvBPaiCod', blank=True, null=True)  # Field name made lowercase.
    pdvbpaiitm = models.IntegerField(db_column='PdvBPaiItm', blank=True, null=True)  # Field name made lowercase.
    pdvsernro = models.CharField(db_column='PdvSerNro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pdvgarnro = models.CharField(db_column='PdvGarNro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    defcod = models.IntegerField(db_column='DefCod', blank=True, null=True)  # Field name made lowercase.
    pdvobspro = models.CharField(db_column='PdvObsPro', max_length=254, blank=True, null=True)  # Field name made lowercase.
    pdvboriidtxt = models.CharField(db_column='PdvBOriIdTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pdvbzfmvdrpro = models.DecimalField(db_column='PdvBZfmVdrPro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbzfmpordes = models.DecimalField(db_column='PdvBZfmPorDes', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcusmed = models.DecimalField(db_column='PdvCusMed', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcustot = models.DecimalField(db_column='PdvCusTot', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmvgcod = models.DecimalField(db_column='PdvMvgCod', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvqtdfat = models.DecimalField(db_column='PdvQtdFat', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvqtdcan = models.DecimalField(db_column='PdvQtdCan', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvqtdtra = models.DecimalField(db_column='PdvQtdTra', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvdplpor = models.DecimalField(db_column='PdvDplPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbromcar = models.IntegerField(db_column='PdvBRomCar', blank=True, null=True)  # Field name made lowercase.
    pdvicmsubred = models.DecimalField(db_column='PdvIcmSubRed', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcreoutpor = models.DecimalField(db_column='PdvCreOutPor', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmsubredap = models.DecimalField(db_column='PdvIcmSubRedAP', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbdesconpor = models.DecimalField(db_column='PdvBDesConPor', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvprotip = models.CharField(db_column='PdvProTip', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvqtdcom = models.DecimalField(db_column='PdvQtdCom', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvlegvaldes = models.DecimalField(db_column='PdvLegValDes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodtotvis = models.DecimalField(db_column='PdvModTotVis', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodtotliq = models.DecimalField(db_column='PdvModTotLiq', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcreoutval = models.DecimalField(db_column='PdvCreOutVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotvis = models.DecimalField(db_column='PdvTotVis', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvtotliq = models.DecimalField(db_column='PdvTotLiq', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbdesconval = models.DecimalField(db_column='PdvBDesConVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvpedcliitem = models.IntegerField(db_column='PdvPedCliItem', blank=True, null=True)  # Field name made lowercase.
    pdvisscidcli = models.CharField(db_column='PdvIssCidCli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvmargcus = models.DecimalField(db_column='PdvMargCus', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargimp = models.DecimalField(db_column='PdvMargImp', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargcom = models.DecimalField(db_column='PdvMargCom', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargfre = models.DecimalField(db_column='PdvMargFre', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargout = models.DecimalField(db_column='PdvMargOut', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargval = models.DecimalField(db_column='PdvMargVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmargpor = models.DecimalField(db_column='PdvMargPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbcommargval = models.DecimalField(db_column='PdvBComMargVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbcommargpor = models.DecimalField(db_column='PdvBComMargPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mbxcod = models.SmallIntegerField(db_column='MbxCod', blank=True, null=True)  # Field name made lowercase.
    pdvsepcod = models.CharField(db_column='PdvSepCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvponpro = models.IntegerField(db_column='PdvPonPro', blank=True, null=True)  # Field name made lowercase.
    pdvcorcod = models.CharField(db_column='PdvCorCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvtamcod = models.SmallIntegerField(db_column='PdvTamCod', blank=True, null=True)  # Field name made lowercase.
    pdvqzncod = models.CharField(db_column='PdvQznCod', max_length=8, blank=True, null=True)  # Field name made lowercase.
    pdvlibdat2 = models.DateTimeField(db_column='PdvLibDat2', blank=True, null=True)  # Field name made lowercase.
    pdvtrcprocod = models.CharField(db_column='PdvTrcProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvtrccorcod = models.CharField(db_column='PdvTrcCorCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvgfcemp = models.IntegerField(db_column='PdvGfcEmp', blank=True, null=True)  # Field name made lowercase.
    pdvgfccod = models.IntegerField(db_column='PdvGfcCod', blank=True, null=True)  # Field name made lowercase.
    pdvprotag = models.CharField(db_column='PdvProTAG', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pdvunf = models.CharField(db_column='PdvUnf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcxa = models.CharField(db_column='PdvCxa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcalcqtd = models.DecimalField(db_column='PdvCalcQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcalcprc = models.DecimalField(db_column='PdvCalcPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcalcdesuni = models.DecimalField(db_column='PdvCalcDesUni', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcalcencuni = models.DecimalField(db_column='PdvCalcEncUni', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvindtip = models.CharField(db_column='PdvIndTip', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdvindbase = models.CharField(db_column='PdvIndBase', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvproprc2 = models.DecimalField(db_column='PdvProPrc2', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvbpdeemp = models.IntegerField(db_column='PdvBPdeEmp', blank=True, null=True)  # Field name made lowercase.
    pdvbpdecod = models.IntegerField(db_column='PdvBPdeCod', blank=True, null=True)  # Field name made lowercase.
    pdvbpdetlhcod = models.SmallIntegerField(db_column='PdvBPdeTlhCod', blank=True, null=True)  # Field name made lowercase.
    pdvbpdetlhscd = models.CharField(db_column='PdvBPdeTlhScd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvicmsitori = models.CharField(db_column='PdvIcmSitOri', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvicmsitpro = models.CharField(db_column='PdvIcmSitPro', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvdesval2 = models.DecimalField(db_column='PdvDesVal2', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvqtdpec = models.DecimalField(db_column='PdvQtdPec', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvqtdcnj = models.DecimalField(db_column='PdvQtdCnj', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvqtdpec2 = models.DecimalField(db_column='PdvQtdPec2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmparbas = models.DecimalField(db_column='PdvIcmParBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmparali = models.DecimalField(db_column='PdvIcmParAli', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmparvalo = models.DecimalField(db_column='PdvIcmParValO', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmparvald = models.DecimalField(db_column='PdvIcmParValD', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfcpali = models.DecimalField(db_column='PdvFcpAli', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfcpbas = models.DecimalField(db_column='PdvFcpBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvfcpval = models.DecimalField(db_column='PdvFcpVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvssdsinerr = models.CharField(db_column='PdvSsdSinErr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvbicmreddes = models.DecimalField(db_column='PdvBIcmRedDes', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbsubbastip = models.CharField(db_column='PdvBSubBasTip', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvbicmbastip = models.CharField(db_column='PdvBIcmBasTip', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvicmparbastip = models.CharField(db_column='PdvIcmParBasTip', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvbicmdesmot = models.CharField(db_column='PdvBIcmDesMot', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pdvprventori = models.DateTimeField(db_column='PdvPrvEntOri', blank=True, null=True)  # Field name made lowercase.
    pdvvlrintegracao1 = models.DecimalField(db_column='PdvVlrIntegracao1', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvsubbru = models.DecimalField(db_column='PdvSubBru', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubpes = models.DecimalField(db_column='PdvSubPes', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubemb = models.DecimalField(db_column='PdvSubEmb', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubrea = models.DecimalField(db_column='PdvSubRea', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubqtd = models.DecimalField(db_column='PdvSubQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodbru = models.DecimalField(db_column='PdvModBru', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodpes = models.DecimalField(db_column='PdvModPes', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodemb = models.DecimalField(db_column='PdvModEmb', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodrea = models.DecimalField(db_column='PdvModRea', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodqtd = models.DecimalField(db_column='PdvModQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbmbxhis = models.CharField(db_column='PdvBMbxHis', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    pdvlibhor3 = models.DateTimeField(db_column='PdvLibHor3', blank=True, null=True)  # Field name made lowercase.
    pdvlibhor2 = models.DateTimeField(db_column='PdvLibHor2', blank=True, null=True)  # Field name made lowercase.
    pdvlibhor1 = models.DateTimeField(db_column='PdvLibHor1', blank=True, null=True)  # Field name made lowercase.
    pdvbressta = models.CharField(db_column='PdvBResSta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvitmorides = models.IntegerField(db_column='PdvItmOriDes', blank=True, null=True)  # Field name made lowercase.
    pdvproenv = models.CharField(db_column='PdvProEnv', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvvodisepro = models.DecimalField(db_column='PdvVodIsePro', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvicmdifval = models.DecimalField(db_column='PdvIcmDifVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvicmdifali = models.DecimalField(db_column='PdvIcmDifAli', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvbpri = models.CharField(db_column='PdvBPri', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvnumrec = models.CharField(db_column='PdvNumRec', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PDV02'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvitmpro'),)


class Pdv03(models.Model):
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (PdvEmpCod, PdvFilCod, PdvPfxCod, PdvCod, PdvCItmCom) found, that is not supported. The first column is selected.
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')  # Field name made lowercase.
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)  # Field name made lowercase.
    pdvcod = models.IntegerField(db_column='PdvCod')  # Field name made lowercase.
    pdvcitmcom = models.SmallIntegerField(db_column='PdvCItmCom')  # Field name made lowercase.
    pdvcrepemp = models.IntegerField(db_column='PdvCRepEmp', blank=True, null=True)  # Field name made lowercase.
    pdvcrepdoc = models.IntegerField(db_column='PdvCRepDoc', blank=True, null=True)  # Field name made lowercase.
    pdvcreptip = models.CharField(db_column='PdvCRepTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvcdattab = models.DateTimeField(db_column='PdvCDatTab', blank=True, null=True)  # Field name made lowercase.
    pdvccompor = models.DecimalField(db_column='PdvCComPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvccomprc = models.DecimalField(db_column='PdvCComPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvccombas = models.DecimalField(db_column='PdvCComBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvccomval = models.DecimalField(db_column='PdvCComVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcsbppor = models.DecimalField(db_column='PdvCSbpPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcsbpbas = models.DecimalField(db_column='PdvCSbpBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcsbpval = models.DecimalField(db_column='PdvCSbpVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmodbas = models.DecimalField(db_column='PdvCModBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmodval = models.DecimalField(db_column='PdvCModVal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcitmped = models.IntegerField(db_column='PdvCItmPed', blank=True, null=True)  # Field name made lowercase.
    pdvcproemp = models.IntegerField(db_column='PdvCProEmp', blank=True, null=True)  # Field name made lowercase.
    pdvcprocod = models.CharField(db_column='PdvCProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcprogru = models.IntegerField(db_column='PdvCProGru', blank=True, null=True)  # Field name made lowercase.
    pdvcproart = models.DecimalField(db_column='PdvCProArt', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pdvcprotam = models.CharField(db_column='PdvCProTam', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pdvcproqtd = models.DecimalField(db_column='PdvCProQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcproqtr = models.DecimalField(db_column='PdvCProQtr', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcprocan = models.DecimalField(db_column='PdvCProCan', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcunicod = models.CharField(db_column='PdvCUniCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pdvcembcod = models.CharField(db_column='PdvCEmbCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcembqtd = models.DecimalField(db_column='PdvCEmbQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcprclis = models.DecimalField(db_column='PdvCPrcLis', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcprcven = models.DecimalField(db_column='PdvCPrcVen', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcprcliq = models.DecimalField(db_column='PdvCPrcLiq', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcprcenc = models.DecimalField(db_column='PdvCPrcEnc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcmodlis = models.DecimalField(db_column='PdvCModLis', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcmodven = models.DecimalField(db_column='PdvCModVen', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcmodliq = models.DecimalField(db_column='PdvCModLiq', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvcmodpor = models.DecimalField(db_column='PdvCModPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmodenc = models.DecimalField(db_column='PdvCModEnc', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcipipor = models.DecimalField(db_column='PdvCIpiPor', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcencpor = models.DecimalField(db_column='PdvCEncPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcdespor = models.DecimalField(db_column='PdvCDesPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcentprv = models.DateTimeField(db_column='PdvCEntPrv', blank=True, null=True)  # Field name made lowercase.
    pdvcentdat = models.DateTimeField(db_column='PdvCEntDat', blank=True, null=True)  # Field name made lowercase.
    pdvcgddgdr1 = models.CharField(db_column='PdvCGddGdr1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcgddcod1 = models.CharField(db_column='PdvCGddCod1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcgddgdr2 = models.CharField(db_column='PdvCGddGdr2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcgddcod2 = models.CharField(db_column='PdvCGddCod2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcgddgdr3 = models.CharField(db_column='PdvCGddGdr3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcgddcod3 = models.CharField(db_column='PdvCGddCod3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvctotitm = models.DecimalField(db_column='PdvCTotItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvccomtip = models.CharField(db_column='PdvCComTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvccomvlrdes = models.DecimalField(db_column='PdvCComVlrDes', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    pdvctplcod = models.SmallIntegerField(db_column='PdvCTplCod', blank=True, null=True)  # Field name made lowercase.
    pdvctotliq = models.DecimalField(db_column='PdvCTotLiq', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmoditm = models.DecimalField(db_column='PdvCModItm', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcvlrtot = models.DecimalField(db_column='PdvCVlrTot', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvctotvis = models.DecimalField(db_column='PdvCTotVis', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmodtotvis = models.DecimalField(db_column='PdvCModTotVis', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcmodtotliq = models.DecimalField(db_column='PdvCModTotLiq', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvcsaiprv = models.DateTimeField(db_column='PdvCSaiPrv', blank=True, null=True)  # Field name made lowercase.
    pdvcproenv = models.CharField(db_column='PdvCProEnv', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdvcpthger = models.CharField(db_column='PdvCPthGer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvccomvalori = models.DecimalField(db_column='PdvCComValOri', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvccomporori = models.DecimalField(db_column='PdvCComPorOri', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PDV03'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvcitmcom'),)


class Pdv04(models.Model):
    """ Parcelas do Pedido de Venda """
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)
    pdvcod = models.IntegerField(db_column='PdvCod')
    pdvitmpar = models.SmallIntegerField(db_column='PdvItmPar')
    pdvvenpra = models.SmallIntegerField(db_column='PdvVenPra', blank=True, null=True)
    pdvvenpar = models.DateTimeField(db_column='PdvVenPar', blank=True, null=True)
    pdvvalpar = models.DecimalField(db_column='PdvValPar', max_digits=19, decimal_places=4, blank=True, null=True)
    pdvvenrea = models.DateTimeField(db_column='PdvVenRea', blank=True, null=True)
    pdvpartip = models.CharField(db_column='PdvParTip', max_length=1, blank=True, null=True)
    pdvparpor = models.DecimalField(db_column='PdvParPor', max_digits=10, decimal_places=4, blank=True, null=True)
    pdvparevedat = models.DateTimeField(db_column='PdvParEveDat', blank=True, null=True)
    pdvparevetxt = models.CharField(db_column='PdvParEveTxt', max_length=100, blank=True, null=True)
    pdvparadtbxa = models.DateTimeField(db_column='PdvParAdtBxa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pdv04'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvitmpar'),)


class Pdv06(models.Model):
    """ Observações do Pedido de Venda """
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)
    pdvcod = models.IntegerField(db_column='PdvCod')
    pdvobsitm = models.SmallIntegerField(db_column='PdvObsItm')
    pdvobsdet = models.TextField(db_column='PdvObsDet', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pdv06'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvobsitm'),)


# --- FAMÍLIA DE MODELOS FTM, FTC, FTD (FICHA TÉCNICA) E TEQ ---

class Ftm01(models.Model):
    """ Ficha Técnica de Material (Cabeçalho) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmanom = models.CharField(db_column='FtmANom', max_length=30, blank=True, null=True)
    ftmamtgemp = models.IntegerField(db_column='FtmAMtgEmp', blank=True, null=True)
    ftmamtgcod = models.SmallIntegerField(db_column='FtmAMtgCod', blank=True, null=True,
                                          help_text="Código do Grupo de Material")
    ftmatipcil = models.CharField(db_column='FtmATipCil', max_length=2, blank=True, null=True)
    ftmatipren = models.CharField(db_column='FtmATipRen', max_length=1, blank=True, null=True)
    ftmacam = models.SmallIntegerField(db_column='FtmACam', blank=True, null=True, help_text="Número de Camadas")
    ftmacic = models.SmallIntegerField(db_column='FtmACic', blank=True, null=True)
    ftmacicuni = models.CharField(db_column='FtmACicUni', max_length=1, blank=True, null=True)
    ftmarpm = models.CharField(db_column='FtmARpm', max_length=20, blank=True, null=True)
    ftmatemmas = models.SmallIntegerField(db_column='FtmATemMas', blank=True, null=True)
    ftmatemcil = models.SmallIntegerField(db_column='FtmATemCil', blank=True, null=True)
    ftmateqemp = models.IntegerField(db_column='FtmATeqEmp', blank=True, null=True,
                                     help_text="Código da Empresa do Equipamento")
    ftmateqcod = models.IntegerField(db_column='FtmATeqCod', blank=True, null=True, help_text="Código do Equipamento")
    ftmatipreg = models.CharField(db_column='FtmATipReg', max_length=1, blank=True, null=True)
    ftmaadiprg = models.DecimalField(db_column='FtmAAdiPrg', max_digits=10, decimal_places=4, blank=True, null=True)
    ftmablqren = models.CharField(db_column='FtmABlqRen', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm01'
        unique_together = (('ftmaempcod', 'ftmacod'),)


class Ftm02(models.Model):
    """ Ficha Técnica de Material (Detalhes) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmdtam = models.CharField(db_column='FtmDTam', max_length=10)
    ftmdespbru = models.DecimalField(db_column='FtmDEspBru', max_digits=10, decimal_places=4, blank=True, null=True)
    ftmdespaca = models.DecimalField(db_column='FtmDEspAca', max_digits=10, decimal_places=4, blank=True, null=True)
    ftmdcilmed = models.DecimalField(db_column='FtmDCilMed', max_digits=9, decimal_places=4, blank=True, null=True)
    ftmdren = models.DecimalField(db_column='FtmDRen', max_digits=13, decimal_places=4, blank=True, null=True)
    ftmdapr = models.DecimalField(db_column='FtmDApr', max_digits=10, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm02'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmdtam'),)


class Ftm03(models.Model):
    """ Ficha Técnica de Material (Componentes) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmgitm = models.SmallIntegerField(db_column='FtmGItm')
    ftmgdes = models.CharField(db_column='FtmGDes', max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm03'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmgitm'),)


class Ftm04(models.Model):
    """ Ficha Técnica de Material (Artigos) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmeart = models.DecimalField(db_column='FtmEArt', max_digits=10, decimal_places=0)
    ftmeobs = models.CharField(db_column='FtmEObs', max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm04'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmeart'),)


class Ftm05(models.Model):
    """ Ficha Técnica de Material (Composição) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmbitm = models.SmallIntegerField(db_column='FtmBItm', help_text="Número do Item / Camada")
    ftmbpor = models.DecimalField(db_column='FtmBPor', max_digits=10, decimal_places=4, blank=True, null=True)
    ftmbfix = models.CharField(db_column='FtmBFix', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm05'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmbitm'),)


class Ftm06(models.Model):
    """ Ficha Técnica de Material (Observações) """
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)
    ftmacod = models.IntegerField(db_column='FtmACod')
    ftmhitm = models.SmallIntegerField(db_column='FtmHItm')
    ftmhobs = models.TextField(db_column='FtmHObs', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftm06'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmhitm'),)


class Ftd01(models.Model):
    """ Ficha Técnica de Grade (Cabeçalho) """
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)
    gddgdrcod = models.CharField(db_column='GddGdrCod', max_length=12)
    gddcod = models.CharField(db_column='GddCod', max_length=12)
    mtgcod = models.SmallIntegerField(db_column='MtgCod')
    gddempcod = models.IntegerField(db_column='GddEmpCod', blank=True, null=True)
    ftdagr = models.CharField(db_column='FtdAgr', max_length=12, blank=True, null=True)
    ftdultitm = models.SmallIntegerField(db_column='FtdUltItm', blank=True, null=True)
    fdtssdseq = models.DecimalField(db_column='FdtSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftd01'
        unique_together = (('mstcod', 'gddgdrcod', 'gddcod', 'mtgcod'),)


class Ftd02(models.Model):
    """ Ficha Técnica de Grade - Itens """
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)
    gddgdrcod = models.CharField(db_column='GddGdrCod', max_length=12)
    gddcod = models.CharField(db_column='GddCod', max_length=12)
    mtgcod = models.SmallIntegerField(db_column='MtgCod')
    ftditm = models.SmallIntegerField(db_column='FtdItm', help_text="Número do Item / Camada")
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', blank=True, null=True)
    ftcacod = models.CharField(db_column='FtcACod', max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftd02'
        unique_together = (('mstcod', 'gddgdrcod', 'gddcod', 'mtgcod', 'ftditm'),)


class Ftc01(models.Model):
    """ Cabeçalho de Fórmulas """
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', primary_key=True)
    ftcacod = models.CharField(db_column='FtcACod', max_length=5)
    ftcanom = models.CharField(db_column='FtcANom', max_length=30, blank=True, null=True)
    ftcaqtdbas = models.DecimalField(db_column='FtcAQtdBas', max_digits=19, decimal_places=4, blank=True, null=True)
    ftcauniemp = models.IntegerField(db_column='FtcAUniEmp', blank=True, null=True)
    ftcaunicod = models.CharField(db_column='FtcAUniCod', max_length=3, blank=True, null=True)
    ftcatotmp = models.DecimalField(db_column='FtcATotMp', max_digits=19, decimal_places=4, blank=True, null=True)
    ftcaultmp = models.SmallIntegerField(db_column='FtcAUltMp', blank=True, null=True)
    mstcod = models.IntegerField(db_column='MstCod', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftc01'
        unique_together = (('ftcaempcod', 'ftcacod'),)


class Ftc02(models.Model):
    """ Itens da Fórmula Química """
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', primary_key=True)
    ftcacod = models.CharField(db_column='FtcACod', max_length=5)
    ftcbitm = models.SmallIntegerField(db_column='FtcBItm', help_text="Sequência do item na fórmula")
    ftcbproemp = models.IntegerField(db_column='FtcBProEmp', blank=True, null=True)
    ftcbprocod = models.CharField(db_column='FtcBProCod', max_length=12, blank=True, null=True)
    ftcbqtd = models.DecimalField(db_column='FtcBQtd', max_digits=19, decimal_places=4, blank=True, null=True)
    ftcbuniemp = models.IntegerField(db_column='FtcBUniEmp', blank=True, null=True)
    ftcbunicod = models.CharField(db_column='FtcBUniCod', max_length=3, blank=True, null=True)
    ftcbqtdfix = models.CharField(db_column='FtcBQtdFix', max_length=1, blank=True, null=True)
    ftcbindper = models.DecimalField(db_column='FtcBIndPer', max_digits=10, decimal_places=4, blank=True, null=True)
    ftcbobs = models.CharField(db_column='FtcBObs', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ftc02'
        unique_together = (('ftcaempcod', 'ftcacod', 'ftcbitm'),)


class Teq01(models.Model):
    """ Cadastro de Equipamentos """
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)
    teqcod = models.IntegerField(db_column='TeqCod')
    teqnom = models.CharField(db_column='TeqNom', max_length=50, blank=True, null=True)
    teqsta = models.CharField(db_column='TeqSta', max_length=7)
    teqtipreg = models.CharField(db_column='TeqTipReg', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teq01'
        unique_together = (('mstcod', 'teqcod'),)
