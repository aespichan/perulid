from .clean import clean_text, clean_sentences
from langdetect import detect
import pickle
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer

class Classifier:

    def __init__(self, method, ngram_range = (2,4), max_features = 1000, threshold = 0.7):
        self.method = method
        self.threshold = threshold
        self.ngram_range = ngram_range
        self.max_features = max_features

    def fit(self, X, y):
        self.tf = TfidfVectorizer(analyzer = "char", ngram_range = self.ngram_range, 
            use_idf = True, max_features = self.max_features)
        X_tf = self.tf.fit_transform(X)
        print("Characterization done.")
        clf = CalibratedClassifierCV(self.method, method='sigmoid', cv=4)
        self.model = clf.fit(X_tf, y)
        print("Fit done.")

    def characterize(self, X):
        if type(X) is not str:
            test = clean_sentences(X)
        else:
            test = clean_text(X)
        return self.tf.transform(test)

    def predict(self, X):
        test_tf = self.characterize(X)
        return self.model.predict(test_tf)

    def probabilities(self, X):
        test_tf = self.characterize(X)
        return self.model.predict_proba(test_tf)

    '''
    Función que predice las clases considerando un threshold.
    Si la mayor probabilidad de pertenecer a una clase está por debajo
    del threshold entonces se usa la librería langdetect para predecir
    la lengua a la que pertenece.

    Inputs
    ------
    El texto que se va a clasificar

    Outputs
    -------
    predicition: la lengua predecida de cada oración del texto (puede ser español e ingles)
    probas: arreglo de tuplas (iso, probabilidad) ordenado por probabilidad para cada oración.
    '''
    def predict_proba(self, X):
        if type(X) is not str:
            test = clean_sentences(X)
        else:
            test = clean_text(X)

        test_tf = self.tf.transform(test)

        probabilities = self.model.predict_proba(test_tf)
        probas, predictions = [],[]

        for i in range(len(test)):
            ## Arreglo de indices de las probabilidades en orden descendente
            sorted_index = probabilities[i].argsort()[::-1]
            sorted_class = [(self.labels[index], probabilities[i][index]) for index in sorted_index]
            probas.append(sorted_class)
            
            max_index = sorted_index[0]
            
            if probabilities[i][max_index] < self.threshold:
                predictions.append(detect(test[i]))
            else:
                predictions.append(self.labels[max_index])

        return predictions, probas

    def save(self, filename):
        output = open(filename, 'wb')
        pickle.dump(self, output)
        output.close()

def load(filename):
    pkl_file = open(filename, 'rb')
    clf = pickle.load(pkl_file)
    pkl_file.close()

    return clf
