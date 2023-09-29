from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderProducts, ProductReview, WishList, Address
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        # messages.warning(request, "You have no products in your wishlist")
        # wishlist = WishList.objects.filter(user=request.user)
        wishlist = 0
        
        
    
    return{
        'categories': categories,
        'vendors': vendors,
        'wishlist': wishlist,
    }