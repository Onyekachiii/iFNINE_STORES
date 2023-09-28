from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderProducts, ProductReview, WishList, Address
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to login before accessing your wishlist")
        wishlist = 0
    
    return{
        'categories': categories,
        'vendors': vendors,
        'wishlist': wishlist,
    }