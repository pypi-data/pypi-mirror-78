
from os.path import basename
from urllib.request import urlretrieve

from django.apps import apps
from django.db import models
from django.db.models.base import ModelBase
from django.core.files import File
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail
from ordered_model.models import OrderedModelBase


class ImageRecordMeta(ModelBase):

    def __new__(mcs, name, bases, attrs):

        new_attrs = dict(attrs)

        parent_field = attrs['parent_field']
        parent_model = attrs['parent_model']

        new_attrs[parent_field] = models.ForeignKey(
            parent_model,
            verbose_name=_("Parent"),
            related_name='images',
            on_delete=models.CASCADE,
            null=True,
            blank=True)

        new_attrs['file'] = models.ImageField(
            verbose_name=_("File"),
            upload_to=parent_field + '_images',
            max_length=255)

        new_attrs['order_with_respect_to'] = parent_field

        return super().__new__(mcs, name, bases, new_attrs)


class ImageRecord(OrderedModelBase):

    parent_model = None
    parent_field = ''

    order = models.PositiveIntegerField(_('Ordering'))

    order_field_name = 'order'

    def __str__(self):
        return str(self.parent)

    @property
    def parent(self):
        return getattr(self, self.parent_field)

    @classmethod
    def get_parent_model_class(cls):

        if isinstance(cls.parent_model, str):
            return apps.get_model(cls.parent_model)

        return cls.parent_model

    def get_preview_url(self):
        try:
            return get_thumbnail(self.file.file, '100').url
        except IOError:
            pass

        return ''

    @classmethod
    def create_from_url(cls, url):

        result = urlretrieve(url)

        return cls.objects.create(
            file=File(open(result[0], 'rb'), name=basename(url)))

    class Meta:
        abstract = True
        ordering = ['order']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class LogoField(models.ImageField):

    def __init__(
            self,
            verbose_name=_('Logo'),
            upload_to='logos',
            blank=True,
            null=True,
            max_length=255,
            editable=False,
            *args, **kwargs):

        super(LogoField, self).__init__(
            verbose_name=verbose_name,
            upload_to=upload_to,
            blank=blank,
            null=null,
            max_length=max_length,
            editable=editable,
            *args, **kwargs)
