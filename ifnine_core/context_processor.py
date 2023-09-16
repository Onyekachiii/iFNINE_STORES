from ifnine_core.models import Product, ProductImages, Category, Vendor, CartOrder, CartOrderItems, ProductReview, WishList, Address



def default(request):
    categories = Category.objects.all()
    # address = Address.object.get(user=request.user)
    
    return{
        'categories': categories,
        # 'address': address
    }