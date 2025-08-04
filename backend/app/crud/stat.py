from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import engine
from app.models.stat import Stat


async def create_stat(stat_data: dict) -> Stat:
    """
    Create a new stat record.

    Args:
        stat_data (dict): Data for the new stat record.

    Returns:
        Stat: The created stat record.
    """
    stat = Stat(**stat_data)
    engine.add(stat)
    await engine.commit()
    await engine.refresh(stat)
    return stat


async def get_stat_by_id(stat_id: UUID) -> Stat:
    """
    Get a stat record by ID.

    Args:
        stat_id (UUID): The ID of the stat record.

    Returns:
        Stat: The stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id).options(selectinload(Stat.post))
    result = await engine.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    return stat


async def get_all_stats() -> list[Stat]:
    """
    Get all stat records.

    Returns:
        List[Stat]: A list of all stat records.
    """
    query = select(Stat).options(selectinload(Stat.post))
    result = await engine.execute(query)
    return result.scalars().all()


async def update_stat(stat_id: UUID, stat_data: dict) -> Stat:
    """
    Update a stat record.

    Args:
        stat_id (UUID): The ID of the stat record.
        stat_data (dict): Data to update the stat record.

    Returns:
        Stat: The updated stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id)
    result = await engine.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    for key, value in stat_data.items():
        setattr(stat, key, value)
    await engine.commit()
    await engine.refresh(stat)
    return stat


async def delete_stat(stat_id: UUID) -> None:
    """
    Delete a stat record.

    Args:
        stat_id (UUID): The ID of the stat record.

    Raises:
        HTTPException: If the stat record is not found.
    """
    query = select(Stat).where(Stat.id == stat_id)
    result = await engine.execute(query)
    stat = result.scalars().first()
    if not stat:
        raise HTTPException(status_code=404, detail="Stat not found")
    await engine.delete(stat)
    await engine.commit()
