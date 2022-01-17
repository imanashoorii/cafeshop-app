from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class PersonAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'refCode', 'is_staff', 'is_active']
    list_editable = ['is_active', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    readonly_fields = ['createdAt', 'updatedAt', 'last_login', 'date_joined']
    fieldsets = (
        (
            None, {
                "fields": ('username', 'password')
            }
        ),
        (
            "Personal info", {
                'fields': ('first_name', 'last_name', 'refCode')
            }
        ),
        (
            "Contact info", {
                'fields': ('phone', 'mobile', 'address', 'email')
            }
        ),
        (
            "Permissions", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (
            "Important dates", {
                'fields': ('last_login', 'date_joined', 'updatedAt', 'createdAt')
            }
        ),
    )


admin.site.register(User, PersonAdmin)
