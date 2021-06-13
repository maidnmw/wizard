import logging
import os
import traceback
import pickle
from datetime import datetime

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict
from django.conf import settings

from backend.app.direction_map import direction_dict, direction_list

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
        log.info('Unpickling Transformer')
        with open(os.path.join(self.model_dir, 'mlb.pickle'), 'rb') as f:
            self.transformer: MultiLabelBinarizer = pickle.load(f)
        log.info('Unpickling Model')
        with open(os.path.join(self.model_dir, 'model.pickle'), 'rb') as f:
            self.model: RandomForestClassifier = pickle.load(f)
        log.info('Detection detector initialization is done')

    def predict(self, groups: List[str]) -> Dict[str, str]:
        log.info('predict called for groups: %s', groups)
        log.info('groups count: %s', len(groups))
        try:
            transformed_group = self.transformer.transform([groups])
            prediction = list(self.model.predict_proba(transformed_group)[0])
            log.info('prediction is %s', prediction)
            prediction_codes = {direction_dict[direction_list[prediction_index]]: prediction[prediction_index]
                                for prediction_index in range(len(prediction))}

            prediction_result = {k: str(round(v * 100, 1)) + '%'
                                 for k, v in sorted(prediction_codes.items(), key=lambda item: item[1], reverse=True)}
            return prediction_result

        except:            
            log.error(f'PREDICTION ERROR\nTIME: {datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")}\nTRACEBACK: {traceback.format_exc()}', )
            return ('Something went wrong in prediction process')
