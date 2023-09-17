import tkinter as tk
import math

def calculate():
    ma = 9365.84
    gg = 1.266
    ga = 1
    Fi = 0.001
    Dp = 10
    Lh = 20

    T1a = float(T1a_entry.get())
    T1g = float(T1g_entry.get())
    T2a = float(T2a_entry.get())
    T2g = float(T2g_entry.get())
    Tg_prom = (T1g + T2g) / 2
    Ta_prom = (T1a + T2a) / 2

    M = M_var.get()

    if M == 1:
        dT2 = T1g - T2a
        dT1 = T2g - T1a
    else:
        dT2 = T1g - T1a
        dT1 = T2g - T2a

    DTML = (dT2 - dT1) / math.log(dT2 / dT1)

    # Glycerol properties
    kg = 0.1193  # Conductivity in Btu/hr-ft-F
    Cpg = 0.6379  # Specific heat capacity in Btu/lbm-F
    vg = 0.03776  # Viscosity in lbm/ft-s
    dg = 74.856  # Density in lbm/ft3


    # Water properties
    ka = 0.37102  # Conductivity in Btu/hr-ft-F
    Cpa = 1.0083  # Specific heat capacity in Btu/lbm-F
    va = 0.0004  # Viscosity in lbm/ft-s
    da = 61.7430  # Density in lbm/ft3

    # Energy balance
    Qa = ma * Cpa * (T2a - T1a)  # Heat flow received by water in Btu/h
    mg = (ma * Cpa * (T2a - T1a)) / (Cpg * (T1g - T2g))  # Mass flow rate of glycerin in lb/h


    N = N_var.get()

    if N == 1:
        # Tubo interno
        Dintt = 1.38 * (1 / 12)  # in ft
        Dextt = 1.66 * (1 / 12)  # in ft
        Det = 1.38 * (1 / 12)  # Equivalent diameter of the tube, in ft
        Aft = math.pi * (Det ** 2) / 4  # Flow area per tube, ft^2
        Gmg = (mg / Aft) * (1 / 3600)  # Mass flow rate of water through the tube. This value is multiplied by 1/3600 to convert mass flow rate from hours to seconds.

        # Anulo
        Dinta = 1.66 * (1 / 12)  # Internal diameter of the annulus, in ft
        Dexta = 2.067 * (1 / 12)  # External diameter of the annulus, in ft
        Dea = ((Dexta ** 2) - (Dinta ** 2)) / Dinta  # Equivalent diameter of the annulus
        Afa = math.pi * (((Dexta ** 2) - (Dinta ** 2)) / 4)  # Flow area per annulus, not to be confused with "a" for water, in ft^2
        Gma = (ma / Afa) * (1 / 3600)  # Mass flow rate of glycerin through the annulus. This value is multiplied by 1/3600 to convert mass flow rate from hours to seconds.

    elif N == 2:
        # Tubo interno
        Dintt = 1.38 * (1 / 12)  # in ft
        Dextt = 1.66 * (1 / 12)
        Det = 1.38 * (1 / 12)
        Aft = math.pi * (Det ** 2) / 4
        Gmg = (mg / Aft) * (1 / 3600)

        # Anulo
        Dinta = 1.66 * (1 / 12)
        Dexta = 2.469 * (1 / 12)
        Dea = ((Dexta ** 2) - (Dinta ** 2)) / Dinta
        Afa = math.pi * (((Dexta ** 2) - (Dinta ** 2)) / 4)
        Gma = (ma / Afa) * (1 / 3600)


    elif N == 3:
        Dintt = 2.067 * (1 / 12)  # in ft
        Dextt = 2.38 * (1 / 12)
        Det = 2.027 * (1 / 12)
        Aft = math.pi * (Det ** 2) / 4
        Gmg = (mg / Aft) * (1 / 3600)

        # Anulo
        Dinta = 2.38 * (1 / 12)
        Dexta = 3.068 * (1 / 12)
        Dea = ((Dexta ** 2) - (Dinta ** 2)) / Dinta
        Afa = math.pi * (((Dexta ** 2) - (Dinta ** 2)) / 4)
        Gma = (ma / Afa) * (1 / 3600)

    elif N == 4:
        # Tubo interno
        Dintt = 3.068 * (1 / 12)  # in ft
        Dextt = 3.50 * (1 / 12)
        Det = 3.068 * (1 / 12)
        Aft = math.pi * (Det ** 2) / 4
        Gmg = (mg / Aft) * (1 / 3600)

        # Anulo
        Dinta = 3.50 * (1 / 12)
        Dexta = 4.026 * (1 / 12)
        Dea = ((Dexta ** 2) - (Dinta ** 2)) / Dinta
        Afa = math.pi * (((Dexta ** 2) - (Dinta ** 2)) / 4)
        Gma = (ma / Afa) * (1 / 3600)

    

    # CALCULO DE REGIMEN DE FLUJO
    # Tubo
    Ret = Det * Gmg / vg

    # Anulo
    Rea = Dea * Gma / va

    # CÁLCULO DEL NÚMERO DE PRANDAL
    Pra = (Cpa * va / ka) * 3600
    Prt = (Cpg * vg / kg) * 3600

    # COEFICIENTES DE CONVECCIÓN - CORRELACIONES DEL NUMERO DE NUSSELT
    # Tubo - : regimen de flujo turbulento = 72011 aprox.
    Nut = 0.683 * (Ret ** 0.466) * (Prt ** (1/3))
    hi = Nut * kg / Dintt

    # Anulo - : regimen de flujo laminar = 2181.7 aprox.
    Nua = 0.027 * (Rea ** 0.805) * (Pra ** (1/3))
    ho = Nua * ka / Dea

    # Coeficiente interno corregido
    hio = hi * (Dintt / Dextt)  # Btu/h-f2-°F
    # Coeficiente total limpio
    Uc = hio * ho / (hio + ho)  # Btu/h-f2-°F
    # Coeficiente total de diseño
    Rd = 0.003  # Enfriados por agua tabla 12 del Kern
    # 1/Ud=(1/Uc)+Rd;
    Ud = 1 / ((1 / Uc) + (Rd * 2))  # Btu/h-f2-°F
    # Area requerida
    Ar = Qa / (Ud * DTML)  # ft^2

    # Longitud requerida
    if N == 1:
        SppL = 0.435
    elif N == 2:
        SppL = 0.435
    elif N == 3:
        SppL = 0.622
    elif N == 4:
        SppL = 0.917


    Lr = Ar / (SppL)

    # Numero de horquillas
    LH = 20  # Longitud de un lateral de una horquilla, en ft
    No_de_horquillass = Lr / (2 * LH)
    Y = math.ceil(No_de_horquillass)

    # Longitud corregida
    Lc = Y * (2 * LH)  # ft

    # Superficie suministrada o de intercambio corregida, area corregida
    Ac = Lc * SppL  # ft^2

    # Corrección del coeficiente de diseño
    Udc = Qa / (Ac * DTML)  # Btu/h-ft^2-°F. Revisar si ese es el Q que va aqui

    # Corrección del factor de encrustamiento, o factor de encrustamiento corregido
    Rdc = (Uc - Udc) / (Uc * Udc)  # h-ft^2-°F/Btu


    # Caida de presión
    # Tubo interno
    fft = 0.0035 + (0.264 / (Ret ** 0.42))
    dFt = (4 * fft * ((Gmg * 3600) ** 2) * Lc) / ((2 * (32.174 * (3600 ** 2))) * (dg ** 2) * Dintt)  # factor de fanning del tubo
    dPt = dFt * dg / 144

    # Anulo
    Dec = Dexta - Dinta  # Diametro equivalente calculado para el anulo, en ft
    Reac = Dec * (Gma) / va  # Reynolds del anulo recalculado. Gma esta entre segundos
    ffa = 0.0035 + (0.264 / (Reac ** 0.42))
    dFa = 4 * ffa * ((Gma * 3600) ** 2) * Lc / (2 * ((32.174) * (3600 ** 2)) * (da ** 2) * Dec)
    V = (Gma * 3600) / (3600 * da)  # Caida de presion por cabeza de velocidad, ft
    Fa = 3 * ((V ** 2) / (2 * (32.32)))  # Perdidas de entrada y salida, ft
    dPa = ((dFa + Fa) * dg) / 144


    # CALCULO DE LA EFECTIVIDAD
    Cc = mg * Cpg
    Cf = ma * Cpa  # Btu/h-°F
    Qmax = Cf * (T1g - T1a)
    efectividad = (Qa / Qmax) * 100



    # Appending the results display
    results_text.config(state=tk.NORMAL)
    results_text.delete("1.0", tk.END)
    results_text.insert(tk.END, f"Calculated Results:\n")
    results_text.insert(tk.END, f"Ret: {Ret}\n")
    results_text.insert(tk.END, f"Rea: {Rea}\n")
    results_text.insert(tk.END, f"Prt: {Prt}\n")
    results_text.insert(tk.END, f"Pra: {Pra}\n")
    results_text.insert(tk.END, f"hi: {hi}\n")
    results_text.insert(tk.END, f"ho: {ho}\n")
    results_text.insert(tk.END, f"hio: {hio}\n")
    results_text.insert(tk.END, f"Uc: {Uc}\n")
    results_text.insert(tk.END, f"Ud: {Ud}\n")
    results_text.insert(tk.END, f"Ar: {Ar}\n")
    results_text.insert(tk.END, f"Lr: {Lr}\n")
    results_text.insert(tk.END, f"Y: {Y}\n")
    results_text.insert(tk.END, f"Lc: {Lc}\n")
    results_text.insert(tk.END, f"Ac: {Ac}\n")
    results_text.insert(tk.END, f"Udc: {Udc}\n")
    results_text.insert(tk.END, f"Rdc: {Rdc}\n")
    results_text.insert(tk.END, f"dPt: {dPt}\n")
    results_text.insert(tk.END, f"dPa: {dPa}\n")
    results_text.insert(tk.END, f"efectividad: {efectividad}\n")
    results_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Heat Exchanger Calculator")

T1a_label = tk.Label(root, text="Temperature Agua de entrada (°F):")
T1a_label.pack()
T1a_entry = tk.Entry(root)
T1a_entry.pack()

T1g_label = tk.Label(root, text="Temperature Glicerina de entrada (°F):")
T1g_label.pack()
T1g_entry = tk.Entry(root)
T1g_entry.pack()

T2a_label = tk.Label(root, text="Temperature Agua de salida (°F):")
T2a_label.pack()
T2a_entry = tk.Entry(root)
T2a_entry.pack()

T2g_label = tk.Label(root, text="Temperature Glicerina de salida (°F):")
T2g_label.pack()
T2g_entry = tk.Entry(root)
T2g_entry.pack()

M_var = tk.IntVar()
M_var.set(1)
M_radio_frame = tk.Frame(root)
M_radio_frame.pack()
M_label = tk.Label(M_radio_frame, text="Choose M:")
M_label.pack()
M_radio1 = tk.Radiobutton(M_radio_frame, text="Contracorriente", variable=M_var, value=1)
M_radio1.pack()
M_radio2 = tk.Radiobutton(M_radio_frame, text="Paralelo", variable=M_var, value=2)
M_radio2.pack()

N_var = tk.IntVar()
N_var.set(1)
N_radio_frame = tk.Frame(root)
N_radio_frame.pack()
N_label = tk.Label(N_radio_frame, text="Choose N:")
N_label.pack()
N_radio1 = tk.Radiobutton(N_radio_frame, text="2X1-1/4", variable=N_var, value=1)
N_radio1.pack()
N_radio2 = tk.Radiobutton(N_radio_frame, text="2-1/2X1", variable=N_var, value=2)
N_radio2.pack()
N_radio3 = tk.Radiobutton(N_radio_frame, text="3X2", variable=N_var, value=3)
N_radio3.pack()
N_radio4 = tk.Radiobutton(N_radio_frame, text="4X3", variable=N_var, value=4)
N_radio4.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

# Results Display
results_frame = tk.Frame(root)
results_frame.pack()
results_label = tk.Label(results_frame, text="Calculated Results:")
results_label.pack()
results_text = tk.Text(results_frame, wrap=tk.WORD, height=20, width=60, state=tk.DISABLED)
results_text.pack()

root.mainloop()