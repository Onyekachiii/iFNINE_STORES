from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from taggit.models import Tag
from ifnine_core.forms import ProductReviewForm
from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderItems, ProductReview, WishList, Address

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
        "product": product,
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
    if query:
        products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by('-date')
    context = {
        "products": products,
        "query": query,
    }
    return render(request, 'core/search.html', context)