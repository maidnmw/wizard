import logging
import os
import traceback
import pickle
import pandas as pd
from datetime import datetime

from sklearn.preprocessing import OneHotEncoder
from sklearn.naive_bayes import GaussianNB
from typing import List
from django.conf import settings

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)
f_handler = logging.FileHandler(filename='logs/error-logs.log')
f_handler.setLevel(logging.ERROR)
log.addHandler(s_handler)
log.addHandler(f_handler)


class DetectionDetectorMeta(type):
    _instances = {}

    def __init__(self, name, bases, mmbs):
        super(DetectionDetectorMeta, self).__init__(name, bases, mmbs)
        self._instance = super(DetectionDetectorMeta, self).__call__()

    def __call__(self, *args, **kw):
        return self._instance


class DetectionDetector(metaclass=DetectionDetectorMeta):
    """Singleton to detect class"""

    def __init__(self):
        log.info('Initializing Detection Detector')
        self.model_dir = settings.DIR_WITH_MODELS
        log.info('Unpickling OHE')
        with open(os.path.join(self.model_dir, 'ohe_subs.pickle'), 'rb') as f:
            self.ohe: OneHotEncoder = pickle.load(f)
        log.info('Unpickling Naive')
        with open(os.path.join(self.model_dir, 'naive.pickle'), 'rb') as f:
            self.naive: GaussianNB = pickle.load(f)
        self.ohe_df = pd.DataFrame([[0 for i in self.ohe.categories]],
                                   columns=self.ohe.categories)
        self.allowed_groups = set(self.ohe_df.columns)
        log.info('Detection detector initialization is done')
        

    def predict(self, groups: List[str]):
        log.info('predict called for groups: %s', groups)
        log.info('groups count: %s', len(groups))
        df = self.ohe_df.copy()
        counter = 0
        for g in groups:
            if g in self.allowed_groups:
                df[g] = 1
                counter += 1
        log.info('groups in common with allowed: %s', counter)
        try:
            prediction = self.naive.predict([df.loc[0]])
            log.info('prediction is %s', prediction)
            return prediction[0]
        except:            
            log.error(f'PREDICTION ERROR\nTIME: {datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")}\nTRACEBACK: {traceback.format_exc()}', )
            return ('Something went wrong in prediction process')
