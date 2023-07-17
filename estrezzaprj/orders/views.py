from django.shortcuts import render,redirect
from carts.models import *
from .models import *
from .forms import OrderForm
from django.http import JsonResponse

import datetime
import json

# Create your views here.

def payments(request):
    
    body = json.loads(request.body)
    print(body)
    # to get order total amount from Order:
    order = Order.objects.get(user= request.user, is_ordered= False, order_number= body['orderID'])
    
    # store trasaction details inside payment model:
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
        
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # move the cart_items to order product table 
    cart_items = CartItem.objects.filter(user= request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id= orderproduct.id)
        
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
        
    # reducing the quantity of sold products
    
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
        
    # clear the cart after ordering
    
    CartItem.objects.filter(user = request.user).delete()
    
    # send order number and trans id back to sendData method to payments.html via json response
    data = {
        'order_number': order.order_number,
        'transID' : payment.payment_id
    }
    return JsonResponse(data)



def place_order(request,total=0, quantity=0):
    current_user = request.user
    
    # if cart count is less than or equals Zero , redirect back to zero
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    
    if cart_count<=0 :
        return redirect('store')
    
    
    grand_total = 0
    gst = 0
    
    for cart_item in cart_items:
        
        total+= (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    gst = (18* total)/100
    grand_total = total+gst
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            
            # store all the information in order table
            
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            
            data.order_total = grand_total
            data.tax = gst
            data.ip = request.META.get('REMOTE_ADDR') #This will give the user ip
            
            data.save()
            
            # generate a order number
            
            yr = int(datetime.date.today().strftime('%Y')) #will give us today, current year
            dt = int(datetime.date.today().strftime('%d')) #will give us today, current date
            mt = int(datetime.date.today().strftime('%m')) #will give us today, current month
            
            d = datetime.date(yr,mt,dt) #d will give the year,month and date in this format
            current_date = d.strftime("%Y%m%d") #eg : 20230714
            
            order_number = current_date + str(data.id) # data.id -> we saved this data, its order id and unique 
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user= current_user, is_ordered = False, order_number=order_number)
            
            # to pass these values to payment lets create a context
            context = {
                'order':order,
                'cart_items': cart_items,
                'total': total,
                'gst' : gst,
                'grand_total': grand_total,
            }
            
            return render(request, 'orders/payments.html', context)
        
        else:
            return redirect('checkout')
            
def order_complete(request):
    
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price*i.quantity

        payment = Payment.objects.get(payment_id=transID)
        
        context = {
            'order' : order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            
        }
        return render(request, 'orders/order_complete.html',context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
        
        
            
            