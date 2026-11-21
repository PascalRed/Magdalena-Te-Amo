"""
TE AMO MAAAAS MAGDALENA ENTIENDELOOOOOO  (Siempre lo hare).

ODIO HTML, Pero amo pyyhon asi que lo pase bieeeen
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.animation import FuncAnimation

# ------------------------------------------------------------------ estilo
_instaladas = {f.name for f in font_manager.fontManager.ttflist}
_mono = ["JetBrains Mono", "Fira Code", "Fira Mono", "IBM Plex Mono", "Cascadia Mono",
         "Consolas", "Menlo", "SF Mono", "DejaVu Sans Mono", "Courier New"]
plt.rcParams["font.family"] = [f for f in _mono if f in _instaladas] or ["monospace"]

FONDO = "#000000"
TEXTO = "#d4d4d4"
APAGADO = "#6b6b6b"
VERDE = "#5af78e"      # color de terminal: funcion activa / linea de comandos
ROJO = "#ff5555"
REJILLA = "#262626"
EJE = "#8a8a8a"

N = 60  # puntos por trazo
X_MIN, X_MAX = -1, 18
Y_MIN, Y_MAX = -1, 3


# ------------------------------------------------------------ funciones base
def linea(x0, y0, x1, y1):
    """Recta de (x0,y0) a (x1,y1):  P(t) = P0 + t (P1 - P0),  t en [0,1]."""
    t = np.linspace(0, 1, N)
    return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t


def elipse(cx, cy, rx, ry, a0=0.0, a1=2 * np.pi):
    """Elipse:  (cx + rx cos a,  cy + ry sin a)."""
    a = np.linspace(a0, a1, N * 2)
    return cx + rx * np.cos(a), cy + ry * np.sin(a)


def corazon(cx=0.0, cy=0.0, s=0.076):
    """x = 16 sin^3 t ;  y = 13cos t - 5cos 2t - 2cos 3t - cos 4t."""
    t = np.linspace(0, 2 * np.pi, N * 3)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return cx + s * x, cy + s * (y + 17)


# ----------------------------------------------------------- plano cartesiano
def plano():
    """Devuelve las rectas del plano, todas generadas con linea()."""
    ejes = [linea(X_MIN, 0, X_MAX, 0),          # y = 0
            linea(0, Y_MIN, 0, Y_MAX)]          # x = 0
    cuadricula = [linea(k, Y_MIN, k, Y_MAX) for k in range(X_MIN, X_MAX + 1) if k != 0]
    cuadricula += [linea(X_MIN, k, X_MAX, k) for k in range(Y_MIN, Y_MAX + 1) if k != 0]
    return ejes, cuadricula


EJES, CUADRICULA = plano()
PLANO_TXT = [
    "fx  y = 0   # eje X",
    "fy  x = 0   # eje Y",
    "    x = k,  y = k   # cuadrícula, k ∈ Z",
]

# ------------------------------------------------------------------ trazos
# (xs, ys, color, ecuacion, dominio)
trazos = []


def add(curva, color, eq, dom):
    trazos.append((curva[0], curva[1], color, eq, dom))


# T
add(linea(0, 2, 2, 2), TEXTO, "y = 2", "0 ≤ x ≤ 2")
add(linea(1, 2, 1, 0), TEXTO, "x = 1", "0 ≤ y ≤ 2")
# E
add(linea(3, 2, 3, 0), TEXTO, "x = 3", "0 ≤ y ≤ 2")
add(linea(3, 2, 4.4, 2), TEXTO, "y = 2", "3 ≤ x ≤ 4.4")
add(linea(3, 1, 4.2, 1), TEXTO, "y = 1", "3 ≤ x ≤ 4.2")
add(linea(3, 0, 4.4, 0), TEXTO, "y = 0", "3 ≤ x ≤ 4.4")
# A
add(linea(5.6, 0, 6.6, 2), TEXTO, "y = 2·(x − 5.6)", "5.6 ≤ x ≤ 6.6")
add(linea(6.6, 2, 7.6, 0), TEXTO, "y = −2·(x − 7.6)", "6.6 ≤ x ≤ 7.6")
add(linea(6.0, 0.8, 7.2, 0.8), TEXTO, "y = 0.8", "6 ≤ x ≤ 7.2")
# M
add(linea(9.4, 0, 9.4, 2), TEXTO, "x = 9.4", "0 ≤ y ≤ 2")
add(linea(9.4, 2, 10.6, 0.6), TEXTO, "y = 2 − 7/6·(x − 9.4)", "9.4 ≤ x ≤ 10.6")
add(linea(10.6, 0.6, 11.8, 2), TEXTO, "y = 0.6 + 7/6·(x − 10.6)", "10.6 ≤ x ≤ 11.8")
add(linea(11.8, 2, 11.8, 0), TEXTO, "x = 11.8", "0 ≤ y ≤ 2")
# O
add(elipse(13.7, 1, 0.9, 1.0, np.pi / 2, np.pi / 2 + 2 * np.pi), TEXTO,
    "((x−13.7)/0.9)² + (y−1)² = 1", "")
# Corazon (parametrica, dos lineas)
add(corazon(16.2, 0), ROJO,
    "x = 16.2 + 1.22·sin³t", "t ∈ [0, 2π]")
CORAZON_Y = "y = 0.076(13cos t−5cos 2t−2cos 3t−cos 4t+17)"


def linea_txt(i):
    """Jeje, sigues bajando? TE AMO"""
    _, _, _, eq, dom = trazos[i]
    return f"f{i + 1:<3}{eq}" + (f"   # {dom}" if dom else "")


# ------------------------------------------------------------------ figura
fig = plt.figure(figsize=(12, 7.4), dpi=100, facecolor=FONDO)
gs = fig.add_gridspec(2, 1, height_ratios=[2.5, 2], hspace=0.08,
                      left=0.025, right=0.975, top=0.915, bottom=0.02)
ax = fig.add_subplot(gs[0])
panel = fig.add_subplot(gs[1])

ax.set_xlim(X_MIN - 0.3, X_MAX + 0.5)
ax.set_ylim(Y_MIN - 0.3, Y_MAX + 0.3)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")
panel.set_xlim(0, 3)
panel.set_ylim(0, 1)
panel.axis("off")

titulo = fig.text(0.025, 0.955, "", ha="left", va="center", fontsize=14, color=VERDE)

# --- plano
l_cuadricula = [ax.plot(*c, color=REJILLA, lw=0.8, zorder=0, visible=False)[0] for c in CUADRICULA]
l_ejes = [ax.plot([], [], color=EJE, lw=1.4, zorder=1)[0] for _ in EJES]
marcas = []
for k in range(X_MIN, X_MAX + 1):
    if k != 0:
        marcas.append(ax.text(k, -0.12, str(k), ha="center", va="top", fontsize=7.5,
                              color=APAGADO, visible=False))
for k in range(Y_MIN, Y_MAX + 1):
    if k != 0:
        marcas.append(ax.text(-0.12, k, str(k), ha="right", va="center", fontsize=7.5,
                              color=APAGADO, visible=False))
marcas.append(ax.text(X_MAX + 0.2, -0.12, "x", fontsize=10, color=EJE, visible=False))
marcas.append(ax.text(0.12, Y_MAX + 0.08, "y", fontsize=10, color=EJE, visible=False))

# --- trazos y etiquetas f1..f15 junto a cada uno
lineas = [ax.plot([], [], color=c, lw=3.2, solid_capstyle="projecting",
                  solid_joinstyle="miter", zorder=3)[0] for _, _, c, _, _ in trazos]
lapiz, = ax.plot([], [], "s", color=VERDE, ms=6, zorder=6)
ETIQUETA_POS = {11: (11.4, 1.0),    # f12: diagonal de la M
                13: (13.7, 1.0),    # f14: centro de la O
                14: (17.3, 0.35)}   # f15: a la derecha del corazon
etiquetas = []
for i, (x, y, *_r) in enumerate(trazos):
    m = len(x) // 2
    px, py = ETIQUETA_POS.get(i, (x[m] + 0.12, y[m] + 0.1))
    etiquetas.append(ax.text(px, py, f"f{i + 1}", fontsize=8, color=VERDE, zorder=7,
                             visible=False, ha="center" if i in ETIQUETA_POS else "left"))

# relleno del corazon (aparece al final)
relleno = ax.fill(trazos[-1][0], trazos[-1][1], color=ROJO, alpha=0, lw=0, zorder=2)[0]

# --- panel: 3 columnas x 7 filas (el corazon usa dos filas)
FILAS = 7
slots = list(range(3 + len(trazos) + 1))   # 3 de plano + trazos + 1 fila extra del corazon


def pos(n):
    col, fila = divmod(n, FILAS)
    return 0.02 + col * 1.0, 0.94 - fila * 0.145


plano_filas = [panel.text(*pos(n), t, fontsize=8.5, va="center", color=APAGADO,
                          visible=False) for n, t in enumerate(PLANO_TXT)]
filas = [panel.text(*pos(3 + i), linea_txt(i), fontsize=8.5, va="center",
                    color=TEXTO if i < len(trazos) - 1 else ROJO, visible=False)
         for i in range(len(trazos))]
fila_y_corazon = panel.text(*pos(3 + len(trazos)), "    " + CORAZON_Y, fontsize=8.5,
                            va="center", color=ROJO, visible=False)

# --- tiempos
F_PLANO = 30
F_TRAZO = 14
F_TOTAL = F_PLANO + len(trazos) * F_TRAZO
F_FINAL = 45


def cursor(frame):
    return "█" if (frame // 8) % 2 == 0 else " "


def update(frame):
    # ---- fase 1: se construye el plano
    if frame < F_PLANO:
        p = (frame + 1) / F_PLANO
        for l, (x, y) in zip(l_ejes, EJES):
            n = max(2, int(len(x) * min(1, p * 1.6)))
            l.set_data(x[:n], y[:n])
        for l in l_cuadricula:
            l.set_visible(p > 0.4)
        for t in plano_filas:
            t.set_visible(True)
        if p > 0.8:
            for t in marcas:
                t.set_visible(True)
        titulo.set_text("$ plot plano   # y = 0,  x = 0,  x = k,  y = k  " + cursor(frame))
        return []

    # ---- fase 2: se dibujan los trazos
    if frame < F_TOTAL:
        i, k = divmod(frame - F_PLANO, F_TRAZO)
        for j in range(i):
            lineas[j].set_data(trazos[j][0], trazos[j][1])
            filas[j].set_visible(True)
            filas[j].set_color(ROJO if j == len(trazos) - 1 else TEXTO)
            etiquetas[j].set_visible(True)
        n = max(2, int(len(trazos[i][0]) * (k + 1) / F_TRAZO))
        lineas[i].set_data(trazos[i][0][:n], trazos[i][1][:n])
        lapiz.set_data([trazos[i][0][n - 1]], [trazos[i][1][n - 1]])
        filas[i].set_visible(True)
        filas[i].set_color(VERDE)
        etiquetas[i].set_visible(True)
        if i == len(trazos) - 1:
            fila_y_corazon.set_visible(True)
            fila_y_corazon.set_color(VERDE)
        titulo.set_text(f"$ plot f{i + 1}   # {trazos[i][3]}  {trazos[i][4]}  " + cursor(frame))
        return []

    # ---- fase 3: el corazon se rellena
    for j in range(len(trazos)):
        lineas[j].set_data(trazos[j][0], trazos[j][1])
        filas[j].set_visible(True)
        filas[j].set_color(ROJO if j == len(trazos) - 1 else TEXTO)
        etiquetas[j].set_visible(True)
    fila_y_corazon.set_visible(True)
    fila_y_corazon.set_color(ROJO)
    lapiz.set_data([], [])
    relleno.set_alpha(min(0.9, 0.9 * (frame - F_TOTAL) / 14))
    titulo.set_text('$ echo "TE AMO"  ' + cursor(frame))
    return []


anim = FuncAnimation(fig, update, frames=F_TOTAL + F_FINAL, interval=40,
                     repeat=False, blit=False)


def guardar_gif(nombre="te_amo.gif", fps=25):
    """Guarda el GIF fotograma a fotograma (paleta reducida: poca memoria)."""
    from PIL import Image
    cuadros = []
    for f in range(F_TOTAL + F_FINAL):
        update(f)
        fig.canvas.draw()
        img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB")
        cuadros.append(img.quantize(colors=32, dither=Image.Dither.NONE))
    cuadros[0].save(nombre, save_all=True, append_images=cuadros[1:],
                    duration=int(1000 / fps), loop=0, optimize=False)
    print("Guardado:", nombre)


if __name__ == "__main__":
    if "--save" in sys.argv:
        guardar_gif()
    else:
        plt.show()
