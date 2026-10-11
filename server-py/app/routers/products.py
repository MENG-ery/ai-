"""家电产品接口：列表 / 详情（效果图 + 细节图 + 参数）"""
from fastapi import APIRouter, HTTPException

from app.data.products import PRODUCTS, get_product

router = APIRouter()


@router.get("/products")
def list_products():
    return {"products": PRODUCTS}


@router.get("/products/{product_id}")
def product_detail(product_id: str):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
