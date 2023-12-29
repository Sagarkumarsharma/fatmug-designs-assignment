from rest_framework import generics, status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone

#vendor apis using generic views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


#all apis of vendor again using APIView to show 
class VendorCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorListView(APIView):
    def get(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')

        if vendor_id:
            #if vendor_id is provided, filter by that specific vendor
            vendor = Vendor.objects.filter(id=vendor_id).first()

            if not vendor:
                return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        else:
            #if no vendor_id provided, list all vendors
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor.delete()
        return Response({"detail": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





#api using generic views to make the task easy and simple
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

#purchase order api using apiview
class PurchaseOrderCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderListView(APIView):
    def get(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        if po_id:
            purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        purchase_order.delete()
        return Response({"detail": "Purchase order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





class VendorPerformanceApiView(APIView):
    def get(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        
        if vendor_id:
            #if vendor_id is provided, retrieve the specific vendor
            vendor = get_object_or_404(Vendor, id=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        else:
            #if no vendor_id provided, return an error or handle as needed
            return Response({"detail": "Vendor ID not provided."}, status=400)


class AcknowledgePurchaseOrder(APIView):
    def post(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)

        #check if purchase order has already been acknowledged
        if purchase_order.acknowledgment_date:
            return Response({"detail": "Purchase order already acknowledged."}, status=status.HTTP_400_BAD_REQUEST)

        #update acknowledgment date with the current time
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        #recalculate average response time
        purchase_order.calculate_average_response_time()

        #serialize the updated purchase order
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)