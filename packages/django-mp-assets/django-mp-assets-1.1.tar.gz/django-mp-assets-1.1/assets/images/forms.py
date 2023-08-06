
import json

from django import forms
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType

from assets.images.utils import refresh_logo


def build_images_form_class(image_model_):

    class ImagesForm(ImagesFormBase):

        image_model = image_model_

        images = forms.ModelMultipleChoiceField(
            image_model.objects.none(), required=False)

        class Meta(ImagesFormBase.Meta):
            model = image_model_.get_parent_model_class()

    return ImagesForm


class ImagesFormBase(forms.ModelForm):

    def __init__(
            self,
            data=None,
            files=None,
            instance=None,
            initial=None,
            **kwargs):

        self._images = instance.images.all() if instance else []

        initial = {'images': [i.id for i in self._images or []]}

        super().__init__(
            data=data,
            files=files,
            instance=instance,
            initial=initial,
            **kwargs)

        if self.is_bound:
            self.fields['images'].queryset = self.image_model.objects.all()

    @property
    def serialized_images(self):
        return json.dumps([
            {'id': i.id, 'url': i.get_preview_url()} for i in self._images
        ])

    @property
    def upload_url(self):
        ct = ContentType.objects.get_for_model(self.image_model)
        return reverse_lazy('images:upload', args=[ct.id])

    def commit(self, instance):

        instance.images.all().update(**{
            self.image_model.parent_field: None
        })

        ordering = {
            img_id: i for i, img_id in enumerate(self.data.getlist('images'))
        }

        for img in self.cleaned_data.get('images') or []:
            setattr(img, img.parent_field, instance)
            img.order = ordering[str(img.id)]
            img.save(update_fields=[img.parent_field, 'order'])

        refresh_logo(instance)

        return instance

    class Media:
        css = {
            'all': [
                'file-manager/file-manager.css',
                'dropzone/dropzone.min.css'
            ]
        }
        js = [
            'dropzone/dropzone.min.js',
            'file-manager/file-manager.js',
        ]

    class Meta:
        fields = ['images']


class UploadImageForm(forms.Form):

    url = forms.URLField(required=False)

    file = forms.ImageField(required=False)
