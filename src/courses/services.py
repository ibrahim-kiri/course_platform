from django.db.models import Q
from .models import Course, Lesson, PublishStatus

# Retrieves all published courses
def get_publish_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

# Retrieves the details of a specific course by its public_id
def get_course_detail(course_id=None):
    if course_id is None:  # Check if the course_id is provided
        return None
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishStatus.PUBLISHED,  # Ensure the course is published
            public_id=course_id             # Match the public_id
        )
    except Course.DoesNotExist:
        # Return None if no matching course is found
        pass
    return obj

# Retrieves the lessons of a given course that are published or coming soon
def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none()  # Initialize an empty QuerySet
    if not isinstance(course_obj, Course):  # Validate the input
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,  # Ensure the course is published
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON]  # Include lessons with appropriate statuses
    )
    return lessons

# Retrieves the details of a specific lesson by its public_id and associated course_id
def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None and course_id is None:  # Check if both parameters are provided
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,  # Match the course's public_id
            course__status=PublishStatus.PUBLISHED,  # Ensure the course is published
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],  # Include lessons with appropriate statuses
            public_id=lesson_id  # Match the lesson's public_id
        )
    except Lesson.DoesNotExist as e:
        # Handle the case where no matching lesson is found
        print("Lesson detail retrieval failed:", e)
        pass
    return obj
