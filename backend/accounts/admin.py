from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User, Follow


class FollowAdminForm(ModelForm):
    class Meta:
        model = Follow
        fields = '__all__'

    def clean(self):
        super().clean()
        if self.cleaned_data['user'] == self.cleaned_data['following']:
            raise ValidationError("Нельзя подписываться на самого себя.")


class FollowAdmin(admin.ModelAdmin):
    form = FollowAdminForm


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('username', 'first_name', 'last_name', 'avatar')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name',
                       'password1', 'password2', 'is_active', 'is_staff',
                       'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)
