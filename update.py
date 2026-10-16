#!/usr/bin/env python3
"""Re-check each tool's source page; log content changes; rebuild. Cron: 0 6 * * 1 python3 /workspace/agentqa/update.py"""
import json,hashlib,re,os,urllib.request,datetime,subprocess
R=os.path.dirname(os.path.abspath(__file__));P=f'{R}/data'
D=json.load(open(f'{P}/tools.json'));H=json.load(open(f'{P}/hashes.json')) if os.path.exists(f'{P}/hashes.json') else {}
C=json.load(open(f'{P}/changes.json')) if os.path.exists(f'{P}/changes.json') else []
today=datetime.date.today().isoformat()
for t in D:
  try:
    raw=urllib.request.urlopen(urllib.request.Request(t['source'],headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}),timeout=20).read().decode('utf8','ignore')
    txt=re.sub(r'\s+',' ',re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>',' ',raw,flags=re.S))
    prices=sorted(set(re.findall(r'\$\d[\d,.]*\s?/\s?(?:mo|month|user)',txt)))
    h=hashlib.sha256(' '.join(prices).encode()+txt[:20000].encode()).hexdigest()
    old=H.get(t['slug'])
    if old and old['hash']!=h:
      what='pricing figures changed: '+', '.join(prices) if old.get('prices')!=prices else 'page content changed'
      C.append({'date':today,'name':t['name'],'what':what,'url':t['source']})
    H[t['slug']]={'hash':h,'prices':prices};t['last_checked']=today
  except Exception as ex: print('fail',t['slug'],ex)
for n,o in ((f'{P}/tools.json',D),(f'{P}/hashes.json',H),(f'{P}/changes.json',C)): json.dump(o,open(n,'w'),indent=1)
subprocess.run(['python3',f'{R}/build.py'])
