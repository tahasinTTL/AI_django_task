from django.shortcuts import render
from .models import StockMarketData
from django.core.management.base import BaseCommand
import json
from django.http import HttpResponse

class StockView(BaseCommand):
    
    def import_data(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)


def import_data(request):
    json_file = 'stock_market_data.json'
    
    with open(json_file, 'r') as file:
            data = json.load(file)
            
    for items in data:
        save_data = StockMarketData(
            date = items['date'],
            trade_code = items['trade_code'],
            high = items['high'],
            low = items['low'],
            open = items['open'],
            close = items['close'],
            volume = items['volume'],
        )
        save_data.save()
        
    return HttpResponse({'msg': 'Saved data'})

def display_data(request):
    data = StockMarketData.objects.all()
    return render(request, 'templates/home.html', {'data': data})