from .clean import clean_text
from langdetect import detect
import pickle

from ..models import Language

class Classifier:

    def __init__(self, model, tf, threshold = 0.7):
        self.model = model
        self.tf = tf
        self.threshold = threshold
        self.labels = list(Language.objects.exclude(family_id=-1).order_by('iso_code').values_list('iso_code', flat=True))

    def characterize(self,text):
        if type(text) is not str:
            return self.tf.transform(text)
        else:
            test = clean_text(text)
            return self.tf.transform(test)

    def predict(self, text):
        test_tf = self.characterize(text)
        return self.model.predict(test_tf)

    def probabilities(self, text):
        test_tf = self.characterize(text)
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
    pred: la lengua predecida de cada oración del texto
    probabilities: las probabilidades por cada lengua por cada oración
    sorted_proba: arreglo de índices de las probabilidades en orden 
        descendente por cada oración.
    '''
    def predict_proba(self, text):
        assert type(text) is str

        test = clean_text(text)
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

def serialize(clf, filename):
    output = open(filename, 'wb')
    pickle.dump(clf, output)
    output.close()

def deserialize(filename):
    pkl_file = open(filename, 'rb')
    clf = pickle.load(pkl_file)
    pkl_file.close()

    return clf
