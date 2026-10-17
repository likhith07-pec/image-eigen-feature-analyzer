from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .forms import ImageUploadForm
from .services import analyze_image
from .sarvam_ai import generate_mathematical_insight


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
                sarvam_insight = generate_mathematical_insight(result)
                context.update(
                    {
                        'result': result,
                        'image_name': image_name,
                        'sarvam_insight': sarvam_insight,
                        'form': ImageUploadForm(
                            initial={'k': result['selected_k'], 'image_name': image_name}
                        ),
                    }
                )
    if request.method == 'GET' and request.GET.get('demo'):
        sample_src = Path(settings.BASE_DIR) / 'sample_upload_image.png'
        if sample_src.exists():
            uploads_dir = Path(settings.MEDIA_ROOT) / 'uploads'
            uploads_dir.mkdir(parents=True, exist_ok=True)
            demo_target = uploads_dir / 'demo_sample.png'
            if not demo_target.exists():
                import shutil
                shutil.copy(sample_src, demo_target)
            try:
                requested_k = int(request.GET.get('k') or 16)
            except ValueError:
                requested_k = 16
            result = analyze_image(demo_target, requested_k)
            sarvam_insight = generate_mathematical_insight(result)
            context.update(
                {
                    'result': result,
                    'image_name': 'demo_sample.png',
                    'sarvam_insight': sarvam_insight,
                    'form': ImageUploadForm(
                        initial={'k': result['selected_k'], 'image_name': 'demo_sample.png'}
                    ),
                }
            )

    return render(request, 'analyzer/home.html', context)


import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .sarvam_ai import ask_sarvam_question, translate_sarvam_text


@csrf_exempt
def api_sarvam_chat(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = request.POST

    question = (data.get("question") or "").strip()
    language = (data.get("language") or "English").strip()
    matrix_context = data.get("context", {})
    history = data.get("history", [])

    if not question:
        return JsonResponse({"success": False, "error": "Question is required"}, status=400)

    res = ask_sarvam_question(question, language, matrix_context, history=history)
    return JsonResponse(res)


@csrf_exempt
def api_sarvam_translate(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = request.POST

    text = (data.get("text") or "").strip()
    language = (data.get("language") or "Hindi").strip()

    if not text:
        return JsonResponse({"success": False, "error": "Text is required"}, status=400)

    res = translate_sarvam_text(text, language)
    return JsonResponse(res)

