from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from taggit.models import Tag
from ifnine_core.forms import ProductReviewForm
from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderItems, ProductReview, WishList, Address
from django.template.loader import render_to_string
from django.contrib import messages


# Create your views here.
def index(request):
    products = Product.objects.filter(product_status= "published", featured=True)
    
    context = {
        "products": products,
    }
    return render(request, 'core/index.html', context)


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


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status= "published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(product_status= "published", vendor=vendor)
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = ProductImages.objects.filter(product=product)
    # product_reviews = ProductReview.objects.filter(product=product)
    products = Product.objects.filter(product_status= "published", category=product.category).exclude(pid=pid)[:4]
    
    #To get all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    #Product review form
    review_form = ProductReviewForm()
    
    product_images = product.product_images.all()
    
    context = {
        "p": product,
        "review_form": review_form,
        "product_images": product_images,
        "reviews": reviews,
        "products": products,
    }
    return render(request, 'core/product-detail.html', context)

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

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
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
    
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        }
    )
    

def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by('-date')
    
    context = {
        "products": products,
        "query": query,
    }
    return render(request, 'core/search.html', context)


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


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])    
        return render(request, 'core/cart.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})
