from docx import Document
from pathlib import Path
import re
p=Path(r'D:/Usuários/Berk_/Desktop/atividade_fs/documentos/Questionario_Investigativo_Projeto_Full_Stack.docx')
d=Document(p)
alltext='\n'.join(x.text for x in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for row in t.rows for c in row.cells)
qs=[int(m.group(1)) for para in d.paragraphs if (m:=re.match(r'^(\d+)\.\s',para.text))]
print('QUESTIONS',qs)
print('IDENTIFICATION',d.paragraphs[3].text,d.tables[0].cell(1,0).text,d.tables[0].cell(1,1).text)
print('Q19',d.tables[1].cell(2,1).text)
print('UNDERSCORE_PLACEHOLDERS',alltext.count('________________'))
print('REMAINING_BACKTICKS',alltext.count(chr(96)))
print('EVIDENCE_ROWS',len(d.tables[-1].rows),'CAPTURES_FILLED',sum(bool(d.tables[-1].cell(i,2).text.strip()) for i in range(1,len(d.tables[-1].rows))))
print('HEADER_REPEAT',d.tables[-1].rows[0]._tr.trPr.xml.find('tblHeader')>=0)
print('CANT_SPLIT_ROWS',sum('cantSplit' in row._tr.trPr.xml for row in d.tables[-1].rows),'OF',len(d.tables[-1].rows))
print('DOCX_BYTES',p.stat().st_size)
log=p.parent/'comandos_executados.txt'; print('LOG_EXISTS',log.exists(),'LOG_BYTES',log.stat().st_size)
