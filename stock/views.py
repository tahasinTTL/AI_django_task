from django.shortcuts import render
from .models import StockMarketData
from django.core.management.base import BaseCommand
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def update_data(request, pk):
    try:
        instance = StockMarketData.objects.get(pk=pk)
    except StockMarketData.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    
    if request.POST:
        content_type = request.headers.get('Content-Type')
        # if content_type == 'multipart/form-data':
        try:
            request_data = request.POST
            if not request_data:
                return HttpResponse("Empty request body", status=400)
            # Parse the JSON data
            data = request_data
            print(data)
            
            instance.date = data.get("date", instance.date)
            instance.trade_code = data.get("trade_code", instance.trade_code)
            instance.low = data.get("low", instance.low)
            instance.high = data.get("high", instance.high)
            instance.open = data.get("open", instance.open)
            instance.close = data.get("close", instance.close)
            instance.volume = data.get("volume", instance.volume)
            
            instance.save()
            return JsonResponse({'success': True}, status=201)
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(print(str(e), 'error in data'))
        # else:
        #     return HttpResponse("Invalid content type", content_type)
    else:
        return JsonResponse({'error': 'Something is wrong'}, status=400)
    