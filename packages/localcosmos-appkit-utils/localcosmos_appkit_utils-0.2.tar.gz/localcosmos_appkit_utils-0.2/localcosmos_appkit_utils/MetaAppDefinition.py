##################################################################################################################
#
# METAAPPDEFINITION
#
# - helper class
# - ios app builder runs on mac and has no django orm access

import uuid
from datetime import datetime, date

class MetaAppDefinition:

    def __init__(self, app_version, meta_app=None, meta_app_definition={}):

        self.app_version = app_version

        if not meta_app and not meta_app_definition:
            raise ValueError('AppDefinition initialization requires either meta_app instance or meta_app_definition')

        
        if meta_app:
            meta_app_definition = self.to_dict(app_version, meta_app)
            self.build_number = meta_app.build_number
                

        for field_name, value in meta_app_definition.items():
            setattr(self, field_name, value)


    @classmethod
    def _to_json(self, value):

        if isinstance(value, (datetime, date)): 
            return value.isoformat()

        if isinstance(value, (uuid.UUID)):
            return str(value)

        return value
        
    
    @classmethod
    def to_dict(cls, app_version, meta_app):

        meta_app_definition = {}
        
        for field in meta_app._meta.concrete_fields:
            if field.concrete == True:

                field_value = field.value_from_object(meta_app)
                json_value = cls._to_json(field_value)

                meta_app_definition[field.name] = json_value
                

        for field_name in ['uuid', 'name', 'primary_language']:
            field_value = cls._to_json(getattr(meta_app.app, field_name))
            meta_app_definition[field_name] = field_value

        return meta_app_definition
        
