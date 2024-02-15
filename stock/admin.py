from django.contrib import admin
from .models import StockMarketData
# Register your models here.


class StockAdmin(admin.ModelAdmin):
    # list_filter=['trade_code']
    # pass
    search_fields = ['trade_code']

# @StockAdmin
admin.site.register(StockMarketData, StockAdmin)