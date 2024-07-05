from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Type

from database import SessionLocal
from sqlalchemy.inspection import inspect

from schemas.comment import CommentDB


templates = Jinja2Templates(directory="templates")

def get_related_models(model: Type, db: Session):
    related_models = {}
    for field_name, relation in inspect(model).relationships.items():
        related_model = relation.mapper.class_
        related_models[field_name] = db.query(related_model).all()
    return related_models


def get_model_fields(model):
    return [c.name for c in inspect(model).columns]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_router(model: Type, template_prefix: str, tag: str):
    router = APIRouter(prefix=f"/{tag}s", tags=[tag.capitalize() + "s"])


    @router.get("/", response_class=HTMLResponse)
    async def read_items(request: Request, db: Session = Depends(get_db)):
        items = db.query(model).all()
        return templates.TemplateResponse(f"{template_prefix}_list.html", {"request": request, "items": items})
    
    @router.get("/create", response_class=HTMLResponse)
    async def create_item(request: Request, db: Session = Depends(get_db)):
        # Получаем списки связанных моделей
        related_models = get_related_models(model, db)
        return templates.TemplateResponse(f"{template_prefix}_create.html",
                                        {"request": request,
                                        "item": None,
                                        **related_models})

    @router.post("/create", response_class=HTMLResponse)
    async def store_item(request: Request, db: Session = Depends(get_db)):
        form = await request.form()
        item_data = {key: form.get(key) for key in form.keys()}
        item = model(**item_data)
        due_date_str = form.get("due_date")
        if due_date_str:
            item.due_date = datetime.fromisoformat(due_date_str)
        db.add(item)
        db.commit()
        return templates.TemplateResponse(f"{template_prefix}_detail.html", {"request": request, "item": item})

    @router.get("/{item_id}", response_class=HTMLResponse)
    
    async def read_item(request: Request, item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag.capitalize()} not found")
        return templates.TemplateResponse(f"{template_prefix}_detail.html",
                                         {"request": request,
                                          "item": item})


    @router.get("/{item_id}/edit", response_class=HTMLResponse)
    async def edit_item(request: Request, item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag.capitalize()} not found")
        
        # Получаем списки связанных моделей
        related_models = get_related_models(model, db)
        return templates.TemplateResponse(f"{template_prefix}_edit.html",
                                           {"request": request,
                                            "item": item,
                                            **related_models
                                            })

    @router.post("/{item_id}/edit", response_class=HTMLResponse)
    async def update_item(request: Request, item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        
        form_data = await request.form()
        
        for field in get_model_fields(model):
            if field in form_data:
                setattr(item, field, form_data.get(field))       
        
        due_date_str = form_data.get("due_date")
        if due_date_str:
            item.due_date = datetime.fromisoformat(due_date_str)
        
        item.updated_at = datetime.now()
        
        db.add(item)
        db.commit()
        
        return templates.TemplateResponse(f"{template_prefix}_detail.html",
                                          {"request": request,
                                            "item": item})

    @router.get("/{item_id}/delete", response_class=HTMLResponse)
    async def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag.capitalize()} not found")
        db.delete(item)
        db.commit()
        return templates.TemplateResponse(f"{template_prefix}_list.html",
                                          {"request": request,
                                           "items": db.query(model).all()})
    

    @router.post("/{item_id}/comments/create", response_class=HTMLResponse)
    async def create_comment(request: Request, item_id: int, db: Session = Depends(get_db)):
        form_data = await request.form()
        author = form_data.get("author")
        text = form_data.get("text")
        item = db.query(model).filter(model.id == item_id).first()
        comment = CommentDB(task_id=item.id, author=author, text=text)
        db.add(comment)
        db.commit()
        return RedirectResponse(url=f"{request.url_for('read_item', item_id=item_id)}", status_code=302)
        
    @router.get("/{item_id}/comments/{comment_id}/delete", response_class=HTMLResponse)
    async def _delete_comment(request: Request, item_id: int, comment_id: int, db: Session = Depends(get_db)):
        comment = db.query(CommentDB).filter(CommentDB.id == comment_id).first()
        db.delete(comment)
        db.commit()
        return RedirectResponse(url=f"{request.url_for('read_item', item_id=item_id)}", status_code=302)
        
    return router
