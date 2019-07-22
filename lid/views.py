from django.shortcuts import render, render_to_response
from django.conf import settings
from .utils.classifier import load
from .utils.clean import split_text, clean_line
from .utils.results import top_percentage, iso_to_name

import os.path as path
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from .models import Inverted_Word

# Create your views here.

def index(request):
    context = {}
    return render(request, 'lid/index.html', context)

def about(request):
    context = {}
    return render(request, 'lid/about.html', context)

def contact(request):
    context = {}
    return render(request, 'lid/about.html', context)

def results(request):
    classifier = load(path.join(settings.CLASSIFIER_DIR,'classifier.pkl'))
    text = clean_line(request.POST['text'])

    if 'option' in request.POST and 'persentence' in request.POST['option']:
        sentences = split_text(text)
        per_sentence = True
    else:
        sentences = [text]
        per_sentence = False

    if (len(sentences) < 1):
        context = {
            'success' : False,
            'message' : 'No se han encontrado oraciones para identificar el lenguaje. Texto ingresado:',
            'text' : request.POST['text']
        }
        return render_to_response('lid/results.html', context)

    pred, proba = classifier.predict_proba(sentences)
    top = top_percentage(proba, 5)
    prediction = iso_to_name(pred)

    pred = json.dumps(list(prediction), cls=DjangoJSONEncoder)
    top = json.dumps(list(top), cls=DjangoJSONEncoder)
    sentences = json.dumps(list(sentences), cls=DjangoJSONEncoder)
    per_sentence = json.dumps(per_sentence)

    context = {
        'success' : True,
        'pred' : pred,
        'proba' : top,
        'sentences' : sentences,
        'per_sentence' : per_sentence,
    }

    return render_to_response('lid/results.html', context)

def resources(request):
    context = {}
    return render(request, 'lid/resources.html', context)

def search_sentences(request):
    search_input = request.POST.get('search_input', None)
    iword_set = Inverted_Word.objects.filter(word = search_input)

    data = []
    for iword in iword_set:
        sentence = iword.sentence.sentence
        language = iword.sentence.file.language.language_name
        url = iword.sentence.file.source
        position = iword.position

        data.append({
            'sentence':sentence, 
            'language':language, 
            'url':url,
            'position':position,
        })

    return JsonResponse({"data":data})