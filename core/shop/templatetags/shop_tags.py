from django import template
from django.db.models import Count
from review.models import ReviewModel, ReviewStatusType

from shop.models import ProductStatusType, ProductModel, WishlistProductModel

register = template.Library()

def get_wishlist_items(user):
    """Return a list of product IDs in the user's wishlist."""
    if user.is_authenticated:
        return WishlistProductModel.objects.filter(user=user).values_list("product__id", flat=True)
    return []

@register.inclusion_tag("includes/latest-products.html", takes_context=True)
def show_latest_products(context):
    request = context.get("request")
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value).order_by("-created_at")[:8]
    wishlist_items = get_wishlist_items(request.user)
    return {"latest_products": latest_products, "request":request, "wishlist_items":wishlist_items}

@register.inclusion_tag("includes/similar-products.html", takes_context=True)
def show_similar_products(context, product):
    request = context.get("request")
    product_categories = product.category.all()
    similar_products = (
        ProductModel.objects.filter(
            status=ProductStatusType.publish.value,
            category__in=product_categories
        )
        .exclude(id=product.id)  
        .distinct()              
        .order_by("-created_at")[:4]  
    )
    wishlist_items = get_wishlist_items(request.user)

    return {"similar_products": similar_products, "request":request, "wishlist_items":wishlist_items}


@register.inclusion_tag("includes/review-summary.html")
def review_summary(product):
    reviews = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted.value)
    total = reviews.count()

    # شمارش ستاره‌ها
    rating_counts_raw = reviews.values("rate").annotate(count=Count("rate"))
    rating_counts = {i: 0 for i in range(1, 6)}
    for item in rating_counts_raw:
        rating_counts[item["rate"]] = item["count"]

    # محاسبه درصدها
    rating_percentages = {
        i: {
            "count": rating_counts[i],
            "percent": round((rating_counts[i] / total) * 100) if total > 0 else 0
        }
        for i in range(1, 6)
    }

    return {
        "product": product,
        "total_reviews": total,
        "rating_data": rating_percentages
    }
    
@register.filter
def dict_get(d, key):
    return d.get(int(key))