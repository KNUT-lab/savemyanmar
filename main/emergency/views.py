from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
# Create your views here.


@csrf_exempt
def Emergency_response(request): #Red Button
    if request.method == 'GET':
        return render(request, 'help.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            return JsonResponse({'status': 'success', 'fields': {'name':f'll'}, 'pk':f'll' })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=405)