# RIS a BibTex

import re

MONTH_MAP = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec',
}

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

ENTRY_SPLITTER = r'\n?([\w][\w])\s+-\s*?(.*)'
TY_PATTERN = r'TY\s+-\s+(\w*)'
ID_PATTERN = r'ID\s+-\s+([\w\-\.\/]+)'


def read_info(path):
    body = []

    try:
        with open( f'pr1/{path}.ris', 'r' ) as file:
            text = file.read().strip()
        
        body = re.findall( ENTRY_SPLITTER, text )
        
    except FileNotFoundError:
        print('\nEl archivo .ris no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')
    
    return body


def write_info(ris_info_list):
    try:
        with open( 'pr1/Salidas/salida_bib.bib', 'w') as file:
            entry_type = ''
            entry_id = ''
            month = ''
            day = ''
            pages = ''
            authors = []
            editors = []
            i = 0
            
            # Encontrar tipo e ID
            while i < len(ris_info_list):
                field = ris_info_list[i]
                k, v = field[0], field[1].strip()
                if k == 'TY':
                    entry_type = ENTRY_TYPE[v]
                elif k == 'ID':
                    entry_id = v            
                i += 1
                
            file.write(f'@{entry_type}{{{entry_id},\n') # Escribir encabezado completo

            for field in ris_info_list:
                k, v = field[0], field[1].strip()
                if k in FIELD_TYPE:
                    file.write(f'{FIELD_TYPE[k]}={{{v}}},\n')
                elif k == 'DA':
                    date = v.split('/')
                    month = date[1]
                    day = date[2]
                elif k == 'AU': # Encontrar autores
                    authors += [v]
                elif k == 'ED': # Encontrar editores
                    editors += [v]
                elif k == 'SP':
                    pages = f'{v}'
                elif k == 'EP':
                    pages += f'--{v}'
                else: 
                    if k == 'ER' or k == 'TY':
                        continue
                    file.write(f'unknown={{{v}}},\n')

            if len(authors) > 0:
                file.write('author={')
                for editor in authors:
                    file.write(f'{f'{editor}\nand ' if editor != authors[-1] else f'{editor}\n'}')
                file.write('},\n')
            
            if len(editors) > 0:
                file.write('editor={')
                for editor in editors:
                    file.write(f'{f'{editor}\nand ' if editor != editors[-1] else f'{editor}\n'}')
                file.write('},\n')
                
            file.write(f'pages={{{pages}}},\n')
            file.write(f'month={{{MONTH_MAP[month]}}},\n' if month else '')
            file.write(f'day={{{day}}},\n' if day else '')            
            
            file.write('}\n')
            
    except FileNotFoundError:
        print('\nEl archivo no fue encontrado')
        
    except Exception as e:
        print(f'\nError: {e}')
