import httpx
base='http://127.0.0.1:8001'
data={"laboratorio":"Laboratório Evidência 6","data_reserva":"2026-11-05","turno":"noite","responsavel":"Matheus Prates Gaspar Silva","quantidade_pessoas":6,"finalidade":"Atividade investigativa Full Stack"}
with httpx.Client() as c:
    print('GET /',c.get(base+'/').status_code)
    print('GET /docs',c.get(base+'/docs').status_code)
    print('RESUMO_ANTES',c.get(base+'/api/reservas/resumo').json())
    r=c.post(base+'/api/reservas',json=data); print('POST_VALIDA',r.status_code,r.json()); rid=r.json()['id']
    bad={**data,'laboratorio':'Laboratório Evidência 7','quantidade_pessoas':0}; r=c.post(base+'/api/reservas',json=bad); print('POST_422',r.status_code,r.json())
    r=c.get(base+'/api/reservas/999999'); print('GET_404',r.status_code,r.json())
    r=c.post(base+'/api/reservas',json=data); print('POST_CONFLITO',r.status_code,r.json())
    upd={**data,'responsavel':'Responsável Atualizado'}; r=c.put(f'{base}/api/reservas/{rid}',json=upd); print('PUT',r.status_code,r.json())
    r=c.get(base+'/api/reservas?turno=noite'); print('FILTRO_NOITE',r.status_code,[x for x in r.json() if x['id']==rid])
    print('RESUMO_DEPOIS',c.get(base+'/api/reservas/resumo').json())
    print('ID_PERSISTENCIA',rid)

