from django.conf import settings
from .classifier import Classifier, serialize
from ..models import Sentence

from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
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

    n_min = 2
    n_max = 4
    max_features = 10000
    base_clf = LinearSVC()

    clf = CalibratedClassifierCV(base_clf, method='sigmoid', cv=4)
    tf = TfidfVectorizer(analyzer="char", ngram_range=(n_min, n_max), use_idf=True, max_features=max_features)
    X_tf = tf.fit_transform(X)
    print("Characterization done.")
    model = clf.fit(X_tf, y)
    print("Fit done.")

    sentence_classifier = Classifier(model, tf)

    # Serialize classifier
    serialize(sentence_classifier, path.join(settings.CLASSIFIER_DIR,'classifier.pkl'))
    print("Finished.")