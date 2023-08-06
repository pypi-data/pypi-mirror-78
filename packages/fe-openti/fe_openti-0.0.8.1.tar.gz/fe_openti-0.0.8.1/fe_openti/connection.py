# -#- coding: utf-8 -#-
import collections
from datetime import datetime
from lxml import etree
import codecs
import logging
import ssl
from facturacion_electronica import clase_util as util
from facturacion_electronica.conexion import Conexion
_logger = logging.getLogger(__name__)

try:
    from suds.client import Client
except ImportError:
    print('Cannot import SUDS')

try:
    import urllib3
    # urllib3.disable_warnings()
    pool = urllib3.PoolManager(timeout=30)
except:
    raise UserError('Error en cargar urllib3')

server_url = {
    'certificacion': 'https://maullin.sii.cl/',
    'produccion': 'https://palena.sii.cl/',
    'certificacion_bol_1': 'https://apicert.sii.cl/recursos/v1',
    'certificacion_bol_2': 'https://pangal.sii.cl/recursos/v1',
    'produccion_bol_1': 'https://api.sii.cl/',
    'produccion_bol_1': 'https://palena.sii.cl/',
}

class Connection(Conexion):
    def __init__(self):
        print("hello")