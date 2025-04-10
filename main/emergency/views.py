from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
import traceback
# Create your views here.


#REST FRAMEWORK
@csrf_exempt
@api_view(['POST'])
def login_json(request): #tied to path '/login'
    logout(request)
    #resp = {"status": 'failed', 'msg': ''}
    resp = {}
    try:
       data = json.loads(request.body)
    except json.JSONDecodeError:
       return JsonResponse({"error": "Invalid JSON"}, status=400)
    print(data)
    username = str(data.get('username', ''))
    password = str(data.get('password', ''))
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print("Pass!")
            login(request, user)
            #resp['status'] = 'success'
            #resp['msg'] = 'Login successful'

            refresh = RefreshToken.for_user(user)
            resp = {
                            'status' : 'success',
                            'msg' : 'Login successful',
                          'refresh': str(refresh),
                          'access': str(refresh.access_token),
                      }
        else:
                resp['msg'] = 'This account is not active'
    else:
        resp['status'] = 'failure'
        resp['msg'] = 'Invalid username or password'

    return JsonResponse(resp)

@csrf_exempt
@api_view(['POST'])
def Emergency_response(request): #Red Button #tied to path '/help'
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
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=405)


@csrf_exempt
@api_view(['GET'])
def get_cities(request): #get_cities #tied to path /cities
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
def get_categories(request): #tied to path /categories
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
def get_Emergencies(request): #tied to path /helplist
    try:

        queryset = EmergencyRequest.objects.all()
        queryset = [
        {
        "name": en.name,
        "phone": en.phone,
        "city": en.city.name,
        "category": en.cat.name,
        "note": en.note,
        "lat": en.latitude,
        "lon": en.longitude
        }
        for en in queryset
        ]
        print(queryset)
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Customize the page size as needed
        page = paginator.paginate_queryset(queryset, request)
        serializer = HelpSerializer(page, many=True)
        return paginator.get_paginated_response({'Emergencies': serializer.data})

    except Exception as e:
        traceback.print_exc()
        print("problem")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@csrf_exempt
@api_view(['GET'])
def get_Emergency(request, id): #tied to path /helps/<str:id>
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
    
@csrf_exempt
@api_view(['GET'])
def get_blogpost(request): #tied to path /blog
    try:
        blogpost_list = Blogpost.objects.all()
        print(f'<blogpost_list>: {blogpost_list}')
        print(f'<blogpost_list_first_item_id>: {blogpost_list.first().id}')
        serializer = BlogpostSerializer(blogpost_list, many=True)
        print(f'<serialized_blogpost_list>: {serializer}')

        return Response({
        'posts': serializer.data
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@csrf_exempt
@api_view(['GET'])
def get_blogpost_page(request, id): #tied to path /blog/<str:id>
    #data = json.loads(request.body)
    #print(data)
    blog_id = id

    print(f'blog_id: {blog_id}')

        # Only try to return a specific emergency if emergency_id is provided and non-empty
    if blog_id not in (None, ''):
        try:
            blog_id = int(blog_id)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid id provided'}, status=400)

    blog = Blogpost.objects.filter(id=blog_id).first()
    print(f'blog_item: {blog}, {blog.author.name}')
    if blog:
        blog_images = list(BlogpostImage.objects.filter(blogpost=blog).all())
        print(blog_images)
        blog_images_filepaths = [b.blogpost_image_absolute_filepath() for b in blog_images]
        #Do not let this reach deployment
        context = {
            "imageUrl": '', ##Images are currently pending and untested
            "title": blog.title,
            "author": blog.author.name,
            "content": blog.content,
            "category": blog.category,
            "createdAt": blog.createdAt,
            "images" : blog_images_filepaths
            }
        return JsonResponse({"request": context})
    else:
        return JsonResponse({'status': 'error', 'message': 'Emergency not found'}, status=404)

@csrf_exempt
@api_view(['POST'])  
def add_blogpost(request): #tied to path /addblog
    print(f'request: {request}, {request.method}, {request.POST},')
    print(f'REQUEST FILES {request.FILES}')
    if request.method == 'POST':
        data = request.POST.dict()
        #print(data['title'])
        b = Blogpost(
            author = Suppliers.objects.first(), ## Important that it is a temporary value
            title = data['title'],
            content = data['content'],
            category = data['category']
            #have not validated with images yet, but this currently works for just text
                     )
        b.save()
        b_imgs_data = request.FILES.getlist('images')
        for b_img in b_imgs_data:
            b2 = BlogpostImage(
                blogpost = b,
                image_reference = b_img
            )
            b2.save()
        #data = json.loads(request.body)
        print("Received:", request)
        return JsonResponse({'message': 'Data received successfully!'})
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def supplier_page(request): #tied to path /add-suppliers for now
    print(f'request: {request}, {request.method}, {request.body}')
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(f'<DATA> {data}')
        cat_list = data['cat'].split(',')
        cat_list = [int(a) for a in cat_list]
        print(cat_list)
        print("Received:", request)
        #print(f"<TMP>{City.objects.filter(id=data['address']).first()}")
        b = Suppliers(
            name = data['name'],
            phone = data['phone'],
            latitude=0,
            longitude=0, #tmp values
            note = data['comment'],
            city = City.objects.get(id=data['address']),
                     )
        b.save()
        b.cat.set(cat_list)
        return JsonResponse({'message': 'Data received successfully!'})


