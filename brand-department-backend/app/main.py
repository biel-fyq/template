from app.microservices.minio_service import MinioService
from config.models import settings
from fastapi import File, Response, UploadFile
from fastapi import FastAPI
from config.parser import create_dir
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
create_dir()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3030",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost",
    "https://datalab.bielcrystal.com",
    "https://datalab-internal.bielcrystal.com",
    "https://biel-partner-miniapp.oss-cn-shenzhen.aliyuncs.com",
    "https://zhipin.bielcrystal.com",
    "https://192.168.88.10",
]
app.add_middleware(
    CORSMiddleware,
    # allow_origins cannot be ["*"] for withCredentials
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/template", summary="上传模板")
async def upload_tempalte(
    file: UploadFile = File(...),
):
    minio_client = MinioService()
    return await minio_client.upload_file(
        settings.MINIO_BUCKET_TEMPLATE,
        file,
        "template_dir",
    )


@app.get("/template", summary="获取模板信息")
def upload_tempalte(
    keyword: Optional[str] = "",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    minio_client = MinioService()
    res = minio_client.get_search_file(
        settings.MINIO_BUCKET_TEMPLATE, keyword, start_date, end_date
    )
    return res


@app.delete("/template", summary="删除模板数据")
def upload_tempalte(
    object_name: Optional[str] = None,
):
    minio_client = MinioService()
    res = minio_client.remove_file(settings.MINIO_BUCKET_TEMPLATE, object_name)
    return res


@app.get("/download", summary="下载模板信息")
def upload_tempalte(
    object_name: Optional[str] = None,
):
    minio_client = MinioService()
    bytes_io = minio_client.download_file(settings.MINIO_BUCKET_TEMPLATE, object_name)
    response = Response(content=bytes_io.getvalue())
    response.headers["Content-Type"] = "application/octet-stream"
    filename = object_name.encode('utf-8')
    response.headers["Content-Disposition"] = f'attachment; filename= {filename}'
    return response
