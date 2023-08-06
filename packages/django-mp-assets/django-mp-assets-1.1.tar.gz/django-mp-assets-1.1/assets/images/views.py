
from urllib.error import HTTPError

from django.http.response import JsonResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from assets.images.forms import UploadImageForm


@csrf_exempt
@require_POST
@staff_member_required
def upload_image(request, content_type_id):

    form = UploadImageForm(data=request.POST, files=request.FILES)

    ct = ContentType.objects.get_for_id(content_type_id)

    image_model = ct.model_class()

    if form.is_valid():

        data = form.cleaned_data

        if data.get('url'):
            try:
                image = image_model.create_from_url(data['url'])
            except HTTPError as e:
                error = _('Can not upload {}: {}').format(data['url'], str(e))
                return HttpResponseBadRequest(error)

        elif data.get('file'):
            image = image_model.objects.create(file=data['file'])

        else:
            return HttpResponseBadRequest('No data')

        return JsonResponse({'id': image.id, 'url': image.get_preview_url()})

    return HttpResponseBadRequest('Data not valid')
