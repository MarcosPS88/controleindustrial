class AcedataRouter:
    """
    Direciona operações de banco de dados para o app 'acedata_core'
    que usa o banco de dados 'acedata'.
    """
    # Adicione aqui o nome de todos os apps que usarão o banco de dados 'acedata'.
    apps_acedata = ['acedata_core',
                    'sisven_pedidos'
                    ]

    def db_for_read(self, model, **hints):
        """
        Define que a leitura dos modelos em 'apps_acedata' deve usar o banco 'acedata'.
        """
        if model._meta.app_label in self.apps_acedata:
            return 'acedata'
        return None

    def db_for_write(self, model, **hints):
        """
        Define que a escrita nos modelos em 'apps_acedata' deve usar o banco 'acedata'.
        """
        if model._meta.app_label in self.apps_acedata:
            return 'acedata'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relações entre um app do 'acedata' e qualquer outro app.
        """
        if (
            obj1._meta.app_label in self.apps_acedata or
            obj2._meta.app_label in self.apps_acedata
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Garante que os modelos do 'acedata_core' só possam ser migrados
        para o banco de dados 'acedata'.
        """
        if app_label in self.apps_acedata:
            return db == 'acedata'
        elif db == 'acedata':
            # Impede que qualquer outro app seja migrado para o banco 'acedata'.
            return False
        return None
