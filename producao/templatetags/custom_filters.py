from django import template
from django.forms import Form

register = template.Library()

@register.filter(name='get_field_value')
def get_field_value(form: Form, op_pk: int):
    """ Tenta obter o valor de um campo dinâmico no formulário. """
    field_name = f'placas_op_{op_pk}'
    if field_name in form.fields:
        # Tenta obter o valor do form populado, senão o valor inicial
        value = form[field_name].value()
        if value is not None:
            return str(value).replace(',', '.') # Garante formato para o input
    return ""