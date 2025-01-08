import uuid
import helpers
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Initialize Cloudinary configuration
helpers.cloudinary_init()

# Access control options for courses
class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email required"

# Publishing status options for courses and lessons
class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"

# Utility function to define the file upload path
def handle_upload(instance, filename):
    return f"{filename}"

# Generate a unique public ID for a model instance
def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"

# Generate a public ID prefix based on instance attributes
def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path.strip("/")
        return path
    public_id = instance.public_id
    model_name_slug = slugify(instance.__class__.__name__)
    return f"{model_name_slug}/{public_id}" if public_id else model_name_slug

# Retrieve the display name for an instance
def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    return getattr(instance, 'title', instance.__class__.__name__)

# Course model
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=get_public_id_prefix, 
        display_name=get_display_name,
        tags=["course", "thumbnail"]
    )
    access = models.CharField(
        max_length=5, 
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
    )
    status = models.CharField(
        max_length=10, 
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate a public ID before saving
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - Course"

    def get_thumbnail(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(self, field_name='image', as_html=False, width=382)

    def get_display_image(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(self, field_name='image', as_html=False, width=750)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

# Lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=['thumbnail', 'lesson'],
        blank=True,
        null=True
    )
    video = CloudinaryField(
        "video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        blank=True,
        null=True,
        type='private',
        tags=['video', 'lesson'],
        resource_type='video'
    )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(
        default=False, 
        help_text="If user does not have access to course, can they see this?"
    )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']

    def save(self, *args, **kwargs):
        # Automatically generate a public ID before saving
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path.rstrip("/")
        return f"{course_path}/lessons/{self.public_id}"

    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON

    @property
    def has_video(self):
        return self.video is not None

    def get_thumbnail(self):
        width = 382
        if self.thumbnail:
            return helpers.get_cloudinary_image_object(self, field_name='thumbnail', format='jpg', as_html=False, width=width)
        elif self.video:
            return helpers.get_cloudinary_image_object(self, field_name='video', format='jpg', as_html=False, width=width)
