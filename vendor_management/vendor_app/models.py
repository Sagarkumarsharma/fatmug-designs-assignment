from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils import timezone
from datetime import timedelta

class Vendor(models.Model):
    vendor_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=200)
    address = models.TextField()

    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    response_time = models.DurationField(null=True, blank=True)
    fulfilment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


    def calculate_on_time_delivery_rate(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self,
            status='completed',
            delivery_date__isnull=False
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            on_time_delivered_orders = completed_orders.filter(delivery_date__lte=timezone.now()).count()
            return (on_time_delivered_orders / total_completed_orders) * 100
        else:
            return 0.0

    def calculate_quality_rating_avg(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self,
            status='completed',
            quality_rating__isnull=False
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            quality_rating_sum = completed_orders.aggregate(quality_rating_sum=models.Sum('quality_rating'))['quality_rating_sum']
            return quality_rating_sum / total_completed_orders
        else:
            return 0.0

            


    from django.db.models import Sum, F, ExpressionWrapper, fields

    def calculate_average_response_time(self):
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=self,
            acknowledgment_date__isnull=False
        )
        total_acknowledged_orders = acknowledged_orders.count()

        if total_acknowledged_orders > 0:
            response_time_sum = acknowledged_orders.aggregate(
                response_time_sum=ExpressionWrapper(
                    Sum(F('acknowledgment_date') - F('issue_date')),
                    output_field=fields.DurationField()
                )
            )['response_time_sum']

            if response_time_sum is not None:
                #convert the timedelta to seconds
                response_time_seconds = response_time_sum.total_seconds()

                #convert the seconds back to timedelta
                average_response_time = timedelta(seconds=response_time_seconds / total_acknowledged_orders)

                return average_response_time
        return timedelta()  #return a zero dura


    def calculate_fulfilment_rate(self):
        total_orders = PurchaseOrder.objects.filter(vendor=self).count()
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=self, status='completed', quality_rating__isnull=True).count()

        return (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0.0

    def update_metrics(self):
        #implement your logic to update metrics for the Vendor
        #you can use similar logic as in the PurchaseOrder model's update_metrics method
        #nsure to replace the metrics calculation logic with your actual implementation

        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        self.quality_rating = self.calculate_quality_rating_avg()
        self.response_time = self.calculate_average_response_time()
        self.fulfilment_rate = self.calculate_fulfilment_rate()

        #save the updated metrics to the database
        self.save()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfilment_rate = models.FloatField()

    def __str__(self):
        return f'{self.vendor.name} - {self.date}'


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, default="")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null = True, default = None)
    order_date = models.DateField(null = True , default = None)
    items = models.JSONField(null=True, default=None)
    quantity = models.PositiveIntegerField(null = True, default = None)
    status = models.CharField(max_length=50, default = "pending")
    delivery_date = models.DateTimeField(null=True, blank=True, default=None)  # allow null and provide a default
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True, default=None)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
 

    def calculate_on_time_delivery_rate(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            delivery_date__isnull=False
        )
        on_time_delivered_orders = completed_orders.filter(delivery_date__lte=self.delivery_date)
        total_completed_orders = completed_orders.count()

        return (on_time_delivered_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0.0

    def calculate_quality_rating_avg(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            quality_rating__isnull=False
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            quality_rating_sum = completed_orders.aggregate(quality_rating_sum=models.Sum('quality_rating'))['quality_rating_sum']
            return quality_rating_sum / total_completed_orders
        else:
            return 0.0

            


    from django.db.models import Sum, F, ExpressionWrapper, fields

    def calculate_average_response_time(self):
        
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False
        )
        total_acknowledged_orders = acknowledged_orders.count()

        if total_acknowledged_orders > 0:
            response_time_sum = acknowledged_orders.aggregate(
                response_time_sum=ExpressionWrapper(
                    Sum(F('acknowledgment_date') - F('issue_date')),
                    output_field=fields.DurationField()
                )
            )['response_time_sum']

            #convert the timedelta to seconds
            response_time_seconds = response_time_sum.total_seconds()

            return response_time_seconds / total_acknowledged_orders
        else:
            return 0.0


    def calculate_fulfilment_rate(self):
        total_orders = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed', quality_rating__isnull=True).count()

        return (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0.0
    
    
    def update_historical_metrics(self, historical_performance):
        historical_performance.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        historical_performance.quality_rating_avg = self.calculate_quality_rating_avg()
        historical_performance.average_response_time = self.calculate_average_response_time()
        historical_performance.fulfilment_rate = self.calculate_fulfilment_rate()

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # update historcal performance metrics
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=self.vendor,
            date=self.delivery_date or self.order_date,  # use delivery_date if available, else order_date
            defaults={
                'on_time_delivery_rate': 0.0,
                'quality_rating_avg': 0.0,
                'average_response_time': 0.0,
                'fulfilment_rate': 0.0,
            }
        )
        self.update_historical_metrics(historical_performance)


        # here we are saving the historical performance record
        historical_performance.save()

    