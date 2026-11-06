import httpx
base='http://127.0.0.1:8001'
with httpx.Client() as c:
    r=c.get(base+'/api/reservas/1'); print('APOS_REINICIO',r.status_code,r.json())
    d=c.delete(base+'/api/reservas/1'); print('DELETE',d.status_code,repr(d.text))
    r=c.get(base+'/api/reservas/1'); print('CONSULTA_APOS_EXCLUSAO',r.status_code,r.json())
    print('DELETE_INTERFACE_RECORD',c.delete(base+'/api/reservas/2').status_code)
    print('REGISTROS_REMANESCENTES',c.get(base+'/api/reservas').json())
