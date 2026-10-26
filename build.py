import json,html,os
R=os.path.dirname(os.path.abspath(__file__));D=json.load(open(f'{R}/data/tools.json'))
ch=json.load(open(f'{R}/data/changes.json')) if os.path.exists(f'{R}/data/changes.json') else []
e=lambda s:html.escape(str(s))
CSS="body{font:15px system-ui;max-width:1100px;margin:auto;padding:1em}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:6px;text-align:left}nav a{margin-right:1em}.note{background:#f6f6f6;padding:.6em}"
SITE='https://realmpastai-web.github.io/agentqa/'
DESC='Independent directory of AI test-automation tools and agents: pricing, free tiers, open-source status and integrations from vendor pages.'
def page(t,b,p='',d='',path=''):return f"<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width'><title>{e(t)} | AgentQA</title><meta name=description content=\"{e(d or DESC)}\"><link rel=canonical href=\"{SITE}{path}\"><style>{CSS}</style><nav><a href={p}index.html><b>AgentQA</b></a><a href={p}compare.html>Compare</a><a href={p}guides.html>Guides</a><a href={p}changes.html>What changed</a><a href={p}about.html>About & disclosure</a></nav>{b}<hr><form class=note onsubmit='alert(\"Newsletter coming soon\");return false'>Weekly AI-testing tool changes: <input type=email placeholder=you@example.com disabled> <button disabled>Subscribe (coming soon)</button></form><p><small>Facts from vendors' public pages; check source links. No paid placements yet.</small></p>"
yn=lambda v:'yes' if v else ('no' if v is False else '?')
rows=''.join(f"<tr data-cat='{e(t['category'])}' data-os='{yn(t['open_source'])}' data-free='{yn(t['free_tier'])}'><td><input type=checkbox value={t['slug']}></td><td><a href=tools/{t['slug']}.html>{e(t['name'])}</a></td><td>{e(t['category'])}</td><td>{e(', '.join(t['tests']))}</td><td>{yn(t['free_tier'])}</td><td>{yn(t['open_source'])}</td><td>{t['last_checked']}</td></tr>" for t in D)
idx=f"""<h1>AI test-automation tools & agents</h1><p>{len(D)} tools tracked.</p><input id=q placeholder='Search…'> <select id=os><option value=''>Open source: any<option>yes<option>no</select> <select id=fr><option value=''>Free tier: any<option>yes<option>no<option>?</select> <button onclick="location='compare.html#'+[...document.querySelectorAll('input:checked')].map(c=>c.value).join(',')">Compare selected</button>
<table><thead><tr><th></th><th>Tool</th><th>Category</th><th>Tests</th><th>Free tier</th><th>Open source</th><th>Checked</th></tr></thead><tbody id=tb>{rows}</tbody></table>
<script>function f(){{let q=document.getElementById('q').value.toLowerCase(),o=document.getElementById('os').value,r=document.getElementById('fr').value;for(const t of document.querySelectorAll('#tb tr'))t.hidden=!(t.textContent.toLowerCase().includes(q)&&(!o||t.dataset.os==o)&&(!r||t.dataset.free==r))}}['q','os','fr'].forEach(i=>document.getElementById(i).oninput=f)</script>"""
os.makedirs(f'{R}/site/tools',exist_ok=True);w=lambda p,s:open(f'{R}/site/{p}','w').write(s)
w('index.html',page('AI test-automation tools & agents directory',idx))
for t in D:
  b=f"<h1>{e(t['name'])}</h1><table>"+''.join(f"<tr><th>{k}</th><td>{e(', '.join(v) if isinstance(v,list) else yn(v) if v in (True,False,None) else v)}</td></tr>" for k,v in t.items() if k!='slug')+f"</table><p><a href='{e(t['url'])}' rel=nofollow>Visit site</a> · <a href='{e(t['source'])}'>Source</a></p>"
  w(f"tools/{t['slug']}.html",page(t['name']+': pricing, free tier & features',b,'../',f"{t['name']} ({t['category']}): pricing, free tier, open-source status and integrations, from the vendor's own page.",f"tools/{t['slug']}.html"))
w('data.json',json.dumps(D))
w('compare.html',page('Compare AI testing tools side by side',"<h1>Side-by-side compare</h1><p>Pick tools on the home page, or edit the URL hash (slugs, comma-separated).</p><div id=c></div><script>fetch('data.json').then(r=>r.json()).then(d=>{let s=location.hash.slice(1).split(',').filter(Boolean);let t=d.filter(x=>s.includes(x.slug));if(!t.length)t=d.slice(0,3);let k=['category','tests','pricing','free_tier','open_source','integrations','last_checked','source'];document.getElementById('c').innerHTML='<table><tr><th></th>'+t.map(x=>'<th>'+x.name+'</th>').join('')+'</tr>'+k.map(f=>'<tr><th>'+f+'</th>'+t.map(x=>'<td>'+(Array.isArray(x[f])?x[f].join(', '):x[f])+'</td>').join('')+'</tr>').join('')+'</table>'})</script>"))
w('changes.html',page('What changed: AI testing tool pricing & page changes',"<h1>What changed this week</h1>"+("<ul>"+''.join(f"<li>{e(c['date'])} — <b>{e(c['name'])}</b>: {e(c['what'])} (<a href='{e(c['url'])}'>page</a>)</li>" for c in ch[::-1][:50])+"</ul>" if ch else "<p>No changes detected yet. Baseline captured 2026-10-16.</p>")))
w('about.html',page('About & disclosure',"<h1>About & sponsor disclosure</h1><p>AgentQA is an independent directory of AI test-automation tools. Data comes from each vendor's public pages and is re-checked automatically.</p><p class=note><b>Disclosure (placeholder):</b> We currently have no sponsors and no affiliate links. If that changes, sponsored listings will be clearly labeled 'Sponsored' and will never change factual data or ordering of non-sponsored entries.</p>"))
# --- guide pages: category lists + X vs Y, generated only from data/tools.json ---
B={t['slug']:t for t in D}
def tbl(L):return "<table><tr><th>Tool</th><th>Category</th><th>Tests</th><th>Pricing</th><th>Free tier</th><th>Open source</th><th>Checked</th></tr>"+''.join(f"<tr><td><a href=tools/{t['slug']}.html>{e(t['name'])}</a></td><td>{e(t['category'])}</td><td>{e(', '.join(t['tests']))}</td><td>{e(t['pricing'])}</td><td>{yn(t['free_tier'])}</td><td>{yn(t['open_source'])}</td><td>{t['last_checked']}</td></tr>" for t in L)+"</table>"
CATS=[('open-source-ai-testing-tools.html','Open-source AI testing tools',lambda t:t['open_source'] is True,'Open-source AI test-automation tools and browser agents, with licenses and pricing as stated on each project page.'),
 ('free-ai-testing-tools.html','AI testing tools with a free plan',lambda t:t['free_tier'] is True,'AI test-automation tools that offer a free plan or are free to use, per each vendor\'s pricing page.'),
 ('playwright-ai-testing-tools.html','AI testing tools that work with Playwright',lambda t:any('playwright' in i.lower() for i in t['integrations']),'AI testing tools and agents built on or integrating with Playwright, from vendor and project pages.'),
 ('mobile-ai-testing-tools.html','AI testing tools for mobile apps',lambda t:any(k in ' '.join(t['tests']).lower() for k in ('mobile','android','ios')),'AI test-automation tools that list mobile, Android or iOS testing, per vendor pages.'),
 ('mcp-ai-testing-tools.html','AI testing tools with an MCP server',lambda t:any('mcp' in i.lower() for i in t['integrations']),'AI test-automation tools that ship or integrate an MCP server so coding agents can drive tests, per vendor and project pages.'),
 ('desktop-ai-testing-tools.html','AI testing tools for desktop apps',lambda t:any('desktop' in x.lower() for x in t['tests']),'AI test-automation tools that list desktop app testing (Windows, macOS or desktop apps), per vendor and project pages.'),
 ('api-ai-testing-tools.html','AI tools for API testing',lambda t:any('api' in x.lower() for x in t['tests']),'AI testing tools that list API testing, with pricing and open-source status from vendor and project pages.'),
 ('ai-testing-tools-with-public-pricing.html','AI testing tools with public pricing',lambda t:'$' in t['pricing'],'AI test-automation tools that publish dollar prices on their own pricing page (no sales call needed to see a number), as last checked.')]
VS=[('stagehand','browser-use'),('midscene','stagehand'),('playwright-mcp','stagehand'),('shortest','midscene'),('momentic','qa-tech'),('testrigor','testsigma'),('alumnium','midscene'),('testzeus-hercules','shortest'),('arbigent','midscene'),('maestro','arbigent'),('testerarmy-e2e','midscene'),('bug0','qa-wolf'),('donobu','momentic'),('ranger','testdriver')]
F=['category','tests','pricing','free_tier','open_source','integrations','last_checked']
def vs(a,b):
  r=''.join(f"<tr><th>{k.replace('_',' ')}</th>"+''.join(f"<td>{e(', '.join(x[k]) if isinstance(x[k],list) else yn(x[k]) if x[k] in (True,False,None) else x[k])}</td>" for x in (a,b))+"</tr>" for k in F)
  r+="<tr><th>source</th>"+''.join(f"<td><a href='{e(x['source'])}' rel=nofollow>{e(x['source'])}</a></td>" for x in (a,b))+"</tr>"
  return f"<h1>{e(a['name'])} vs {e(b['name'])}</h1><p>Side-by-side facts taken only from each vendor's or project's own page (last checked dates shown). No ratings or reviews; '?' means not verified.</p><table><tr><th></th><th><a href=tools/{a['slug']}.html>{e(a['name'])}</a></th><th><a href=tools/{b['slug']}.html>{e(b['name'])}</a></th></tr>{r}</table>"
G=[]
for fn,t,f,d in CATS:
  L=[x for x in D if f(x)];G.append((fn,t));w(fn,page(t,f"<h1>{e(t)} ({len(L)})</h1><p>{e(d)}</p>"+tbl(L),'',f"{len(L)} {d if d[:2]=='AI' else d[0].lower()+d[1:]}",fn))
for a,b in VS:
  fn=f"{a}-vs-{b}.html";t=f"{B[a]['name']} vs {B[b]['name']}";G.append((fn,t))
  w(fn,page(t+': pricing, features & open source compared',vs(B[a],B[b]),'',f"{t}: category, pricing, free tier, open-source status and integrations compared side by side, from official pages.",fn))
w('guides.html',page('Guides: AI testing tool categories & comparisons',"<h1>Guides</h1><ul>"+''.join(f"<li><a href={fn}>{e(t)}</a></li>" for fn,t in G)+"</ul>",'','Category lists and X vs Y comparisons of AI test-automation tools, generated from verified vendor data.','guides.html'))
U=['','compare.html','changes.html','about.html','guides.html']+[fn for fn,_ in G]+[f"tools/{t['slug']}.html" for t in D]
import datetime;td=datetime.date.today().isoformat()
w('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"<url><loc>{SITE}{u}</loc><lastmod>{td}</lastmod></url>\n" for u in U)+'</urlset>\n')
w('robots.txt',f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print('built',len(D),'tools,',len(G),'guide pages + sitemap')
