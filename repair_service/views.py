from django.http import Http404
from rest_framework import status
import requests
import json
import os
import datetime
from requests.exceptions import HTTPError

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
print(os.environ.get('X_API_KEY'))

class repairSubmit(APIView):
    def post(self, request, format=None):
        # We have to do Work order, for repair in repair_list, deliverMethod, customer info all tied to the same WO. 

        #### First create and save new Work Order and get newly created Work_Order ####
        work_order = Work_Order.objects.create(
            delivery_method = request.data["delivery_method"],
            collection_date = request.data["collection_date"]
            )
        latest_wo_id = Work_Order.objects.latest('id')  

        if request.data["delivery_method"] == 'local':
            print("running Detrack")
            # create Detract pickup with customer's pickup date:
            url = 'https://app.detrack.com/api/v2/dn/jobs'
            
            headers = {
                'Content-Type':'application/json',
                'X-API-KEY': os.environ.get('X_API_KEY'),
            }
            
            collection_date = datetime.datetime.strptime(request.data["collection_date"], "%Y-%m-%d").date()
            
            itemList = []
            if len(request.data['repairs']) > 1:
                for repair in request.data['repairs']:
                    itemList.append({
                        "sku": f"{repair['serial']}",
                        "description": f"{repair['serial']}\n{repair['brand']}-{repair['model']}",
                        "quantity": 1
                    })
            
            elif len(request.data['repairs']) < 1:
                itemList.append({
                    "sku": "none",
                    "description": "none",
                    "quantity": 1
                })
            else:
                itemList.append({
                    "sku": f"{request.data['repairs'][0]['serial']}",
                    "description": f"{request.data['repairs'][0]['serial']}\n{request.data['repairs'][0]['brand']}-{request.data['repairs'][0]['model']}",
                    "quantity": 1
                })


            payload = {
                "data": {
                    "type": "Collection",
                    "do_number": f"{latest_wo_id.id}c",
                    "date": f"{collection_date}",
                    "notify_email": f"{request.data['contact']['email']}",
                    "address": f"{request.data['address']['streetOne']}\n{request.data['address']['streetTwo']}\n{request.data['address']['city']} {request.data['address']['state']}, {request.data['address']['zip']}",
                    "items": itemList,
                    "assign_to": 'Old corolla',
                    "status": "dispatched",
                    "tracking_status": "Info received",
                }
            }
            

            try:
                r = requests.post(url, headers=headers, json=payload)
                # If the response was successful, no Exception will be raised
                r.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            else:
                print('Success!')

        #### Second create the customer info ####
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
            except Exception as e:
                print(e)   


        # if local is choosen then we will have to make a Collection job
        # in Detract app
        # next view addresses this, customer chooses collection date




        return Response( status=status.HTTP_201_CREATED)

