from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas import ProductCreate, ProductPublic, ProductUpdate
from services.product_service import ProductService

router = APIRouter(prefix='/products', tags=['products'])


@router.post('', response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    try:
        product = await ProductService.create_product(
            session=session,
            title=data.title,
            description=data.description,
            price=data.price,
            quantity=data.quantity,
            seller_id=data.seller_id
        )

        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/{product_id}', response_model=ProductPublic)
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await ProductService.get_product_by_id(
        session=session,
        product_id=product_id
    )

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    return product


@router.get('/by-seller/{seller_id}', response_model=list[ProductPublic])
async def get_product_by_seller(seller_id: int, session: AsyncSession = Depends(get_session)):
    return await ProductService.get_product_by_seller(session=session, seller_id=seller_id)


@router.get('/by-title/{title}', response_model=list[ProductPublic])
async def get_product_by_title(title: str, session: AsyncSession = Depends(get_session)):
    return await ProductService.get_product_by_title(session=session, title=title)


@router.patch('/{product_id}', response_model=ProductPublic)
async def update_product(product_id: int, data: ProductUpdate, session: AsyncSession = Depends(get_session)):
    product = await ProductService.get_product_by_id(
        session=session,
        product_id=product_id
    )

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    return await ProductService.update_product(session=session, product=product, **data.model_dump(exclude_unset=True))


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await ProductService.get_product_by_id(
        product_id=product_id,
        session=session)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    await ProductService.delete_product(product=product, session=session)
