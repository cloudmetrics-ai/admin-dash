# CRUD Operations Guide

This guide shows you how to add new entities with full CRUD (Create, Read, Update, Delete) operations to your application.

---

## Overview

Adding a new entity involves 4 main steps:

1. **Backend Model** - Database table definition
2. **Backend API** - REST endpoints
3. **Frontend Pages** - UI for CRUD operations
4. **Database Migration** - Apply schema changes

---

## Example: Product CRUD

Let's build a complete Product management system.

### Step 1: Create Backend Model

**File**: `backend/app/models/product.py`

```python
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    sku = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Register in** `backend/app/models/__init__.py`:
```python
from app.models.product import Product
```

### Step 2: Create Pydantic Schemas

**File**: `backend/app/schemas/product.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    sku: str = Field(..., min_length=1, max_length=100)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
```

### Step 3: Create API Endpoints

**File**: `backend/app/api/v1/products.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all products with pagination"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if SKU already exists
    existing = db.query(Product).filter(Product.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only provided fields
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return None
```

**Register in** `backend/app/api/v1/__init__.py`:
```python
from app.api.v1 import products

# In create_api_router():
api_router.include_router(products.router)
```

### Step 4: Create Database Migration

```bash
cd backend
alembic revision --autogenerate -m "Add products table"
alembic upgrade head
```

### Step 5: Create Frontend API Client

**File**: `frontend/src/lib/api/products.ts`

```typescript
import api from '../api';

export interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  stock: number;
  sku: string;
  created_at: string;
  updated_at?: string;
}

export interface ProductCreate {
  name: string;
  description?: string;
  price: number;
  stock: number;
  sku: string;
}

export const productsApi = {
  list: async (skip = 0, limit = 100) => {
    const response = await api.get<Product[]>(`/api/v1/products?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  get: async (id: number) => {
    const response = await api.get<Product>(`/api/v1/products/${id}`);
    return response.data;
  },

  create: async (data: ProductCreate) => {
    const response = await api.post<Product>('/api/v1/products', data);
    return response.data;
  },

  update: async (id: number, data: Partial<ProductCreate>) => {
    const response = await api.put<Product>(`/api/v1/products/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/products/${id}`);
  },
};
```

### Step 6: Create Frontend Pages

**File**: `frontend/src/app/products/page.tsx` (List Page)

```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { productsApi, Product } from '@/lib/api/products';

export default function ProductsPage() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await productsApi.list();
      setProducts(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this product?')) return;
    
    try {
      await productsApi.delete(id);
      setProducts(products.filter(p => p.id !== id));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete product');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <h1>Products</h1>
        <Link href="/products/create">
          <button>Create Product</button>
        </Link>
      </div>

      {error && <div style={{ color: 'red' }}>{error}</div>}

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            <tr key={product.id}>
              <td>{product.sku}</td>
              <td>{product.name}</td>
              <td>${product.price.toFixed(2)}</td>
              <td>{product.stock}</td>
              <td>
                <Link href={`/products/${product.id}/edit`}>Edit</Link>
                {' | '}
                <button onClick={() => handleDelete(product.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**File**: `frontend/src/app/products/create/page.tsx` (Create Page)

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { productsApi } from '@/lib/api/products';

export default function CreateProductPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: 0,
    stock: 0,
    sku: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await productsApi.create(formData);
      router.push('/products');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create product');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px' }}>
      <h1>Create Product</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Name *</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>SKU *</label>
          <input
            type="text"
            value={formData.sku}
            onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
            required
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Price *</label>
          <input
            type="number"
            step="0.01"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) })}
            required
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Stock</label>
          <input
            type="number"
            value={formData.stock}
            onChange={(e) => setFormData({ ...formData, stock: parseInt(e.target.value) })}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={4}
          />
        </div>

        {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Product'}
        </button>
      </form>
    </div>
  );
}
```

---

## Quick Reference

### Backend Checklist
- [ ] Create model in `backend/app/models/`
- [ ] Create schemas in `backend/app/schemas/`
- [ ] Create API router in `backend/app/api/v1/`
- [ ] Register router in `backend/app/api/v1/__init__.py`
- [ ] Create and run migration

### Frontend Checklist
- [ ] Create API client in `frontend/src/lib/api/`
- [ ] Create list page in `frontend/src/app/[entity]/page.tsx`
- [ ] Create create page in `frontend/src/app/[entity]/create/page.tsx`
- [ ] Create edit page in `frontend/src/app/[entity]/[id]/edit/page.tsx`

---

## Best Practices

1. **Validation**: Always validate on both frontend and backend
2. **Error Handling**: Provide clear error messages
3. **Loading States**: Show loading indicators
4. **Confirmation**: Ask before deleting
5. **Pagination**: Implement for large datasets
6. **Search/Filter**: Add for better UX
7. **Permissions**: Check user permissions before operations

---

## Next Steps

- Add search and filtering
- Implement sorting
- Add bulk operations
- Create export functionality
- Add image uploads
- Implement soft deletes
