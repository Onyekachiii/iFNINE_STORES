from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from taggit.models import Tag
from django.db.models import Count, Avg
from ifnine_core.forms import ProductReviewForm
from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderProducts, ProductReview, WishList, Address
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from userauths.models import ContactUs, Profile
from django.core import serializers

import calendar
from django.db.models.functions import ExtractMonth


# To list products in homepage
def index(request):
    products = Product.objects.filter(product_status= "published", featured=True)
    
    context = {
        "products": products,
    }
    return render(request, 'core/index.html', context)


# To list products in shop
def product_list_view(request):
    products = Product.objects.filter(product_status= "published")
   
    
    context = {
        "products": products,

    }
    return render(request, 'core/product-list.html', context)
    

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'core/category-list.html', context)


# To list productzs in each category
def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status= "published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)


# To get all vendors
def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, 'core/vendor-list.html', context)


# To get vendor detail
def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(product_status= "published", vendor=vendor)
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, 'core/vendor-detail.html', context)


# To get a product detail
def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = ProductImages.objects.filter(product=product)
    # product_reviews = ProductReview.objects.filter(product=product)
    products = Product.objects.filter(product_status= "published", category=product.category).exclude(pid=pid)[:4]
    
    #To get all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    #Product review form
    review_form = ProductReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count == 1:
            make_review = False
    
    product_images = product.product_images.all()
    
    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "product_images": product_images,
        "reviews": reviews,
        "products": products,
    }
    return render(request, 'core/product-detail.html', context)

# To get a tag list
def tag_list(request, tag_slug=None):
    product = Product.objects.filter(product_status= "published").order_by('-id')
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = product.filter(tags__in=[tag])
        
    context = {
        "products" : products,
        "tag" : tag
    }
    
    return render(request, 'core/tag.html', context)


# To add reviews and ratings
def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }    
    
    average_review = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_review': average_review,
        }
    )
    

# To search for products
def search_view(request):
    query = request.GET.get('q')
    
    query = None
    if query is not None:
        products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by('-date')
    
    
        context = {
            "query": query,
            "products": products,
        }
        return render(request, 'core/search.html', context)
    
    else:
        messages.warning(request, "Please enter a search query")
        return redirect('core:index')


# To filter products by categories & vendors
def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    products = Product.objects.filter(product_status= "published").order_by("-id").distinct()
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
        
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data":data})


# To add to cart
def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'price': request.GET['price'],
        'qty':  request.GET['qty'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


# To list products in cart
@login_required
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])    
        return render(request, 'core/cart.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('core:index')
    
    
# To delete item from cart
@login_required
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


# To update cart
@login_required
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = int(request.GET['qty'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


# To checkout
@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    # Checking if cart_data_obj is in session
    if 'cart_data_obj' in request.session:
        
        # Getting total amount for paypal
        for product_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
        
        # Creating order objects
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount,
        )    
        
        # Getting total amount for the cart
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
            cart_order_products = CartOrderProducts.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price']),
            )

    host = request.get_host()
    paypal_dict = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : cart_total_amount,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice' : "INVOICE_NO-" + str(order.id),
        'currency_code' : "USD",
        'notify_url': 'http://{}{}'.format(host,reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('core:payment-completed')),
        'cancel_url': 'http://{}{}'.format(host,reverse('core:payment-failed')),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "Please specify one address in your profile")
        active_address = None
            
    return render(request, 'core/checkout.html', {'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button, 'active_address':active_address})
            

# To show invoice after payment
@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


# If payment fails
@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


# User Profile
@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    context = {
        "profile": profile,
    }
    
    return render(request, 'core/user-profile.html', context)


# To view user dashb oard
@login_required
def customer_dashboard(request):
    address = Address.objects.filter(user=request.user)
    
    
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    month = []
    total_orders = []
    
    for o in orders:
        month.append(calendar.month_name[o['month']])
        total_orders.append(o['count'])
    
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        
        new_address = Address.objects.create(
            user=request.user, 
            address=address, 
            mobile=mobile,
            )
        
        messages.success(request, "Address added succesfully")
        return redirect("core:dashboard")

    context = {
        "orders": orders,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)


# To view user history
@login_required
def user_history(request):
    order_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    context = {
        "order_list": order_list,
    }
    return render(request, 'core/user-history.html', context)

# To view order details
def order_detail(request, id):
    orders = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=orders)
    
    context = {
        "order_items": order_items,
    }
    return render(request, 'core/order-detail.html', context)

# To change address
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})

# For contact us page
def contact(request):
    return render(request, 'core/contact.html')

# For contact form
def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    message = request.GET['message']
    
    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        message = message,
    )
    
    data = {
        "bool": True,
        "message": "Message sent successfully"
    }
    return JsonResponse({"data":data})

# To add to wishlist
def add_to_wishlist(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    
    context = {}
    
    wishlist_count = WishList.objects.filter(user=request.user, product=product).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool": True,
        }
    else:
        new_wishlist = WishList.objects.create(
            product = product,
            user = request.user
        )
        context ={
            "bool": True,
        }
    
    return JsonResponse(context)

# To view wishlist
@login_required
def wishlist_view(request):
    wishlist = WishList.objects.filter(user=request.user)

    context = {
        "w" : wishlist,
    }
    return render(request, "core/wishlist.html", context)


# To remove from wishlist
@login_required
def remove_from_wishlist(request):
    pid = request.GET['id']
    wishlist = WishList.objects.filter(user=request.user)
    product = WishList.objects.get(id=pid)
    product.delete()
    
    context = {
        "bool" : True,
        "w": wishlist,
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data": data, "w": wishlist_json})
    
