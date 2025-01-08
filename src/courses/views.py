import helpers
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from . import services

# View for listing courses
def course_list_view(request):
    """
    Fetch and display a list of published courses.
    Uses different templates based on whether the request is a standard or an HTMX request.
    """
    queryset = services.get_publish_courses()  # Retrieve all published courses
    context = {
        "object_list": queryset  # Add the course list to the context
    }
    template_name = "courses/list.html"  # Default template for standard requests
    if request.htmx:
        # HTMX requests use a snippet template and limit the displayed courses
        template_name = "courses/snippets/list-display.html"
        context['queryset'] = queryset[:3]  # Limit to the first 3 courses
    return render(request, template_name, context)

# View for displaying course details
def course_detail_view(request, course_id=None, *args, **kwargs):
    """
    Fetch and display details of a specific course along with its lessons.
    Raises a 404 error if the course is not found.
    """
    course_obj = services.get_course_detail(course_id=course_id)  # Fetch the course details
    if course_obj is None:
        raise Http404  # Raise a 404 error if the course does not exist
    lessons_queryset = services.get_course_lessons(course_obj)  # Fetch the lessons for the course
    context = {
        "object": course_obj,  # Add the course object to the context
        "lessons_queryset": lessons_queryset,  # Add the lessons to the context
    }
    # return JsonResponse({"data": course_obj.id, 'lesson_ids': [x.path for x in lessons_queryset] })
    return render(request, "courses/detail.html", context)

# View for displaying lesson details
def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    """
    Fetch and display details of a specific lesson.
    Checks if email is required to access the lesson and redirects if necessary.
    Handles cases where the lesson is not published or has no video.
    """
    print(course_id, lesson_id)
    lesson_obj = services.get_lesson_detail(
        course_id=course_id,
        lesson_id=lesson_id
    )  # Fetch the lesson details
    if lesson_obj is None:
        raise Http404  # Raise a 404 error if the lesson does not exist
    
    # Check if email access is required for the lesson
    email_id_exists = request.session.get('email_id')
    if lesson_obj.requires_email and not email_id_exists:
        print(request.path)
        request.session['next_url'] = request.path  # Store the current path for redirection
        return render(request, "courses/email-required.html", {})  # Render the email-required template
    
    # Default template for lessons that are coming soon
    template_name = "courses/lesson-coming-soon.html"
    context = {
        "object": lesson_obj  # Add the lesson object to the context
    }

    # If the lesson is not marked as coming soon and has an associated video
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        """
        The lesson is published, and a video is available. Render the lesson template with video.
        """
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj, 
            field_name='video',  # Specify the field name for the video
            as_html=True,  # Return the video as an embeddable HTML element
            width=1250  # Set the width for the video player
        )
        context['video_embed'] = video_embed_html  # Add the video embed HTML to the context
    
    return render(request, template_name, context)
