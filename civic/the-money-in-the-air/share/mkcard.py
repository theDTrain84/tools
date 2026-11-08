# Writes card.html (1200x630 share card for civic/the-money-in-the-air) with the page's own by-race bars,
# drawn by build.py from data.json. Method copied from stories/php2shell (build/share/mkcard.py).
# usage: python3 mkcard.py && node render.cjs && node preview.mjs
import os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(here))
import build
D = build.DATA
chart = build.by_race_svg(340)
head = D["meta"]["headline"]  # "At least $659 million spent on Ohio's 2026 races for Senate, governor and the U.S. House."
big = D["total"]["display"]  # "$659 million"
assert big in head, head
pre, rest = head.split(big, 1)
pre, rest = pre.strip(), rest.strip()
races = ", ".join(f'{r["name"].split(",")[0]} {build.money(r["v"])}' for r in D["total"]["races"])
html = '''<!doctype html>
<html><head><meta charset="utf-8">
<!-- Share card for civic/the-money-in-the-air, 1200x630. Render: node render.cjs (writes ../../../assets/share/the-money-in-the-air.jpg). Subjects stay inside x 180..1020 (homeview's safe zone). Drawn chart only; no logos, no faces. -->
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,500&family=Public+Sans:wght@400;500;700;800&family=IBM+Plex+Mono:wght@400;500&display=block" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden;background:#F3F6F8;font-family:"Public Sans",sans-serif;color:#162029}
.a{position:absolute}
h1{font-family:"Fraunces",serif;font-weight:600;line-height:1.02;letter-spacing:-.028em}
h1 .big{display:block;font-size:1.42em;letter-spacing:-.04em;line-height:.95;color:#3E6A9E;margin-bottom:6px}
.sub{color:#38434d}
.k{font-family:"Fraunces",serif;font-style:italic;font-weight:500;font-size:16px;color:#5a6670}
.box{background:#fff;border:1.5px solid #162029;border-radius:18px;padding:12px 14px 8px;width:370px}
.box h3{font-family:"Fraunces",serif;font-weight:600;font-size:16px;margin:0 2px 2px}
.chart{display:block;width:100%;height:auto;overflow:visible}
.chart .grid{stroke:#dbe2e7;stroke-width:1}
.chart .ax{font-family:"IBM Plex Mono",monospace;font-size:11px;fill:#5a6670}
.chart .yr{font-family:"Fraunces",serif;font-weight:700;font-size:16px;fill:#162029}
.chart .ln{fill:none;stroke:#3E6A9E;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.chart .ld{fill:none;stroke:#3E6A9E;stroke-width:2.4;stroke-dasharray:2 6;stroke-linecap:round}
.chart .pt{fill:#3E6A9E;stroke:#fff;stroke-width:2}
.chart .lab{font-family:"Fraunces",serif;font-weight:700;font-size:17px;fill:#162029}
.chart .lab.s{font-family:"Public Sans",sans-serif;font-weight:700;font-size:12.5px}
.chart .lab.dim{font-weight:400;fill:#5a6670}
.cap{font-size:12.5px;line-height:1.3;color:#38434d;margin:6px 4px 2px}
.brs{display:block;margin:8px 2px 0;overflow:visible}
.brs .bn{font-family:"Fraunces",serif;font-weight:700;font-size:16px;fill:#162029}
.brs .bvv{font-family:"Fraunces",serif;font-weight:700;font-size:16px;fill:#162029}
.key{font-size:12.5px;color:#38434d;margin:2px 4px 0}
.key i{display:inline-block;width:11px;height:11px;margin-right:5px;vertical-align:-1px}
</style></head>
<body>
<div class="a" style="left:0;top:0;right:0;height:10px;background:#3E6A9E"></div>
<svg class="a" style="left:196px;top:46px" width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="#162029" stroke-width="2.4"/><g fill="#162029"><circle cx="20" cy="7" r="2.6"/><circle cx="32.4" cy="16" r="2.6"/><circle cx="27.6" cy="30.5" r="2.6"/><circle cx="12.4" cy="30.5" r="2.6"/><circle cx="7.6" cy="16" r="2.6"/></g></svg>
<div class="a" style="left:248px;top:46px;font-weight:800;font-size:19px;letter-spacing:.08em">DNSC</div>
<div class="a" style="left:248px;top:69px;font-size:16px;color:#38434d">From the public record</div>
<div class="a k" style="right:196px;top:50px;text-align:right"><span style="display:inline-block;width:18px;height:1.5px;background:#C9A24A;vertical-align:.3em;margin-right:8px"></span>Ohio &middot; the 2026 election</div>
<div class="a" style="left:196px;top:104px;width:808px;height:3px;background:#162029"></div>
<h1 id="hd" class="a" style="left:194px;top:136px;width:420px;font-size:46px">PRE<span class="big">BIG</span>REST</h1>
<div id="sub" class="a sub" style="left:196px;width:410px;font-size:17px;line-height:1.36">What the campaigns and the outside groups have reported spending, race by race, from the FEC and Ohio filings.</div>
<div class="a box" style="left:634px;top:150px"><h3>Spent, by race</h3><p class="key"><i style="background:#162029"></i>outside groups &nbsp; <i style="background:#3E6A9E"></i>campaigns</p>CHART<p class="cap">Outside groups and the candidates&rsquo; campaigns, as reported to the FEC and the Ohio Secretary of State.</p></div>
<div class="a" style="left:196px;top:560px;font-weight:700;font-size:18px;color:#3E6A9E">tools.dnsc.ai/civic/the-money-in-the-air</div>
<script>
(async()=>{await document.fonts.ready;const hd=document.getElementById('hd'),sb=document.getElementById('sub');
 for(let z=48;z>=34;z-=1){hd.style.fontSize=z+'px';const b=hd.getBoundingClientRect();sb.style.top=(b.bottom+18)+'px';
  if(sb.getBoundingClientRect().bottom<=540&&b.right<=620)break;}
 const bad=[...document.querySelectorAll('body *')].filter(e=>{if(e.closest('svg')&&e.tagName!=='svg')return false;const r=e.getBoundingClientRect();if(!r.width||!r.height)return false;if(r.left===0&&r.width===1200)return false;return r.left<179.5||r.right>1020.5;}).map(e=>e.tagName+' '+Math.round(e.getBoundingClientRect().left)+'-'+Math.round(e.getBoundingClientRect().right));
 document.body.dataset.bad=JSON.stringify(bad.slice(0,6));document.body.dataset.ready=1;})();
</script>
</body></html>
'''.replace('PRE', build.esc(pre)).replace('BIG', build.esc(big)).replace('REST', build.esc(rest)).replace('RACES', build.esc(races)).replace('CHART', chart)
assert chr(0x2014) not in html
open(os.path.join(here, 'card.html'), 'w').write(html); print('card.html written')
