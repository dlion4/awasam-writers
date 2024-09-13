from awasam.orders.models import Course, Normal
from .choices import (
    ACADEMIC_LEVEL_CHOICES,
    ASSIGNMENT_SIZE_CHOICES,
    DEADLINE_CHOICES,
    ASSIGNMENT_TYPE_CHOICES,
    SUBJECT_CHOICES,
    ASSIGNMENT_SLIDES_SIZE_CHOICES,
    ASSIGNMENT_SOURCES_SIZE_CHOICES,
)
from django import forms


class CustomRadioSelect(forms.RadioSelect):
    template_name = 'dashboard/client/components/order/widgets/radio_select.html'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class NormalOrderForm(forms.ModelForm):
    academic_level = forms.ChoiceField(
        choices=ACADEMIC_LEVEL_CHOICES,
        widget=CustomRadioSelect(attrs={
           "onchange": "calculateValue()",
        })
    )
    deadline = forms.ChoiceField(
        choices=DEADLINE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    assignment_type = forms.ChoiceField(
        choices=ASSIGNMENT_TYPE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
        
    )
    spacing = forms.ChoiceField(
        choices=(
            ("1", "Double"),
            ("1.8", "Single"),
        ),
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    assignment_size = forms.ChoiceField(
        choices=ASSIGNMENT_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    slides = forms.ChoiceField(
        choices=ASSIGNMENT_SLIDES_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    sources = forms.ChoiceField(
        choices=ASSIGNMENT_SOURCES_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        )
    )
    citation = forms.ChoiceField(
        choices=(
            ('Harvard', 'Harvard'),
            ('Chicago', 'Chicago'),
            ('Turabian', 'Turabian'),
            ('APA', 'APA'),
            ('Other', 'Other'),
        ), 
        widget=CustomRadioSelect(attrs={}),
        required=False,
    )
    language = forms.ChoiceField(
        choices=(
        ('USA English', 'English (US)'),
        ('UK English', 'English (UK)'),
        ), 
        widget=CustomRadioSelect(attrs={
            "onchange": "calculateValue()",
        })
    )
    attach_plagiarism_report = forms.ChoiceField(
        widget=CustomRadioSelect(),
        choices=(
            ("0", "No"),
            ("1", "Yes"),
        )
    )
    uploads = MultipleFileField(required=False)
    price = forms.CharField(widget=forms.HiddenInput(),required=False)
    academic_level_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    deadline_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    subject_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    assignment_type_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    spacing_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    assignment_size_pages_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    slides_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    sources_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    citation_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    language_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    other_citation = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Please insert the citation type here"}),required=False)
    
    class Meta:
        model = Normal
        fields = [
            'academic_level',
            'topic',
            'deadline',
            'assignment_type',
            'subject',
            'spacing',
            'assignment_size',
            "slides",
            'sources',
            'citation',
            'other_citation',
            'language',
            'description',
            'uploads',
            'attach_plagiarism_report',
            
            # for the reading of the orders
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
            
            "price",
        ]
    
        widgets = {
            'topic': forms.TextInput(attrs={"class": "form-control", "placeholder": "Your project title"}),
            'description': forms.Textarea(attrs={"class": "form-control content", "placeholder": "Your paper  instructions"}),
        }
        

class CourseAddForm(forms.ModelForm):
    academic_level = forms.ChoiceField(
        required=True,
        choices=ACADEMIC_LEVEL_CHOICES,
        widget=CustomRadioSelect(attrs={
           "onchange": "handleChangeValue(this)",
        })
    )
    academic_level_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    subject = forms.ChoiceField(
        required=True,
        choices=SUBJECT_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "handleChangeValue(this)",
            },
        )
        
    )
    subject_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    
    
    class Meta:
        model = Course
        fields = [
            "academic_level",
            "academic_level_text",
            "title",
            "subject",
            "subject_text",
            "number_of_weeks_or_assignments",
            "description",
            "course_budget",
            "course_url",
            "student_username",
            "student_course_login_password",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title of your course"}),
            "number_of_weeks_or_assignments":forms.NumberInput(attrs={"class": "form-control", "placeholder": "1", }),
            "description": forms.Textarea(attrs={"class": "form-control content", "placeholder": "Course description", "rows": 5}),
            "course_budget": forms.NumberInput(attrs={"class": "input100 border-start-0 ms-0 form-control", "placeholder": "1000.00", }),
            "course_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com/course", }),
            "student_username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your username for login in with in your course platform"}),
            "student_course_login_password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your password for login in with in your course platform"}),
        }
        help_texts = {
            "student_course_login_password": "This password is case sensitive.",
            "number_of_weeks_or_assignments": "Number of weeks or number of assignments to be done for this course.",
            "course_url": "Please copy and paste the URL to the student login page of your course",
            "student_username": "Your username for login in =to the course portal",
        }
