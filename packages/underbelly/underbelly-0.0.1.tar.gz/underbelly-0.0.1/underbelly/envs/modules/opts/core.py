from toolz.itertoolz import getter
from underbelly.envs import *
from underbelly.envs.models import *
from underbelly.envs.modules import *
from underbelly.envs.utils import *
from underbelly.imports import *


class _Interopt(base_model):
    db: Optional[IDatabase] = None
    model: Optional[ISchema] = None
    conn: Optional[IConnection] = None

    class Config:
        arbitrary_types_allowed = True

    def is_none(self) -> bool:
        z = lambda x: x is None
        b = list(filter(z, list(self.__values__)))
        return b == 0


class Operators(abc.ABC, metaclass=VerificationType):
    """Operators

    This is where all of the operations happen prior to sending to the database.
    
    * Connecting to the database for the first time.
    * Extracting and preprocessing variables before sending to the database.
    * Linking items together when they're stored (relationships).
    
    Each operator is different.
    """
    optenv: Optional[_Interopt] = None

    def attach(self, db: IDatabase, schema: ISchema, conn: IConnection):
        self.optenv = _Interopt()
        self.optenv.db = db
        self.optenv.model = schema
        self.optenv.conn = conn
        self._verify_fields()

    def connect(self):
        if self.optenv.is_none():
            raise AttributeError("Not all fields we entered.")
        logger.success("All values are there calling the db.connect function!")
        self.optenv.db.initialize(self.optenv.conn)

    def reset(self):
        self.connect()

    def _verify_fields(self):
        if self.optenv is not None:
            self.reset()

    def step(self, *args, **kwargs):
        raise NotImplementedError


__all__ = ['Operators']

if __name__ == "__main__":

    wrapped = Operators()
    wrapped.attach(
        db=PlaceholderDB(),
        schema=MetricSchema(),
        conn=IConnection(),
    )
