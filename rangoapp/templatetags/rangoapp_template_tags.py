from django import template
from rangoapp.models import Category

register = template.Library()


@register.inclusion_tag('rangoapp/templatetags/cats.html')
def get_category_list(category=None):
    return {'cats': Category.objects.order_by('id'),
            'act_cat': category}
