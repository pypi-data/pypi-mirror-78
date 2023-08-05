"""Utilities for manipulating data from a REDCap project"""

from dataforge.sources.redcap.schema import schema
import pandas as pd
import glob
import os
import re

class REDCapProject:
    
    def __init__(self, project_name='', path='tmp/redcap'):
        
        last_export = self._last_export(project_name, path)
        if not last_export:
            raise Exception('No REDCap exports found')
        if project_name:
            project_name = project_name + '_'
        base = os.path.join(path, project_name)
        
        try:
            datafile = f'{base}DATA_LABELS_{last_export}.csv'
            # We use the Python engine here because it handles embedded newlines
            self.data = pd.read_csv(datafile, engine='python', dtype='object',
                                    keep_default_na=False)
        except FileNotFoundError:
            print(f'Error reading REDCap data file: {datafile}')
            raise
        
        try:
            metafile = f'{base}{last_export}.REDCap.xml'
            with open(metafile) as f:
                self.meta = schema.parse(f.read()).studies[0]
        except FileNotFoundError:
            print(f'Error reading REDCap metadata file: {metafile}')
            raise
        
        self.meta_data = self.meta.meta_data_versions[0]
        self.form_defs = self._get_form_defs()
    
    def _last_export(self, project_name, path):
        """Return datetime of last REDCap export"""
        if project_name:
            project_name = project_name + '_'
        files = sorted(glob.glob(f'{os.path.join(path, project_name)}*'))
        if files:
            s = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{4})\.csv$', files[-1])
            if s:
                return s.group(1)
    
    def _get_item_defs(self):
        """Dicionary of all items indexed by OID"""
        item_defs = {}
        for item_def in self.meta_data.item_defs:
            item_defs[item_def.oid] = item_def
        return item_defs
    
    def _get_item_groups(self):
        """Dicionary of item groups indexed by OID"""
        item_defs = self._get_item_defs()
        item_groups = {}
        for item_group_def in self.meta_data.item_group_defs:
            item_groups[item_group_def.oid] = []
            for item_ref in item_group_def.item_refs:
                item_groups[item_group_def.oid].append(item_defs[item_ref.item_oid])
        return item_groups
    
    def _get_form_defs(self):
        """Dictionary of all forms indexed by form name
        
        Note that we intentionally collapse over item groups here, since the
        metadata lost (i.e., sections and matrices) is not necessary for
        creating data products and the result is considerably simpler.
        """
        form_defs = {}
        item_groups = self._get_item_groups()
        for form_def in self.meta_data.form_defs:
            form_defs[form_def.name] = []
            for item_group_ref in form_def.item_group_refs:
                form_defs[form_def.name].extend(item_groups[item_group_ref.item_group_oid])
        return form_defs
