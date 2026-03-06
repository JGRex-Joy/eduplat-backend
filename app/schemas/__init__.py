from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserAboutCreate, UserAboutUpdate, UserAboutResponse, UserProfileResponse
from app.schemas.academic import AcademicInfoCreate, AcademicInfoUpdate, AcademicInfoResponse
from app.schemas.extracurricular import ExtracurricularCreate, ExtracurricularResponse

__all__ = [
    "RegisterRequest", "LoginRequest", "TokenResponse",
    "UserAboutCreate", "UserAboutUpdate", "UserAboutResponse", "UserProfileResponse",
    "AcademicInfoCreate", "AcademicInfoUpdate", "AcademicInfoResponse",
    "ExtracurricularCreate", "ExtracurricularResponse",
]