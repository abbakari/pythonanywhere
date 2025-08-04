from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Ticket, Category, Budget, UserProfile, TicketMessage
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fields = ('department', 'office_name', 'phone', 'avatar', 'is_admin')

class UserAdminExtended(UserAdmin):
    inlines = (UserProfileInline,)
    add_form = UserCreationFormExtended
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdminExtended)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin', 'department', 'phone']
    list_filter = ['is_admin', 'department']
    search_fields = ['user__username', 'user__email', 'department']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'category', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at', 'is_internal']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['message', 'ticket__title']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'spent', 'remaining', 'category']
    list_filter = ['category']
    search_fields = ['name']
