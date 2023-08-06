from django.contrib import admin

from drf_expiring_token.models import ExpiringToken


@admin.register(ExpiringToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'expires',)
    fields = ('user',)
    ordering = ('-expires',)
