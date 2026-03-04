"""Unit tests for item use cases"""

from unittest.mock import AsyncMock

import pytest

from app.items.application.use_cases.item_use_cases import (
    CreateItemUseCase,
    DeleteItemUseCase,
    GetAllItemsUseCase,
    GetItemUseCase,
    UpdateItemUseCase,
)
from tests.items.application.fixtures import (
    create_item_create_dto,
    create_item_entity,
    create_item_update_dto,
)


class TestGetItemUseCase:
    class TestCreateItemUseCase:
        """Test CreateItemUseCase"""

        @pytest.mark.asyncio
        async def test_create_item_with_due_date(self):
            mock_repo = AsyncMock()
            due_date = "2026-03-05T12:00:00"
            dto = create_item_create_dto(name="Test", due_date=due_date)
            entity = create_item_entity(id=1, name="Test", due_date=due_date)
            mock_repo.create.return_value = entity
            use_case = CreateItemUseCase(mock_repo)
            result = await use_case.execute(dto)
            assert result.due_date == due_date
            mock_repo.create.assert_called_once()

    class TestUpdateItemUseCase:
        """Test UpdateItemUseCase"""

        @pytest.mark.asyncio
        async def test_update_item_due_date(self):
            mock_repo = AsyncMock()
            due_date = "2026-03-10T12:00:00"
            entity = create_item_entity(id=1, name="Test", due_date=None)
            updated_entity = create_item_entity(id=1, name="Test", due_date=due_date)
            mock_repo.get_by_id.return_value = entity
            mock_repo.update.return_value = updated_entity
            use_case = UpdateItemUseCase(mock_repo)
            dto = create_item_update_dto(due_date=due_date)
            result = await use_case.execute(1, dto)
            assert result.due_date == due_date
            mock_repo.get_by_id.assert_called_once_with(1)
            mock_repo.update.assert_called_once()
    """Test GetItemUseCase"""

    @pytest.mark.asyncio
    async def test_execute_returns_item_when_found(self):
        """Test getting an item that exists"""
        # Arrange
        mock_repo = AsyncMock()
        item_entity = create_item_entity(id=1, name="Test Item")
        mock_repo.get_by_id.return_value = item_entity
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=1)

        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Item"
        mock_repo.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_execute_returns_none_when_not_found(self):
        """Test getting an item that doesn't exist"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        use_case = GetItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=999)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(999)


class TestGetAllItemsUseCase:
    """Test GetAllItemsUseCase"""

    @pytest.mark.asyncio
    async def test_execute_returns_all_items(self):
        """Test getting all items"""
        # Arrange
        mock_repo = AsyncMock()
        item_entities = [
            create_item_entity(id=1, name="Item 1"),
            create_item_entity(id=2, name="Item 2"),
        ]
        mock_repo.get_all.return_value = item_entities
        use_case = GetAllItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert len(result) == 2
        assert result[0].name == "Item 1"
        assert result[1].name == "Item 2"
        mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    @pytest.mark.asyncio
    async def test_execute_with_pagination(self):
        """Test getting all items with custom pagination"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.get_all.return_value = []
        use_case = GetAllItemsUseCase(mock_repo)

        # Act
        await use_case.execute(skip=10, limit=50)

        # Assert
        mock_repo.get_all.assert_called_once_with(skip=10, limit=50)

    @pytest.mark.asyncio
    async def test_execute_returns_empty_list_when_no_items(self):
        """Test getting all items when none exist"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.get_all.return_value = []
        use_case = GetAllItemsUseCase(mock_repo)

        # Act
        result = await use_case.execute()

        # Assert
        assert result == []
        mock_repo.get_all.assert_called_once()


class TestCreateItemUseCase:
    """Test CreateItemUseCase"""

    @pytest.mark.asyncio
    async def test_execute_creates_item(self):
        """Test creating an item"""
        # Arrange
        mock_repo = AsyncMock()
        dto = create_item_create_dto(name="New Item", description="New Description")
        created_entity = create_item_entity(id=1, name="New Item", description="New Description")
        mock_repo.create.return_value = created_entity
        use_case = CreateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(dto)

        # Assert
        assert result.id == 1
        assert result.name == "New Item"
        assert result.description == "New Description"
        mock_repo.create.assert_called_once()
        # Verify the Item entity passed to create has the correct properties
        call_args = mock_repo.create.call_args
        assert call_args[0][0].name == "New Item"
        assert call_args[0][0].description == "New Description"

    @pytest.mark.asyncio
    async def test_execute_creates_item_with_tags(self):
        """Test creating an item with tags"""
        # Arrange
        mock_repo = AsyncMock()
        dto = create_item_create_dto(name="Item with Tags", tag_ids=[1, 2])
        created_entity = create_item_entity(id=1, name="Item with Tags")
        mock_repo.create.return_value = created_entity
        use_case = CreateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(dto)

        # Assert
        assert result.id == 1
        mock_repo.create.assert_called_once()
        # Verify tag_ids were passed
        call_args = mock_repo.create.call_args
        assert call_args[1]["tag_ids"] == [1, 2]


class TestUpdateItemUseCase:
    """Test UpdateItemUseCase"""

    @pytest.mark.asyncio
    async def test_execute_updates_item(self):
        """Test updating an existing item"""
        # Arrange
        mock_repo = AsyncMock()
        current_item = create_item_entity(id=1, name="Old Name", description="Old Description")
        updated_item = create_item_entity(id=1, name="New Name", description="New Description")
        mock_repo.get_by_id.return_value = current_item
        mock_repo.update.return_value = updated_item
        dto = create_item_update_dto(name="New Name", description="New Description")
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=1, dto=dto)

        # Assert
        assert result is not None
        assert result.name == "New Name"
        assert result.description == "New Description"
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_partial_update(self):
        """Test updating only some fields of an item"""
        # Arrange
        mock_repo = AsyncMock()
        current_item = create_item_entity(id=1, name="Old Name", description="Old Description")
        updated_item = create_item_entity(id=1, name="New Name", description="Old Description")
        mock_repo.get_by_id.return_value = current_item
        mock_repo.update.return_value = updated_item
        dto = create_item_update_dto(name="New Name", description=None)
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=1, dto=dto)

        # Assert
        assert result is not None
        assert result.name == "New Name"
        # Description should remain unchanged since we passed None
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_returns_none_when_item_not_found(self):
        """Test updating a non-existent item"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        dto = create_item_update_dto()
        use_case = UpdateItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=999, dto=dto)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(999)
        mock_repo.update.assert_not_called()


class TestDeleteItemUseCase:
    """Test DeleteItemUseCase"""

    @pytest.mark.asyncio
    async def test_execute_deletes_item(self):
        """Test deleting an existing item"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.delete.return_value = True
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=1)

        # Assert
        assert result is True
        mock_repo.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_execute_returns_false_when_item_not_found(self):
        """Test deleting a non-existent item"""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.delete.return_value = False
        use_case = DeleteItemUseCase(mock_repo)

        # Act
        result = await use_case.execute(item_id=999)

        # Assert
        assert result is False
        mock_repo.delete.assert_called_once_with(999)
