
from django.forms import Field, ValidationError
from django.utils.translation import ugettext_lazy as _

from assets.images.widgets import ImagesFormFieldWidget
from assets.images.forms import build_images_form_class


class ImagesFormField(Field):

    widget = ImagesFormFieldWidget
    form = None

    def __init__(self, image_model):
        self._image_model = image_model
        super().__init__()

    def init_form(self, *args, **kwargs):

        form_class = build_images_form_class(self._image_model)

        self.form = form_class(*args, **kwargs)
        self.widget.form = self.form

    def clean(self, *args, **kwargs):

        if not self.form.is_valid():
            raise ValidationError(_('Form is invalid.'))

        return self.form.cleaned_data

    def commit(self, *args, **kwargs):
        return self.form.commit(*args, **kwargs)
