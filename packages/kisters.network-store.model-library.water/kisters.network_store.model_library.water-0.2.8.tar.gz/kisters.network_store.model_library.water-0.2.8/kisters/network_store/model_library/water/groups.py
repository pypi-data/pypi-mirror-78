from kisters.network_store.model_library.base import BaseGroup as _BaseGroup
from pydantic import Field


class _Group(_BaseGroup):
    domain: str = Field("water", const=True)


class HydroPowerPlant(_Group):
    element_class: str = Field("HydroPowerPlant", const=True)


class PumpingStation(_Group):
    element_class: str = Field("PumpingStation", const=True)


class SluiceComplex(_Group):
    element_class: str = Field("SluiceComplex", const=True)


class WeirComplex(_Group):
    element_class: str = Field("WeirComplex", const=True)
