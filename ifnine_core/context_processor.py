from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderItems, ProductReview, WishList, Address



def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    return{
        'categories': categories,
        'vendors': vendors,
    }