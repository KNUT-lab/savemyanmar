from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


@csrf_exempt
@api_view(['POST'])
def Emergency_response(request): #Red Button
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
            print(data)
            Cty = City.objects.filter(id=data['address']).first()
            Cat = Categories.objects.filter(id=data['cat']).first()
            EmergencyRequest.objects.create(
                name = data['name'],
                phone_number = data['phone'],
                note =data['comment'],
                latitude =data['lat'],
                longitude =data['lon'],
                city = Cty,
                cat = Cat, 
            )

            return JsonResponse({'status': 'success', 'fields': {'name':f'll'}, 'pk':f'll' })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=405)


@csrf_exempt
@api_view(['GET'])
def get_cities(request): #get_cities
    # Retrieve all Category objects
    cus_list = City.objects.all()

    # Serialize the data
    serializer = CitySerializer(cus_list, many=True)

    # Return the serialized data in JSON format
    return Response({
        'cities': serializer.data
    })

@csrf_exempt
@api_view(['GET'])
def get_categories(request): #get_cities
    # Retrieve all Category objects
    cus_list = Categories.objects.all()

    # Serialize the data
    serializer = CategorySerializer(cus_list, many=True)

    # Return the serialized data in JSON format
    return Response({
        'categories': serializer.data
    })


@csrf_exempt
@api_view(['GET'])
def get_Emergencies(request):
    try:

        queryset = EmergencyRequest.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Customize the page size as needed
        page = paginator.paginate_queryset(queryset, request)
        serializer = HelpSerializer(page, many=True)
        return paginator.get_paginated_response({'Emergencies': serializer.data})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@csrf_exempt
@api_view(['GET'])
def get_Emergency(request, id):
    #data = json.loads(request.body)
    #print(data)
    emergency_id = id

        # Only try to return a specific emergency if emergency_id is provided and non-empty
    if emergency_id not in (None, ''):
        try:
            emergency_id = int(emergency_id)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid id provided'}, status=400)
    print(emergency_id)
    emergency = EmergencyRequest.objects.filter(id=emergency_id).first()
    if emergency:
        # Replace 'name' with the actual field you want to return.
        context = {
            "name": emergency.name,
            "phone": emergency.phone_number,
            "city": emergency.city.name,
            "category": emergency.cat.name,
            "note":emergency.note,
            "lat":emergency.latitude,
            "lon":emergency.longitude
            }
        return JsonResponse({"request": context})
    else:
        return JsonResponse({'status': 'error', 'message': 'Emergency not found'}, status=404)