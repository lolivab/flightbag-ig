# uso: IGTOKEN=... python3 ig_post.py N   (publica el post N de posts.json con imagenes de /posts)
import sys,json,os,time,urllib.request,urllib.parse
B='https://raw.githubusercontent.com/lolivab/flightbag-ig/main/'
TOK=os.environ['IGTOKEN']; UID='17841443242816248'; API='https://graph.instagram.com/v23.0'
n=int(sys.argv[1]); P=json.load(urllib.request.urlopen(B+'posts.json'))[str(n)]
names=[]; k=1
while True:
    nm=f'w{n:02d}_{k}.jpg'
    try: urllib.request.urlopen(B+'posts/'+nm,timeout=20); names.append(nm); k+=1
    except Exception: break
print(len(names),'imagenes')
def call(path,**kw):
    r=urllib.request.Request(f'{API}/{path}',data=urllib.parse.urlencode(kw).encode(),headers={'Authorization':'Bearer '+TOK})
    try: return json.load(urllib.request.urlopen(r,timeout=60))
    except urllib.error.HTTPError as e: print(e.read().decode()); sys.exit(1)
def get(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(f'{API}/{path}',headers={'Authorization':'Bearer '+TOK}),timeout=60))
u=lambda nm:B+'posts/'+nm
if len(names)==1: c=call(f'{UID}/media',image_url=u(names[0]),caption=P['text'],alt_text=P['alt'][0])['id']
else:
    ch=[call(f'{UID}/media',image_url=u(nm),is_carousel_item='true',alt_text=P['alt'][i])['id'] for i,nm in enumerate(names)]
    c=call(f'{UID}/media',media_type='CAROUSEL',children=','.join(ch),caption=P['text'])['id']
for _ in range(40):
    s=get(f'{c}?fields=status_code')['status_code']
    if s=='FINISHED': break
    if s=='ERROR': print('ERROR'); sys.exit(1)
    time.sleep(3)
print(call(f'{UID}/media_publish',creation_id=c)); print('publicado post',n)
