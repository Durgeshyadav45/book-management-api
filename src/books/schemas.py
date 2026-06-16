from pydantic import BaseModel
from datetime import date



class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date : date
    language : str
    
    
    
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date : date
    language : str
    
class BookResponseModel(BaseModel):
    id : int
    title: str
    author: str
    publisher: str
    published_date : date
    language : str
    
    
    class Config:
        from_attributes = True
    

    
    

# from pydantic import BaseModel
# from datetime import date
# from typing import Optional

# class BookCreateModel(BaseModel):
#     title: str
#     author: str
#     publisher: str
#     published_date: date
#     page_count: int
#     language: str

# class BookUpdateModel(BaseModel):
#     title: Optional[str] = None
#     author: Optional[str] = None
#     publisher: Optional[str] = None
#     page_count: Optional[int] = None
#     language: Optional[str] = None