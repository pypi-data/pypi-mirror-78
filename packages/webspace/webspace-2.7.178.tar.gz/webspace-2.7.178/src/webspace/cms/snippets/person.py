from wagtail.images.models import Image
from django.db import models
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ClusterableModel


class APerson(ClusterableModel):
    help_text = models.CharField(max_length=100, default='', blank=True)

    first_name = models.CharField(blank=True, max_length=200, default='')
    last_name = models.CharField(blank=True, max_length=200, default='')
    title = models.CharField(default='', max_length=200, blank=True, help_text='Titre')
    description = RichTextField(default='', blank=True, help_text='Bio')

    email_contact = models.CharField(blank=True, max_length=200, default='')

    facebook = models.URLField(blank=True, help_text='Facebook page URL')
    instagram = models.URLField(blank=True, help_text='Instagram page URL')
    linkedin = models.URLField(blank=True, help_text='Linkedin page URL')
    twitter = models.URLField(blank=True, help_text='Twitter page URL')
    pinterest = models.URLField(blank=True, help_text='Pinterest page URL')
    youtube = models.URLField(blank=True, help_text='Youtube page URL')
    calendly = models.URLField(blank=True, help_text='Calendly URL')

    image_miniature = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image Miniature",
    )
    image_presentation = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image Presentation",
    )

    general_panels = [
        FieldPanel('help_text'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email_contact'),
        FieldPanel('title'),
        FieldPanel('description'),
    ]

    socials_panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('linkedin'),
        FieldPanel('twitter'),
        FieldPanel('youtube'),
        FieldPanel('pinterest'),
        FieldPanel('calendly'),
    ]

    images_panels = [
        ImageChooserPanel('image_miniature'),
        ImageChooserPanel('image_presentation'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(socials_panels, heading='Socials'),
        ObjectList(images_panels, heading='Images'),
    ])

    def __str__(self):
        return self.help_text

    class Meta:
        abstract = True
        app_label = 'cms'

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
