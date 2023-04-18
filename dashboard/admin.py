from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import account as model_account,category as model_category,transaction as model_transaction
# Register your models here.
class accountinline(admin.TabularInline):
    model = model_account
    extra = 1

class categoryinline(admin.TabularInline):
    model = model_category
    extra = 1

class UserAdmin(AuthUserAdmin):
    inlines=[accountinline,categoryinline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(model_transaction)