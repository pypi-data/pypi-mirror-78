from django.db import models
import django.forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import (InlinePanel, FieldPanel, MultiFieldPanel)
from wagtail.contrib.forms.models import FormBuilder, WagtailAdminFormPageForm
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, PageChooserPanel
from wagtail.core import fields
from wagtail.admin.edit_handlers import EditHandler
from wagtail.admin.edit_handlers import StreamFieldPanel

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from webspace.loader import get_model, get_class
from webspace.cms import constants


class MyFormBuilder(FormBuilder):

    def create_singleline_field(self, field, options):
        options['max_length'] = 255
        return django.forms.CharField(
            widget=django.forms.TextInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_multiline_field(self, field, options):
        return django.forms.CharField(
            widget=django.forms.Textarea(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_email_field(self, field, options):
        return django.forms.EmailField(
            widget=django.forms.EmailInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_url_field(self, field, options):
        return django.forms.URLField(
            widget=django.forms.URLInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_number_field(self, field, options):
        return django.forms.DecimalField(
            widget=django.forms.NumberInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_checkbox_field(self, field, options):
        return django.forms.BooleanField(
            widget=django.forms.CheckboxInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_date_field(self, field, options):
        return django.forms.DateField(
            widget=django.forms.DateInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def create_datetime_field(self, field, options):
        return django.forms.DateTimeField(
            widget=django.forms.DateTimeInput(attrs={
                'placeholder': field.placeholder,
                'required': field.required
            }),
            **options
        )

    def get_field_options(self, field):
        options = super().get_field_options(field)
        return options


class AFormField(AbstractFormField):
    form = ParentalKey('Form', related_name='form_fields')
    placeholder = models.CharField(verbose_name='Placeholder', max_length=255, blank=True)
    """
    icon = models.ForeignKey(
        'cms.IconSnippet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Icon"
    )
    """

    panels = AbstractFormField.panels + [
        FieldPanel('placeholder'),
        #  SnippetChooserPanel('icon')
    ]

    class Meta:
        abstract = True
        app_label = 'cms'

    def get_verbose_name(self):
        return ''


class FormSubmissionsPanel(EditHandler):
    template = "wagtailforms/edit_handlers/form_responses_panel.html"

    def render(self):
        FormSubmission = get_model('cms', 'FormSubmission')
        submissions = FormSubmission.objects.filter(form=self.instance)
        submission_count = submissions.count()

        if not submission_count:
            return ''

        return mark_safe(render_to_string(self.template, {
            'self': self,
            'submission_count': submission_count,
            'last_submit_time': submissions.order_by('submit_time').last().submit_time,
            'last_submissions': submissions.order_by('submit_time').all()[:10],
        }))

    def on_model_bound(self):
        if not self.heading:
            self.heading = '%s submissions' % self.model.get_verbose_name()


ActionManager = get_class('cms.blocks.actions', 'ActionManager')
action_manager = ActionManager()


class AForm(ClusterableModel):
    template = "wagtailforms/edit_handlers/form_responses_panel.html"

    base_form_class = WagtailAdminFormPageForm
    form_builder = MyFormBuilder
    submissions_list_view_class = None
    help_text = models.CharField(verbose_name="Nom du formulaire", max_length=100, default='', blank=True)
    text = fields.RichTextField(
        verbose_name="Texte avant le formulaire",
        default='',
        blank=True,
        features=settings.RICH_TEXT_FEATURES
    )
    text_align = models.CharField(
        choices=constants.ALIGN_TEXT_CHOICES,
        default=constants.ALIGN_TEXT_LEFT,
        max_length=100,
        help_text="Permet de changer le theme"
    )
    inline = models.BooleanField(default=False)

    button_text = models.CharField(
        verbose_name="Bouton text",
        max_length=250,
        default='Submit',
        blank=True
    )
    button_theme = models.CharField(
        verbose_name="Bouton theme",
        choices=constants.BUTTON_CHOICES,
        max_length=250,
        default=constants.BUTTON_PRIMARY_FULL,
        blank=True
    )

    redirection_url = models.CharField(verbose_name="Url de redirection", max_length=250, default='', blank=True)
    redirection_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Page de redirection après un formulaire validé"
    )

    animation = models.BooleanField(default=False)

    actions = action_manager.get_actions()

    fields_panel = [
        InlinePanel("form_fields", label="Menu Items")
    ]

    settings_panel = [
        FieldPanel("help_text"),
        MultiFieldPanel([
            FieldPanel("text"),
            FieldPanel("text_align"),
        ], "Text du haut"),
        MultiFieldPanel([
            FieldPanel("button_text"),
            FieldPanel('button_theme'),
        ], "Bouton"),
        MultiFieldPanel([
            PageChooserPanel("redirection_page"),
            FieldPanel('redirection_url'),
        ], "Redirection"),
        FieldPanel("inline"),
        FieldPanel("animation")
    ]

    submissions_panel = [
        FormSubmissionsPanel(),
    ]

    actions_panel = [
        StreamFieldPanel('actions'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(fields_panel, heading='Champs'),
        ObjectList(settings_panel, heading='Paramètres'),
        ObjectList(submissions_panel, heading='Soumissions'),
        ObjectList(actions_panel, heading='Actions'),
    ])

    class Meta:
        abstract = True
        app_label = 'cms'

    def __str__(self):
        return self.help_text

    def get_form_fields(self):
        return self.form_fields.all().order_by('sort_order')

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields())
        return fb.get_form_class()

    def get_form_parameters(self):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)
        toto = form_class(*args, **form_params)
        return toto

    def get_verbose_name():
        return ''


from wagtail.contrib.forms.models import AbstractFormSubmission


class AFormSubmission(AbstractFormSubmission):
    form = models.ForeignKey('cms.Form', related_name='submissions_form', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, related_name='submissions_page', on_delete=models.CASCADE)

    class Meta:
        abstract = True
        app_label = 'cms'
