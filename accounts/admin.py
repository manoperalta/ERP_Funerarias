from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'cargo', 'telefone', 'is_staff'
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('cargo', 'telefone', 'data_nascimento', 'endereco', 'foto_perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('cargo', 'telefone', 'data_nascimento', 'endereco', 'foto_perfil')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


