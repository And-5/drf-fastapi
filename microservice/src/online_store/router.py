from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from online_store.models import Product
from online_store.schemas import ProductCreate, ProductUpdate, ProductModel

router = APIRouter(
    prefix="/store",
    tags=["Store"]
)


@router.get("/", response_model=List[ProductModel])
async def get_all_product(session: AsyncSession = Depends(get_async_session)):
    query = select(Product).order_by(Product.id)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.get("/{product_id}", response_model=ProductModel)
async def get_specific_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    products = result.scalar_one_or_none()
    return products


@router.post("/")
async def add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{product_id}")
async def delete_specific_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Product).where(Product.id == product_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/")
async def delete_all_product(session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Product)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch("/{product_id}")
async def update_specific_product(product_id: int, product_data: ProductUpdate,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = select(Product).filter(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar()
    if product is None:
        return {"message": "Product not found"}
    if not product:
        return {"message": "Product not found"}
    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    await session.commit()
    return {"message": "Product was updated"}
