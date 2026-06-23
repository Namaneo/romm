from fastapi import HTTPException, Request

from decorators.auth import protected_route
from handler.auth.constants import Scope
from handler.filesystem import fs_platform_handler
from handler.filesystem.assets_handler import build_asset_file_response
from utils.router import APIRouter

router = APIRouter(
    prefix="/raw",
    tags=["raw"],
)


@protected_route(router.head, "/library/{path:path}", [Scope.ASSETS_READ])
def head_raw_library(request: Request, path: str):
    try:
        resolved_path = fs_platform_handler.validate_path(path)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Library file not found") from exc

    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="Library file not found")

    return build_asset_file_response(resolved_path)


@protected_route(router.get, "/library/{path:path}", [Scope.ASSETS_READ])
def get_raw_library(request: Request, path: str):
    try:
        resolved_path = fs_platform_handler.validate_path(path)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Library file not found") from exc

    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="Library file not found")

    return build_asset_file_response(resolved_path)
