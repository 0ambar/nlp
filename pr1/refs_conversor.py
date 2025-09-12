import to_bib, to_ris

print('\t====== BIBTEX TO RIS ')
bib_path = 'Pruebas2/BibTex/journal_test3'
to_ris.write_info(to_ris.read_info(bib_path))


print('\t====== RIS TO BIBTEX ')
ris_path = 'Pruebas2/RIS/journal_test2'
to_bib.write_info(to_bib.read_info(ris_path))