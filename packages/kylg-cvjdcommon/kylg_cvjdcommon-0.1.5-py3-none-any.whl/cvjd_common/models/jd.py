from typing import List

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True)
class Jd:
    jd_id: str = attr.ib()
    jd_type: str = attr.ib()
    jd_desc: str = attr.ib()


class JdSchema(AttrsSchema):
    class Meta:
        target = Jd
        register_as_scheme = True


@attr.s(auto_attribs=True)
class TermedJd(Jd):
    terms: List[str] = attr.Factory(list)


class TermedJdSchema(AttrsSchema):
    class Meta:
        target = TermedJd
        register_as_scheme = True


@attr.s(auto_attribs=True)
class PredictResult:
    total_results: int = attr.ib()
    results: List[Jd] = attr.Factory(list)


class PredictResultSchema(AttrsSchema):
    class Meta:
        target = PredictResult
        register_as_scheme = True
