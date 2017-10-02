from ..models import Language
import numpy as np

def load_language_dict():
    language_dict = {}
    languages = list(Language.objects.all())

    for language in languages:
        language_dict[language.iso_code] = language.language_name

    return language_dict

_language_dict = load_language_dict()

def top_percentage(probabilities, proba_order, k):
    top = []
    probabilities *= 100
    probabilities = np.round(probabilities,3)
    languages = list(Language.objects.order_by('iso_code').all())
    for j in range(len(proba_order)):
        sentence_top = []
        remaining_proba = 100
        for i in range(k-1):
            index = proba_order[j][i]
            language = languages[index]
            proba = probabilities[j][index]
            remaining_proba -= proba

            sentence_top.append((language.language_name, proba))
        sentence_top.append(("Otros", round(remaining_proba,3)))
        top.append(sentence_top)
    return top

def iso_to_name(iso_list):
    language_list = []
    for iso in iso_list:
        language_list.append(_language_dict[iso])

    return language_list

