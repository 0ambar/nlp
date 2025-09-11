# RIS a BibTex

import re

FIELD_TYPE = {
    'TI': 'title',
    'PY': 'year',
    'VL': 'volume',
    'IS': 'number',
    'DO': 'doi',
    'UR': 'url',
    'PB': 'publisher',
    'JO': 'journal',
    'BT': 'booktitle',
    'ET': 'edition',
    'KW': 'keywords',
    'SN': 'issn',
    'CY': 'address',
    'AB': 'abstract',
}

# Fields that can have multiple values
MULTI_VALUES = ['AU', 'ED']

ENTRY_TYPE = {
    'JOUR': 'Article',
    'CONF': 'InProceedings'
}

ENTRY_SPLITTER = r'\n*([A-Z][A-Z])\s+-\s+(.*)'
TY_PATTERN = r'TY\s+-\s+(\w*)'
ID_PATTERN = r'ID\s+-\s+([\w\-\.\/]+)'


def read_info(text):
    body = re.findall( ENTRY_SPLITTER, text )
    return body


def write_info(ris_info_list):
    try:
        with open( 'pr1/Salidas/salida_bib.bib', 'w') as file:
            entry_type = ''
            entry_id = ''
            authors = ''
            editors = ''
            month = ''
            day = ''
            pages = ''
            
            # Encontrar tipo e ID
            for field in ris_info_list:
                k, v = field[0], field[1]
                if k == 'TY':
                    entry_type = ENTRY_TYPE[v]
                elif k == 'ID':
                    entry_id = v            
                elif k == 'DA':
                    date = v.split('/')
                    month = date[1]
                    day = date[2]
                elif k == 'AU': # Encontrar autores y editores
                    authors += f'{v}\nand '
                elif k == 'ED':
                    editors += f'{v}\nand '
                elif k == 'SP':
                    pages = f'{v}'
                elif k == 'EP':
                    pages += f'--{v}'
            
            file.write(f'@{entry_type}{{{entry_id},\n') # Escribir encabezado completo
            file.write(f'author={{{authors}}},\n')
            file.write(f'editor={{{editors}}},\n')            
            file.write(f'pages={{{pages}}},\n')
            file.write(f'month={{{month}}},\n' if month else '')
            file.write(f'day={{{day}}},\n' if day else '')            


            for field in ris_info_list:
                k, v = field[0], field[1]
                if k in FIELD_TYPE:
                    file.write(f'{FIELD_TYPE[k]}={{{v}}},\n')
            
            file.write('}\n')
            
    except FileNotFoundError:
        print('\nEl archivo no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')


try:
    with open( 'pr1/Pruebas1/journal1.ris', 'r' ) as file:
        text = file.read().strip()
    
    ris_info_list = read_info(text)
    
    write_info(ris_info_list)

except FileNotFoundError:
    print('\nEl archivo .ris no fue encontrado')
    
except Exception as e:
    print(f'\nError: {e}')

