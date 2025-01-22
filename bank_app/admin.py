from django.contrib import admin
from .models import Account

# Register the Account model with the admin interface
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'balance', 'pin')  
    search_fields = ('account_number', 'user__username', 'user__email') 
    list_filter = ('user',)  
    
    fieldsets = (
        (None, {
            'fields': ('user', 'account_number', 'pin', 'balance')
        }),
    )

admin.site.register(Account, AccountAdmin)