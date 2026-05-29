#!/usr/bin/env python3
"""
Simple, clean CS2 Dust II map (96x72).
Focus on gameplay: clear corridors, proper connectivity, fun combat.
"""
W, H = 96, 72
m = [[0]*W for _ in range(H)]

B=1;BLD=2;STR=3;WD=4;MTL=5

def fill(x1,y1,x2,y2,v=1):
    for y in range(max(0,y1),min(H,y2+1)):
        for x in range(max(0,x1),min(W,x2+1)): m[y][x]=v

def hline(x1,x2,y,v=1):
    for x in range(max(0,x1),min(W,x2+1)):
        if 0<=y<H: m[y][x]=v

def vline(x,y1,y2,v=1):
    for y in range(max(0,y1),min(H,y2+1)):
        if 0<=x<W: m[y][x]=v

def rect(x1,y1,x2,y2,v=1):
    hline(x1,x2,y1,v); hline(x1,x2,y2,v); vline(x1,y1,y2,v); vline(x2,y1,y2,v)

def room(x1,y1,x2,y2,v=STR,doors=None):
    rect(x1,y1,x2,y2,v)
    fill(x1+1,y1+1,x2-1,y2-1,0)
    if doors:
        for d in doors:
            if d=='n': hline(x1+2,x2-2,y1,0)
            elif d=='s': hline(x1+2,x2-2,y2,0)
            elif d=='e': vline(x2,y1+2,y2-2,0)
            elif d=='w': vline(x1,y1+2,y2-2,0)

# Border
for x in range(W): m[0][x]=B; m[H-1][x]=B
for y in range(H): m[y][0]=B; m[y][W-1]=B

# === T SPAWN (bottom-left) ===
room(4,52,20,66, BLD, ['n','e'])

# === CT SPAWN (bottom-right) ===
room(72,52,88,66, BLD, ['n','w'])

# === B SITE (top-left) ===
room(4,4,28,22, STR, ['s','e'])
fill(6,6,10,10, MTL)   # platform
fill(6,7,9,9, 0)        # platform top
fill(18,6,20,8, WD)     # box
fill(22,14,24,16, WD)   # box near entrance

# === A SITE (top-right) ===
room(62,4,88,24, STR, ['s','w'])
fill(70,8,72,10, WD)    # box1
fill(70,6,74,8, WD)     # double box
fill(80,6,82,8, MTL)    # goose
fill(64,6,66,8, MTL)    # ramp
fill(76,14,77,16, MTL)  # wall

# === LONG A (right side corridor: x:56-60, y:8-56) ===
vline(54,8,56,STR); vline(55,8,56,STR)
vline(61,8,56,STR); vline(62,8,56,STR)
for y in range(9,56):
    for x in range(56,61): m[y][x]=0
# Long A doors at y=34
hline(54,55,34,MTL); hline(61,62,34,MTL)
# Blue box
fill(57,32,59,33, WD)
# Pit
rect(62,12,66,16, WD); fill(63,13,65,15,0); vline(62,13,15,0)
# Cover
fill(57,46,58,47, WD)

# === MID (center: x:36-42, y:28-56) ===
vline(34,28,56,STR); vline(35,28,56,STR)
vline(43,28,56,STR); vline(44,28,56,STR)
for y in range(29,56):
    for x in range(36,43): m[y][x]=0
# Mid doors at y=42
hline(34,35,42,MTL); hline(43,44,42,MTL)
# Mid box
fill(38,48,40,49, WD)
# Openings
vline(34,46,50,0)  # left
vline(44,46,50,0)  # right
hline(36,42,56,0)  # bottom
hline(36,42,28,0)  # top

# === SHORT A (y:16-20, x:28-56) ===
hline(26,56,14,STR); hline(26,56,20,STR)
for y in range(15,20):
    for x in range(27,56): m[y][x]=0
hline(26,28,14,0); hline(26,28,20,0)  # west open
vline(56,16,18,0)  # east open to A

# === SHORT A STAIRS (x:32-38, y:20-28) ===
vline(30,20,28,STR); vline(31,20,28,STR)
vline(39,20,28,STR); vline(40,20,28,STR)
for y in range(21,28):
    for x in range(32,39): m[y][x]=0
vline(34,14,20,0)  # top to catwalk
hline(39,40,26,0)  # bottom from mid

# === CT MID (x:46-52, y:28-56) ===
vline(45,28,56,STR); vline(46,28,56,STR)
vline(53,28,56,STR); vline(54,28,56,STR)
for y in range(29,56):
    for x in range(47,53): m[y][x]=0
hline(45,46,42,MTL); hline(53,54,42,MTL)  # doors
hline(47,52,56,0)  # bottom
hline(47,52,28,0)  # top

# === B TUNNELS (left side: x:12-18, y:22-56) ===
vline(10,22,56,STR); vline(11,22,56,STR)
vline(19,22,56,STR); vline(20,22,56,STR)
for y in range(23,56):
    for x in range(12,19): m[y][x]=0
# Tunnel cover
fill(14,36,15,37, WD)
# Bottom opening
hline(12,18,56,0)

# Tunnel to B connector (y:22-26, x:18-28)
hline(18,28,21,STR); hline(18,28,27,STR)
for x in range(18,28): m[22][x]=0; m[23][x]=0; m[24][x]=0; m[25][x]=0; m[26][x]=0
# B door
vline(28,22,26,0)

# === B-MID CONNECTOR (x:30-34, y:28-46) ===
vline(29,28,46,STR); vline(30,28,46,STR)
vline(34,28,46,STR); vline(35,28,46,STR)
for y in range(29,46):
    for x in range(31,34): m[y][x]=0
hline(31,33,46,0)  # bottom to mid
hline(31,33,28,0)  # top

# Tunnel to B-mid horizontal
hline(20,29,38,STR); hline(20,29,42,STR)
for x in range(20,29): m[39][x]=0; m[40][x]=0; m[41][x]=0

# === CONNECTORS ===
# T spawn exit corridor east to Long A area (y:58-62, x:20-54)
hline(20,54,57,STR); hline(20,54,63,STR)
for x in range(20,55): m[58][x]=0; m[59][x]=0; m[60][x]=0; m[61][x]=0; m[62][x]=0
vline(54,57,63,STR)  # connects to Long A area
# Cover in corridor
fill(30,59,31,60, WD)
fill(42,59,43,60, WD)

# T spawn exit corridor north to B tunnels (x:14-20, y:38-52)
hline(13,20,38,STR); hline(13,20,52,STR)
for x in range(14,20): m[39][x]=0; m[40][x]=0; m[41][x]=0; m[42][x]=0; m[43][x]=0; m[44][x]=0; m[45][x]=0; m[46][x]=0; m[47][x]=0; m[48][x]=0; m[49][x]=0; m[50][x]=0; m[51][x]=0

# CT spawn exit corridor west (y:58-62, x:54-72)
hline(54,72,57,STR); hline(54,72,63,STR)
for x in range(54,73): m[58][x]=0; m[59][x]=0; m[60][x]=0; m[61][x]=0; m[62][x]=0

# Open the corridor-T spawn connections
hline(20,20,58,0); hline(20,20,59,0); hline(20,20,60,0); hline(20,20,61,0); hline(20,20,62,0)
vline(72,58,62,0)

# Cover boxes in outside area
fill(30,46,31,47, WD)
fill(44,46,45,47, WD)
fill(50,50,51,51, WD)

# === RE-OPEN critical paths ===
hline(4,20,56,0)   # T spawn south
hline(72,88,56,0)  # CT spawn south
vline(20,56,66,0)  # T east exit (re-open after corridor walls)
vline(72,56,66,0)  # CT west exit

def verify():
    from collections import deque
    def bfs(sx,sy):
        vis=set(); q=deque([(sx,sy)]); vis.add((sx,sy))
        while q:
            x,y=q.popleft()
            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx,ny=x+dx,y+dy
                if 0<=nx<W and 0<=ny<H and (nx,ny) not in vis and m[ny][nx]==0:
                    vis.add((nx,ny)); q.append((nx,ny))
        return vis
    vis=bfs(12,60)
    targets=[('B site',16,12),('A site',76,12),('Mid',39,42),('CT spawn',80,60),
             ('Long A',58,34),('Short A',42,17),('B tunnels',15,40),('B-mid',32,38)]
    for name,x,y in targets:
        ok=(x,y) in vis; tile=m[y][x]
        print(f'T-> {name} ({x},{y}): {"OK" if ok else "BLOCKED"} tile={tile}')

def show():
    for y in range(H):
        line=''
        for x in range(W):
            v=m[y][x]
            if v==0: line+=' '
            elif v==1: line+='#'
            elif v==2: line+='B'
            elif v==3: line+='|'
            elif v==4: line+='='
            elif v==5: line+='+'
        print(line)

if __name__=="__main__":
    import sys
    if '--verify' in sys.argv: verify()
    elif '--js' in sys.argv:
        for y,row in enumerate(m):
            print('   ['+','.join(str(v) for v in row)+']'+(',' if y<H-1 else ''))
    else: show()
    oc=sum(1 for row in m for v in row if v==0)
    wc=sum(1 for row in m for v in row if v>0)
    sys.stderr.write(f"// {W}x{H} open={oc} wall={wc}\n")
