from os import getcwd, path
import aiofiles
from io import BytesIO
from minio import Minio
from minio.helpers import ObjectWriteResult
from pydantic import BaseModel, Field
from config.models import CommonResponse, ErrorResponse, settings
from config.parser import conf_parser
from app.decorator.src import logger
from minio import Minio


class MinioObjectInfo(BaseModel):
    bucket_name: str = Field(None, description="bucket名称")
    object_name: str = Field(None, description="对象名称")
    version_id: str = Field(None, description="版本id")
    etag: str = Field(None, description="etag")
    last_modified: str = Field(None, description="最后更新时间")
    location: str = Field(None, description="")
    content_type: str = Field(None, description="文件类型")
    date: str = Field(None, description="时间")


class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_CONFIG.endpoint,
            access_key=settings.MINIO_CONFIG.access_key,
            secret_key=settings.MINIO_CONFIG.secret_key,
        )
        self.default_bucket = settings.MINIO_BUCKET_TEMPLATE

    def create_bucket(self, bucket_name: str) -> bool:
        """

        Parameters
        ----------
        bucket_name : _type_
            _description_

        Returns
        -------
        successful_creation
            boolean indicating the function has completed execution
        """
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
        else:
            logger.error(f"Bucket {bucket_name} already exists")

        return True

    async def upload_file(self, bucket_name, file, local_file_dir, minio_dir=""):
        try:
            # 存储临时文件
            content = await file.read()
            local_file_dir = conf_parser()["BASIC"][local_file_dir]
            local_file_path = path.join(getcwd(), local_file_dir, file.filename)
            print(local_file_path, 'local_file_path')
            async with aiofiles.open(local_file_path, "wb") as out_file:
                await out_file.write(content)
                write_result = self.upload_from_localpath(
                    bucket_name, file.filename, local_file_path, minio_dir
                ).data
                # 删除临时文件
                await aiofiles.os.remove(local_file_path)
                return CommonResponse(
                    data=MinioObjectInfo(
                        bucket_name=write_result.bucket_name,
                        object_name=write_result.object_name,
                        version_id=write_result.version_id,
                        etag=write_result.etag,
                    ),
                    msg=f"上传成功[{write_result.object_name}]",
                )
        except Exception as e:
            logger.info(f"Minio error:{e}")
            return ErrorResponse(msg=f"上传失败[{e}]")

    def upload_from_localpath(
        self, bucket_name, minio_filename, local_file_path, minio_dir=""
    ):
        if minio_dir:
            minio_filename = minio_dir + "/" + minio_filename

        write_result: ObjectWriteResult = self.client.fput_object(
            bucket_name,
            minio_filename,
            local_file_path,
        )
        logger.info(
            f"{local_file_path} is successfully uploaded as "
            f"object {minio_filename} to bucket {bucket_name}"
        )
        return CommonResponse(data=write_result)

    def download_file(self, bucket_name: str, object_name: str):
        try:
            data = self.client.get_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
            file_stream = BytesIO(data.read())
            file_stream.seek(0)
            return file_stream
        except Exception as e:
            ErrorResponse(msg="下载失败")

    def stat_object(self, bucket_name, object_name):
        try:
            data = self.client.stat_object(bucket_name, object_name)
            return CommonResponse(data=data)
        except Exception as e:
            logger.info(f"Minio error: stat_object {e}")
            return ErrorResponse(msg=e)

    def get_search_file(self, bucket_name, keyword, start_date, end_date):
        try:
            objects = self.client.list_objects(
                bucket_name, prefix=keyword, recursive=True
            )
            sorted_objects = sorted(
                objects, key=lambda obj: obj.last_modified, reverse=True
            )
            # 时间搜索
            if start_date != None and end_date != None:
                sorted_objects = [
                    obj
                    for obj in sorted_objects
                    if start_date
                    <= obj.last_modified.strftime("%Y-%m-%d %H:%M:%S")
                    <= end_date
                ]
            templateArr = []
            for obj in sorted_objects:
                templateObj = {}
                templateObj['name'] = obj.object_name
                templateObj['date'] = obj.last_modified
                templateObj['etag'] = obj.etag
                templateArr.append(templateObj)
            return CommonResponse(data=templateArr, msg="成功获取数据")
        except Exception as err:
            ErrorResponse(msg="上传失败", data=err)

    def remove_file(self, bucket_name, object_name):
        try:
            self.client.remove_object(bucket_name, object_name)
            return CommonResponse(msg="删除数据成功")
        except Exception as err:
            ErrorResponse(msg="删除数据失败", data=err)
