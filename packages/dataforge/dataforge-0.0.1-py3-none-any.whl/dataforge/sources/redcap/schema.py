"""REDCap extensions to CDISC ODM schema"""

from dataforge.schema.cdisc_odm import schema

@schema.define
class GlobalVariables:
    def __init__(self,
                 study_names = [],
                 redcap_repeating_instruments_and_eventses = []):
        self.study_names = study_names
        self.redcap_repeating_instruments_and_eventses = redcap_repeating_instruments_and_eventses

@schema.define
class redcap_RepeatingInstrumentsAndEvents:
    def __init__(self,
                 redcap_repeating_events = [],
                 redcap_repeating_instrumentses = []):
        self.redcap_repeating_events = redcap_repeating_events
        self.redcap_repeating_instrumentses = redcap_repeating_instrumentses

@schema.define
class redcap_RepeatingEvent:
    def __init__(self,
                 redcap_unique_event_name):
        self.redcap_unique_event_name = redcap_unique_event_name

@schema.define
class redcap_RepeatingInstruments:
    def __init__(self,
                 redcap_repeating_instruments = []):
        self.redcap_repeating_instruments = redcap_repeating_instruments

@schema.define
class redcap_RepeatingInstrument:
    def __init__(self,
                 redcap_unique_event_name,
                 redcap_repeat_instrument):
        self.redcap_unique_event_name = redcap_unique_event_name
        self.redcap_repeat_instrument = redcap_repeat_instrument

@schema.define
class ItemDef:
    def __init__(self,
                 oid,
                 name,
                 redcap_field_type):
        self.oid = oid
        self.name = name
        self.redcap_field_type = redcap_field_type
