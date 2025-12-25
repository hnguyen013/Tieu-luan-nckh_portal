from .students import Student
from .faculty import Faculty
from .course import Course
from .academic_years import AcademicYear
from .project_types import ProjectType
from .lecturer import Lecturer
from .projects import (
    Project,
    ProjectStudent,
    ProjectLecturer,
    ProjectAttachment,
    ProjectStatusLog,
)

__all__ = [
    "Student",
    "Faculty",
    "Course",
    "AcademicYear",
    "ProjectType",
    "Project",
    "ProjectStudent",
    "ProjectLecturer",
    "ProjectAttachment",
    "ProjectStatusLog",
    "Lecturer",
]
