from underbelly.imports import *
from underbelly.envs.models import *
from .core import Operators


class MetricOperator(Operators):

    def dispatch(self, payload: IPayload):
        self.optenv.db.save(payload)