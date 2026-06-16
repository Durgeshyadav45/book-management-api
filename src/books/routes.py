from fastapi import APIRouter, HTTPException, Depends,status,UploadFile,File
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.schemas import BookCreateModel,BookResponseModel,BookUpdateModel
from src.books.service import BookService
from src.db.database import get_db
from src.auth.dependencies import admin_only


book_router = APIRouter()
book_service = BookService()


#--------- Routers--------

#--------Create Book ---------
@book_router.post("/",response_model=BookResponseModel, status_code=status.HTTP_201_CREATED)
async def create_book(book:BookCreateModel, db:AsyncSession = Depends(get_db)):
    return await book_service.create_book(book, db)

#-------Get All Book-----------
@book_router.get("/",response_model=list[BookResponseModel])
async def get_all_books(
    search: str |None = None,
    page: int = 1, 
    limit: int = 20, 
    db:AsyncSession = Depends(get_db)
):
    return await book_service.get_all_books(search, page, limit, db)



#------Get Single Book----------
@book_router.get("/{book_id}", response_model=BookResponseModel)
async def get_single_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_service.get_single_book(book_id, db)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



#----------Update Book----------
@book_router.put("/{book_id}",response_model=BookResponseModel)
async def update_book(book_id: int, data:BookUpdateModel, db:AsyncSession = Depends(get_db)):
    update_book = await book_service.update_book(book_id, data, db)
    
    if not update_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return update_book


#---------Delete Book----------
@book_router.delete("/{book_id}", dependencies=[Depends(admin_only)])
async def delete_book(
    book_id: int, 
    db:AsyncSession = Depends(get_db), 
):
    deleted_book = await book_service.delete_book(book_id, db)
    
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return{
        "message": "Book deleted"
    }



#------Upload Book File ----------
@book_router.post("/upload/{book_id}")
async def upload_book_filter(
    book_id: int,
    image: UploadFile = File(...),
    pdf: UploadFile =File(...)
):
    return await book_service.upload_book_files(book_id, image, pdf)
    
    


