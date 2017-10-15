from ..models import Language
import numpy as np

def load_language_dict():
    language_dict = {}
    languages = list(Language.objects.all())

    for language in languages:
        language_dict[language.iso_code] = language.language_name

    return language_dict

_language_dict = load_language_dict()

def top_percentage(probabilities, k):
    top = []

    for sample in probabilities:
        sample_top = []
        remaining_proba = 100
        for i in range(k-1):
            iso = sample[i][0]
            proba = round(sample[i][1]*100,3)
            remaining_proba -= proba
            sample_top.append((_language_dict[iso],proba))
        sample_top.append(("Otros",round(remaining_proba,3)))
        top.append(sample_top)

    return top

def iso_to_name(iso_list):
    language_list = []
    for iso in iso_list:
        if iso in _language_dict:
            language_list.append(_language_dict[iso])
        else:
            language_list.append(iso)

    return language_list

