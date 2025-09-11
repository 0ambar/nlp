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
    r'\s*@(\w*\s*)'                 # Tipo de entrada (grupo 1)
    r'\{'                           # Llave de apertura
    r'([\w\-\.\/]+)'                # Identificador (grupo 2)
    r','                            # Coma
    r'(.*\n*)'                      # Contenido (grupo 3)
    r'(.*\})'                       # Resto hasta cierre (grupo 4, se desecha)
)
FIELDS_SPLITTER = r'\w*\s*=\s*'     # Every key-value pattern
CONTENT_PATTERN = r'\{(.*)\}'       # Values pattern
TAG_PATTERN = r'\w*[^=]'            # Key pattern


def read_info(text):
    body = re.search( ENTRY_SPLITTER, text, re.DOTALL )

    entry_type = ''
    identifier = ''
    body_fields = ''
    if body:
        entry_type = body.group(1).lower()
        identifier = body.group(2).lower()
        body_fields = body.group(3)
    
    tags_with_equals = re.findall( FIELDS_SPLITTER, body_fields )
    fields_content = re.split( FIELDS_SPLITTER, body_fields )
    
    bib_map = {}
    bib_map['type'] = entry_type
    bib_map['id'] = identifier
    i = 0
    while i < len(tags_with_equals):
        content = re.search(CONTENT_PATTERN, fields_content[i + 1], re.DOTALL).group(1)
        clean_tag = re.search(TAG_PATTERN, tags_with_equals[i]).group()
        clean_content = re.split(r'\nand\s+', content) if clean_tag in MULTI_VALUES else content
        bib_map[clean_tag] = clean_content
        i += 1


    return bib_map
        

def write_info(bib_map):
    try:
        with open( 'pr1/Salidas/salida.ris', 'w') as file:
            date = '///'
            for k, v in bib_map.items():
                match k:
                    case 'type':
                        file.write(f'TY  - {ENTRY_TYPE[v]}\n')
                    case 'id':
                        file.write(f'ID  - {v}\n')
                    case 'author' | 'editor':
                        for author in v:
                            file.write(f'{FIELD_TYPE[k]}  - {author}\n')
                    case 'pages':
                        pages = v.split('--')
                        sp = pages[0]
                        ep = pages[-1]
                        file.write(f'SP  - {sp}\nEP  - {ep}\n')
                    case 'year':
                        date = f'{v}/'
                        file.write(f'{FIELD_TYPE[k]}  - {v}\n')
                    case 'month':
                        date += f'{v}/'
                    case 'day':
                        date += f'{v}'
                        file.write(f'DA  - {date}\n')
                    case _:
                        file.write(f'{FIELD_TYPE[k]}  - {v}\n')
            
            file.write('ER  -\n')
            
    except FileNotFoundError:
        print('\nEl archivo no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')


try:
    with open( 'pr1/Pruebas1/conference2.bib', 'r' ) as file:
        text = file.read().strip()
    
    bib_map = read_info(text)
    write_info(bib_map)


except FileNotFoundError:
    print('\nEl archivo .bib no fue encontrado')
    
except Exception as e:
    print(f'\nError: {e}')

