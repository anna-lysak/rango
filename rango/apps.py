from django.contrib.admin.apps import AdminConfig


class RangoAdminConfig(AdminConfig):
    default_site = 'rango.admin.RangoAdmin'