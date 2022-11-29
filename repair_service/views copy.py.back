from django.http import Http404
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

class repairSubmit(APIView):
    def post(self, request, format=None):
        # We have to do Work order, for repair in repair_list, deliverMethod, customer info all tied to the same WO and SO. 
        latest_wo_id = ''
        #### First create and save new Work Order and Sales Order ####
        # try:
        #     workOrderSerializer = WorkOrderSerializer(data={
        #         "completed": False
        #     })

        #     if workOrderSerializer.is_valid():
        #         workOrderSerializer.save()
        #         latest_wo_id = int(Work_Order.objects.latest('id'))
        # except Exception as e:
        #     print(e)

        work_order = Work_Order.objects.create(delivery_method = request.data["deliveryMethod"])
        latest_wo_id = Work_Order.objects.latest('id')

        #### Get id's for newly  created WO and SO ####    

        #### Second create the customer info and delivery method ####
        try:
            print(request.data['contact'])
            CustomerContact.objects.create(
                first_name = request.data['contact']['firstName'],
                last_name = request.data['contact']['lastName'],
                email = request.data['contact']['email'],
                phone =  request.data['contact']['phone'],
                work_order = latest_wo_id
            )
            CustomerAddress.objects.create(
                street_line_one = request.data['address']['streetOne'],
                street_line_two = request.data['address']['streetTwo'],
                city = request.data['address']['city'],
                state = request.data['address']['state'],
                zip = request.data['address']['zip'],
                work_order = latest_wo_id
            )
            # customerContactSerializer = CustomerContactSerializer(data={
            #     'first_name': request.data['firstName'],
            #     'last_name': request.data['lastName'],
            #     'email': request.data['email'],
            #     'phone': request.data['phone'],
            #     'work_order': latest_wo_id

            # })
            # customerAddressSerializer = customerAddressSerializer(data={
            #     'street_line_one': request.data['streetOne'],
            #     'street_line_two': request.data['streetTwo'],
            #     'city': request.data['city'],
            #     'state': request.data['state'],
            #     'zip': request.data['zip'],
            #     'work_order': request.data['zip']
            # })
            

            # if customerContactSerializer.is_valid():
            #     customerContactSerializer.save()
            # if customerAddressSerializer.is_valid():
            #     customerAddressSerializer.save()
            
        except Exception as e:
            print(e)
        print(request.data['repairs'])
        #### Create repair for every repair submitted under this WO #### 
        if len(request.data['repairs']) > 1:
            for repair in request.data['repairs']:
                try:
                    Repair.objects.create(
                        brand = repair["brand"],
                        model = repair["model"],
                        serial = repair["serial"],
                        work_order = latest_wo_id,
                    )
                    # repairSerializer = RepairSerializer(data={
                    #     'brand': repair["brand"],
                    #     'model': repair["model"],
                    #     'serial': repair["serial"],
                    #     'work_order': latest_wo_id,
                    # })
                    # if repairSerializer.is_valid():
                    #     repairSerializer.save()
                    
                except Exception as e:
                    print(e)
        else:
            try:
                print(request.data['repairs'][0]["brand"])
                Repair.objects.create(
                    brand = request.data['repairs'][0]["brand"],
                    model = request.data['repairs'][0]["model"],
                    serial = request.data['repairs'][0]["serial"],
                    work_order = latest_wo_id,
                )
                # repairSerializer = RepairSerializer(data={
                #     'brand': request.data['repairs'][0]["brand"],
                #     'model': request.data['repairs'][0]["model"],
                #     'serial': request.data['repairs'][0]["serial"],
                #     'work_order': latest_wo_id,
                # })
                # if repairSerializer.is_valid():
                #     repairSerializer.save()
                

            except Exception as e:
                print(e)

        
        return Response( status=status.HTTP_201_CREATED)





# @api_view()
# def hello_world(request):
#     return Response({"message": "Hello, world!"})

# @api_view(['GET', 'POST'])
# def hello_world(request):
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})

# def post(self,request):
#     serializer = TodoSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)