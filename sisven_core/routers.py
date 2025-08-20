class LegadoRouter:
    """
    Direciona operações de banco de dados para um conjunto de apps
    que usam o banco de dados 'sisven'.
    """
    # Crie uma lista com os nomes de todos os apps que usarão o banco legado
    apps_legados = ['sisven_users', 
                    'sisven_consulta_precos',
                    'sisven_conf_comissoes',
                    'sisven_core',
                    
                    ] 

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps_legados:
            return 'sisven'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.apps_legados:
            return 'sisven'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.apps_legados or
            obj2._meta.app_label in self.apps_legados
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.apps_legados:
            return db == 'sisven'
        elif db == 'sisven':
            return False
        return None