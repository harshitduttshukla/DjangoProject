# from django.shortcuts import render
# from .models import ChaiVarity
# from django.shortcuts import get_object_or_404

# # Create your views here.

# def all_chai(request):
#     chais = ChaiVarity.objects.all()
#     return render(request, 'harshit/all_chai.html',{'chais': chais})


# def chai_detail(request, chai_id):
#     chai = get_object_or_404(ChaiVarity, pk=chai_id)
#     return render(request,'harshit/chai_detail.html',{'chai': chai})


 


from django.http import JsonResponse,HttpResponseBadRequest
from .models import Producttt
from django.views.decorators.csrf import csrf_exempt
import json

def products_list(request):
    products = list(Producttt.objects.values())
    return JsonResponse(products,safe=False)

def product_detail(request, product_id):
    try:
        product = Producttt.objects.get(id=product_id)
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "description" : product.description,
        })
    except Producttt.DoesNotExist:
        return JsonResponse({"error":"product not found"},status = 404)
    

@csrf_exempt
def product_create(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed for product create")
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("Invalid JSON")

    product = Producttt.objects.create(
        name= data["name"],
        price=data["price"],
        description=data.get("description","")
    )

    return JsonResponse({"id":product.id,"message":"Created"},status=201)

@csrf_exempt
def product_update(request,product_id):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponseBadRequest("Only put and patch allowed")
    
    try:
        product = Producttt.objects.get(id=product_id)
    except Producttt.DoesNotExist:
        return JsonResponse({"error":"product not found"},status=404)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("Invalid JSON")

    product.name = data.get("name",product.name)
    product.price = data.get('price',product.price)
    product.description = data.get("description",product.description)
    product.save()

    return  JsonResponse({"message":"Update"})

@csrf_exempt
def product_delete(request,product_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Only DELETE Allowed")
    
    try:
        product = Producttt.objects.get(id=product_id)
        product.delete()
        return  JsonResponse({"message": "Deleted"})
    except Producttt.DoesNotExist:
        return JsonResponse({"error":"Product not found"},status=404)



        # new code for practes

    class CorrelationViewSet(viewsets.viewSet):
        @action(detail=False,methods=['post'],url_path='correlate')
        def correlate(self,request):
            """Correlate logs based on various criteria"""
        serializer = CorrelationSerializer(data=request.data)
        if not serialize.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_date
        time_window = data.get('time_window_minutes',10)

        if data.get('correlation_id'):
            logs = logCorrelationService.correlate_by_correlation_id(
                data['correlation_id',time_window]
            )
        elif data.get('source_ip'):
            logs = LogCorrelationService.correlate_by_source_ip(
                data['source_ip'],time_window
            )
        elif data.get('user'):
            log = LogCorrealtionServiece.correlate_by_user(
                data['user'],time_window
            )
        else:
            return Response(
                {'error':'At least one correlation field is required'},
                status = status.HTTP_400_BAD_REQUSET
            )
        serializer = LogEntrySerializer(logs,many=True)
        return Response({
            'count': logs.count(),
            'logs':serializer.data
        })
        
