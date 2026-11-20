# Build index.html (English, default) and zh/index.html (Chinese) from shared parts
import sys,os
D=sys.argv[1] if len(sys.argv)>1 else 'src'
head=open(f'{D}/head.html',encoding='utf-8').read(); script=open(f'{D}/script.html',encoding='utf-8').read()
zh_main=open(f'{D}/main.html',encoding='utf-8').read(); en_main=open(f'{D}/main_en.html',encoding='utf-8').read()
BASE='https://iehrhei.github.io/relief/'
CSS='''.controls a.lang{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;background:rgba(236,231,221,.75);color:var(--muted);border:1px solid var(--faint);padding:.45rem .8rem;border-radius:999px;text-decoration:none;line-height:1.2}
.controls a.lang:hover{color:var(--ink)}
@media (max-width:900px){.controls a.lang{padding:.35rem .65rem;font-size:.62rem}}
html[lang="en"]{--display:"Cormorant Garamond","Iowan Old Style",Georgia,serif}
html[lang="en"] body{font-size:17.5px;line-height:1.85;hyphens:auto;-webkit-hyphens:auto}
html[lang="en"] h1{font-weight:300;letter-spacing:.01em;font-size:clamp(3rem,7.5vw,5.4rem)}
html[lang="en"] h1 .sub{font-style:italic;letter-spacing:.02em;font-size:.4em;margin-top:.6rem}
html[lang="en"] h2{font-weight:400;letter-spacing:.01em;font-size:1.7rem}
html[lang="en"] .glyph{font-family:"Noto Serif SC",serif}
html[lang="en"] .dek{font-size:1.08rem;line-height:1.85}
html[lang="en"] .howto{letter-spacing:0}
html[lang="en"] p.solo{letter-spacing:0;font-size:1.12rem}
</style>'''
def page(lang):
    h=head.replace('</style>',CSS,1)
    if lang=='en':
        rep=[('<html lang="zh-CN">','<html lang="en">'),
             ('<title>浮雕：谁在雕刻这颗星球</title>','<title>Relief: Who Carves the Earth</title>'),
             ('<meta name="description" content="地质、生命与人类，三位雕塑家如何塑造了地球的浮雕。读到哪里，一条真实的大西洋中脊就在纸上显现到哪里。">','<meta name="description" content="Rock, water and life: how three sculptors carved the relief of the Earth. As you read, a real strip of the Mid-Atlantic Ridge comes up on the paper like a rubbing.">'),
             ('<meta property="og:title" content="浮雕：谁在雕刻这颗星球">','<meta property="og:title" content="Relief: Who Carves the Earth">'),
             ('<meta property="og:description" content="地质、生命与人类，三位雕塑家如何塑造了地球的浮雕。读到哪里，一条真实的大西洋中脊就在纸上显现到哪里。">','<meta property="og:description" content="Rock, water and life: how three sculptors carved the relief of the Earth. As you read, a real strip of the Mid-Atlantic Ridge comes up on the paper like a rubbing.">'),
             ('<meta property="og:url" content="https://iehrhei.github.io/relief/">',f'<meta property="og:url" content="{BASE}">\n<link rel="alternate" hreflang="en" href="{BASE}">\n<link rel="alternate" hreflang="zh-CN" href="{BASE}zh/">'),
             ('正在铺开海底 · ETOPO 2022','Laying out the seafloor · ETOPO 2022'),
             ('<button id="plain" type="button" aria-pressed="false">纯文字</button><button id="sound" type="button" aria-pressed="false">声音 · 关</button>',
              '<a class="lang" href="zh/index.html" hreflang="zh-CN" lang="zh-CN">中文</a><button id="plain" type="button" aria-pressed="false">Text only</button><button id="sound" type="button" aria-pressed="false">Sound · off</button>'),
             ('<span id="hudDepth">海面</span>','<span id="hudDepth">sea surface</span>'),
             ('声呐 <b id="hudPings">12</b> / 12<br>你已测绘这片海底的 <b id="hudPct">0.0%</b>','pings <b id="hudPings">12</b> / 12<br>seafloor mapped <b id="hudPct">0.0%</b>')]
        main=en_main
    else:
        rep=[('<meta charset="utf-8">','<meta charset="utf-8">\n<base href="../">'),
             ('<meta property="og:url" content="https://iehrhei.github.io/relief/">',f'<meta property="og:url" content="{BASE}zh/">\n<link rel="alternate" hreflang="en" href="{BASE}">\n<link rel="alternate" hreflang="zh-CN" href="{BASE}zh/">'),
             ('<button id="plain" type="button" aria-pressed="false">纯文字</button>','<a class="lang" href="index.html" hreflang="en" lang="en">EN</a><button id="plain" type="button" aria-pressed="false">纯文字</button>')]
        main=zh_main
    for a,b in rep:
        assert a in h,(lang,a[:50]); h=h.replace(a,b)
    return h+main+script
os.makedirs('zh',exist_ok=True)
open('index.html','w',encoding='utf-8').write(page('en'))
open('zh/index.html','w',encoding='utf-8').write(page('zh'))
print('ok')
