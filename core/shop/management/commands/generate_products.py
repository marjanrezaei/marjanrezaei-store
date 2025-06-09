from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from shop.models import ProductModel, ProductCategoryModel
from accounts.models import User
import random
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent


class Command(BaseCommand):
    help = "Generate fake products with images"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()
        categories = ProductCategoryModel.objects.all()

        if not users.exists() or not categories.exists():
            self.stdout.write(self.style.ERROR("Ensure users and categories exist in the database!"))
            return
        
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
        ]
        
        for _ in range(20):  # Generate 20 fake products
            user = random.choice(users)
            title = fake.word()
            slug = slugify(title)
            description = fake.paragraph()
            stock = fake.random_int(min=1, max=500)
            status = random.choice([choice[0] for choice in ProductModel.status.field.choices])
            price = fake.random_int(min=10, max=1000)
            discount_percent = fake.random_int(min=0, max=50)
           
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image, "rb"), name = Path(selected_image).name)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                description=description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
                image=image_obj
            )

            product.category.set(random.sample(list(categories), k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("Successfully added fake products with images"))