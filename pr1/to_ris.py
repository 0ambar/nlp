# BibTex to RIS

import re

MONTH_MAP = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

FIELD_TYPE = {
    'author': 'AU',
    'title': 'TI', 
    'year': 'PY',
    'volume': 'VL',
    'number': 'IS',
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
    'abstract': 'AB',
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

SPLITTER = (
    r'\s*@(\w*\s*)'                 # Tipo de entrada (grupo 1)
    r'\{'                           # Llave de apertura
    r'([\w\-\.\/]+)'                # Identificador (grupo 2)
    r','                            # Coma
    r'(.*\n*)'                      # Contenido (grupo 3)
    r'(.*\})'                       # Resto hasta cierre (grupo 4, se desecha)
)
FIELDS_SPLITTER = r'\s*,*\n*\s*\w*\s*=\s*'      # Every key-value pattern
CONTENT_PATTERN = r'\{(.*)\}'                   # Values pattern
TAG_PATTERN = r'(\w*)\s*=\s*'                   # Key pattern


def read_info(path):
    bib_map = {}
    text = ''
    entry_type = ''
    identifier = ''
    body_fields = ''
    i = 0
    
    try:
        with open( f'pr1/{path}.bib', 'r' ) as file:
            text = file.read().strip()

        body = re.search( SPLITTER, text, re.DOTALL )

        # Get each group
        if body:
            entry_type = body.group(1).lower()
            identifier = body.group(2).lower()
            body_fields = body.group(3)
        
        # Divide tags and content
        tag_list = re.findall( TAG_PATTERN, body_fields )
        fields_content = re.split( FIELDS_SPLITTER, body_fields )
        fields_content = fields_content[1:]

        # Contruct bib_map
        bib_map['type'] = entry_type
        bib_map['id'] = identifier
        while i < len(tag_list):
            content = re.search(CONTENT_PATTERN, fields_content[i], re.DOTALL).group(1)
            tag = tag_list[i]
            clean_content = re.split(r'\n?and\s+', content) if tag in MULTI_VALUES else content
            bib_map[tag] = clean_content
            i += 1

    except FileNotFoundError:
        print('\nEl archivo .bib no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')    

    return bib_map
        

def write_info(bib_map):
    try:
        with open( 'pr1/Salidas/salida_ris.ris', 'w') as file:
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
                        pages = re.split(r'[–-]+', v) # v.split('--')
                        sp = pages[0]
                        ep = pages[-1]
                        file.write(f'SP  - {sp}\nEP  - {ep}\n')
                    case 'year':
                        date = f'{v}/'
                        file.write(f'{FIELD_TYPE[k]}  - {v}\n')
                    case 'month':
                        date += f'{MONTH_MAP[v]}/'
                    case 'day':
                        date += f'{v}'
                        file.write(f'DA  - {date}\n')
                    case _:
                        file.write(f'{FIELD_TYPE[k] if k in FIELD_TYPE else 'UK'}  - {v}\n')
            
            file.write('ER  -\n')
            
    except FileNotFoundError:
        print('\nEl archivo no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')
