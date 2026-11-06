from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
p=Path(r'D:/Usuários/Berk_/Desktop/atividade_fs/documentos/Questionario_Investigativo_Projeto_Full_Stack.docx')
d=Document(p)
# Markdown code delimiters were not intended as visible punctuation in Word.
for para in d.paragraphs:
    if '`' in para.text:
        para.text = para.text.replace('`','')
for table in d.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                if '`' in para.text:
                    para.text = para.text.replace('`','')
# The new evidence register already satisfies the five prompts; remove their duplicated generic checklist.
for para in list(d.paragraphs):
    txt=para.text.strip()
    if txt == 'Resultados observados das evidências' or txt == 'Para cada evidência, informe:' or txt in {
        '1. O que foi executado.','2. O que foi observado.','3. Qual arquivo e função explicam o resultado.',
        '4. Qual trecho confirma a explicação.','5. Qual teste protege esse comportamento ou qual teste deveria ser criado.'
    }:
        para._element.getparent().remove(para._element)
# Keep each evidence entry intact and repeat the table header if it continues to another page.
for table in d.tables:
    if len(table.columns)==3 and table.rows and table.cell(0,0).text=='Código' and table.cell(0,2).text=='Captura':
        headerPr=table.rows[0]._tr.get_or_add_trPr()
        repeat=OxmlElement('w:tblHeader'); repeat.set(qn('w:val'),'true'); headerPr.append(repeat)
        for row in table.rows:
            trPr=row._tr.get_or_add_trPr()
            trPr.append(OxmlElement('w:cantSplit'))
        break
d.save(p)
print('Refinado:',p)
