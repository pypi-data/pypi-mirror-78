from marshmallow_annotations.ext.attrs import AttrsSchema
import attr
from typing import List


@attr.s(auto_attribs=True)
class Cv(object):
    cv_id: str = attr.ib()
    cv_desc: str = attr.ib()


class CvSchema(AttrsSchema):
    class Meta:
        target = Cv
        register_as_scheme = True


@attr.s(auto_attribs=True)
class TermedCv(Cv):
    terms: List[str] = attr.Factory(list)


class TermedCvSchema(AttrsSchema):
    class Meta:
        target = TermedCv
        register_as_scheme = True
