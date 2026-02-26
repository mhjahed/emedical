# admin_tools/admin.py

from django.contrib import admin
from .models import SystemSetting, Notification, AuditLog, BackupLog


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_public', 'updated_at']
    list_filter = ['is_public']
    search_fields = ['key', 'value']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__email']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'description', 'created_at']
    list_filter = ['action', 'model_name', 'created_at']
    search_fields = ['description', 'user__email']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'user_agent', 'extra_data', 'created_at']


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_size', 'backup_type', 'status', 'created_at']
    list_filter = ['backup_type', 'status', 'created_at']