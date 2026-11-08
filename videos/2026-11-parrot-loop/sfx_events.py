"""Línea de tiempo de efectos del video Parrot USB. S = {id_escena: segundo de inicio}; T = Track (ver engine/audio/sfxlib.py)."""
from sfxlib import *


def build(T, S, lib=None):
    # transitions
    for k,v in S.items():
        if k!='s1': T.put(v-0.12,whoosh(0.4),0.55)
    # s1 hook: fly-in, settle, scan
    T.put(0.0,boom(),0.9); T.put(0.0,whoosh(0.9,True),0.5); T.put(0.95,thunk(),0.8); T.put(0.05,pop(1100),0.4)
    for k in range(9): T.put(1.05+k*(2/14),tick(),0.35)
    T.put(2.3,ding(1760,0.4),0.35)
    for t in (0.55,1.9,2.9): T.put(t,glitch(),0.45)
    T.put(2.3,pop(1300),0.45)
    # s2 why
    t=S['s2']
    T.put(t+0.25,pop(800),0.4)
    T.put(t+1.4,powerdown(),0.7)
    for i in range(4): T.put(t+1.5+i*0.08,glitch(0.06),0.3)
    T.put(t+1.9,buzz(),0.5)
    T.put(t+3.4,powerup(),0.55)
    for i in range(4): T.put(t+3.55+i*0.08,ding(1318.5+i*220,0.35),0.35)
    T.put(t+3.9,chime(),0.7)
    # s3 needs
    t=S['s3']
    for lt,dl in ((0.35,0),(0.85,0),(1.35,0)): T.put(t+lt,whoosh(0.25),0.25)
    for lt in (1.0,1.5,2.0): T.put(t+lt,pop(1200),0.5); T.put(t+lt+0.02,ding(1760,0.3),0.25)
    T.put(t+3.0,alert(),0.6)
    # s4 deps
    t=S['s4']
    T.put(t+0.15,whoosh(0.3),0.25)
    T.typing(t+0.55,15); T.enter(t+1.1); T.line(t+1.25)
    T.typing(t+1.55,38); T.enter(t+2.85)
    for lt in (3.25,3.45,3.65): T.line(t+lt)
    T.put(t+3.9,tick(),0.3); T.put(t+2.2,pop(1000),0.35)
    # s5 clone
    t=S['s5']
    T.typing(t+0.5,47); T.enter(t+2.1)
    for lt in (2.5,2.8): T.line(t+lt)
    T.put(t+1.6,pop(1000),0.35)
    # s6 extract
    t=S['s6']
    T.typing(t+0.5,10); T.enter(t+0.85); T.typing(t+1.1,22); T.enter(t+1.85); T.typing(t+2.15,12); T.enter(t+2.55); T.line(t+2.7)
    T.put(t+3.0,ding(1568,0.5),0.5); T.put(t+3.0,sparkle(5),0.35)
    # s7 install
    t=S['s7']
    T.typing(t+0.5,10); T.enter(t+0.85); T.typing(t+1.2,21); T.enter(t+1.95); T.line(t+2.25)
    T.put(t+2.5,alert(),0.6)
    # s8 menu
    t=S['s8']
    T.typing(t+0.45,3,g=0.6); T.enter(t+0.6); T.line(t+0.85)
    for a,b in ((0.9,2.9),(2.9,5.2),(5.2,7.6)):
        ch=a+(b-a)*0.72
        T.put(t+a+0.05,whoosh(0.2),0.15)
        n={0.9:1,2.9:3,5.2:2}[a]
        for k in range(1,n): T.put(t+a+0.25+(ch-a-0.25-0.2)*k/n*0.9,tick(),0.5)
        T.put(t+ch,pop(1400),0.55); T.put(t+ch,thunk(),0.5); T.put(t+ch+0.05,ding(1760,0.35),0.3)
    # s9 iso / usb / go
    t=S['s9']
    for lt in (0.3,1.5,3.4): T.put(t+lt,whoosh(0.28),0.3)
    for lt in (1.2,3.1): T.put(t+lt,pop(1200),0.5); T.put(t+lt,ding(1568,0.4),0.35)
    T.put(t+1.9,alert(),0.45); T.put(t+2.5,alert(),0.35)
    T.put(t+4.2,thunk(),1.0); T.put(t+4.2,pop(700),0.5)
    T.put(t+4.4,riser(2.55),0.5)
    T.put(t+7.0,chime(),0.9); T.put(t+7.0,sparkle(8),0.45)
    # s10 plug-in, boot keys, data flow
    t=S['s10']
    T.put(t+0.2,whoosh(0.9,True),0.4)
    T.put(t+1.1,thunk(),1.1); T.put(t+1.1,pop(500),0.6); T.put(t+1.14,ding(2093,0.25),0.35)
    T.put(t+1.3,pop(1200),0.6); T.put(t+1.3,tick(),0.6); T.put(t+1.45,ding(1568,0.3),0.3); T.put(t+2.2,tick(),0.55); T.put(t+2.8,thunk(),0.7); T.put(t+2.8,pop(900),0.35)
    for i in range(14): T.put(t+2.9+i*0.1+0.55,tick(),0.35); T.put(t+2.9+i*0.1,pop(1400+i*40),0.15)
    T.put(t+2.9,powerup(),0.5)
    T.put(t+3.2,chime(),0.9)
    # cierre circular: vuelo de regreso al cuadro 0 (whoosh en el pico del movimiento)
    t=S['s10']+5.0-0.7
    T.put(t,whoosh(0.7,False),0.55); T.put(t+0.3,thunk(),0.25)
