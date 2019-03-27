from django.shortcuts import render
from .models import Person
from .serializer import PersonSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

@csrf_exempt
def PersonData(request):
    if request.method == 'GET':
        perdata=Person.objects.all()
        serializer=PersonSerializer(perdata, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        json_parser= JSONParser()
        data=json_parser.parse(request)
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Data Added":serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def person_detail(request, id):
    try:
        person_by_id=Person.objects.get(id=id)
    except Person.DoesNotExist as e:
        return JsonResponse({"error":"Given ID is not found."}, status=404)

    if request.method=='GET':
        # data=person_by_id
        serializer=PersonSerializer(person_by_id)
        return JsonResponse(serializer.data)

    elif request.method=='DELETE':
        person_by_id.delete()
        serializer=PersonSerializer(person_by_id)
        return JsonResponse({"Success":str(id)+'--Data Deleted'})

    elif request.method == 'PUT':
        json_parser=JSONParser()
        data1=request
        print(data1)
        data=json_parser.parse(request)
        print(data)
        serializer=PersonSerializer(person_by_id,data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors, status=400)
