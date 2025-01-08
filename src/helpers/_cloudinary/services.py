from django.conf import settings
from django.template.loader import get_template

def get_cloudinary_image_object(instance, 
                                field_name="image", 
                                as_html=False, 
                                format=None, 
                                width=1200):

    # Ensure the instance has the specified field
    if not hasattr(instance, field_name):
        return ""

    # Get the image object from the instance
    image_object = getattr(instance, field_name)
    if not image_object:  # Return empty if the field is empty
        return ""

    # Define options for the image transformation
    image_options = {
        "width": width
    }
    if format is not None:  # Add format option if specified
        image_options['format'] = format

    # Return HTML representation if requested
    if as_html:
        return image_object.image(**image_options)

    # Otherwise, return the image URL
    url = image_object.build_url(**image_options)
    return url


def get_cloudinary_video_object(instance, 
                                field_name="video", 
                                as_html=False, 
                                width=None, 
                                height=None, 
                                sign_url=True,  # For private videos
                                fetch_format="auto", 
                                quality="auto", 
                                controls=True, 
                                autoplay=True):

    # Ensure the instance has the specified field
    if not hasattr(instance, field_name):
        return ""

    # Get the video object from the instance
    video_object = getattr(instance, field_name)
    if not video_object:  # Return empty if the field is empty
        return ""

    # Define options for the video transformation
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay,
    }
    if width is not None:  # Add width option if specified
        video_options['width'] = width
    if height is not None:  # Add height option if specified
        video_options['height'] = height
    if height and width:  # Crop video if both width and height are specified
        video_options['crop'] = "limit"

    # Generate the video URL
    url = video_object.build_url(**video_options)

    # Return HTML representation if requested
    if as_html:
        template_name = "videos/snippets/embed.html"
        tmpl = get_template(template_name)  # Load the template
        cloud_name = settings.CLOUDINARY_CLOUD_NAME  # Get Cloudinary cloud name from settings
        _html = tmpl.render({
            'video_url': url,
            'cloud_name': cloud_name,
            'base_color': "#007cae"  # Base color for the video player
        })
        return _html

    # Otherwise, return the video URL
    return url
