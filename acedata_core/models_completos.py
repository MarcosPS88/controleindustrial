class Emb01(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, EmbCod) found, that is not supported. The first column is selected.
    embcod = models.CharField(db_column='EmbCod', max_length=12)  # Field name made lowercase.
    embempcod = models.IntegerField(db_column='EmbEmpCod')  # Field name made lowercase.
    embdat = models.DateTimeField(db_column='EmbDat', blank=True, null=True)  # Field name made lowercase.
    embsta = models.CharField(db_column='EmbSta', max_length=7, blank=True, null=True)  # Field name made lowercase.
    embnom = models.CharField(db_column='EmbNom', max_length=120, blank=True, null=True)  # Field name made lowercase.
    embabr = models.CharField(db_column='EmbAbr', max_length=15, blank=True, null=True)  # Field name made lowercase.
    embconest = models.CharField(db_column='EmbConEst', max_length=13, blank=True, null=True)  # Field name made lowercase.
    embgruemp = models.IntegerField(db_column='EmbGruEmp', blank=True, null=True)  # Field name made lowercase.
    embgrucod = models.IntegerField(db_column='EmbGruCod', blank=True, null=True)  # Field name made lowercase.
    embmaremp = models.IntegerField(db_column='EmbMarEmp', blank=True, null=True)  # Field name made lowercase.
    embmarcod = models.IntegerField(db_column='EmbMarCod', blank=True, null=True)  # Field name made lowercase.
    embloc = models.CharField(db_column='EmbLoc', max_length=15, blank=True, null=True)  # Field name made lowercase.
    embempune = models.IntegerField(db_column='EmbEmpUne', blank=True, null=True)  # Field name made lowercase.
    embuniest = models.CharField(db_column='EmbUniEst', max_length=3, blank=True, null=True)  # Field name made lowercase.
    embempunv = models.IntegerField(db_column='EmbEmpUnv', blank=True, null=True)  # Field name made lowercase.
    embuniven = models.CharField(db_column='EmbUniVen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    embempunc = models.IntegerField(db_column='EmbEmpUnc', blank=True, null=True)  # Field name made lowercase.
    embunicom = models.CharField(db_column='EmbUniCom', max_length=3, blank=True, null=True)  # Field name made lowercase.
    embtemgar = models.SmallIntegerField(db_column='EmbTemGar', blank=True, null=True)  # Field name made lowercase.
    embtipgar = models.CharField(db_column='EmbTipGar', max_length=3, blank=True, null=True)  # Field name made lowercase.
    embpes = models.DecimalField(db_column='EmbPes', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embcomcus = models.CharField(db_column='EmbComCus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embalmemp = models.IntegerField(db_column='EmbAlmEmp', blank=True, null=True)  # Field name made lowercase.
    embalmcod = models.SmallIntegerField(db_column='EmbAlmCod', blank=True, null=True)  # Field name made lowercase.
    embreptem = models.SmallIntegerField(db_column='EmbRepTem', blank=True, null=True)  # Field name made lowercase.
    emblotide = models.DecimalField(db_column='EmbLotIde', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    emblotmin = models.DecimalField(db_column='EmbLotMin', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    emblotmax = models.DecimalField(db_column='EmbLotMax', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embqtdpad = models.DecimalField(db_column='EmbQtdPad', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embqtdmul = models.DecimalField(db_column='EmbQtdMul', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embcollis = models.CharField(db_column='EmbColLis', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embcattip = models.CharField(db_column='EmbCatTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embiqqemp = models.IntegerField(db_column='EmbIqqEmp', blank=True, null=True)  # Field name made lowercase.
    embiqqcod = models.SmallIntegerField(db_column='EmbIqqCod', blank=True, null=True)  # Field name made lowercase.
    embfatcon = models.DecimalField(db_column='EmbFatCon', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embfattip = models.CharField(db_column='EmbFatTip', max_length=13, blank=True, null=True)  # Field name made lowercase.
    stpcod = models.SmallIntegerField(db_column='StpCod', blank=True, null=True)  # Field name made lowercase.
    embvlrven = models.DecimalField(db_column='EmbVlrVen', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    embrefuniemp = models.IntegerField(db_column='EmbRefUniEmp', blank=True, null=True)  # Field name made lowercase.
    embrefunicod = models.CharField(db_column='EmbRefUniCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    embfabcod = models.CharField(db_column='EmbFabCod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    embori = models.CharField(db_column='EmbOri', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embras = models.CharField(db_column='EmbRas', max_length=6, blank=True, null=True)  # Field name made lowercase.
    embcencod = models.IntegerField(db_column='EmbCenCod', blank=True, null=True)  # Field name made lowercase.
    embcenemp = models.IntegerField(db_column='EmbCenEmp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EMB01'
        unique_together = (('mstcod', 'embcod'),)

class Ter01(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    tercod = models.IntegerField(db_column='TerCod', blank=True, null=True)  # Field name made lowercase.
    tercpf = models.CharField(db_column='TerCpf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tertipdoc = models.CharField(db_column='TerTipDoc', max_length=6, blank=True, null=True)  # Field name made lowercase.
    terdoccon = models.CharField(db_column='TerDocCon', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terdat = models.DateTimeField(db_column='TerDat', blank=True, null=True)  # Field name made lowercase.
    tersta = models.CharField(db_column='TerSta', max_length=7, blank=True, null=True)  # Field name made lowercase.
    tertip = models.CharField(db_column='TerTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternom = models.CharField(db_column='TerNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terraz = models.CharField(db_column='TerRaz', max_length=50, blank=True, null=True)  # Field name made lowercase.
    termod = models.CharField(db_column='TerMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terinstip = models.CharField(db_column='TerInsTip', max_length=6, blank=True, null=True)  # Field name made lowercase.
    terinsest = models.CharField(db_column='TerInsEst', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terinsmun = models.CharField(db_column='TerInsMun', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terendfat = models.CharField(db_column='TerEndFat', max_length=60, blank=True, null=True)  # Field name made lowercase.
    terfatnro = models.IntegerField(db_column='TerFatNro', blank=True, null=True)  # Field name made lowercase.
    terfatcom = models.CharField(db_column='TerFatCom', max_length=60, blank=True, null=True)  # Field name made lowercase.
    terbaifat = models.CharField(db_column='TerBaiFat', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tercidcodf = models.IntegerField(db_column='TerCidCodF', blank=True, null=True)  # Field name made lowercase.
    tercepfat = models.CharField(db_column='TerCepFat', max_length=9, blank=True, null=True)  # Field name made lowercase.
    tercxpfat = models.IntegerField(db_column='TerCxpFat', blank=True, null=True)  # Field name made lowercase.
    terccpfat = models.CharField(db_column='TerCcpFat', max_length=9, blank=True, null=True)  # Field name made lowercase.
    terfon1 = models.CharField(db_column='TerFon1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfax1 = models.CharField(db_column='TerFax1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfon2 = models.CharField(db_column='TerFon2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfax2 = models.CharField(db_column='TerFax2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfon3 = models.CharField(db_column='TerFon3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfax3 = models.CharField(db_column='TerFax3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terema = models.CharField(db_column='TerEma', max_length=150, blank=True, null=True)  # Field name made lowercase.
    terhom = models.CharField(db_column='TerHom', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tercli = models.CharField(db_column='TerCli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    teralu = models.CharField(db_column='TerAlu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terfor = models.CharField(db_column='TerFor', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terrep = models.CharField(db_column='TerRep', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertra = models.CharField(db_column='TerTra', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tercol = models.CharField(db_column='TerCol', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tercon = models.CharField(db_column='TerCon', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmk = models.CharField(db_column='TerTmk', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksta = models.CharField(db_column='TerTmkSta', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tericm = models.CharField(db_column='TerIcm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terultban = models.SmallIntegerField(db_column='TerUltBan', blank=True, null=True)  # Field name made lowercase.
    terultent = models.SmallIntegerField(db_column='TerUltEnt', blank=True, null=True)  # Field name made lowercase.
    tercplaemp = models.IntegerField(db_column='TerCPlaEmp', blank=True, null=True)  # Field name made lowercase.
    tercplacod = models.IntegerField(db_column='TerCPlaCod', blank=True, null=True)  # Field name made lowercase.
    terfplaemp = models.IntegerField(db_column='TerFPlaEmp', blank=True, null=True)  # Field name made lowercase.
    terfplacod = models.IntegerField(db_column='TerFPlaCod', blank=True, null=True)  # Field name made lowercase.
    terenqfed = models.CharField(db_column='TerEnqFed', max_length=5, blank=True, null=True)  # Field name made lowercase.
    terenqest = models.CharField(db_column='TerEnqEst', max_length=5, blank=True, null=True)  # Field name made lowercase.
    terusrins = models.CharField(db_column='TerUsrIns', max_length=100, blank=True, null=True)  # Field name made lowercase.
    terusralt = models.CharField(db_column='TerUsrAlt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sttcod = models.SmallIntegerField(db_column='SttCod', blank=True, null=True)  # Field name made lowercase.
    teradm = models.CharField(db_column='TerAdm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    terinssuf = models.CharField(db_column='TerInsSuf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tersufdes = models.DecimalField(db_column='TerSufDes', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    terstaqua = models.CharField(db_column='TerStaQua', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ternas = models.DateTimeField(db_column='TerNas', blank=True, null=True)  # Field name made lowercase.
    ternompai = models.CharField(db_column='TerNomPai', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ternommae = models.CharField(db_column='TerNomMae', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tercpfrsp = models.CharField(db_column='TerCpfRsp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terrgrsp = models.CharField(db_column='TerRGRsp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terape = models.CharField(db_column='TerApe', max_length=8, blank=True, null=True)  # Field name made lowercase.
    terestciv = models.CharField(db_column='TerEstCiv', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terprof = models.CharField(db_column='TerProf', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ternac = models.CharField(db_column='TerNac', max_length=2, blank=True, null=True)  # Field name made lowercase.
    terulticd = models.SmallIntegerField(db_column='TerUltIcd', blank=True, null=True)  # Field name made lowercase.
    terultret = models.SmallIntegerField(db_column='TerUltRet', blank=True, null=True)  # Field name made lowercase.
    tercodatu = models.CharField(db_column='TerCodAtu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tercodold = models.CharField(db_column='TerCodOld', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tercodnew = models.CharField(db_column='TerCodNew', max_length=6, blank=True, null=True)  # Field name made lowercase.
    teriseimp = models.CharField(db_column='TerIseImp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tersincon = models.DateTimeField(db_column='TerSinCon', blank=True, null=True)  # Field name made lowercase.
    tercodfor = models.CharField(db_column='TerCodFor', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tercodcli = models.CharField(db_column='TerCodCli', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tersufdesicm = models.CharField(db_column='TerSufDesIcm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tersufdespis = models.CharField(db_column='TerSufDesPis', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tersufdescof = models.CharField(db_column='TerSufDesCof', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tersufdesipi = models.CharField(db_column='TerSufDesIpi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    teremaildanfe = models.CharField(db_column='TerEmailDANFE', max_length=160, blank=True, null=True)  # Field name made lowercase.
    tervissem1 = models.CharField(db_column='TerVisSem1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervissem2 = models.CharField(db_column='TerVisSem2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervissem3 = models.CharField(db_column='TerVisSem3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervissem4 = models.CharField(db_column='TerVisSem4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervisseg = models.CharField(db_column='TerVisSeg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervister = models.CharField(db_column='TerVisTer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervisqua = models.CharField(db_column='TerVisQua', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervisqui = models.CharField(db_column='TerVisQui', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tervissex = models.CharField(db_column='TerVisSex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terpotven = models.DecimalField(db_column='TerPotVen', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    tervissem5 = models.CharField(db_column='TerVisSem5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terultacr = models.DecimalField(db_column='TerUltAcr', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    terproindtot = models.CharField(db_column='TerProIndTot', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternfeemaildanfe = models.CharField(db_column='TerNFeEmailDanfe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternfeemailxml1 = models.CharField(db_column='TerNFeEmailXml1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternfeemailxml2 = models.CharField(db_column='TerNFeEmailXml2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternfeemailtip = models.CharField(db_column='TerNFeEmailTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terponsal = models.IntegerField(db_column='TerPonSal', blank=True, null=True)  # Field name made lowercase.
    ternatret = models.CharField(db_column='TerNatRet', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tercpfnro = models.CharField(db_column='TerCpfNro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tertmksem1 = models.CharField(db_column='TerTmkSem1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksem2 = models.CharField(db_column='TerTmkSem2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksem3 = models.CharField(db_column='TerTmkSem3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksem4 = models.CharField(db_column='TerTmkSem4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksem5 = models.CharField(db_column='TerTmkSem5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmkseg = models.CharField(db_column='TerTmkSeg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmkter = models.CharField(db_column='TerTmkTer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmkqua = models.CharField(db_column='TerTmkQua', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmkqui = models.CharField(db_column='TerTmkQui', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertmksex = models.CharField(db_column='TerTmkSex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terindemp = models.IntegerField(db_column='TerIndEmp', blank=True, null=True)  # Field name made lowercase.
    terinddoc = models.IntegerField(db_column='TerIndDoc', blank=True, null=True)  # Field name made lowercase.
    terindsta = models.CharField(db_column='TerIndSta', max_length=2, blank=True, null=True)  # Field name made lowercase.
    terindobs = models.CharField(db_column='TerIndObs', max_length=100, blank=True, null=True)  # Field name made lowercase.
    terindprc = models.DateTimeField(db_column='TerIndPrc', blank=True, null=True)  # Field name made lowercase.
    terecf = models.CharField(db_column='TerEcf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terssddoc = models.DecimalField(db_column='TerSsdDoc', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    terssdseq = models.DecimalField(db_column='TerSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    terfilvin = models.IntegerField(db_column='TerFilVin', blank=True, null=True)  # Field name made lowercase.
    terempvin = models.IntegerField(db_column='TerEmpVin', blank=True, null=True)  # Field name made lowercase.
    teravaqua = models.CharField(db_column='TerAvaQua', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terindcon = models.CharField(db_column='TerIndCon', max_length=2, blank=True, null=True)  # Field name made lowercase.
    teroricod = models.IntegerField(db_column='TerOriCod', blank=True, null=True)  # Field name made lowercase.
    terorimst = models.IntegerField(db_column='TerOriMst', blank=True, null=True)  # Field name made lowercase.
    tersufdatval = models.DateTimeField(db_column='TerSufDatVal', blank=True, null=True)  # Field name made lowercase.
    tercpfnropf = models.CharField(db_column='TerCpfNroPF', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terbolcsocod = models.CharField(db_column='TerBolCsoCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ternasrsp = models.DateTimeField(db_column='TerNasRsp', blank=True, null=True)  # Field name made lowercase.
    terstadat = models.DateTimeField(db_column='TerStaDat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER01'
        unique_together = (('terempcod', 'terdoc'),)


class Ter02(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc, TerItmCon) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    teritmcon = models.SmallIntegerField(db_column='TerItmCon')  # Field name made lowercase.
    ternomcon = models.CharField(db_column='TerNomCon', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tersetcon = models.CharField(db_column='TerSetCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tercarcon = models.CharField(db_column='TerCarCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfoncon1 = models.CharField(db_column='TerFonCon1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfoncon2 = models.CharField(db_column='TerFonCon2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terfoncon3 = models.CharField(db_column='TerFonCon3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    terramcon = models.IntegerField(db_column='TerRamCon', blank=True, null=True)  # Field name made lowercase.
    terfaxcon = models.CharField(db_column='TerFaxCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    teremacon = models.CharField(db_column='TerEmaCon', max_length=150, blank=True, null=True)  # Field name made lowercase.
    ternascon = models.DateTimeField(db_column='TerNasCon', blank=True, null=True)  # Field name made lowercase.
    teranicon = models.CharField(db_column='TerAniCon', max_length=5, blank=True, null=True)  # Field name made lowercase.
    terctccon = models.CharField(db_column='TerCtcCon', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER02'
        unique_together = (('terempcod', 'terdoc', 'teritmcon'),)


class Ter03(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc, TerItmBan) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    teritmban = models.SmallIntegerField(db_column='TerItmBan')  # Field name made lowercase.
    terpadban = models.CharField(db_column='TerPadBan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ternroban = models.SmallIntegerField(db_column='TerNroBan', blank=True, null=True)  # Field name made lowercase.
    ternroage = models.CharField(db_column='TerNroAge', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ternomage = models.CharField(db_column='TerNomAge', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ternrocco = models.CharField(db_column='TerNroCco', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tertipcco = models.CharField(db_column='TerTipCco', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tertitcco = models.CharField(db_column='TerTitCco', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tertitcpf = models.CharField(db_column='TerTitCpf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tercidcoda = models.IntegerField(db_column='TerCidCodA', blank=True, null=True)  # Field name made lowercase.
    termodban = models.CharField(db_column='TerModBan', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER03'
        unique_together = (('terempcod', 'terdoc', 'teritmban'),)


class Ter04(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc, TerItmEnt) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    teritment = models.SmallIntegerField(db_column='TerItmEnt')  # Field name made lowercase.
    traemdent = models.IntegerField(db_column='TraEmdEnt', blank=True, null=True)  # Field name made lowercase.
    tradcdent = models.IntegerField(db_column='TraDcdEnt', blank=True, null=True)  # Field name made lowercase.
    tranomdes = models.CharField(db_column='TraNomDes', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terfrdent = models.CharField(db_column='TerFrdEnt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    traemrent = models.IntegerField(db_column='TraEmrEnt', blank=True, null=True)  # Field name made lowercase.
    tradcrent = models.IntegerField(db_column='TraDcrEnt', blank=True, null=True)  # Field name made lowercase.
    tranomred = models.CharField(db_column='TraNomRed', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terfrrent = models.CharField(db_column='TerFrrEnt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terendent = models.CharField(db_column='TerEndEnt', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ternroent = models.IntegerField(db_column='TerNroEnt', blank=True, null=True)  # Field name made lowercase.
    tercoment = models.CharField(db_column='TerComEnt', max_length=60, blank=True, null=True)  # Field name made lowercase.
    terbaient = models.CharField(db_column='TerBaiEnt', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tercidcode = models.IntegerField(db_column='TerCidCodE', blank=True, null=True)  # Field name made lowercase.
    tercepent = models.CharField(db_column='TerCepEnt', max_length=9, blank=True, null=True)  # Field name made lowercase.
    tercxpent = models.IntegerField(db_column='TerCxpEnt', blank=True, null=True)  # Field name made lowercase.
    terccpent = models.CharField(db_column='TerCcpEnt', max_length=9, blank=True, null=True)  # Field name made lowercase.
    terrpeent = models.IntegerField(db_column='TerRpeEnt', blank=True, null=True)  # Field name made lowercase.
    terrpdent = models.IntegerField(db_column='TerRpdEnt', blank=True, null=True)  # Field name made lowercase.
    terrecent = models.CharField(db_column='TerRecEnt', max_length=254, blank=True, null=True)  # Field name made lowercase.
    terfrernf = models.CharField(db_column='TerFreRnf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terentpad = models.CharField(db_column='TerEntPad', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terfrefxa = models.SmallIntegerField(db_column='TerFreFxa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER04'
        unique_together = (('terempcod', 'terdoc', 'teritment'),)


class Ter05(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc, TerItmRet) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    teritmret = models.SmallIntegerField(db_column='TerItmRet')  # Field name made lowercase.
    traemdret = models.IntegerField(db_column='TraEmdRet', blank=True, null=True)  # Field name made lowercase.
    tradcdret = models.IntegerField(db_column='TraDcdRet', blank=True, null=True)  # Field name made lowercase.
    terfrdret = models.CharField(db_column='TerFrdRet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    traemrret = models.IntegerField(db_column='TraEmrRet', blank=True, null=True)  # Field name made lowercase.
    tradcrret = models.IntegerField(db_column='TraDcrRet', blank=True, null=True)  # Field name made lowercase.
    terfrrret = models.CharField(db_column='TerFrrRet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terendret = models.CharField(db_column='TerEndRet', max_length=60, blank=True, null=True)  # Field name made lowercase.
    ternroret = models.IntegerField(db_column='TerNroRet', blank=True, null=True)  # Field name made lowercase.
    tercomret = models.CharField(db_column='TerComRet', max_length=60, blank=True, null=True)  # Field name made lowercase.
    terbairet = models.CharField(db_column='TerBaiRet', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tercidcodr = models.IntegerField(db_column='TerCidCodR', blank=True, null=True)  # Field name made lowercase.
    tercepret = models.CharField(db_column='TerCepRet', max_length=9, blank=True, null=True)  # Field name made lowercase.
    tercxpret = models.IntegerField(db_column='TerCxpRet', blank=True, null=True)  # Field name made lowercase.
    terccpret = models.CharField(db_column='TerCcpRet', max_length=9, blank=True, null=True)  # Field name made lowercase.
    terpadret = models.CharField(db_column='TerPadRet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terhorret = models.CharField(db_column='TerHorRet', max_length=50, blank=True, null=True)  # Field name made lowercase.
    terequret = models.CharField(db_column='TerEquRet', max_length=50, blank=True, null=True)  # Field name made lowercase.
    terconret = models.CharField(db_column='TerConRet', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terfonret = models.CharField(db_column='TerFonRet', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER05'
        unique_together = (('terempcod', 'terdoc', 'teritmret'),)


class Ter06(models.Model):
    terempcod = models.IntegerField(db_column='TerEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (TerEmpCod, TerDoc, TerProCod, TerEmbCod) found, that is not supported. The first column is selected.
    terdoc = models.IntegerField(db_column='TerDoc')  # Field name made lowercase.
    terprocod = models.CharField(db_column='TerProCod', max_length=12)  # Field name made lowercase.
    terembcod = models.CharField(db_column='TerEmbCod', max_length=12)  # Field name made lowercase.
    terproemp = models.IntegerField(db_column='TerProEmp', blank=True, null=True)  # Field name made lowercase.
    terembemp = models.IntegerField(db_column='TerEmbEmp', blank=True, null=True)  # Field name made lowercase.
    terprocdm = models.CharField(db_column='TerProCdm', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terproucp = models.DateTimeField(db_column='TerProUcp', blank=True, null=True)  # Field name made lowercase.
    terproeccemp = models.IntegerField(db_column='TerProEccEmp', blank=True, null=True)  # Field name made lowercase.
    terproecccod = models.IntegerField(db_column='TerProEccCod', blank=True, null=True)  # Field name made lowercase.
    terprocemp = models.CharField(db_column='TerProCEmp', max_length=50, blank=True, null=True)  # Field name made lowercase.
    terprocpro = models.CharField(db_column='TerProCPro', max_length=50, blank=True, null=True)  # Field name made lowercase.
    terprocemb = models.CharField(db_column='TerProCEmb', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terprocprc = models.DecimalField(db_column='TerProCPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    terprocper = models.CharField(db_column='TerProCPer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terpromodpor1 = models.DecimalField(db_column='TerProModPor1', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    terpromodpor2 = models.DecimalField(db_column='TerProModPor2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    terpromodpor3 = models.DecimalField(db_column='TerProModPor3', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    terproconnro = models.CharField(db_column='TerProConNro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terprocondat = models.DateTimeField(db_column='TerProConDat', blank=True, null=True)  # Field name made lowercase.
    terprolicnrome = models.CharField(db_column='TerProLicNroME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terprolicvalme = models.DateTimeField(db_column='TerProLicValME', blank=True, null=True)  # Field name made lowercase.
    terprolicnropf = models.CharField(db_column='TerProLicNroPF', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terprolicvalpf = models.DateTimeField(db_column='TerProLicValPF', blank=True, null=True)  # Field name made lowercase.
    terprolicnrossp = models.CharField(db_column='TerProLicNroSSP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terprolicvalssp = models.DateTimeField(db_column='TerProLicValSSP', blank=True, null=True)  # Field name made lowercase.
    terproprcpra = models.DecimalField(db_column='TerProPrcPra', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    terproultprc = models.DecimalField(db_column='TerProUltPrc', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    terproultqtd = models.DecimalField(db_column='TerProUltQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    terproultlis = models.DecimalField(db_column='TerProUltLis', max_digits=14, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    terprodat = models.DateTimeField(db_column='TerProDat', blank=True, null=True)  # Field name made lowercase.
    terprolicvalib = models.DateTimeField(db_column='TerProLicValIB', blank=True, null=True)  # Field name made lowercase.
    terprolicnroib = models.CharField(db_column='TerProLicNroIB', max_length=20, blank=True, null=True)  # Field name made lowercase.
    terprossdseq = models.DecimalField(db_column='TerProSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TER06'
        unique_together = (('terempcod', 'terdoc', 'terprocod', 'terembcod'),)

class Rep01(models.Model):
    repempcod = models.IntegerField(db_column='RepEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (RepEmpCod, RepDoc) found, that is not supported. The first column is selected.
    repdoc = models.IntegerField(db_column='RepDoc')  # Field name made lowercase.
    repcod = models.IntegerField(db_column='RepCod', blank=True, null=True)  # Field name made lowercase.
    reptipdoc = models.CharField(db_column='RepTipDoc', max_length=6, blank=True, null=True)  # Field name made lowercase.
    repdat = models.DateTimeField(db_column='RepDat', blank=True, null=True)  # Field name made lowercase.
    repsta = models.CharField(db_column='RepSta', max_length=7, blank=True, null=True)  # Field name made lowercase.
    repnom = models.CharField(db_column='RepNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    repide = models.CharField(db_column='RepIde', max_length=10, blank=True, null=True)  # Field name made lowercase.
    repraz = models.CharField(db_column='RepRaz', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reptip = models.CharField(db_column='RepTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rependfat = models.CharField(db_column='RepEndFat', max_length=60, blank=True, null=True)  # Field name made lowercase.
    repnrofat = models.IntegerField(db_column='RepNroFat', blank=True, null=True)  # Field name made lowercase.
    repcomfat = models.CharField(db_column='RepComFat', max_length=60, blank=True, null=True)  # Field name made lowercase.
    repbaifat = models.CharField(db_column='RepBaiFat', max_length=60, blank=True, null=True)  # Field name made lowercase.
    repcidcodf = models.IntegerField(db_column='RepCidCodF', blank=True, null=True)  # Field name made lowercase.
    repcepfat = models.CharField(db_column='RepCepFat', max_length=9, blank=True, null=True)  # Field name made lowercase.
    repcxpfat = models.IntegerField(db_column='RepCxpFat', blank=True, null=True)  # Field name made lowercase.
    repccpfat = models.CharField(db_column='RepCcpFat', max_length=9, blank=True, null=True)  # Field name made lowercase.
    repinsest = models.CharField(db_column='RepInsEst', max_length=20, blank=True, null=True)  # Field name made lowercase.
    repinstip = models.CharField(db_column='RepInsTip', max_length=6, blank=True, null=True)  # Field name made lowercase.
    repinsmun = models.CharField(db_column='RepInsMun', max_length=20, blank=True, null=True)  # Field name made lowercase.
    repfon1 = models.CharField(db_column='RepFon1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfax1 = models.CharField(db_column='RepFax1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfon2 = models.CharField(db_column='RepFon2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfax2 = models.CharField(db_column='RepFax2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfon3 = models.CharField(db_column='RepFon3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfax3 = models.CharField(db_column='RepFax3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repema = models.CharField(db_column='RepEma', max_length=150, blank=True, null=True)  # Field name made lowercase.
    rephom = models.CharField(db_column='RepHom', max_length=150, blank=True, null=True)  # Field name made lowercase.
    repmod = models.CharField(db_column='RepMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repareemp = models.IntegerField(db_column='RepAreEmp', blank=True, null=True)  # Field name made lowercase.
    reparecod = models.CharField(db_column='RepAreCod', max_length=5, blank=True, null=True)  # Field name made lowercase.
    repcalcom = models.CharField(db_column='RepCalcom', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reptplemp = models.IntegerField(db_column='RepTplEmp', blank=True, null=True)  # Field name made lowercase.
    reptplcod = models.SmallIntegerField(db_column='RepTplCod', blank=True, null=True)  # Field name made lowercase.
    repcpf = models.CharField(db_column='RepCpf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    repmkt = models.CharField(db_column='RepMkt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repdvd = models.CharField(db_column='RepDvd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repmovint = models.CharField(db_column='RepMovInt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repultban = models.SmallIntegerField(db_column='RepUltBan', blank=True, null=True)  # Field name made lowercase.
    repultvis = models.DecimalField(db_column='RepUltVis', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    repultapa = models.DecimalField(db_column='RepUltApa', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    repultdpa = models.DecimalField(db_column='RepUltDpa', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    repcodatu = models.CharField(db_column='RepCodAtu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repcodold = models.CharField(db_column='RepCodOld', max_length=20, blank=True, null=True)  # Field name made lowercase.
    repcodnew = models.CharField(db_column='RepCodNew', max_length=6, blank=True, null=True)  # Field name made lowercase.
    repenqest = models.CharField(db_column='RepEnqEst', max_length=5, blank=True, null=True)  # Field name made lowercase.
    repenqfed = models.CharField(db_column='RepEnqFed', max_length=5, blank=True, null=True)  # Field name made lowercase.
    repexphis = models.CharField(db_column='RepExpHis', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sttcod = models.SmallIntegerField(db_column='SttCod', blank=True, null=True)  # Field name made lowercase.
    repcevemp = models.IntegerField(db_column='RepCevEmp', blank=True, null=True)  # Field name made lowercase.
    repcevcod = models.SmallIntegerField(db_column='RepCevCod', blank=True, null=True)  # Field name made lowercase.
    repultlis = models.DecimalField(db_column='RepUltLis', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    repmemeqv = models.CharField(db_column='RepMemEqv', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repvenmod2 = models.CharField(db_column='RepVenMod2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repvencb = models.CharField(db_column='RepVenCB', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repvisapo = models.CharField(db_column='RepVisApo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repsinsd = models.CharField(db_column='RepSinSD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP01'
        unique_together = (('repempcod', 'repdoc'),)


class Rep02(models.Model):
    repempcod = models.IntegerField(db_column='RepEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (RepEmpCod, RepDoc, RepItmCon) found, that is not supported. The first column is selected.
    repdoc = models.IntegerField(db_column='RepDoc')  # Field name made lowercase.
    repitmcon = models.SmallIntegerField(db_column='RepItmCon')  # Field name made lowercase.
    repnomcon = models.CharField(db_column='RepNomCon', max_length=30, blank=True, null=True)  # Field name made lowercase.
    repsetcon = models.CharField(db_column='RepSetCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repcarcon = models.CharField(db_column='RepCarCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repfoncon = models.CharField(db_column='RepFonCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repramcon = models.IntegerField(db_column='RepRamCon', blank=True, null=True)  # Field name made lowercase.
    repfaxcon = models.CharField(db_column='RepFaxCon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    repemacon = models.CharField(db_column='RepEmaCon', max_length=150, blank=True, null=True)  # Field name made lowercase.
    repnascon = models.DateTimeField(db_column='RepNasCon', blank=True, null=True)  # Field name made lowercase.
    repanicon = models.CharField(db_column='RepAniCon', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP02'
        unique_together = (('repempcod', 'repdoc', 'repitmcon'),)


class Rep03(models.Model):
    repempcod = models.IntegerField(db_column='RepEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (RepEmpCod, RepDoc, RepItmBan) found, that is not supported. The first column is selected.
    repdoc = models.IntegerField(db_column='RepDoc')  # Field name made lowercase.
    repitmban = models.SmallIntegerField(db_column='RepItmBan')  # Field name made lowercase.
    reppadban = models.CharField(db_column='RepPadBan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repnroban = models.SmallIntegerField(db_column='RepNroBan', blank=True, null=True)  # Field name made lowercase.
    repnroage = models.CharField(db_column='RepNroAge', max_length=6, blank=True, null=True)  # Field name made lowercase.
    repnomage = models.CharField(db_column='RepNomAge', max_length=30, blank=True, null=True)  # Field name made lowercase.
    repnrocco = models.CharField(db_column='RepNroCco', max_length=15, blank=True, null=True)  # Field name made lowercase.
    reptitcco = models.CharField(db_column='RepTitCco', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reptitcpf = models.CharField(db_column='RepTitCpf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reptipcco = models.CharField(db_column='RepTipCco', max_length=1, blank=True, null=True)  # Field name made lowercase.
    repcidcoda = models.IntegerField(db_column='RepCidCodA', blank=True, null=True)  # Field name made lowercase.
    repmodban = models.CharField(db_column='RepModBan', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP03'
        unique_together = (('repempcod', 'repdoc', 'repitmban'),)


class Rep04(models.Model):
    repempcod = models.IntegerField(db_column='RepEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (RepEmpCod, RepDoc, RepCItm) found, that is not supported. The first column is selected.
    repdoc = models.IntegerField(db_column='RepDoc')  # Field name made lowercase.
    repcitm = models.SmallIntegerField(db_column='RepCItm')  # Field name made lowercase.
    repcfpgcod = models.SmallIntegerField(db_column='RepCFpgCod', blank=True, null=True)  # Field name made lowercase.
    repcrepmstemp = models.IntegerField(db_column='RepCRepMstEmp', blank=True, null=True)  # Field name made lowercase.
    repcrepmstdoc = models.IntegerField(db_column='RepCRepMstDoc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP04'
        unique_together = (('repempcod', 'repdoc', 'repcitm'),)

class Cid01(models.Model):
    cidcod = models.IntegerField(db_column='CidCod', primary_key=True)  # Field name made lowercase.
    cidnom = models.CharField(db_column='CidNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    estcod = models.CharField(db_column='EstCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paiscod = models.IntegerField(db_column='PaisCod', blank=True, null=True)  # Field name made lowercase.
    cidcep = models.CharField(db_column='CidCep', max_length=9, blank=True, null=True)  # Field name made lowercase.
    cidmun = models.CharField(db_column='CidMun', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cidcodibge = models.CharField(db_column='CidCodIbge', max_length=7, blank=True, null=True)  # Field name made lowercase.
    cidiss = models.DecimalField(db_column='CidIss', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    cidzfmalc = models.CharField(db_column='CidZfmAlc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cidsta = models.CharField(db_column='CidSta', max_length=7, blank=True, null=True)  # Field name made lowercase.
    cidssdseq = models.DecimalField(db_column='CidSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cidlng = models.DecimalField(db_column='CidLng', max_digits=17, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    cidlat = models.DecimalField(db_column='CidLat', max_digits=17, decimal_places=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CID01'

class Opr01(models.Model):
    opraempcod = models.IntegerField(db_column='OprAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (OprAEmpCod, OprAFilCod, OprAPfxCod, OprACod) found, that is not supported. The first column is selected.
    oprafilcod = models.IntegerField(db_column='OprAFilCod')  # Field name made lowercase.
    oprapfxcod = models.CharField(db_column='OprAPfxCod', max_length=5)  # Field name made lowercase.
    opracod = models.IntegerField(db_column='OprACod')  # Field name made lowercase.
    opratip = models.SmallIntegerField(db_column='OprATip', blank=True, null=True)  # Field name made lowercase.
    opraagr = models.IntegerField(db_column='OprAAgr', blank=True, null=True)  # Field name made lowercase.
    opranrolot = models.CharField(db_column='OprANroLot', max_length=15, blank=True, null=True)  # Field name made lowercase.
    opranrolotseq = models.SmallIntegerField(db_column='OprANroLotSeq', blank=True, null=True)  # Field name made lowercase.
    opratiplot = models.CharField(db_column='OprATipLot', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oprasit = models.CharField(db_column='OprASit', max_length=2, blank=True, null=True)  # Field name made lowercase.
    opracodacaopen = models.CharField(db_column='OprACodAcaoPen', max_length=20, blank=True, null=True)  # Field name made lowercase.
    opradatemi = models.DateTimeField(db_column='OprADatEmi', blank=True, null=True)  # Field name made lowercase.
    oprahoremi = models.CharField(db_column='OprAHorEmi', max_length=5, blank=True, null=True)  # Field name made lowercase.
    opradatscp = models.DateTimeField(db_column='OprADatScp', blank=True, null=True)  # Field name made lowercase.
    opradatlpr = models.DateTimeField(db_column='OprADatLpr', blank=True, null=True)  # Field name made lowercase.
    opradatisp = models.DateTimeField(db_column='OprADatIsp', blank=True, null=True)  # Field name made lowercase.
    opradatfab = models.DateTimeField(db_column='OprADatFab', blank=True, null=True)  # Field name made lowercase.
    opradatval = models.DateTimeField(db_column='OprADatVal', blank=True, null=True)  # Field name made lowercase.
    opradatenc = models.DateTimeField(db_column='OprADatEnc', blank=True, null=True)  # Field name made lowercase.
    opraent = models.DateTimeField(db_column='OprAEnt', blank=True, null=True)  # Field name made lowercase.
    opraprvpro = models.DateTimeField(db_column='OprAPrvPro', blank=True, null=True)  # Field name made lowercase.
    opraproemp = models.IntegerField(db_column='OprAProEmp', blank=True, null=True)  # Field name made lowercase.
    opraprocod = models.CharField(db_column='OprAProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opraembcod = models.CharField(db_column='OprAEmbCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opragddcod1 = models.CharField(db_column='OprAGddCod1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opragddcod2 = models.CharField(db_column='OprAGddCod2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opragddcod3 = models.CharField(db_column='OprAGddCod3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opraftmcod = models.IntegerField(db_column='OprAFtmCod', blank=True, null=True)  # Field name made lowercase.
    opranom = models.CharField(db_column='OprANom', max_length=120, blank=True, null=True)  # Field name made lowercase.
    oprauniven = models.CharField(db_column='OprAUniVen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    oprauniest = models.CharField(db_column='OprAUniEst', max_length=3, blank=True, null=True)  # Field name made lowercase.
    oprapes = models.DecimalField(db_column='OprAPes', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprapeccxa = models.SmallIntegerField(db_column='OprAPecCxa', blank=True, null=True)  # Field name made lowercase.
    opraqtdcjt = models.DecimalField(db_column='OprAQtdCjt', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprapescjt = models.DecimalField(db_column='OprAPesCjt', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    opraqtdped = models.DecimalField(db_column='OprAQtdPed', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    opraqtdprv = models.DecimalField(db_column='OprAQtdPrv', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprapesprv = models.DecimalField(db_column='OprAPesPrv', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    opraqtdrea = models.DecimalField(db_column='OprAQtdRea', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprapesrea = models.DecimalField(db_column='OprAPesRea', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    opraalmemp = models.IntegerField(db_column='OprAAlmEmp', blank=True, null=True)  # Field name made lowercase.
    opraalmcod = models.SmallIntegerField(db_column='OprAAlmCod', blank=True, null=True)  # Field name made lowercase.
    opraobs = models.CharField(db_column='OprAObs', max_length=254, blank=True, null=True)  # Field name made lowercase.
    opramod = models.CharField(db_column='OprAMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opraimp = models.CharField(db_column='OprAImp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opraultpdv = models.IntegerField(db_column='OprAUltPdv', blank=True, null=True)  # Field name made lowercase.
    opraultmat = models.SmallIntegerField(db_column='OprAUltMat', blank=True, null=True)  # Field name made lowercase.
    opraultent = models.SmallIntegerField(db_column='OprAUltEnt', blank=True, null=True)  # Field name made lowercase.
    opraoritab = models.CharField(db_column='OprAOriTab', max_length=3, blank=True, null=True)  # Field name made lowercase.
    opraoripfx = models.CharField(db_column='OprAOriPfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    opraoricod = models.DecimalField(db_column='OprAOriCod', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    opratrncod = models.DecimalField(db_column='OprATrnCod', max_digits=12, decimal_places=0)  # Field name made lowercase.
    opracodpai = models.IntegerField(db_column='OprACodPai', blank=True, null=True)  # Field name made lowercase.
    opracsmunt = models.DecimalField(db_column='OprACsmUnt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam10 = models.DecimalField(db_column='OprARatTam10', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam09 = models.DecimalField(db_column='OprARatTam09', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam08 = models.DecimalField(db_column='OprARatTam08', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam07 = models.DecimalField(db_column='OprARatTam07', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam06 = models.DecimalField(db_column='OprARatTam06', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam05 = models.DecimalField(db_column='OprARatTam05', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam04 = models.DecimalField(db_column='OprARatTam04', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam03 = models.DecimalField(db_column='OprARatTam03', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam02 = models.DecimalField(db_column='OprARatTam02', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarattam01 = models.DecimalField(db_column='OprARatTam01', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprarctacod = models.CharField(db_column='OprARctaCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oprarctaemp = models.IntegerField(db_column='OprARctaEmp', blank=True, null=True)  # Field name made lowercase.
    opraftmtxlar = models.DecimalField(db_column='OprAFtmtxLar', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    opraratcod = models.CharField(db_column='OprARatCod', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opraratfil = models.IntegerField(db_column='OprARatFil', blank=True, null=True)  # Field name made lowercase.
    opraratemp = models.IntegerField(db_column='OprARatEmp', blank=True, null=True)  # Field name made lowercase.
    opraemietq = models.CharField(db_column='OprAEmiEtq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opraplm = models.CharField(db_column='OprAPlm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oprakitnro = models.CharField(db_column='OprAKitNro', max_length=40, blank=True, null=True)  # Field name made lowercase.
    opranrortb = models.CharField(db_column='OprANroRtb', max_length=15, blank=True, null=True)  # Field name made lowercase.
    opraprvent = models.DateTimeField(db_column='OprAPrvEnt', blank=True, null=True)  # Field name made lowercase.
    oprapesfin = models.CharField(db_column='OprAPesFin', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPR01'
        unique_together = (('opraempcod', 'oprafilcod', 'oprapfxcod', 'opracod'),)


class Opr02(models.Model):
    opraempcod = models.IntegerField(db_column='OprAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (OprAEmpCod, OprAFilCod, OprAPfxCod, OprACod, OprBItm) found, that is not supported. The first column is selected.
    oprafilcod = models.IntegerField(db_column='OprAFilCod')  # Field name made lowercase.
    oprapfxcod = models.CharField(db_column='OprAPfxCod', max_length=5)  # Field name made lowercase.
    opracod = models.IntegerField(db_column='OprACod')  # Field name made lowercase.
    oprbitm = models.SmallIntegerField(db_column='OprBItm')  # Field name made lowercase.
    oprbgddcod1 = models.CharField(db_column='OprBGddCod1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oprbgddcod2 = models.CharField(db_column='OprBGddCod2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oprbgddcod3 = models.CharField(db_column='OprBGddCod3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oprbpdvemp = models.IntegerField(db_column='OprBPdvEmp', blank=True, null=True)  # Field name made lowercase.
    oprbpdvfil = models.IntegerField(db_column='OprBPdvFil', blank=True, null=True)  # Field name made lowercase.
    oprbpdvcod = models.IntegerField(db_column='OprBPdvCod', blank=True, null=True)  # Field name made lowercase.
    oprbpdvpfx = models.CharField(db_column='OprBPdvPfx', max_length=5, blank=True, null=True)  # Field name made lowercase.
    oprbpdvitm = models.IntegerField(db_column='OprBPdvItm', blank=True, null=True)  # Field name made lowercase.
    oprbqtdprv = models.DecimalField(db_column='OprBQtdPrv', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprbpapcod = models.IntegerField(db_column='OprBPapCod', blank=True, null=True)  # Field name made lowercase.
    oprbuni = models.CharField(db_column='OprBUni', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPR02'
        unique_together = (('opraempcod', 'oprafilcod', 'oprapfxcod', 'opracod', 'oprbitm'),)


class Opr03(models.Model):
    opraempcod = models.IntegerField(db_column='OprAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (OprAEmpCod, OprAFilCod, OprAPfxCod, OprACod, OprCItm) found, that is not supported. The first column is selected.
    oprafilcod = models.IntegerField(db_column='OprAFilCod')  # Field name made lowercase.
    oprapfxcod = models.CharField(db_column='OprAPfxCod', max_length=5)  # Field name made lowercase.
    opracod = models.IntegerField(db_column='OprACod')  # Field name made lowercase.
    oprcitm = models.SmallIntegerField(db_column='OprCItm')  # Field name made lowercase.
    oprcproemp = models.IntegerField(db_column='OprCProEmp', blank=True, null=True)  # Field name made lowercase.
    oprcprocod = models.CharField(db_column='OprCProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oprcconest = models.CharField(db_column='OprCConEst', max_length=13, blank=True, null=True)  # Field name made lowercase.
    oprcalmemp = models.IntegerField(db_column='OprCAlmEmp', blank=True, null=True)  # Field name made lowercase.
    oprcalmcod = models.SmallIntegerField(db_column='OprCAlmCod', blank=True, null=True)  # Field name made lowercase.
    oprcuni = models.CharField(db_column='OprCUni', max_length=3, blank=True, null=True)  # Field name made lowercase.
    oprcqtd = models.DecimalField(db_column='OprCQtd', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    oprcprc = models.DecimalField(db_column='OprCPrc', max_digits=11, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    oprcrmtseq = models.SmallIntegerField(db_column='OprCRmtSeq', blank=True, null=True)  # Field name made lowercase.
    oprcfan = models.CharField(db_column='OprCFan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oprcrprseq = models.SmallIntegerField(db_column='OprCRprSeq', blank=True, null=True)  # Field name made lowercase.
    oprccencod = models.IntegerField(db_column='OprCCenCod', blank=True, null=True)  # Field name made lowercase.
    oprcniv = models.SmallIntegerField(db_column='OprCNiv', blank=True, null=True)  # Field name made lowercase.
    oprcnivcla = models.CharField(db_column='OprCNivCla', max_length=30, blank=True, null=True)  # Field name made lowercase.
    oprctvbcod = models.IntegerField(db_column='OprCTvbCod', blank=True, null=True)  # Field name made lowercase.
    oprctvbemp = models.IntegerField(db_column='OprCTvbEmp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPR03'
        unique_together = (('opraempcod', 'oprafilcod', 'oprapfxcod', 'opracod', 'oprcitm'),)


class Opr04(models.Model):
    opraempcod = models.IntegerField(db_column='OprAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (OprAEmpCod, OprAFilCod, OprAPfxCod, OprACod, OprDItm) found, that is not supported. The first column is selected.
    oprafilcod = models.IntegerField(db_column='OprAFilCod')  # Field name made lowercase.
    oprapfxcod = models.CharField(db_column='OprAPfxCod', max_length=5)  # Field name made lowercase.
    opracod = models.IntegerField(db_column='OprACod')  # Field name made lowercase.
    oprditm = models.SmallIntegerField(db_column='OprDItm')  # Field name made lowercase.
    oprdftcemp = models.IntegerField(db_column='OprDFtcEmp', blank=True, null=True)  # Field name made lowercase.
    oprdftccod = models.CharField(db_column='OprDFtcCod', max_length=5, blank=True, null=True)  # Field name made lowercase.
    oprdpes = models.DecimalField(db_column='OprDPes', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPR04'
        unique_together = (('opraempcod', 'oprafilcod', 'oprapfxcod', 'opracod', 'oprditm'),)

class Ftm01(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmanom = models.CharField(db_column='FtmANom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ftmamtgemp = models.IntegerField(db_column='FtmAMtgEmp', blank=True, null=True)  # Field name made lowercase.
    ftmamtgcod = models.SmallIntegerField(db_column='FtmAMtgCod', blank=True, null=True)  # Field name made lowercase.
    ftmatipcil = models.CharField(db_column='FtmATipCil', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ftmatipren = models.CharField(db_column='FtmATipRen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ftmacam = models.SmallIntegerField(db_column='FtmACam', blank=True, null=True)  # Field name made lowercase.
    ftmacic = models.SmallIntegerField(db_column='FtmACic', blank=True, null=True)  # Field name made lowercase.
    ftmacicuni = models.CharField(db_column='FtmACicUni', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ftmarpm = models.CharField(db_column='FtmARpm', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ftmatemmas = models.SmallIntegerField(db_column='FtmATemMas', blank=True, null=True)  # Field name made lowercase.
    ftmatemcil = models.SmallIntegerField(db_column='FtmATemCil', blank=True, null=True)  # Field name made lowercase.
    ftmateqemp = models.IntegerField(db_column='FtmATeqEmp', blank=True, null=True)  # Field name made lowercase.
    ftmateqcod = models.IntegerField(db_column='FtmATeqCod', blank=True, null=True)  # Field name made lowercase.
    ftmatipreg = models.CharField(db_column='FtmATipReg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ftmaadiprg = models.DecimalField(db_column='FtmAAdiPrg', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmablqren = models.CharField(db_column='FtmABlqRen', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTM01'
        unique_together = (('ftmaempcod', 'ftmacod'),)


class Ftm02(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod, FtmDTam) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmdtam = models.CharField(db_column='FtmDTam', max_length=10)  # Field name made lowercase.
    ftmdespbru = models.DecimalField(db_column='FtmDEspBru', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmdespaca = models.DecimalField(db_column='FtmDEspAca', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmdcilmed = models.DecimalField(db_column='FtmDCilMed', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmdren = models.DecimalField(db_column='FtmDRen', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmdapr = models.DecimalField(db_column='FtmDApr', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTM02'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmdtam'),)


class Ftm03(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod, FtmGItm) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmgitm = models.SmallIntegerField(db_column='FtmGItm')  # Field name made lowercase.
    ftmgdes = models.CharField(db_column='FtmGDes', max_length=254, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTM03'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmgitm'),)


class Ftm04(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod, FtmEArt) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmeart = models.DecimalField(db_column='FtmEArt', max_digits=10, decimal_places=0)  # Field name made lowercase.
    ftmeobs = models.CharField(db_column='FtmEObs', max_length=254, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTM04'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmeart'),)


class Ftm05(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod, FtmBItm) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmbitm = models.SmallIntegerField(db_column='FtmBItm')  # Field name made lowercase.
    ftmbpor = models.DecimalField(db_column='FtmBPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftmbfix = models.CharField(db_column='FtmBFix', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTM05'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmbitm'),)


class Ftm06(models.Model):
    ftmaempcod = models.IntegerField(db_column='FtmAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtmAEmpCod, FtmACod, FtmHItm) found, that is not supported. The first column is selected.
    ftmacod = models.IntegerField(db_column='FtmACod')  # Field name made lowercase.
    ftmhitm = models.SmallIntegerField(db_column='FtmHItm')  # Field name made lowercase.
    ftmhobs = models.TextField(db_column='FtmHObs', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'FTM06'
        unique_together = (('ftmaempcod', 'ftmacod', 'ftmhitm'),)

class Pro01(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, ProCod) found, that is not supported. The first column is selected.
    procod = models.CharField(db_column='ProCod', max_length=12)  # Field name made lowercase.
    pronomdet = models.TextField(db_column='ProNomDet', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    proclaemb = models.CharField(db_column='ProClaEmb', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prorprcod = models.CharField(db_column='ProRprCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    propermp = models.DecimalField(db_column='ProPerMp', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proadiprg = models.DecimalField(db_column='ProAdiPrg', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proadirea = models.DecimalField(db_column='ProAdiRea', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prodescod = models.CharField(db_column='ProDesCod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prodesarq = models.CharField(db_column='ProDesArq', max_length=254, blank=True, null=True)  # Field name made lowercase.
    proprzctc = models.SmallIntegerField(db_column='ProPrzCtc', blank=True, null=True)  # Field name made lowercase.
    promascen = models.CharField(db_column='ProMasCen', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prolstcod = models.CharField(db_column='ProLstCod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    proanpcod = models.CharField(db_column='ProAnpCod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    proconforcont = models.CharField(db_column='ProConForCont', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prositepub = models.CharField(db_column='ProSitePub', max_length=1, blank=True, null=True)  # Field name made lowercase.
    promedida = models.CharField(db_column='ProMedida', max_length=10, blank=True, null=True)  # Field name made lowercase.
    prolibusr = models.CharField(db_column='ProLibUsr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    proultcat = models.SmallIntegerField(db_column='ProUltCat', blank=True, null=True)  # Field name made lowercase.
    proartemp = models.IntegerField(db_column='ProArtEmp', blank=True, null=True)  # Field name made lowercase.
    probartcod = models.DecimalField(db_column='ProBArtCod', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    probarttam = models.CharField(db_column='ProBArtTam', max_length=10, blank=True, null=True)  # Field name made lowercase.
    probarttampcp = models.CharField(db_column='ProBArtTamPcp', max_length=10, blank=True, null=True)  # Field name made lowercase.
    probartcodbas = models.DecimalField(db_column='ProBArtCodBas', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    probartacb = models.CharField(db_column='ProBArtAcb', max_length=30, blank=True, null=True)  # Field name made lowercase.
    probqtdfur = models.CharField(db_column='ProBQtdFur', max_length=30, blank=True, null=True)  # Field name made lowercase.
    probminven = models.CharField(db_column='ProBMinVen', max_length=10, blank=True, null=True)  # Field name made lowercase.
    probartting = models.CharField(db_column='ProBArtTing', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prorpscod = models.IntegerField(db_column='ProRpsCod', blank=True, null=True)  # Field name made lowercase.
    proultesp = models.SmallIntegerField(db_column='ProUltEsp', blank=True, null=True)  # Field name made lowercase.
    profoto = models.BinaryField(db_column='ProFoto', blank=True, null=True)  # Field name made lowercase.
    profototip = models.CharField(db_column='ProFotoTip', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proqtdpeccnj = models.SmallIntegerField(db_column='ProQtdPecCnj', blank=True, null=True)  # Field name made lowercase.
    propescnj = models.DecimalField(db_column='ProPesCnj', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    probtamcxa = models.CharField(db_column='ProBTamCxa', max_length=15, blank=True, null=True)  # Field name made lowercase.
    probnpecxa = models.SmallIntegerField(db_column='ProBNpeCxa', blank=True, null=True)  # Field name made lowercase.
    probcxahor = models.SmallIntegerField(db_column='ProBCxaHor', blank=True, null=True)  # Field name made lowercase.
    probtipmod = models.CharField(db_column='ProBTipMod', max_length=30, blank=True, null=True)  # Field name made lowercase.
    probtipmol = models.CharField(db_column='ProBTipMol', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proultmch = models.SmallIntegerField(db_column='ProUltMch', blank=True, null=True)  # Field name made lowercase.
    prolocmdl = models.CharField(db_column='ProLocMdl', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proobs = models.TextField(db_column='ProObs', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    probmtgcod = models.SmallIntegerField(db_column='ProBMtgCod', blank=True, null=True)  # Field name made lowercase.
    probterdoc = models.IntegerField(db_column='ProBTerDoc', blank=True, null=True)  # Field name made lowercase.
    promarcod = models.IntegerField(db_column='ProMarCod', blank=True, null=True)  # Field name made lowercase.
    proloc = models.CharField(db_column='ProLoc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prouniven = models.CharField(db_column='ProUniVen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prouniest = models.CharField(db_column='ProUniEst', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prounicom = models.CharField(db_column='ProUniCom', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proicmcod = models.SmallIntegerField(db_column='ProIcmCod', blank=True, null=True)  # Field name made lowercase.
    protemgar = models.SmallIntegerField(db_column='ProTemGar', blank=True, null=True)  # Field name made lowercase.
    protipgar = models.CharField(db_column='ProTipGar', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proonuemp = models.IntegerField(db_column='ProOnuEmp', blank=True, null=True)  # Field name made lowercase.
    proonunro = models.CharField(db_column='ProOnuNro', max_length=4, blank=True, null=True)  # Field name made lowercase.
    prorisemp = models.IntegerField(db_column='ProRisEmp', blank=True, null=True)  # Field name made lowercase.
    proriscla = models.CharField(db_column='ProRisCla', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prorisnro = models.CharField(db_column='ProRisNro', max_length=6, blank=True, null=True)  # Field name made lowercase.
    proncmcod = models.CharField(db_column='ProNcmCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    propesliq = models.DecimalField(db_column='ProPesLiq', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    propesbru = models.DecimalField(db_column='ProPesBru', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proras = models.CharField(db_column='ProRas', max_length=6, blank=True, null=True)  # Field name made lowercase.
    prorpremp = models.IntegerField(db_column='ProRprEmp', blank=True, null=True)  # Field name made lowercase.
    profan = models.CharField(db_column='ProFan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prorefuni = models.CharField(db_column='ProRefUni', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proreffat = models.DecimalField(db_column='ProRefFat', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proreftft = models.CharField(db_column='ProRefTft', max_length=13, blank=True, null=True)  # Field name made lowercase.
    pronrocas = models.CharField(db_column='ProNroCas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    proautfun = models.CharField(db_column='ProAutFun', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prolotpil = models.CharField(db_column='ProLotPil', max_length=16, blank=True, null=True)  # Field name made lowercase.
    profictec = models.CharField(db_column='ProFicTec', max_length=8, blank=True, null=True)  # Field name made lowercase.
    proreptem = models.SmallIntegerField(db_column='ProRepTem', blank=True, null=True)  # Field name made lowercase.
    prolotide = models.DecimalField(db_column='ProLotIde', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prolotmin = models.DecimalField(db_column='ProLotMin', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prolotmax = models.DecimalField(db_column='ProLotMax', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proconmed = models.DecimalField(db_column='ProConMed', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proorgemp = models.IntegerField(db_column='ProOrgEmp', blank=True, null=True)  # Field name made lowercase.
    proorgcod = models.SmallIntegerField(db_column='ProOrgCod', blank=True, null=True)  # Field name made lowercase.
    proorgreg = models.CharField(db_column='ProOrgReg', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proorgven = models.DateTimeField(db_column='ProOrgVen', blank=True, null=True)  # Field name made lowercase.
    prousaprg = models.CharField(db_column='ProUsaPrg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    propestip = models.CharField(db_column='ProPesTip', max_length=5, blank=True, null=True)  # Field name made lowercase.
    profabcod = models.CharField(db_column='ProFabCod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    procenemp = models.IntegerField(db_column='ProCenEmp', blank=True, null=True)  # Field name made lowercase.
    procencod = models.IntegerField(db_column='ProCenCod', blank=True, null=True)  # Field name made lowercase.
    prolibsit = models.CharField(db_column='ProLibSit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prolibdat = models.DateTimeField(db_column='ProLibDat', blank=True, null=True)  # Field name made lowercase.
    probnfedat = models.DateTimeField(db_column='ProBNfeDat', blank=True, null=True)  # Field name made lowercase.
    probnfeser = models.CharField(db_column='ProBNfeSer', max_length=3, blank=True, null=True)  # Field name made lowercase.
    probnfenro = models.DecimalField(db_column='ProBNfeNro', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    probnfsdat = models.DateTimeField(db_column='ProBNfsDat', blank=True, null=True)  # Field name made lowercase.
    probobs = models.CharField(db_column='ProBObs', max_length=50, blank=True, null=True)  # Field name made lowercase.
    probficmod = models.CharField(db_column='ProBFicMod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profrmrevn = models.SmallIntegerField(db_column='ProFrmRevN', blank=True, null=True)  # Field name made lowercase.
    profrmrevd = models.DateTimeField(db_column='ProFrmRevD', blank=True, null=True)  # Field name made lowercase.
    profrmemid = models.DateTimeField(db_column='ProFrmEmiD', blank=True, null=True)  # Field name made lowercase.
    propfarevn = models.SmallIntegerField(db_column='ProPfaRevN', blank=True, null=True)  # Field name made lowercase.
    propfarevd = models.DateTimeField(db_column='ProPfaRevD', blank=True, null=True)  # Field name made lowercase.
    propfaemid = models.DateTimeField(db_column='ProPfaEmiD', blank=True, null=True)  # Field name made lowercase.
    proeiprevn = models.SmallIntegerField(db_column='ProEipRevN', blank=True, null=True)  # Field name made lowercase.
    proeiprevd = models.DateTimeField(db_column='ProEipRevD', blank=True, null=True)  # Field name made lowercase.
    proeipcadd = models.DateTimeField(db_column='ProEipCadD', blank=True, null=True)  # Field name made lowercase.
    proforqui = models.CharField(db_column='ProForQui', max_length=200, blank=True, null=True)  # Field name made lowercase.
    propesmol = models.CharField(db_column='ProPesMol', max_length=15, blank=True, null=True)  # Field name made lowercase.
    profun = models.CharField(db_column='ProFun', max_length=254, blank=True, null=True)  # Field name made lowercase.
    prodesqui = models.CharField(db_column='ProDesQui', max_length=400, blank=True, null=True)  # Field name made lowercase.
    procor = models.CharField(db_column='ProCor', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proalc = models.CharField(db_column='ProAlc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proaci = models.CharField(db_column='ProAci', max_length=1, blank=True, null=True)  # Field name made lowercase.
    protox = models.CharField(db_column='ProTox', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proinf = models.CharField(db_column='ProInf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    probio = models.CharField(db_column='ProBio', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prodadseg = models.CharField(db_column='ProDadSeg', max_length=254, blank=True, null=True)  # Field name made lowercase.
    promodusa = models.CharField(db_column='ProModUsa', max_length=400, blank=True, null=True)  # Field name made lowercase.
    pronatfis = models.CharField(db_column='ProNatFis', max_length=50, blank=True, null=True)  # Field name made lowercase.
    progarqui = models.CharField(db_column='ProGarQui', max_length=254, blank=True, null=True)  # Field name made lowercase.
    procomnf = models.CharField(db_column='ProComNF', max_length=70, blank=True, null=True)  # Field name made lowercase.
    pronom = models.CharField(db_column='ProNom', max_length=120, blank=True, null=True)  # Field name made lowercase.
    procla = models.CharField(db_column='ProCla', max_length=25, blank=True, null=True)  # Field name made lowercase.
    probmtgemp = models.IntegerField(db_column='ProBMtgEmp', blank=True, null=True)  # Field name made lowercase.
    probteremp = models.IntegerField(db_column='ProBTerEmp', blank=True, null=True)  # Field name made lowercase.
    prodat = models.DateTimeField(db_column='ProDat', blank=True, null=True)  # Field name made lowercase.
    prosta = models.CharField(db_column='ProSta', max_length=7, blank=True, null=True)  # Field name made lowercase.
    prosubnom = models.CharField(db_column='ProSubNom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    proconest = models.CharField(db_column='ProConEst', max_length=13, blank=True, null=True)  # Field name made lowercase.
    progruemp = models.IntegerField(db_column='ProGruEmp', blank=True, null=True)  # Field name made lowercase.
    progrucod = models.IntegerField(db_column='ProGruCod', blank=True, null=True)  # Field name made lowercase.
    promaremp = models.IntegerField(db_column='ProMarEmp', blank=True, null=True)  # Field name made lowercase.
    profat = models.DecimalField(db_column='ProFat', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    protft = models.CharField(db_column='ProTft', max_length=13, blank=True, null=True)  # Field name made lowercase.
    proempunv = models.IntegerField(db_column='ProEmpUnv', blank=True, null=True)  # Field name made lowercase.
    proempune = models.IntegerField(db_column='ProEmpUne', blank=True, null=True)  # Field name made lowercase.
    proempunc = models.IntegerField(db_column='ProEmpUnc', blank=True, null=True)  # Field name made lowercase.
    proncmemp = models.IntegerField(db_column='ProNcmEmp', blank=True, null=True)  # Field name made lowercase.
    prorefemp = models.IntegerField(db_column='ProRefEmp', blank=True, null=True)  # Field name made lowercase.
    proalmemp = models.IntegerField(db_column='ProAlmEmp', blank=True, null=True)  # Field name made lowercase.
    proalmcod = models.SmallIntegerField(db_column='ProAlmCod', blank=True, null=True)  # Field name made lowercase.
    procattip = models.CharField(db_column='ProCatTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prolisger = models.CharField(db_column='ProLisGer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prolisemi = models.CharField(db_column='ProLisEmi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proriccod = models.IntegerField(db_column='ProRicCod', blank=True, null=True)  # Field name made lowercase.
    proripcod = models.IntegerField(db_column='ProRipCod', blank=True, null=True)  # Field name made lowercase.
    protcpcod = models.IntegerField(db_column='ProTcpCod', blank=True, null=True)  # Field name made lowercase.
    progdtemp = models.IntegerField(db_column='ProGdtEmp', blank=True, null=True)  # Field name made lowercase.
    progdtcod = models.SmallIntegerField(db_column='ProGdtCod', blank=True, null=True)  # Field name made lowercase.
    proiqqemp = models.IntegerField(db_column='ProIqqEmp', blank=True, null=True)  # Field name made lowercase.
    proiqqcod = models.SmallIntegerField(db_column='ProIqqCod', blank=True, null=True)  # Field name made lowercase.
    progptemp = models.IntegerField(db_column='ProGptEmp', blank=True, null=True)  # Field name made lowercase.
    progptcod = models.IntegerField(db_column='ProGptCod', blank=True, null=True)  # Field name made lowercase.
    proimobil = models.CharField(db_column='ProImobil', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stpcod = models.SmallIntegerField(db_column='StpCod', blank=True, null=True)  # Field name made lowercase.
    proser = models.CharField(db_column='ProSer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    protip = models.CharField(db_column='ProTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    promarluc = models.DecimalField(db_column='ProMarLuc', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procub = models.DecimalField(db_column='ProCub', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    promovuni = models.CharField(db_column='ProMovUni', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prodesfat = models.DecimalField(db_column='ProDesFat', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procubord = models.IntegerField(db_column='ProCubOrd', blank=True, null=True)  # Field name made lowercase.
    prodsccrtemp = models.IntegerField(db_column='ProDscCrtEmp', blank=True, null=True)  # Field name made lowercase.
    prodsccrt = models.IntegerField(db_column='ProDscCrt', blank=True, null=True)  # Field name made lowercase.
    pronrmemp = models.IntegerField(db_column='ProNrmEmp', blank=True, null=True)  # Field name made lowercase.
    pronrmcod = models.IntegerField(db_column='ProNrmCod', blank=True, null=True)  # Field name made lowercase.
    pronrmtstemp = models.IntegerField(db_column='ProNrmTstEmp', blank=True, null=True)  # Field name made lowercase.
    pronrmtstcod = models.IntegerField(db_column='ProNrmTstCod', blank=True, null=True)  # Field name made lowercase.
    proexgcrt = models.CharField(db_column='ProExgCrt', max_length=1)  # Field name made lowercase.
    procrtcrp = models.CharField(db_column='ProCrtCrp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procrtlig = models.CharField(db_column='ProCrtLig', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procrtdrz = models.CharField(db_column='ProCrtDrz', max_length=1, blank=True, null=True)  # Field name made lowercase.
    propon = models.IntegerField(db_column='ProPon', blank=True, null=True)  # Field name made lowercase.
    probrin = models.CharField(db_column='ProBrin', max_length=1, blank=True, null=True)  # Field name made lowercase.
    protskemp = models.IntegerField(db_column='ProTskEmp', blank=True, null=True)  # Field name made lowercase.
    protskcod = models.CharField(db_column='ProTskCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    protavemp = models.IntegerField(db_column='ProTavEmp', blank=True, null=True)  # Field name made lowercase.
    protavcod = models.CharField(db_column='ProTavCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    procavcod = models.CharField(db_column='ProCavCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procavnom = models.CharField(db_column='ProCavNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proeavcod = models.CharField(db_column='ProEavCod', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prolnhemp = models.IntegerField(db_column='ProLnhEmp', blank=True, null=True)  # Field name made lowercase.
    prolnhcod = models.CharField(db_column='ProLnhCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    proavi = models.CharField(db_column='ProAvi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pronometq = models.CharField(db_column='ProNomEtq', max_length=150, blank=True, null=True)  # Field name made lowercase.
    promedalt = models.DecimalField(db_column='ProMedAlt', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    promedlar = models.DecimalField(db_column='ProMedLar', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    promedcomp = models.DecimalField(db_column='ProMedComp', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    proori = models.CharField(db_column='ProOri', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profamemp = models.IntegerField(db_column='ProFamEmp', blank=True, null=True)  # Field name made lowercase.
    profamcod = models.IntegerField(db_column='ProFamCod', blank=True, null=True)  # Field name made lowercase.
    prodirroh = models.CharField(db_column='ProDirRoh', max_length=1, blank=True, null=True)  # Field name made lowercase.
    probinfcnl = models.CharField(db_column='ProBInfCnl', max_length=254, blank=True, null=True)  # Field name made lowercase.
    probnbgemp = models.IntegerField(db_column='ProBNbgEmp', blank=True, null=True)  # Field name made lowercase.
    probnbgnro = models.IntegerField(db_column='ProBNbgNro', blank=True, null=True)  # Field name made lowercase.
    protvbctr = models.SmallIntegerField(db_column='ProTvbCtr', blank=True, null=True)  # Field name made lowercase.
    protvbemp = models.IntegerField(db_column='ProTvbEmp', blank=True, null=True)  # Field name made lowercase.
    protvbcod = models.IntegerField(db_column='ProTvbCod', blank=True, null=True)  # Field name made lowercase.
    promedare = models.DecimalField(db_column='ProMedAre', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prooprajucnj = models.CharField(db_column='ProOprAjuCnj', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prosus = models.CharField(db_column='ProSus', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prosol = models.CharField(db_column='ProSol', max_length=50, blank=True, null=True)  # Field name made lowercase.
    proevesub = models.CharField(db_column='ProEveSub', max_length=400, blank=True, null=True)  # Field name made lowercase.
    proind = models.CharField(db_column='ProInd', max_length=400, blank=True, null=True)  # Field name made lowercase.
    procul1 = models.CharField(db_column='ProCul1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procul2 = models.CharField(db_column='ProCul2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procul3 = models.CharField(db_column='ProCul3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procul4 = models.CharField(db_column='ProCul4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodos1 = models.CharField(db_column='ProDos1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodos2 = models.CharField(db_column='ProDos2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodos3 = models.CharField(db_column='ProDos3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodos4 = models.CharField(db_column='ProDos4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proapl1 = models.CharField(db_column='ProApl1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proapl2 = models.CharField(db_column='ProApl2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proapl3 = models.CharField(db_column='ProApl3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proapl4 = models.CharField(db_column='ProApl4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodil1 = models.CharField(db_column='ProDil1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodil2 = models.CharField(db_column='ProDil2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodil3 = models.CharField(db_column='ProDil3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodil4 = models.CharField(db_column='ProDil4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    proph = models.DecimalField(db_column='ProPH', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prodentec = models.CharField(db_column='ProDenTec', max_length=100, blank=True, null=True)  # Field name made lowercase.
    promodapl = models.CharField(db_column='ProModApl', max_length=50, blank=True, null=True)  # Field name made lowercase.
    proreputi = models.CharField(db_column='ProRepUti', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proultloc = models.IntegerField(db_column='ProUltLoc', blank=True, null=True)  # Field name made lowercase.
    prossdseq = models.DecimalField(db_column='ProSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    procest = models.CharField(db_column='ProCest', max_length=9, blank=True, null=True)  # Field name made lowercase.
    proempvin = models.IntegerField(db_column='ProEmpVin', blank=True, null=True)  # Field name made lowercase.
    profilvin = models.IntegerField(db_column='ProFilVin', blank=True, null=True)  # Field name made lowercase.
    proprjnom = models.CharField(db_column='ProPrjNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    propltnro = models.CharField(db_column='ProPltNro', max_length=10, blank=True, null=True)  # Field name made lowercase.
    prokitqtd = models.SmallIntegerField(db_column='ProKitQtd', blank=True, null=True)  # Field name made lowercase.
    propesbol = models.DecimalField(db_column='ProPesBol', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    probtmldemp = models.IntegerField(db_column='ProBTmldEmp', blank=True, null=True)  # Field name made lowercase.
    probtmldcod = models.IntegerField(db_column='ProBTmldCod', blank=True, null=True)  # Field name made lowercase.
    protipser = models.CharField(db_column='ProTipSer', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pronroci = models.CharField(db_column='ProNroCi', max_length=20, blank=True, null=True)  # Field name made lowercase.
    proclatop = models.IntegerField(db_column='ProClaTop', blank=True, null=True)  # Field name made lowercase.
    proexgser = models.CharField(db_column='ProExgSer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prollc = models.SmallIntegerField(db_column='ProLLC', blank=True, null=True)  # Field name made lowercase.
    provisrep = models.CharField(db_column='ProVisRep', max_length=1, blank=True, null=True)  # Field name made lowercase.
    provisven = models.CharField(db_column='ProVisVen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    provisdis = models.CharField(db_column='ProVisDis', max_length=1, blank=True, null=True)  # Field name made lowercase.
    proonuqtd = models.CharField(db_column='ProOnuQtd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prorissub = models.CharField(db_column='ProRisSub', max_length=10, blank=True, null=True)  # Field name made lowercase.
    prorencodnat = models.IntegerField(db_column='ProRenCodNat', blank=True, null=True)  # Field name made lowercase.
    propespul = models.CharField(db_column='ProPesPul', max_length=1, blank=True, null=True)  # Field name made lowercase.
    probtemp = models.SmallIntegerField(db_column='ProBTemp', blank=True, null=True)  # Field name made lowercase.
    probrelpln = models.CharField(db_column='ProBRelPln', max_length=1, blank=True, null=True)  # Field name made lowercase.
    probrelprt = models.CharField(db_column='ProBRelPrt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    probmatmol = models.CharField(db_column='ProBMatMol', max_length=50, blank=True, null=True)  # Field name made lowercase.
    probobspln = models.CharField(db_column='ProBObsPln', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    proconestvig = models.DateTimeField(db_column='ProConEstVig', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRO01'
        unique_together = (('mstcod', 'procod'),)


class Pro02(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, ProCod, ProCatItm) found, that is not supported. The first column is selected.
    procod = models.CharField(db_column='ProCod', max_length=12)  # Field name made lowercase.
    procatitm = models.SmallIntegerField(db_column='ProCatItm')  # Field name made lowercase.
    procatemp = models.IntegerField(db_column='ProCatEmp', blank=True, null=True)  # Field name made lowercase.
    procatfor = models.IntegerField(db_column='ProCatFor', blank=True, null=True)  # Field name made lowercase.
    procatapr = models.CharField(db_column='ProCatApr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatfis = models.CharField(db_column='ProCatFis', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatfic = models.CharField(db_column='ProCatFic', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatlit = models.CharField(db_column='ProCatLit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatskl = models.IntegerField(db_column='ProCatSkl', blank=True, null=True)  # Field name made lowercase.
    procatnfe = models.IntegerField(db_column='ProCatNFe', blank=True, null=True)  # Field name made lowercase.
    procatnfc = models.IntegerField(db_column='ProCatNFc', blank=True, null=True)  # Field name made lowercase.
    procatfax = models.CharField(db_column='ProCatFax', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatune = models.IntegerField(db_column='ProCatUne', blank=True, null=True)  # Field name made lowercase.
    procatuni = models.CharField(db_column='ProCatUni', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procaticm = models.DecimalField(db_column='ProCatIcm', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatred = models.DecimalField(db_column='ProCatRed', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatsit = models.CharField(db_column='ProCatSit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procatipi = models.DecimalField(db_column='ProCatIpi', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatimp = models.CharField(db_column='ProCatImp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatconnom = models.CharField(db_column='ProCatConNom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procatconfon = models.CharField(db_column='ProCatConFon', max_length=15, blank=True, null=True)  # Field name made lowercase.
    procatconfax = models.CharField(db_column='ProCatConFax', max_length=15, blank=True, null=True)  # Field name made lowercase.
    procatconema = models.CharField(db_column='ProCatConEma', max_length=150, blank=True, null=True)  # Field name made lowercase.
    procaticmcre = models.CharField(db_column='ProCatIcmCre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatipicre = models.DecimalField(db_column='ProCatIpiCre', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatncmemp = models.IntegerField(db_column='ProCatNcmEmp', blank=True, null=True)  # Field name made lowercase.
    procatncmcod = models.CharField(db_column='ProCatNcmCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    procatcom = models.CharField(db_column='ProCatCom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    procatpro = models.CharField(db_column='ProCatPro', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procatemb = models.CharField(db_column='ProCatEmb', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procatobs = models.CharField(db_column='ProCatObs', max_length=254, blank=True, null=True)  # Field name made lowercase.
    procatipisitcod = models.CharField(db_column='ProCatIpiSitCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procatpissitcod = models.CharField(db_column='ProCatPisSitCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procatpisali = models.DecimalField(db_column='ProCatPisAli', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatpisred = models.DecimalField(db_column='ProCatPisRed', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatpiscre = models.CharField(db_column='ProCatPisCre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatcofsitcod = models.CharField(db_column='ProCatCofSitCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procatcofali = models.DecimalField(db_column='ProCatCofAli', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatcofred = models.DecimalField(db_column='ProCatCofRed', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatcofcre = models.CharField(db_column='ProCatCofCre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatqtm = models.DecimalField(db_column='ProCatQtm', max_digits=13, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procattft = models.CharField(db_column='ProCatTft', max_length=13, blank=True, null=True)  # Field name made lowercase.
    procatfat = models.DecimalField(db_column='ProCatFat', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatcdm = models.CharField(db_column='ProCatCdm', max_length=60, blank=True, null=True)  # Field name made lowercase.
    procatgarqui = models.CharField(db_column='ProCatGarQui', max_length=400, blank=True, null=True)  # Field name made lowercase.
    procatnatfis = models.CharField(db_column='ProCatNatFis', max_length=50, blank=True, null=True)  # Field name made lowercase.
    procatorgtip = models.CharField(db_column='ProCatOrgTip', max_length=2, blank=True, null=True)  # Field name made lowercase.
    procatorgcod = models.CharField(db_column='ProCatOrgCod', max_length=30, blank=True, null=True)  # Field name made lowercase.
    procatcofcred = models.DecimalField(db_column='ProCatCofCred', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatpiscred = models.DecimalField(db_column='ProCatPisCred', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatforpre = models.CharField(db_column='ProCatForPre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    procatmulcom = models.DecimalField(db_column='ProCatMulCom', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    empcod = models.IntegerField(db_column='EmpCod', blank=True, null=True)  # Field name made lowercase.
    procaticmdif = models.DecimalField(db_column='ProCatIcmDif', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatadrem = models.DecimalField(db_column='ProCatAdRem', max_digits=11, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    procatfcv = models.DecimalField(db_column='ProCatFcv', max_digits=11, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRO02'
        unique_together = (('mstcod', 'procod', 'procatitm'),)

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
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (PdvEmpCod, PdvFilCod, PdvPfxCod, PdvCod, PdvItmPar) found, that is not supported. The first column is selected.
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')  # Field name made lowercase.
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)  # Field name made lowercase.
    pdvcod = models.IntegerField(db_column='PdvCod')  # Field name made lowercase.
    pdvitmpar = models.SmallIntegerField(db_column='PdvItmPar')  # Field name made lowercase.
    pdvvenpra = models.SmallIntegerField(db_column='PdvVenPra', blank=True, null=True)  # Field name made lowercase.
    pdvvenpar = models.DateTimeField(db_column='PdvVenPar', blank=True, null=True)  # Field name made lowercase.
    pdvvalpar = models.DecimalField(db_column='PdvValPar', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvmodpar = models.DecimalField(db_column='PdvModPar', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvsubpar = models.DecimalField(db_column='PdvSubPar', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvvenrea = models.DateTimeField(db_column='PdvVenRea', blank=True, null=True)  # Field name made lowercase.
    pdvpartip = models.CharField(db_column='PdvParTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdvparpor = models.DecimalField(db_column='PdvParPor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pdvparevedat = models.DateTimeField(db_column='PdvParEveDat', blank=True, null=True)  # Field name made lowercase.
    pdvparevetxt = models.CharField(db_column='PdvParEveTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pdvparadtbxa = models.DateTimeField(db_column='PdvParAdtBxa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PDV04'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvitmpar'),)

class Pdv06(models.Model):
    pdvempcod = models.IntegerField(db_column='PdvEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (PdvEmpCod, PdvFilCod, PdvPfxCod, PdvCod, PdvObsItm) found, that is not supported. The first column is selected.
    pdvfilcod = models.IntegerField(db_column='PdvFilCod')  # Field name made lowercase.
    pdvpfxcod = models.CharField(db_column='PdvPfxCod', max_length=5)  # Field name made lowercase.
    pdvcod = models.IntegerField(db_column='PdvCod')  # Field name made lowercase.
    pdvobsitm = models.SmallIntegerField(db_column='PdvObsItm')  # Field name made lowercase.
    pdvobsdet = models.TextField(db_column='PdvObsDet', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'PDV06'
        unique_together = (('pdvempcod', 'pdvfilcod', 'pdvpfxcod', 'pdvcod', 'pdvobsitm'),)


class Ftd01(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, GddGdrCod, GddCod, MtgCod) found, that is not supported. The first column is selected.
    gddgdrcod = models.CharField(db_column='GddGdrCod', max_length=12)  # Field name made lowercase.
    gddcod = models.CharField(db_column='GddCod', max_length=12)  # Field name made lowercase.
    mtgcod = models.SmallIntegerField(db_column='MtgCod')  # Field name made lowercase.
    gddempcod = models.IntegerField(db_column='GddEmpCod', blank=True, null=True)  # Field name made lowercase.
    ftdagr = models.CharField(db_column='FtdAgr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ftdultitm = models.SmallIntegerField(db_column='FtdUltItm', blank=True, null=True)  # Field name made lowercase.
    fdtssdseq = models.DecimalField(db_column='FdtSsdSeq', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTD01'
        unique_together = (('mstcod', 'gddgdrcod', 'gddcod', 'mtgcod'),)


class Ftd02(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, GddGdrCod, GddCod, MtgCod, FtdItm) found, that is not supported. The first column is selected.
    gddgdrcod = models.CharField(db_column='GddGdrCod', max_length=12)  # Field name made lowercase.
    gddcod = models.CharField(db_column='GddCod', max_length=12)  # Field name made lowercase.
    mtgcod = models.SmallIntegerField(db_column='MtgCod')  # Field name made lowercase.
    ftditm = models.SmallIntegerField(db_column='FtdItm')  # Field name made lowercase.
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', blank=True, null=True)  # Field name made lowercase.
    ftcacod = models.CharField(db_column='FtcACod', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTD02'
        unique_together = (('mstcod', 'gddgdrcod', 'gddcod', 'mtgcod', 'ftditm'),)

class Ftc01(models.Model):
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtcAEmpCod, FtcACod) found, that is not supported. The first column is selected.
    ftcacod = models.CharField(db_column='FtcACod', max_length=5)  # Field name made lowercase.
    ftcanom = models.CharField(db_column='FtcANom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ftcaqtdbas = models.DecimalField(db_column='FtcAQtdBas', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftcauniemp = models.IntegerField(db_column='FtcAUniEmp', blank=True, null=True)  # Field name made lowercase.
    ftcaunicod = models.CharField(db_column='FtcAUniCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ftcatotmp = models.DecimalField(db_column='FtcATotMp', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftcaultmp = models.SmallIntegerField(db_column='FtcAUltMp', blank=True, null=True)  # Field name made lowercase.
    mstcod = models.IntegerField(db_column='MstCod', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTC01'
        unique_together = (('ftcaempcod', 'ftcacod'),)


class Ftc02(models.Model):
    ftcaempcod = models.IntegerField(db_column='FtcAEmpCod', primary_key=True)  # Field name made lowercase. The composite primary key (FtcAEmpCod, FtcACod, FtcBItm) found, that is not supported. The first column is selected.
    ftcacod = models.CharField(db_column='FtcACod', max_length=5)  # Field name made lowercase.
    ftcbitm = models.SmallIntegerField(db_column='FtcBItm')  # Field name made lowercase.
    ftcbproemp = models.IntegerField(db_column='FtcBProEmp', blank=True, null=True)  # Field name made lowercase.
    ftcbprocod = models.CharField(db_column='FtcBProCod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ftcbqtd = models.DecimalField(db_column='FtcBQtd', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftcbuniemp = models.IntegerField(db_column='FtcBUniEmp', blank=True, null=True)  # Field name made lowercase.
    ftcbunicod = models.CharField(db_column='FtcBUniCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ftcbqtdfix = models.CharField(db_column='FtcBQtdFix', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ftcbindper = models.DecimalField(db_column='FtcBIndPer', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ftcbobs = models.CharField(db_column='FtcBObs', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTC02'
        unique_together = (('ftcaempcod', 'ftcacod', 'ftcbitm'),)

class Teq01(models.Model):
    mstcod = models.IntegerField(db_column='MstCod', primary_key=True)  # Field name made lowercase. The composite primary key (MstCod, TeqCod) found, that is not supported. The first column is selected.
    teqcod = models.IntegerField(db_column='TeqCod')  # Field name made lowercase.
    teqnom = models.CharField(db_column='TeqNom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    teqsta = models.CharField(db_column='TeqSta', max_length=7)  # Field name made lowercase.
    teqtipreg = models.CharField(db_column='TeqTipReg', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEQ01'
        unique_together = (('mstcod', 'teqcod'),)