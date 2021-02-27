import logging
import os
import pickle
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.naive_bayes import GaussianNB
from typing import List
from django.conf import settings

log = logging.getLogger(__name__)


class DetectionDetector:
    """Singleton to detect class"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DetectionDetector, cls).__new__(cls)
        return cls.instance

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
        log.info(self.allowed_groups)

    def predict(self, groups: List[str]):
        log.info('predict called for groups: %s', groups)
        df = self.ohe_df.copy()
        counter = 0
        for g in groups:
            if g in self.allowed_groups:
                df[g] = 1
                counter += 1
        log.info('groups in common with allowed: %s', counter)
        prediction = self.naive.predict([df.loc[0]])
        log.info('prediction is %s', prediction)
        return prediction[0]
