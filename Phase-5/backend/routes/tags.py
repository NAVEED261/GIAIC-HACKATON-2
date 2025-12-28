"""
Tag Routes - Phase-5
API endpoints for tag management

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session

from models.tag import Tag, TagCreate, TagRead, TagUpdate
from services.tag_service import TagService
from db import get_session
from middleware.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["Tags"])


def get_tag_service(session: Session = Depends(get_session)) -> TagService:
    return TagService(session)


@router.post("/", response_model=TagRead, status_code=201)
async def create_tag(
    tag_data: TagCreate,
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Create a new tag"""
    tag = await service.create_tag(current_user.id, tag_data)
    return tag


@router.get("/", response_model=List[dict])
async def get_tags(
    include_counts: bool = Query(True, description="Include task counts"),
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Get all tags for the user"""
    if include_counts:
        return service.get_tags_with_counts(current_user.id)
    else:
        tags = service.get_tags(current_user.id)
        return [{"id": t.id, "name": t.name, "color": t.color, "description": t.description} for t in tags]


@router.get("/popular", response_model=List[dict])
async def get_popular_tags(
    limit: int = Query(10, ge=1, le=50),
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Get most used tags"""
    return service.get_popular_tags(current_user.id, limit)


@router.get("/search", response_model=List[TagRead])
async def search_tags(
    query: str = Query(..., min_length=1),
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Search tags by name"""
    return service.search_tags(current_user.id, query)


@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(
    tag_id: int,
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Get a single tag"""
    tag = service.get_tag(tag_id, current_user.id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Update a tag"""
    tag = await service.update_tag(tag_id, current_user.id, tag_data)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Delete a tag"""
    success = await service.delete_tag(tag_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")


@router.post("/merge", response_model=dict)
async def merge_tags(
    source_tag_id: int,
    target_tag_id: int,
    current_user = Depends(get_current_user),
    service: TagService = Depends(get_tag_service)
):
    """Merge source tag into target tag"""
    success = await service.merge_tags(current_user.id, source_tag_id, target_tag_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to merge tags")
    return {"merged": True, "source_tag_id": source_tag_id, "target_tag_id": target_tag_id}
