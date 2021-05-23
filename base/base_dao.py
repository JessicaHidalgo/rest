from sqlachemy.orm import query 
from sqlalchemy.orm.exc import MultipleResultsFound

class BaseDao: 
    _model = None

    def __init__(self,model=None):
        from user_service.models import db
        self.session = db.session
        self._model = model 

    def change_model(self, model):
        self._model = model 
    
    @property
    def model(self):
        return self._model

    @property
    def queryset(self): 
        return self._model.query
    
    def save(self,**data):
        model = self._model(**data)
        self.session.add(model)
        self.session.commit()
        return model 

    def save_or_update(self, commit=True,data=None,**filters):
        save_obj = True 
        if filters:
            query = self.queryset.filter_by(**filters)
            obj = query.one_or_none()
            if obj:
                save_obj = False
                for field, value in data.items():
                    if field == "password":
                        value = value 
                    if hasattr(obj,field):
                        setattr(obj,field,value)
                    
        if save_obj: 
            obj = self.model(**data)
            self.session.add(obj)
        if commit: 
           self.session.commit()
        return obj 
    
    def _get(self,**filters):
        try:
            query = self.queryset.filter_by(**filters)
            obj = query.one_or_none()
            if obj is None: 
                raise Exception('object not found')
            return obj
        except MultipleResultsFound:
                raise MultipleResultsFound
        
    def update(self, data= None, **filters):
        obj = self._get(**filters)
        for field, value in data.items():
            if hasattr(obj,field):
                setattr(obj,field,value)
            else:
                raise Exception('Field not found in Model')
        self.session.commit()
        return obj
    
    def delete(self, **filters):
        obj = self._get(**filters)
        if obj is None: 
            raise Exception('Object not found to delete')
        self.session.delete(obj)
        self.session.commit()
        return obj
    
    def filter(self,**filters):
        query = self.queryset.filter_by(**filters)
        return query.all()

    def get (self,**filters):
        return self._get(**filters)

    
#Custom exceptions
#Hash in psw
