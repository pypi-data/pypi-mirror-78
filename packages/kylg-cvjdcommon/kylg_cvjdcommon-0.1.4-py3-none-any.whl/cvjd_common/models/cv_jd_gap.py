from typing import List

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema

from cvjd_common.models.cv import TermedCv
from cvjd_common.models.jd import TermedJd


@attr.s(auto_attribs=True)
class CvJd:
    cv: TermedCv = attr.ib()
    jd: TermedJd = attr.ib()


class CvJdSchema(AttrsSchema):
    class Meta:
        target = CvJd
        register_as_scheme = True


@attr.s(auto_attribs=True)
class CvJdGap:
    jd: TermedJd = attr.ib()
    cvHtml: str = attr.ib()
    jdHtml: str = attr.ib()
    gapTerms: List[str] = attr.Factory(list)


class CvJdGapSchema(AttrsSchema):
    class Meta:
        target = CvJdGap
        register_as_scheme = True


@attr.s(auto_attribs=True)
class CvJdGapResult:
    termedCv: TermedCv = attr.ib()
    docGap: CvJdGap = attr.ib()


class CvJdGapResultSchema(AttrsSchema):
    class Meta:
        target = CvJdGapResult
        register_as_scheme = True
