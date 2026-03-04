from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TagInItemDTO(BaseModel):
    """Simplified Tag DTO for inclusion in Item responses"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str


class ItemDTO(BaseModel):
    """DTO for Item responses"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    tags: list[TagInItemDTO] = []
        due_date: datetime | None = None


class ItemCreateDTO(BaseModel):
    """DTO for creating items"""

    name: str
    description: str | None = None
    tag_ids: list[int] = []
        due_date: datetime | None = None


class ItemUpdateDTO(BaseModel):
    """DTO for updating items"""

    name: str | None = None
    description: str | None = None
    tag_ids: list[int] | None = None
        due_date: datetime | None = None

def __str__(self) -> str:
    """String representation of ItemDTO"""
    tags_str = "\n".join(f"  - {tag.name} ({tag.color})" for tag in self.tags)
    return (
        f"Item(id={self.id}, name={self.name}, "
        f"description={self.description}, created_at={self.created_at}, "
        f"updated_at={self.updated_at})\nTags:\n{tags_str}"
    )
