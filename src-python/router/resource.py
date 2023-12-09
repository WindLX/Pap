from time import time
from os import remove, path, walk
from shutil import make_archive
from asyncio import to_thread

from schemas.resource import ResourceSchema
from service.logger import logger
from service.config import path_config

from fastapi import status, APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter(prefix="/resource")


@router.post("/upload_resource", response_model=ResourceSchema, status_code=status.HTTP_202_ACCEPTED, include_in_schema=True)
async def upload_resource(file: UploadFile) -> ResourceSchema:
    """upload resource

    Returns:
        ResourceSchema: resource

    Raises:
        HTTPException: error response 400
    """
    logger.info(f"POST /resource/upload_resource")
    try:
        file_name = file.filename
        assert file_name is not None
        file_path = path.join(path_config.res_dir, file_name)
        if path.exists(file_path):
            file_name = file_name.split(
                ".")[0] + "_" + str(int(time())) + "." + file_name.split(".")[1]
            file_path = path.join(path_config.res_dir, file_name)
        data = await file.read()
        with open(file_path, "wb") as f:
            f.write(data)
        return ResourceSchema(name=file_name, url=file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get_resources", response_model=list[ResourceSchema], status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_resources() -> list[ResourceSchema]:
    """get all resources

    Returns:
        list[ResourceSchema]: resources
    """
    logger.debug(f"GET /resource/get_resources")
    all_resources = []
    for files in walk(path_config.res_dir):
        for file in files[2]:
            url = path.join(path_config.res_dir, file)
            all_resources.append(ResourceSchema(name=file, url=url))
    return all_resources


@router.delete("/delete_resource", status_code=status.HTTP_200_OK, include_in_schema=True)
async def delete_resource(url: str):
    """delete resource

    Args:
        url (str): resource url

    Raises:
        HTTPException: error response 404
    """
    logger.info(f"POST /resource/delete_resource?url={url}")
    if path.exists(url):
        remove(url)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@router.get("/export_data", status_code=status.HTTP_200_OK, include_in_schema=True)
async def export_data() -> FileResponse:
    """export data

    Returns:
        FileResponse: archive data
    """
    logger.info(f"GET /resource/export_data")
    try:
        zip_file_path = "./data"
        await to_thread(make_archive, zip_file_path, 'zip', base_dir=zip_file_path)
        return FileResponse(zip_file_path + '.zip')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/remove_zip", status_code=status.HTTP_200_OK, include_in_schema=True)
async def remove_zip():
    """remove zip
    """
    logger.debug(f"DELETE /resource/remove_zip")
    zip_path = "./data.zip"
    if path.exists(zip_path):
        remove(zip_path)


@router.get("/get_stream", status_code=status.HTTP_200_OK, include_in_schema=True)
async def get_stream(url: str):
    if not path.exists(url):
        raise HTTPException(status_code=404, detail="Video file not found")

    return StreamingResponse(open(url, "rb"))
