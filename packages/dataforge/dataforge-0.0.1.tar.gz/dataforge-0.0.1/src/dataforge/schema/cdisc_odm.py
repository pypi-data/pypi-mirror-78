"""Schema for CDISC ODM"""

from xmarshal import Schema

schema = Schema()

@schema.define
class ODM:
    def __init__(self,
                 studies = []):
        self.studies = studies

@schema.define
class Study:
    def __init__(self,
                 global_variableses = [],
                 meta_data_versions = []):
        self.global_variableses = global_variableses
        self.meta_data_versions = meta_data_versions

@schema.define
class GlobalVariables:
    def __init__(self,
                 study_names = []):
        self.study_names = study_names

@schema.define
class MetaDataVersion:
    def __init__(self,
                 protocols = [],
                 form_defs = [],
                 item_group_defs = [],
                 item_defs = []):
        self.protocols = protocols
        self.form_defs = form_defs
        self.item_group_defs = item_group_defs
        self.item_defs = item_defs

@schema.define
class StudyName(str):
    def __new__(self, cdata):
        return super().__new__(self, cdata)

@schema.define
class Protocol:
    def __init__(self,
                 study_event_refs = []):
        self.study_event_refs = study_event_refs

@schema.define
class FormDef:
    def __init__(self,
                 name,
                 item_group_refs = []):
        self.name = name
        self.item_group_refs = item_group_refs

@schema.define
class ItemGroupRef:
    def __init__(self,
                 item_group_oid):
        self.item_group_oid = item_group_oid

@schema.define
class ItemGroupDef:
    def __init__(self,
                 oid,
                 name,
                 item_refs = []):
        self.oid = oid
        self.name = name
        self.item_refs = item_refs

@schema.define
class ItemRef:
    def __init__(self,
                 item_oid):
        self.item_oid = item_oid

@schema.define
class ItemDef:
    def __init__(self,
                 oid,
                 name):
        self.oid = oid
        self.name = name
