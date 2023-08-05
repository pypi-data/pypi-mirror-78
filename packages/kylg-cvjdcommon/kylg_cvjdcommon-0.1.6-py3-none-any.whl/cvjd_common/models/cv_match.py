from cvjd_common.models.cv import TermedCv
import attr
from typing import List
from marshmallow_annotations.ext.attrs import AttrsSchema
from cvjd_common.models.cv_jd_gap import CvJdGap


@attr.s(auto_attribs=True)
class CvMatch:
    cv: TermedCv = attr.ib()
    gapList: List[CvJdGap] = attr.Factory(list)


class CvMatchSchema(AttrsSchema):
    class Meta:
        target = CvMatch
        register_as_scheme = True
