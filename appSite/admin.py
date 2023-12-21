from django.contrib import admin
from appSite.models import AllowHostModel, SenderLogManagerModel, SenderLogModel
import appSite.globalvar as gv
import __version__

admin.site.site_header = 'Binance Resender'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Binance Resender Server ' + __version__.version


@admin.register(AllowHostModel)
class AdminAllowHostModel(admin.ModelAdmin):
    list_display = ['ip', 'datetime']

    def save_model(self, request, obj, form, change):
        obj.save()
        allowed_ips = self.get_allowed_ips()
        gv.set('allowed_ips', allowed_ips)

    @staticmethod
    def get_allowed_ips() -> list:
        allowed_ips = []
        for allowHostModel in AllowHostModel.objects.all():
            ip = allowHostModel.ip
            allowed_ips.append(ip)
        return allowed_ips


@admin.register(SenderLogManagerModel)
class AdminSenderLogManagerModel(admin.ModelAdmin):
    list_display = ['use_log']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        use_log = self.get_use_log()
        gv.set('use_log', use_log)

    @staticmethod
    def get_use_log() -> int:
        for senderLogManagerModel in SenderLogManagerModel.objects.all():
            use_log = senderLogManagerModel.use_log
            return use_log
        return SenderLogManagerModel.USE_LOG_CHOICES[0][0]


@admin.register(SenderLogModel)
class AdminSenderLogModel(admin.ModelAdmin):
    list_display = ['ip', 'datetime', 'status', 'error_msg']
    search_fields = ['ip']
    list_filter = ['datetime', 'status']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
