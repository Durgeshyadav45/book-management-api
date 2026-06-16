from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.books.models import Book
from sqlalchemy import select, or_
from src.books.schemas import BookCreateModel, BookUpdateModel, BookResponseModel
import os
import json
from src.db.radis import redis_client

class BookService:
    
    #------Create Book------
    async def create_book(self,data:BookCreateModel, db:AsyncSession):
        new_book = Book(
            
            title = data.title,
            author = data.author,
            publisher = data.publisher,
            published_date = data.published_date,
            language = data.language,
            
            
        )
        
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        
        
    
    #------clear Cache---------
        redis_client.flushdb()
        
        return new_book
    
    
    #---------Get All Book----------
    async def get_all_books(self,search, page, limit, db:AsyncSession):
        
        cache_key = f"books{search}:{page}: {limit}"
        cache_books = redis_client.get(cache_key)
        
        #----- Cache Hit------
        if cache_books:
            return json.loads(cache_books)
        
        
        skip = (page-1) * limit
        statement = select(Book)
        if search:
            statement = statement.where(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                    Book.publisher.ilike(f"%{search}%")
                )
            )
        
        #------Pagination ----------
        statement = (
            statement.offset(skip).limit(limit)
        )
            
        result = await db.execute(statement)
        books = result.scalars().all()
        
        #------ Convert data---------
        books_data = []
        
        for book in books:
            books_data.append({
                "id": book.id,
                "title": book.title,
                "author":book.author,
                "publisher": book.publisher,
                "published_date":str(book.published_date),
                "language": book.language
            }) 
            
            #-------Store Cache----------
            redis_client.setex(cache_key, 60, json.dumps(books_data))
        
        return books
    
    
    #---------Get Single Book----------#
    async def get_single_book(self, book_id:int, db:AsyncSession):
        cache_key = f"book:{{book_id}}"
        cached_book = redis_client.get(cache_key)
        if cached_book:
            return json.load(cached_book)
        
        statement = select(Book).where(Book.id == book_id )
        result = await db.execute(statement)
        book = result.scalar_one_or_none()
        
        if not book:
            return None
        
        book_data = {
            "id": book.id,
            "title": book.title,
            "author":book.author,
            "publisher": book.publisher,
            "published_date":str(book.published_date),
            "language": book.language,
            
        }
        redis_client.setex(cache_key, 60, json.dumps(book_data))
        return book_data
    
    
    
    async def update_book(self,book_id: int, data: BookUpdateModel,db:AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        
        result = await db.execute(statement)
        book = result.scalar_one_or_none()
        
        if not book:
            return None
        
        book.title = data.title
        book.author = data.author
        book.publisher = data.publisher
        
        await db.commit()
        await db. refresh(book)
        
        return book
        
        
            

    
    async def upload_book_files(self, book_id, image, pdf):
        image_data = await image.read()
        pdf_data = await pdf.read()
        
        os.makedirs("uploads", exist_ok=True)
        
        image_path = f"uploads/{image.filename}"
        pdf_path = f"uploads/{pdf.filename}"
    
        #------ Save Image--------
        with open(image_path, "wb") as img_file:
          img_file.write(image_data)
        
        #--------Save PDF---------
        with open(pdf_path, "wb") as pdf_file:
          pdf_file.write(pdf_data)
        
        return{
            "message": "Files uploaded seccessfully",
            "book_id": book_id,
            "image_name": image.filename,
            "pdf_name": pdf.filename,
            "image_path": image_path,
            "pdf_path": pdf_path
        }
    
    
    
    
    
    
    

    
    
    
    
    async def get_single_book(self, book_id:int , db:AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()
    
    async def update_book(self, book_id: int, data:BookUpdateModel, db:AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await db.execute(statement)
        
        book = result.scalar_one_or_none()
        if book is None:
            return None
        
        book.title = data.title
        book.author = data.author
        book.publisher = data.publisher
        book.published_date = data.published_date
        book.language = data.language

        await db.commit()
        await db.refresh(book)
        return book
    
    
  
        
        
    async def delete_book(self, book_id: int, db:AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await db.execute(statement)
        
        book = result.scalar_one_or_none()
        
        if not book: 
            return None
        
        await db.delete(book)
        await db.commit()
        
        return{
            "Message": "Book deleted successfully"
        }
        
        




















# from sqlmodel.ext.asyncio.session import AsyncSession
# from src.books.schemas import BookCreateModel, BookUpdateModel
# from sqlmodel import select, desc
# from .models import Book
# from datetime import datetime


# class BookService:

#     async def get_all_books(self, session: AsyncSession):
#         statement = select(Book).order_by(desc(Book.created_at))
#         result = await session.exec(statement)
#         return result.all()   

#     async def get_book(self, book_uid: str, session: AsyncSession):
#         statement = select(Book).where(Book.uid == book_uid)
#         result = await session.exec(statement)
#         return result.first()

#     async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
#         new_book = Book(**book_data.model_dump())
#         new_book.published_date = datetime.strptime()
#         session.add(new_book)
#         await session.commit()
#         await session.refresh(new_book)  
#         return new_book

#     async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
#         book_to_update = await self.get_book(book_uid, session)  

#         if book_to_update:
#             update_data_dict = update_data.model_dump(exclude_unset=True)

#             for k, v in update_data_dict.items():
#                 setattr(book_to_update, k, v)

#             await session.commit()
#             await session.refresh(book_to_update)  
#             return book_to_update

#         return None

#     async def delete_book(self, book_uid: str, session: AsyncSession):
#         book_to_delete = await self.get_book(book_uid, session)  

#         if book_to_delete:
#             await session.delete(book_to_delete)
#             await session.commit()
#             return True

#         return False