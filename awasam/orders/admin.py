from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Normal, NormalOrderFile, NormalOrderCompleted, Course
# Register your models here.
class NormalOrderFileInline(admin.StackedInline):
    model = NormalOrderFile
    extra = 0
    

@admin.register(Normal)
class NormalOrderAdmin(admin.ModelAdmin):
    list_display = (
        "academic_level_text",
        "deadline_text",
        "subject_text",
        "assignment_type_text",
        "spacing_text",
        "assignment_size_pages_text",
        "slides_text",
        "sources_text",
        "citation_text",
        "language_text",
        "is_paid",
        "is_completed",
        "is_revision",
        "order_date",
        "completed_date",
        "price",
    )
    inlines = [
        NormalOrderFileInline
    ]
    
    
@admin.register(NormalOrderCompleted)
class NormalOrderCompletedAdmin(admin.ModelAdmin):
    list_display = (
        "writer",
        "normal_order",
        "completed_date"
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "academic_level",
        "academic_level_text",
        "subject",
        "subject_text",
        "number_of_weeks_or_assignments",
        "course_budget",
        "course_url",
        "student_username",
        "student_course_login_password",
        "is_paid",
        "is_completed",
        "is_assigned",
        "order_date",
        "completed_date",
        "is_active",
    ]
