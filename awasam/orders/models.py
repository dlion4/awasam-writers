from django.db import models
from awasam.users.models import Profile
from django.utils.text import slugify
from django.urls import reverse
from urllib.parse import quote
from django.db.models import QuerySet

import mimetypes
from .choices import (
    ACADEMIC_LEVEL_CHOICES,
    ASSIGNMENT_SIZE_CHOICES,
    DEADLINE_CHOICES,
    ASSIGNMENT_TYPE_CHOICES,
    SUBJECT_CHOICES,
    ASSIGNMENT_SLIDES_SIZE_CHOICES,
    ASSIGNMENT_SOURCES_SIZE_CHOICES,
    CITATION_CHOICES,
    EXPERT_CHOICES,
)

class NormalManager(models.Manager):
    def get_queryset(self):
        # Return only active objects
        return super().get_queryset().filter(is_active=True)

# Create your models here.
class Normal(models.Model):
    client = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="profile_normal_order",
    )
    academic_level = models.CharField(
        max_length=100,
        choices=ACADEMIC_LEVEL_CHOICES,
    )
    
    topic = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    deadline = models.CharField(
        max_length=100,
        choices=DEADLINE_CHOICES,
    )
    assignment_type = models.CharField(
        max_length=3000,
        choices=ASSIGNMENT_TYPE_CHOICES,
        
    )
    subject = models.CharField(
        max_length=200,
        choices=SUBJECT_CHOICES,
    )
    spacing = models.CharField(
        max_length=100,
        choices=(
            ("1", "Double"),
            ("1.8", "Single"),
        ),
    )
    assignment_size = models.CharField(
        max_length=100,
        choices=ASSIGNMENT_SIZE_CHOICES,
    )
    slides = models.CharField(
        max_length=100,
        choices=ASSIGNMENT_SLIDES_SIZE_CHOICES,
    )
    sources = models.CharField(
        max_length=100,
        choices=ASSIGNMENT_SOURCES_SIZE_CHOICES,
    )
    citation = models.CharField(
        max_length=300,
        choices=CITATION_CHOICES,
        blank=True,
    )
    other_citation = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    attach_plagiarism_report = models.CharField(
        max_length=5, default="0", help_text="value of 1 is yes")
    academic_level_text = models.CharField(max_length=100, blank=True)
    deadline_text = models.CharField(max_length=100, blank=True)
    subject_text = models.CharField(max_length=100, blank=True)
    assignment_type_text = models.CharField(max_length=100, blank=True)
    spacing_text = models.CharField(max_length=100, blank=True)
    assignment_size_pages_text = models.CharField(max_length=100, blank=True)
    slides_text = models.CharField(max_length=100, blank=True)
    sources_text = models.CharField(max_length=100, blank=True)
    citation_text = models.CharField(max_length=100, blank=True)
    language_text = models.CharField(max_length=100, blank=True)
    
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_revision = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    
    order_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    
    revision_instruction= models.TextField(blank=True, null=True)
    fine = models.DecimalField(max_digits=15, decimal_places=2, default=7.00)
    comment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=1, default="N")
    
    
    class Meta:
        get_latest_by = "order_date"
    
    def __str__(self):
        return str(self.topic)
    def get_client_order_absolute_url(self):
        return reverse(
            "dashboard:clients:orders:normal_order_detail_view", kwargs={
            "pk": self.pk,
            "normal_order_slug":self.slug,
            })
    def get_client_order_delete_url(self):
        return reverse(
            "dashboard:clients:orders:normal_order_delete_view", kwargs={
            "pk": self.pk,
            "normal_order_slug":self.slug,
            })
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.topic)
        return super().save(*args, **kwargs)
    
    
    def get_latest_normal_order(self):
        return NormalOrderCompleted.objects.filter(normal_order=self).latest()
    def get_normal_completed_order(self):
        return  NormalOrderCompleted.objects.filter(normal_order=self).filter(approved=True).latest()
    
    def get_normal_approve_order_url(self):
        completed_order = self.get_latest_normal_order()
        file_name = completed_order.file.name
        file_type, _ = mimetypes.guess_type(file_name)
        file_type = file_type or 'application/octet-stream'
        file_name_encoded = quote(file_name)
        return reverse(
            "dashboard:admins:admin_approve_order_view",
            kwargs={
                "pk": self.pk,
                "file_type": file_type,
                "file_name": file_name_encoded,
            }
        )
    def get_writer_order_absolute_url(self):
        return reverse(
                "dashboard:writers:normal_order_detail_view", 
                kwargs={
                "pk": self.pk,
                "normal_order_slug": self.slug,
            })
        
    def get_mark_normal_approved_order_url(self):
        return reverse(
                "dashboard:admins:mark_normal_approved_order_view", kwargs={
                "pk": self.pk,
                "normal_order_slug": self.slug,
            }
        )
        
    
    
class NormalOrderFile(models.Model):
    normal_order = models.ForeignKey(Normal, on_delete=models.CASCADE, related_name="order_files")
    uploads = models.FileField(blank=True, null=True, upload_to="norma_order/")


class NormalOrderCompleted(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="writer_normal_order")
    normal_order = models.ForeignKey(Normal, on_delete=models.CASCADE, related_name="normal_completed_order")
    file = models.FileField(upload_to='normal_order/completed/files/')
    comment = models.TextField(blank=True)
    completed_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Completed Order"
        verbose_name_plural = "Completed Orders"
        get_latest_by = "completed_date"
    def get_purchase_url(self):
        return reverse("dashboard:payments:purchase_paper", kwargs={"paper_id": self.pk})
    
    
class Course(models.Model):
    client = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="profile_course_order",
    )
    academic_level = models.CharField(
        max_length=100,
        choices=ACADEMIC_LEVEL_CHOICES,
    )
    academic_level_text = models.CharField(max_length=1000)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    subject = models.CharField(
        max_length=200,
        choices=SUBJECT_CHOICES,
    )
    subject_text = models.CharField(max_length=1000)
    number_of_weeks_or_assignments = models.IntegerField(default=1)
    description = models.TextField()
    course_budget = models.DecimalField(max_digits=15, decimal_places=2)
    course_url = models.URLField(max_length=3000)
    student_username = models.CharField(max_length=1000)
    student_course_login_password = models.CharField(max_length=3000, help_text="This is case sensitive")
    
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    
    order_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=1, default="C")
    
    class Meta:
        get_latest_by = "order_date"
    
    def __str__(self):
        return f"Course: ({self.title})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_writer_order_absolute_url(self):
        return reverse(
                "dashboard:writers:course_order_detail_view", 
                kwargs={
                "pk": self.pk,
                "course_order_slug": self.slug,
            })
        
    