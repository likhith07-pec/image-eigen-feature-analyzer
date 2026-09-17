from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .forms import ImageUploadForm
from .services import analyze_image


def analyzer_home(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        image_name = form.cleaned_data.get('image_name') or ''
        uploaded_image = form.cleaned_data.get('image')

        if uploaded_image:
            storage = FileSystemStorage(location=settings.MEDIA_ROOT / 'uploads')
            image_name = storage.save(uploaded_image.name, uploaded_image)

        if image_name:
            image_path = Path(settings.MEDIA_ROOT) / 'uploads' / image_name
            if image_path.exists():
                requested_k = form.cleaned_data.get('k') or 8
                result = analyze_image(image_path, requested_k)
                context.update(
                    {
                        'result': result,
                        'image_name': image_name,
                        'form': ImageUploadForm(
                            initial={'k': result['selected_k'], 'image_name': image_name}
                        ),
                    }
                )
            else:
                context['error'] = 'The selected image could not be found. Please upload it again.'
        else:
            context['error'] = 'Please choose an image to start the analysis.'

    return render(request, 'analyzer/home.html', context)
