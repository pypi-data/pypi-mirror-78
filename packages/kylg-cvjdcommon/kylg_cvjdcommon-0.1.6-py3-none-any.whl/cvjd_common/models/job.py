import attr
from marshmallow_annotations.ext.attrs import AttrsSchema
from cvjd_common.models.cv_match import CvMatch


@attr.s(auto_attribs=True)
class Job:
    status: str = attr.ib()
    cvMatch: CvMatch = attr.ib()


class JobSchema(AttrsSchema):
    class Meta:
        target = Job
        register_as_scheme = True
