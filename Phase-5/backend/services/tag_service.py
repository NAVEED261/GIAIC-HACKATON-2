"""
Tag Service - Phase-5
Handles tag management for task categorization

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, func
from models.tag import Tag, TagCreate, TagUpdate, TaskTag


class TagService:
    """
    Service for managing tags

    Features:
    - CRUD operations
    - Tag usage statistics
    - Bulk operations
    """

    def __init__(self, session: Session):
        self.session = session

    async def create_tag(self, user_id: int, tag_data: TagCreate) -> Tag:
        """Create a new tag"""
        tag = Tag(
            user_id=user_id,
            name=tag_data.name,
            color=tag_data.color,
            description=tag_data.description
        )

        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

        return tag

    async def update_tag(
        self,
        tag_id: int,
        user_id: int,
        tag_data: TagUpdate
    ) -> Optional[Tag]:
        """Update a tag"""
        tag = self.session.get(Tag, tag_id)

        if not tag or tag.user_id != user_id:
            return None

        update_data = tag_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tag, key, value)

        self.session.commit()
        self.session.refresh(tag)

        return tag

    async def delete_tag(self, tag_id: int, user_id: int) -> bool:
        """Delete a tag"""
        tag = self.session.get(Tag, tag_id)

        if not tag or tag.user_id != user_id:
            return False

        # Delete all task-tag associations first
        task_tags = self.session.exec(
            select(TaskTag).where(TaskTag.tag_id == tag_id)
        ).all()

        for tt in task_tags:
            self.session.delete(tt)

        self.session.delete(tag)
        self.session.commit()

        return True

    def get_tag(self, tag_id: int, user_id: int) -> Optional[Tag]:
        """Get a single tag"""
        tag = self.session.get(Tag, tag_id)

        if not tag or tag.user_id != user_id:
            return None

        return tag

    def get_tags(self, user_id: int) -> List[Tag]:
        """Get all tags for a user"""
        statement = select(Tag).where(
            Tag.user_id == user_id
        ).order_by(Tag.name)

        return self.session.exec(statement).all()

    def get_tags_with_counts(self, user_id: int) -> List[dict]:
        """Get all tags with task counts"""
        tags = self.get_tags(user_id)
        result = []

        for tag in tags:
            count = self.session.exec(
                select(func.count(TaskTag.task_id)).where(
                    TaskTag.tag_id == tag.id
                )
            ).one()

            result.append({
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "description": tag.description,
                "task_count": count
            })

        return result

    def search_tags(self, user_id: int, query: str) -> List[Tag]:
        """Search tags by name"""
        statement = select(Tag).where(
            Tag.user_id == user_id,
            Tag.name.ilike(f"%{query}%")
        ).order_by(Tag.name)

        return self.session.exec(statement).all()

    async def merge_tags(
        self,
        user_id: int,
        source_tag_id: int,
        target_tag_id: int
    ) -> bool:
        """
        Merge source tag into target tag

        All tasks with source_tag will be reassigned to target_tag
        """
        source_tag = self.session.get(Tag, source_tag_id)
        target_tag = self.session.get(Tag, target_tag_id)

        if not source_tag or source_tag.user_id != user_id:
            return False
        if not target_tag or target_tag.user_id != user_id:
            return False

        # Get all task-tag associations for source
        task_tags = self.session.exec(
            select(TaskTag).where(TaskTag.tag_id == source_tag_id)
        ).all()

        for tt in task_tags:
            # Check if task already has target tag
            existing = self.session.exec(
                select(TaskTag).where(
                    TaskTag.task_id == tt.task_id,
                    TaskTag.tag_id == target_tag_id
                )
            ).first()

            if not existing:
                # Create new association with target
                new_tt = TaskTag(task_id=tt.task_id, tag_id=target_tag_id)
                self.session.add(new_tt)

            # Delete old association
            self.session.delete(tt)

        # Delete source tag
        self.session.delete(source_tag)
        self.session.commit()

        return True

    def get_popular_tags(self, user_id: int, limit: int = 10) -> List[dict]:
        """Get most used tags"""
        tags_with_counts = self.get_tags_with_counts(user_id)
        sorted_tags = sorted(tags_with_counts, key=lambda x: x["task_count"], reverse=True)
        return sorted_tags[:limit]
