from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from shop.models import ProductModel, ProductCategoryModel
from accounts.models import User
import random

class Command(BaseCommand):
    help = "Generate fake products with images"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()
        categories = ProductCategoryModel.objects.all()

        if not users.exists() or not categories.exists():
            self.stdout.write(self.style.ERROR("Ensure users and categories exist in the database!"))
            return

        for _ in range(20):  # Generate 20 fake products
            user = random.choice(users)
            title = fake.sentence(nb_words=3)
            slug = slugify(title)
            description = fake.paragraph()
            stock = fake.random_int(min=1, max=500)
            status = random.choice([choice[0] for choice in ProductModel.status.field.choices])
            price = fake.random_int(min=10, max=1000)
            discount_percent = fake.random_int(min=0, max=50)

            # Generate fake image URL (Example: Lorem Picsum or Unsplash placeholder)
            image_url = f"https://picsum.photos/400/400?random={random.randint(1,1000)}"

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                description=description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
                image=image_url
            )

            product.category.set(random.sample(list(categories), k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("Successfully added fake products with images"))