#!/usr/bin/env python3
"""Add the Cloudflare Web Analytics beacon before </body> on every published HTML page. Idempotent.
Run after any build: python3 add-analytics.py"""
import os,re,sys
TOKEN="4cca1d9e1eab422b9abffe2ffd5a9399"
SNIP=f"<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{\"token\": \"{TOKEN}\"}}'></script><!-- End Cloudflare Web Analytics -->"
n=0;skip=0
for root,dirs,files in os.walk('.'):
    if '/.git' in root or 'node_modules' in root: continue
    for f in files:
        if not f.endswith('.html') or '.before-' in f: continue
        p=os.path.join(root,f); s=open(p,encoding='utf-8').read()
        if TOKEN in s: skip+=1; continue
        if '</body>' not in s: print('no </body>:',p); continue
        i=s.rfind('</body>'); s=s[:i]+SNIP+'\n'+s[i:]
        open(p,'w',encoding='utf-8').write(s); n+=1
print(f'added {n}, already had {skip}')
