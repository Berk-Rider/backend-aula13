from docx import Document
from pathlib import Path
root=Path(r'D:/Usuários/Berk_/Desktop/atividade_fs')
p=root/'documentos/Questionario_Investigativo_Projeto_Full_Stack.docx'
d=Document(p)
for table in d.tables:
    if len(table.rows)==4 and table.cell(0,0).text=='Ação executada':
        for cell in table.rows[2].cells:
            if 'Banco normal' in cell.text:
                cell.text=cell.text.replace('Banco normal dados/reservas.db foi verificado com 0 reservas após a suíte; os testes usam banco temporário.','Banco normal `dados/reservas.db` foi verificado com 0 reservas após a suíte; os testes usam banco temporário.')
        for cell in table.rows[3].cells:
            if 'contagem zero' in cell.text:
                cell.text=cell.text.replace('A contagem zero no banco normal confirma que os testes não gravaram nele.','A contagem zero observada no banco normal e o caminho temporário configurado confirmam o isolamento da suíte.')
        break
d.save(p)
log=root/'documentos/comandos_executados.txt'
s=log.read_text(encoding='utf-8').replace('Banco normal dados/reservas.db permaneceu com 0 registros após a suíte.','Banco normal dados/reservas.db foi verificado com 0 registros após a suíte.')
log.write_text(s,encoding='utf-8')
print('Atualizado')

