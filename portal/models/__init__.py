from .students import Student
from .faculty import Faculty
from .course import Course
from .major import Major
from .academic_years import AcademicYear
from .project_types import ProjectType
from .lecturer import Lecturer
from .lecturer_language import LecturerLanguage
from .lecturer_specialty import LecturerSpecialty
from .research_field import ResearchField
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
    "Major",
    "ResearchField",
    "LecturerLanguage",
    "LecturerSpecialty",
]
