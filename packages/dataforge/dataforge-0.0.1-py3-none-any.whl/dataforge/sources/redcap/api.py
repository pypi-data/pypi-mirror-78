"""CLI access to REDCap projects through API"""

import click
import keyring
import pycurl
import datetime, os, sys
from urllib.parse import urlparse, urlencode

PROJECT_XML = {
    'content': 'project_xml',
    'format': 'xml',
    'returnMetadataOnly': 'true',
    'exportFiles': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

PROJECT_DATA = {
    'content': 'record',
    'format': 'csv',
    'type': 'flat',
    'rawOrLabel': 'label',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'true',
    'returnFormat': 'json'
}

def export_to_file(parms, url, token, cainfo, outfile):
    """Make call to REDCap API and write result to file"""
    parms.update({'token':token})
    postfields = urlencode(parms)
    
    with open(outfile, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(c.WRITEDATA, f)
        if cainfo:
            c.setopt(c.CAINFO, cainfo)
        c.perform()
        c.close()

@click.command()
@click.argument('url', envvar='REDCAP_URL')
@click.option('--token', '-t', help='REDCap API token')
@click.option('--cainfo', '-c', envvar='REDCAP_CAINFO',
              type=click.Path(exists=True),
              help='Path to file containing certificate chain')
@click.option('--project_name', '-p', envvar='REDCAP_PROJECT',
              help='REDCap project name abbreviation (no spaces)')
@click.option('--outdir', '-o', envvar='REDCAP_OUTDIR', default='tmp/redcap',
              show_default=True)
def export(url, token, cainfo, project_name, outdir):
    """Export data and metadata from REDCap project"""
    
    if token is None:
        token = keyring.get_password(urlparse(url).hostname, project_name)
        if token is None:
            sys.exit('Token not found in system keyring')
    
    if project_name is None:
        project_name = ''
    elif project_name != '':
        project_name = project_name + '_'
    
    os.makedirs(outdir, exist_ok=True)
    ts = '{:%Y-%m-%d_%H%M}'.format(datetime.datetime.now())
    
    fname = '{}{}.REDCap.xml'.format(project_name, ts)
    export_to_file(PROJECT_XML, url, token, cainfo, os.path.join(outdir,fname))
    
    fname = '{}DATA_LABELS_{}.csv'.format(project_name, ts)
    export_to_file(PROJECT_DATA, url, token, cainfo, os.path.join(outdir,fname))
