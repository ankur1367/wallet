from django.contrib import admin

from .models import Wallet, AccountStatement, Currency, DiffOperation

admin.site.register(Wallet)
admin.site.register(AccountStatement)
admin.site.register(Currency)
admin.site.register(DiffOperation)