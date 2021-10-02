import random
from django.db import models
from django.conf import settings
from django.utils import timezone
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy


def upload_image(instance, filename):
    return f"posts/{filename}"


def custom_slugify(value):
    slug = value.split()
    if len(slug) > 5:
        slug = slug[:5]
    slug.append(str(random.randint(0, 99999)))
    return "_".join(slug)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            # filter to only published posts
            return super().get_queryset().filter(status="published")

    # protect will protect posts being deleted
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=100)
    excerpt = models.TextField(null=True)
    content = models.TextField()

    # image
    image = models.ImageField(
        ugettext_lazy("Image"), upload_to=upload_image, default="posts/default.jpg"
    )

    # use for identifying posts
    slug = AutoSlugField(populate_from="title", unique=True, slugify=custom_slugify)
    # slug = models.SlugField(max_length=255, unique_for_date="published")
    published = models.DateTimeField(default=timezone.now)

    # delete all posts if user got deleted
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, rel="blog_posts"
    )

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    status = models.CharField(max_length=10, choices=options, default="published")

    objects = models.Manager()

    # get all published objects
    post_objects = PostObjects()

    class Meta:
        ordering = [("-published")]  # decending, ascending is published

    def __str__(self):
        return self.title
