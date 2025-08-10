from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME_GARDEN = "home_garden"
    BEAUTY = "beauty"
    SPORTS = "sports"
    TOYS = "toys"
    BOOKS = "books"
    OTHER = "other"

class ProductStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class Product(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: ProductCategory
    price: float = Field(..., gt=0)
    retail_price: float = Field(..., gt=0)
    cost_price: Optional[float] = None
    sku: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    status: ProductStatus = ProductStatus.DRAFT
    supplier_id: Optional[str] = None
    supplier_name: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('price', 'retail_price')
    def validate_prices(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

    @validator('retail_price')
    def validate_retail_price(cls, v, values):
        if 'price' in values and v < values['price']:
            raise ValueError('Retail price cannot be less than selling price')
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: ProductCategory
    price: float
    retail_price: float
    images: List[str]
    status: ProductStatus
    rating: Optional[float]
    review_count: Optional[int]
    tags: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: ProductCategory
    price: float = Field(..., gt=0)
    retail_price: float = Field(..., gt=0)
    tags: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    supplier_id: Optional[str] = None
    supplier_name: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[float] = Field(None, gt=0)
    retail_price: Optional[float] = Field(None, gt=0)
    tags: Optional[List[str]] = None
    images: Optional[List[str]] = None
    status: Optional[ProductStatus] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)

class ProductSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[ProductCategory] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    status: Optional[ProductStatus] = None
    tags: Optional[List[str]] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0) 