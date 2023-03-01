from typing import Any, Optional
from pydantic import BaseModel, BaseSettings
from pydantic.fields import Field


class CommonResponse(BaseModel):
    code: int = Field(default=200, description="状态码： 200 正常 其它 异常")
    msg: str = Field(default="操作成功", description="消息")
    data: Optional[Any] = Field(default="", description="数据包")


class ErrorResponse(BaseModel):
    code: int = Field(default=-1, description="状态码： 200 正常 其它 异常")
    msg: str = Field(default="操作失败", description="消息")
    data: Optional[Any] = Field(default="", description="数据包")


class MinioStruct(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str


class Settings(BaseSettings):
    # Minio Settings
    class Config:
        env_file = ".env"

    MINIO_CONFIG: MinioStruct
    MINIO_BUCKET_TEMPLATE: str


settings = Settings()
