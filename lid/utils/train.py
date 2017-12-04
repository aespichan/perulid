from django.conf import settings
from .classifier import Classifier
from ..models import Sentence

from sklearn.svm import LinearSVC
import os.path as path

def sentences_dataset():
    sentences = Sentence.objects.all()
    X,y = [],[]
    for sentence in sentences:
        X.append(sentence.sentence)
        y.append(sentence.iso_code)

    return X,y

def train_model():
    X, y = sentences_dataset()
    base_clf = LinearSVC()
    sentence_classifier = Classifier(base_clf)
    sentence_classifier.fit(X, y)
    # Serialize classifier
    sentence_classifier.save(path.join(settings.CLASSIFIER_DIR,'classifier.pkl'))
    print("Finished.")