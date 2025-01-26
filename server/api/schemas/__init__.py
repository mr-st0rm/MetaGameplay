from pydantic import BaseModel, ConfigDict


class BaseOrmModel(BaseModel):
    """
    Base model that includes from_attributes flag.
    """

    model_config = ConfigDict(from_attributes=True)
