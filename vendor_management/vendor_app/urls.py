from django.urls import path
from .views import ( 
    VendorListView, 
    VendorCreateView,
    VendorPerformanceApiView,
    AcknowledgePurchaseOrder,
    PurchaseOrderCreateView,
    PurchaseOrderListView,
    )

    #   VendorListCreateView, 
    # VendorRetrieveUpdateDestroyView,
    #   
    # 
    

urlpatterns = [
    #url for generic views api ,
    # path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'), 
    # path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'), #using primary key, retrieve,delete, update
    
    #url for generic views api for purchase order
    # path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    # path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase-order-retrieve-update-destroy'),
    

    #url for APIView apis,i create this crud combo only to show separate api for vendors,same thing we can do for purchare_order
    path('api/vendors/', VendorListView.as_view(), name='vendor-list'), #get api ,if yoou want reterieve data using params as vendor_id
    path('api/vendors/', VendorCreateView.as_view(), name='vendor-create'), #post api
    path('api/vendors/<int:vendor_id>/', VendorListView.as_view(), name='vendor-update'), #put api
    path('api/vendors/<int:vendor_id>/', VendorListView.as_view(), name='vendor-delete'), # delete api
    #url for vendor apis using APIView
    path('api/purchase_orders/', PurchaseOrderCreateView.as_view(), name='purchase-order-create'),
    path('api/purchase_orders_list/', PurchaseOrderListView.as_view(), name='purchase-order-list'), #list of all orders
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderListView.as_view(), name='purchase-order-detail'), #perform get,put,delete
    

    #url for vendor performance
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceApiView.as_view(), name='vendor-performance'),


    #acknowledged date
    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),
]

