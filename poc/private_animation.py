#!/usr/bin/env python3
"""Private pension animation POC. Run on VPS; output is standalone HTML."""
import argparse, base64, hashlib, json, pathlib, urllib.request, os, re
p=argparse.ArgumentParser()
p.add_argument("--percentage",type=int,default=40)
p.add_argument("--months",type=int,default=3)
a=p.parse_args()
if not 0 <= a.percentage <= 100 or not 1 <= a.months <= 24: p.error("Invalid parameters")
lines=[
"Je ontvangt salaris van je werkgever.",
"Daarmee draag je bij aan het inkomen van jullie samen.",
"Maar als jij overlijdt, valt jouw salaris weg.",
"Via je pensioenfonds is er een partnerpensioen verzekerd.",
f"Je partner ontvangt dan {a.percentage} procent van je pensioengevend salaris.",
"Dat pensioen ontvangt je partner zolang die leeft.",
"Zo wordt een deel van het inkomensverlies opgevangen.",
"Maar wat gebeurt er als je uit dienst gaat?",
"Je ontvangt geen salaris meer van deze werkgever.",
f"Je partnerpensioen blijft nog {a.months} maanden verzekerd.",
"Daarna stopt deze tijdelijke dekking.",
"Gelukkig zijn er mogelijkheden om partnerpensioen verzekerd te houden."
]
os.umask(0o077)
folder=pathlib.Path.home()/ "pensioen-poc"
folder.mkdir(exist_ok=True)
voice="pNInz6obpgDQGcFmaJgB"
model="eleven_multilingual_v2"
text=" ".join(lines)
payload=json.dumps({"text":text,"model_id":model},ensure_ascii=False).encode()
cache=folder/(hashlib.sha256(voice.encode()+payload).hexdigest()+".json")
if cache.exists(): result=json.loads(cache.read_text())
else:
    key=(pathlib.Path.home()/".elevenlabs-key").read_text().strip()
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps",data=payload,headers={"xi-api-key":key,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=90) as res: result=json.load(res)
    cache.write_text(json.dumps(result))
alignment=result["alignment"]
chars=alignment["characters"]
if "".join(chars)!=text: raise RuntimeError("Alignment differs from original text")
starts=[]; ends=[]; pos=0
for line in lines:
    starts.append(alignment["character_start_times_seconds"][pos])
    ends.append(alignment["character_end_times_seconds"][pos+len(line)-1])
    pos+=len(line)+1
html=r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Partnerpensioen – privé POC</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f4ef;color:#273b3b;font:16px system-ui,sans-serif}main{max-width:940px;margin:30px auto;padding:20px}h1{font-size:clamp(24px,4vw,36px);margin:0 0 8px}p{color:#586869}svg{width:100%;background:#fcfbf8;border-radius:24px;border:1px solid #deded5}audio{width:100%;margin:16px 0}#caption{font-size:clamp(18px,3vw,25px);min-height:75px;text-align:center;line-height:1.45}small{color:#687674}svg text{font-family:system-ui,sans-serif}</style>
<main><small>PENSIOEN ONTDEKT · PRIVÉ PROTOTYPE</small><h1>Partnerpensioen</h1><p>Fictieve regeling · __PCT__% van pensioengevend salaris · __MONTHS__ maanden tijdelijke dekking</p>
<svg viewBox="0 0 800 450" role="img" aria-label="Animatie partnerpensioen">
<defs>
<g id="person"><path d="M-22 61 L-18 147 H-2 L4 86 L10 147 H26 L27 61" fill="#d4bc96"/><path d="M-18 145 h18 v11 h-27 q-4-8 9-11 M10 145 h16 q12 0 13 11 H10" fill="#fff" stroke="#aab4ad"/><path d="M-29 3 Q-42 4 -44 37 L-40 65 Q-34 72 -29 64 L-24 28 M29 3 Q42 4 44 37 L40 65 Q34 72 29 64 L24 28" fill="currentColor"/><path d="M-28 1 Q0-10 28 1 L29 73 H-29Z" fill="currentColor"/><path d="M-9 -1 H9 V59 H-9Z" fill="#fffdf7"/><rect x="-10" y="-17" width="20" height="22" rx="6" fill="#d8a47e"/><ellipse cy="-42" rx="28" ry="32" fill="#e6b38d"/><g fill="#3d3028"><circle cx="-10" cy="-43" r="2.8"/><circle cx="10" cy="-43" r="2.8"/></g></g>
</defs>
<rect x="25" y="355" width="750" height="2" fill="#deded5"/>
<g id="employer" transform="translate(45 155)"><rect width="140" height="175" rx="7" fill="#7995a6"/><rect x="12" y="12" width="116" height="17" rx="4" fill="#b9cbd1"/><g fill="#e8f1ef"><rect x="18" y="45" width="23" height="24" rx="3"/><rect x="58" y="45" width="23" height="24" rx="3"/><rect x="98" y="45" width="23" height="24" rx="3"/><rect x="18" y="83" width="23" height="24" rx="3"/><rect x="58" y="83" width="23" height="24" rx="3"/><rect x="98" y="83" width="23" height="24" rx="3"/></g><rect x="53" y="132" width="34" height="43" rx="3" fill="#405c69"/><text x="70" y="195" text-anchor="middle" font-size="16" fill="#43575b">Werkgever</text></g>
<g id="fund" transform="translate(37 171)" opacity="0"><path d="M0 38 L78 0 L156 38Z" fill="#39776d"/><rect x="8" y="43" width="140" height="10" rx="3" fill="#39776d"/><g fill="#8ab0a2"><rect x="17" y="55" width="23" height="87" rx="3"/><rect x="66" y="55" width="23" height="87" rx="3"/><rect x="115" y="55" width="23" height="87" rx="3"/></g><rect y="144" width="156" height="15" rx="3" fill="#39776d"/><text x="78" y="179" text-anchor="middle" font-size="16" fill="#345f56">Pensioenfonds</text></g>
<path d="M193 235 Q278 141 365 250" fill="none" stroke="#a8b8ac" stroke-dasharray="4 8" id="flowpath"/>
<g id="coins"></g>
<g transform="translate(403 267)"><path d="M-28 -36 L-17 -7 Q-66 14 -51 50 Q-44 70 0 70 Q44 70 51 50 Q66 14 17 -7 L28 -36Z" fill="#91b6a3"/><path d="M-19 -9 H19" stroke="#39776d" stroke-width="7" stroke-linecap="round"/><text y="43" text-anchor="middle" font-size="40" font-weight="700" fill="#fff">€</text><text y="104" text-anchor="middle" font-size="16" fill="#43575b">Gezinsinkomen</text></g>
<g id="participant" transform="translate(581 183)" color="#415f78"><use href="#person"/><path d="M-28 -48 Q-40 -72 -12 -78 Q8 -92 27 -66 L27 -46 Q14 -65 -3 -58 Q-17 -54 -28 -48Z" fill="#514035"/><path d="M-19 -32 Q0-14 19-32 L15 -19 Q0-9 -15-19Z" fill="#72503c" opacity=".7"/><path id="smileA" d="M-7 -30 Q0 -24 7 -30" stroke="#652e29" fill="none" stroke-width="2" stroke-linecap="round"/></g>
<g id="partner" transform="translate(700 183)" color="#759986"><use href="#person"/><path d="M-27 -47 Q-38 -74 -7 -79 Q22 -88 31 -58 L29 -43 Q18 -54 9 -65 Q-6 -47 -27 -47Z" fill="#694a38"/><circle cx="15" cy="-82" r="15" fill="#694a38"/><circle cx="-24" cy="-29" r="4" fill="none" stroke="#c59a57" stroke-width="2"/><circle cx="24" cy="-29" r="4" fill="none" stroke="#c59a57" stroke-width="2"/><path id="smileB" d="M-7 -30 Q0 -24 7 -30" stroke="#652e29" fill="none" stroke-width="2" stroke-linecap="round"/></g>
<g id="percent" opacity="0"><rect x="240" y="42" width="205" height="77" rx="15" fill="#e4eee7"/><text x="342" y="82" text-anchor="middle" font-size="32" font-weight="700" fill="#39776d">__PCT__%</text><text x="342" y="104" text-anchor="middle" font-size="14" fill="#39776d">pensioengevend salaris</text></g>
<g id="coverage" opacity="0"><rect x="223" y="30" width="295" height="87" rx="15" fill="#e4eee7"/><text x="370" y="58" text-anchor="middle" font-size="17" fill="#345f56">__MONTHS__ maanden verzekerd</text><rect x="247" y="76" width="247" height="12" rx="6" fill="#c8d8cc"/><rect id="bar" x="247" y="76" width="247" height="12" rx="6" fill="#39776d"/></g>
<g id="options" opacity="0"><rect x="223" y="30" width="330" height="87" rx="15" fill="#e4eee7"/><text x="388" y="64" text-anchor="middle" font-size="18" font-weight="600" fill="#345f56">Partnerpensioen behouden?</text><text x="388" y="88" text-anchor="middle" font-size="15" fill="#345f56">Er zijn mogelijkheden.</text></g>
</svg>
<audio id="audio" controls preload="metadata" src="data:audio/mpeg;base64,__AUDIO__"></audio><div id="caption" aria-live="off"></div><small>Audio: ElevenLabs. Illustraties en fictieve parameters voor technische demonstratie; geen pensioenadvies. Alleen privé testen.</small>
</main>
<script>
const lines=__LINES__, starts=__STARTS__, ends=__ENDS__, pct=__PCT__;
const el=id=>document.getElementById(id), audio=el('audio'), path=el('flowpath');
const coins=Array.from({length:7},()=>{const c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('r',9);c.setAttribute('fill','#d6aa55');c.setAttribute('stroke','#b7893d');el('coins').append(c);return c;});
const clamp=x=>Math.max(0,Math.min(1,x)), fade=(t,start)=>clamp((t-start)/1.2), op=(id,v)=>el(id).setAttribute('opacity',v);
function draw(){const t=audio.currentTime;let i=0;while(i+1<starts.length&&t>=starts[i+1])i++;
el('caption').textContent=lines[i];
const reset=starts[7], dead=starts[2], leave=starts[8], fund=starts[3];
let a=t<reset?1-fade(t,dead):1, e=t<reset?1-fade(t,dead):1-fade(t,leave);
let f=t<reset?fade(t,fund):fade(t,starts[9])*(1-fade(t,starts[10]));
op('participant',a);op('employer',e);op('fund',f);
el('smileB').setAttribute('d',t>=dead&&t<reset?'M-7 -28 H7':'M-7 -30 Q0 -24 7 -30');
let rate=t<dead?1:t>=starts[4]&&t<reset?pct/100:t>=reset&&t<leave?1:0;
op('flowpath',rate?0.65:0);
coins.forEach((c,j)=>{const q=path.getPointAtLength(((t*.52+j/7)%1)*path.getTotalLength());c.setAttribute('cx',q.x);c.setAttribute('cy',q.y);c.setAttribute('opacity',j<Math.round(7*rate)?1:0)});
op('percent',i>=4&&i<=6?fade(t,starts[4]):0);
op('coverage',i===9?fade(t,starts[9]):0);
el('bar').setAttribute('width',247*(1-clamp((t-starts[9])/(starts[10]-starts[9]))));
op('options',i===11?fade(t,starts[11]):0);
requestAnimationFrame(draw);
}draw();
</script></html>'''
for k,v in {"__PCT__":str(a.percentage),"__MONTHS__":str(a.months),"__AUDIO__":result["audio_base64"],"__LINES__":json.dumps(lines,ensure_ascii=False),"__STARTS__":json.dumps(starts),"__ENDS__":json.dumps(ends)}.items(): html=html.replace(k,v)
out=folder/"partnerpensioen.html"
out.write_text(html,encoding="utf-8")
print(f"Ready: {out}")
