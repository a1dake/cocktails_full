from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import *
from base.admin import BaseAdmin


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone')}),
        ('Личная информаця', {'fields': ('first_name', 'last_name', 'date_of_birth', 'avatar', 'gender')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
        ('Прочее', {'fields': ('jwt_updated_at', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_filter = (
        'roles',
        'is_admin',
        'is_active',
    )
    list_display = ('id', 'username', 'fio', 'date_joined', 'roles', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name',)
    ordering = ('id',)

    change_list_template = 'admin/user_profile_change_list.html'

    @display(description='ФИ')
    def fio(self, obj: User):
        return f'{obj.last_name or ""} {obj.first_name or ""}'.strip()


@admin.register(TempCode)
class TempCodeAdmin(BaseAdmin):
    list_display = ('id', 'email', 'verification_code', 'created_at')
    search_fields = ('id', 'email', 'verification_code', 'created_at')
    ordering = ('id',)


@admin.register(Referral)
class ReferralAdmin(BaseAdmin):
    list_display = ('id', 'user', 'code', 'description')
    search_fields = ('user__email', 'code', 'user__username', 'user__phone')
    ordering = ('id',)


@admin.register(Point)
class PointAdmin(BaseAdmin):
    list_display = ('id', 'user', 'points')
    search_fields = ('user__email', 'points', 'user__username', 'user__phone')
    ordering = ('id',)