# BibTex to RIS

import re

FIELD_TYPE = {
    'author': 'AU',
    'title': 'TI', 
    'year': 'PY',
    'volume': 'VL',
    'number': 'IS',
    'pages': 'SP/EP',  # Requiere procesamiento especial para SP y EP
    'doi': 'DO',
    'url': 'UR',
    'publisher': 'PB',
    'journal': 'JO',
    'booktitle': 'BT',
    'editor': 'ED',
    'edition': 'ET',
    'keywords': 'KW',
    'issn': 'SN',
    'isbn': 'SN',
    'address': 'CY', 
    'abstract': 'AB'
}

# Fields that can have multiple values
MULTI_VALUES = [
    'author',
    'editor'
]

ENTRY_TYPE = {
    'article': 'JOUR',
    'inproceedings': 'CONF'
}

ENTRY_SPLITTER = (
    r'(\s*@\w*\s*)'                 # Tipo de entrada (grupo 1)
    r'\{'                           # Llave de apertura
    r'([\w\-\.\/]+)'                # Identificador (grupo 2)
    r','                            # Coma
    r'(.*\n*)'                      # Contenido (grupo 3)
    r'(.*\})'                       # Resto hasta cierre (grupo 4, se desecha)
)
FIELDS_SPLITTER = r'\w*\s*=\s*'     # Every key-value pattern
CONTENT_PATTERN = r'\{(.*)\}'       # Values pattern
TAG_PATTERN = r'\w*[^=]'            # Key pattern



try:
    with open( 'pr1/Pruebas1/conference2.bib', 'r' ) as archivo:
        text = archivo.read().strip()
    
    body = re.search( ENTRY_SPLITTER, text, re.DOTALL )

    entry_type = ''
    body_fields = ''
    if body:
        entry_type = body.group(1).lower()
        identifier = body.group(2).lower()
        body_fields = body.group(3)
    
    tags_with_equals = re.findall( FIELDS_SPLITTER, body_fields )
    fields_content = re.split( FIELDS_SPLITTER, body_fields )
    
    bib_map = {}
    i = 0
    while i < len(tags_with_equals):
        content = re.search(CONTENT_PATTERN, fields_content[i + 1], re.DOTALL).group(1)
        clean_tag = re.search(TAG_PATTERN, tags_with_equals[i]).group()
        bib_map[clean_tag] = content
        i += 1

    for key, value in bib_map.items():
        print(f'\n{key}: {re.split(r'and\s+', value) if key in MULTI_VALUES else value}')
        

    
except FileNotFoundError:
    print('\nEl archivo no fue encontrado')
    
except Exception as e:
    print(f'\nError: {e}')

