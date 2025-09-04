from core.utils.liara_upload import upload_to_liara
from shop.models import ProductImageModel


def handle_profile_image(profile, image_file, host):
    """Upload new profile image and delete old one if exists."""
    if image_file:
        # Delete old image
        profile.delete_image()

        # Save new image
        filename = f"profile/{profile.user.id}_{image_file.name}"
        if "onrender.com" in host:
            profile.image_url = upload_to_liara(image_file, filename)
        else:
            profile.image.save(filename, image_file)

        profile.save()


def handle_product_main_image(product, image_file, host):
    """Upload new main product image and delete old one if exists."""
    if image_file:
        product.delete_main_image()
        filename = f"products/{product.id}_{image_file.name}"
        if "onrender.com" in host:
            product.image_url = upload_to_liara(image_file, filename, folder="products")
        else:
            product.image.save(filename, image_file)
        product.save()

def handle_product_extra_images(product, extra_files, host):
    """Upload extra images for product."""

    for extra_file in extra_files:
        filename = f"products/extra/{product.id}_{extra_file.name}"
        if "onrender.com" in host:
            url = upload_to_liara(extra_file, filename)
            ProductImageModel.objects.create(product=product, url=url)
        else:
            img_instance = ProductImageModel(product=product)
            img_instance.file.save(filename, extra_file)
            img_instance.save()
