from django import forms

from awasam.orders.models import Course
from awasam.orders.models import Normal

from .choices import ACADEMIC_LEVEL_CHOICES
from .choices import ASSIGNMENT_SIZE_CHOICES
from .choices import ASSIGNMENT_SLIDES_SIZE_CHOICES
from .choices import ASSIGNMENT_SOURCES_SIZE_CHOICES
from .choices import ASSIGNMENT_TYPE_CHOICES
from .choices import CITATION_CHOICES
from .choices import DEADLINE_CHOICES
from .choices import EXPERT_CHOICES
from .choices import SUBJECT_CHOICES
from .choices import SOFTWARE_CHOICES


class CustomRadioSelect(forms.RadioSelect):
    template_name = "dashboard/client/components/order/widgets/radio_select.html"

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        return (
            [single_file_clean(d, initial) for d in data]
            if isinstance(data, (list, tuple))
            else [single_file_clean(data, initial)]
        )

class NormalOrderForm(forms.ModelForm):
    academic_level = forms.ChoiceField(
        choices=ACADEMIC_LEVEL_CHOICES,
        widget=CustomRadioSelect(attrs={
           "onchange": "calculateValue()",
        }),
    )
    deadline = forms.ChoiceField(
        choices=DEADLINE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
    )
    assignment_type = forms.ChoiceField(
        choices=ASSIGNMENT_TYPE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
    )
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
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
        ),
    )
    assignment_size = forms.ChoiceField(
        choices=ASSIGNMENT_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
    )
    slides = forms.ChoiceField(
        choices=ASSIGNMENT_SLIDES_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
    )
    sources = forms.ChoiceField(
        choices=ASSIGNMENT_SOURCES_SIZE_CHOICES,
        widget=forms.Select(
        attrs={
                "class": "form-control  py-2",
                "style": "cursor:pointer",
                "onchange": "calculateValue()",
            },
        ),
    )
    citation = forms.ChoiceField(
        choices=CITATION_CHOICES,
        widget=CustomRadioSelect(attrs={}),
        required=False,
    )
    language = forms.ChoiceField(
        choices=(
        ("USA English", "English (US)"),
        ("UK English", "English (UK)"),
        ),
        widget=CustomRadioSelect(attrs={
            "onchange": "calculateValue()",
        }),
    )
    attach_plagiarism_report = forms.ChoiceField(
        widget=CustomRadioSelect(),
        choices=(("0", "No"),("1", "Yes")),
    )
    uploads = MultipleFileField(required=False)
    price = forms.CharField(widget=forms.HiddenInput(),required=False)
    academic_level_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    deadline_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    subject_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    assignment_type_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    spacing_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    assignment_size_pages_text = forms.CharField(
        widget=forms.HiddenInput(),required=False)
    slides_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    sources_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    citation_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    language_text = forms.CharField(widget=forms.HiddenInput(),required=False)
    other_citation = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Please insert the citation type here"}),required=False)

    draft = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "selectgroup-input",  # Custom class
                "id": "draft_yes",  # ID for the checkbox
                "onchange": "calculate(this);",  # JavaScript event
                "value":"10.00",
            },
        ),
        label="Draft",
        help_text="Allows a review  version of the document before final submission.",
        required=False,
    )

    files_of_sources = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "selectgroup-input",
                "id": "files_yes",
                "onchange": "calculate(this.form);",
                "value": "10.00",
            },
        ),
        label="Files of Sources",
        help_text="You will be able to receive file copies of the sources.",
        required=False,
    )
    high_priority_status = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "selectgroup-input",
                "id": "priority_yes",
                "onchange": "calculate(this.form);",
                "value": "2.00",
            },
        ),
        label="High Priority Status",
        help_text="Your project will be treated with high priority.",
        required=False,
    )
    summary_1_page_option = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "selectgroup-input",
                "id": "summary_yes",
                "onchange": "calculate(this.form);",
                "value": "2.00",
            },
        ),
        label="1 Page Summary",
        help_text="A brief one-page summary of the project.",
        required=False,
    )
    ai_check_option = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "selectgroup-input",
                "id": "aicheck_yes",
                "onchange": "calculate(this.form);",
                "value": "10.00",
            },
        ),
        label="AI Check",
        help_text="Suitable for a basic level of AI verification at a lower cost.",
        required=False,
    )

    expert_type = forms.ChoiceField(
        choices=EXPERT_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "selectgroup-input",
                "onchange": "selectExpert(this);",
            },
        ),
        label="Type of Expert",
        required=False,
    )
    software_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "id": "softwareCheck",
                "onclick": "toggleSoftwareOptions(this)",
                "style": "width: 18px; height: 18px;",
            },
        ),
        label="If yes, check this box.",
    )

    software_options = forms.ChoiceField(
        choices=SOFTWARE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control select2-show-search form-select",
                "data-placeholder": "Choose software",
                "style": "display: none;",  # Hide initially
                "id": "softwareOptions",
            },
        ),
        label="Software",
    )

    class Meta:
        model = Normal
        fields = [
            "academic_level",
            "topic",
            "deadline",
            "assignment_type",
            "subject",
            "spacing",
            "assignment_size",
            "slides",
            "sources",
            "citation",
            "other_citation",
            "language",
            "description",
            "uploads",
            "attach_plagiarism_report",

            # Extra field
            "draft",
            "files_of_sources",
            "high_priority_status",
            "summary_1_page_option",
            "ai_check_option",
            "expert_type",
            "software_required",
            "software_options",


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
            "topic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your project title"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control content",
                    "placeholder": "Your paper  instructions"}),
        }


class CourseAddForm(forms.ModelForm):
    academic_level = forms.ChoiceField(
        required=True,
        choices=ACADEMIC_LEVEL_CHOICES,
        widget=CustomRadioSelect(attrs={
           "onchange": "handleChangeValue(this)",
        }),
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
        ),
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
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of your course"}),
            "number_of_weeks_or_assignments":forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "1"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control content",
                    "placeholder": "Course description", "rows": 5}),
            "course_budget": forms.NumberInput(
                attrs={"class": "input100 border-start-0 ms-0 form-control",
                       "placeholder": "1000.00"}),
            "course_url": forms.URLInput(
                attrs={"class": "form-control", "placeholder":
                    "https://example.com/course"}),
            "student_username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": """
                    Your username for login in with in your course platform""",
                    }),
            "student_course_login_password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": """
                    Your password for login in with in your course platform"""}),
        }
        help_texts = {
            "student_course_login_password": "This password is case sensitive.",
            "number_of_weeks_or_assignments": """
            Number of weeks or number of assignments to be done for this course.""",
            "course_url": """
            Please copy and paste the URL to the student login page of your course""",
            "student_username": "Your username for login in =to the course portal",
        }
