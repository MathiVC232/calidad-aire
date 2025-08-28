import streamlit as st
import numpy as np
from PIL import Image, ImageDraw

st.set_page_config(page_title="Purificador Hero", layout="centered")

# ---------- Variables ----------
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'pollution' not in st.session_state: st.session_state.pollution = 0
if 'monsters' not in st.session_state: st.session_state.monsters = []
if 'player_pos' not in st.session_state: st.session_state.player_pos = [200, 400]
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'player_type' not in st.session_state: st.session_state.player_type = None
if 'boss' not in st.session_state: st.session_state.boss = None

# ---------- Personajes ----------
characters = {
    "Básico": {"color": (50,150,255), "speed": 20, "range": 30},
    "Rápido": {"color": (50,255,50), "speed": 30, "range": 30},
    "Potente": {"color": (255,200,50), "speed": 20, "range": 50},
    "Maestro": {"color": (255,50,255), "speed": 30, "range": 50}
}

# ---------- Funciones ----------
def spawn_monsters(level):
    count = 5 + level
    monsters = [(np.random.randint(50,350), np.random.randint(50,350)) for _ in range(count)]
    return monsters

def spawn_boss(level):
    # Boss más grande, distinto color
    color = [(150,0,0),(200,0,0),(255,0,0),(255,100,0),(255,150,0)][level-1]
    pos = [200,100]
    return {"pos": pos, "size": 50+10*level, "color": color, "hp": 3+level}

def draw_game():
    img = Image.new("RGB", (400, 450), color=(180,230,255))
    draw = ImageDraw.Draw(img)
    # Monstruos normales
    for mx,my in st.session_state.monsters:
        draw.ellipse((mx-15,my-15,mx+15,my+15), fill=(255,0,0))
    # Boss
    if st.session_state.boss:
        bx,by = st.session_state.boss["pos"]
        s = st.session_state.boss["size"]
        draw.rectangle((bx-s,by-s,bx+s,by+s), fill=st.session_state.boss["color"])
        draw.text((bx-15,by-10), f'HP:{st.session_state.boss["hp"]}', fill=(255,255,255))
    # Jugador
    px, py = st.session_state.player_pos
    color = characters[st.session_state.player_type]["color"]
    r = 20
    draw.rectangle((px-r,py-r,px+r,py+r), fill=color)
    # Barra de contaminación
    draw.rectangle((10,10,310,30), outline=(0,0,0))
    fill = int((st.session_state.pollution/100)*300)
    draw.rectangle((10,10,10+fill,30), fill=(255,50,50))
    return img

def move_player(dx,dy):
    if st.session_state.game_over: return
    px,py = st.session_state.player_pos
    px = min(380,max(20, px+dx))
    py = min(430,max(20, py+dy))
    st.session_state.player_pos = [px, py]

def catch_monsters():
    if st.session_state.game_over: return
    px,py = st.session_state.player_pos
    rng = characters[st.session_state.player_type]["range"]
    caught = []
    for i,(mx,my) in enumerate(st.session_state.monsters):
        if abs(mx-px)<rng and abs(my-py)<rng:
            caught.append(i)
            st.session_state.score += 1
            st.session_state.pollution = max(0, st.session_state.pollution-5)
    for i in reversed(caught):
        st.session_state.monsters.pop(i)
    # Boss
    if st.session_state.boss:
        bx,by = st.session_state.boss["pos"]
        size = st.session_state.boss["size"]
        if abs(bx-px)<rng+size and abs(by-py)<rng+size:
            st.session_state.boss["hp"] -=1
            if st.session_state.boss["hp"]<=0:
                st.session_state.boss = None
                st.session_state.level += 1
                next_level()

def next_level():
    if st.session_state.level>5:
        st.session_state.game_over = True
        return
    st.session_state.monsters = spawn_monsters(st.session_state.level)
    if st.session_state.level==5:
        st.session_state.boss = spawn_boss(5)
    else:
        st.session_state.boss = spawn_boss(st.session_state.level)

def increase_pollution():
    if st.session_state.game_over: return
    st.session_state.pollution += 2 + st.session_state.level
    if st.session_state.pollution >= 100:
        st.session_state.game_over = True

# ---------- INTERFAZ ----------
st.title("Purificador Hero - Streamlit")

if not st.session_state.player_type:
    st.subheader("Elige tu personaje:")
    for char in characters:
        if st.button(char):
            st.session_state.player_type = char
            next_level()
else:
    if st.session_state.game_over:
        st.subheader("¡Fin del juego!")
        st.write(f"Puntaje: {st.session_state.score}")
        if st.session_state.level>5:
            st.write("🎉 ¡Ganaste todos los niveles!")
        else:
            st.write("😢 Aula contaminada")
        if st.button("Reiniciar"):
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.pollution = 0
            st.session_state.monsters = []
            st.session_state.player_pos = [200,400]
            st.session_state.game_over = False
            st.session_state.player_type = None
            st.session_state.boss = None
    else:
        st.write(f"Nivel: {st.session_state.level} | Puntaje: {st.session_state.score} | Contaminación: {st.session_state.pollution:.1f}%")
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            if st.button("⬅️"): move_player(-characters[st.session_state.player_type]["speed"],0)
        with col2:
            if st.button("⬆️"): move_player(0,-characters[st.session_state.player_type]["speed"])
        with col3:
            if st.button("➡️"): move_player(characters[st.session_state.player_type]["speed"],0)
        if st.button("⬇️"): move_player(0,characters[st.session_state.player_type]["speed"])
        if st.button("💨 Aspirar"): catch_monsters()
        increase_pollution()
        img = draw_game()
        st.image(img)
