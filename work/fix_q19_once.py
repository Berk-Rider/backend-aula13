from docx import Document
from pathlib import Path
root=Path(r'D:/Usuários/Berk_/Desktop/atividade_fs')
p=root/'documentos/Questionario_Investigativo_Projeto_Full_Stack.docx'
d=Document(p)
t=d.tables[1]
t.cell(2,1).text=t.cell(2,1).text.replace('Banco normal dados/reservas.db permaneceu com 0 reservas antes/depois da suíte; os testes usam banco temporário.','Banco normal dados/reservas.db foi verificado com 0 reservas após a suíte; os testes usam banco temporário.')
d.save(p)
log=root/'documentos/comandos_executados.txt'
s=log.read_text(encoding='utf-8').replace('Banco normal dados/reservas.db permaneceu com 0 registros após a suíte.','Banco normal dados/reservas.db foi verificado com 0 registros após a suíte.')
log.write_text(s,encoding='utf-8')
print(t.cell(2,1).text)
