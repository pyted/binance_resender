from django.apps import AppConfig
import appSite.globalvar as gv

gv.threading_init()


class AppsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appSite'
    verbose_name = 'Binance Resender Mananger'
