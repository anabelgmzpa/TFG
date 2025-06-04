from Analisis.scrap import Scrap as sc

# Comentario 1
def coment1(evol, tamaño, tipo, ambito):
    partes_just=[]
    tamaños= {
            "PyME (<250 empleados)" : 1,
            "Grande (>250 empleados)" : 2
    }
    ambitos= {
        "Nacional" : 5,
        "Internacional" : 6
    }
    if evol=="Sube":
        valor= "N"
        fila= 2
    if evol=="Sube mucho":
        valor= "MN"
        fila= 2
    if evol=="Baja":
        valor= "P"
        fila= 4
    if evol=="Baja mucho":
        valor= "MP"
        fila= 4
    elif evol=="Se mantiene":
        valor= "E"
        just= "Irrelevante, no presenta ninguna variación."
        return valor, just
    partes_just.append("Según sus características:\n")
    partes_just.append(f"{sc.scrap_excel_coments(fila, tamaños[tamaño], 1)}")
    if tipo=="Pública":
        partes_just.append(f"{sc.scrap_excel_coments(fila, 3, 1)}")
    partes_just.append(f"{sc.scrap_excel_coments(fila, ambitos[ambito], 1)}")
    just= "\n".join(partes_just)
    return valor, just

# Comentario 2
def coment2(evol, tamaño, tipo, ambito):
    if evol=="Sube":
        valor= "P"
        just= f"Según su sector -> Defensa:\n\n{sc.scrap_excel_coments(48, 7, 0)}"
    if evol=="Sube mucho":
        valor= "MP"
        just= f"Según su sector -> Defensa:\n\n{sc.scrap_excel_coments(48, 7, 0)}"
    if evol=="Baja":
        valor= "N"
        just= f"Según su sector -> Defensa:\n\n{sc.scrap_excel_coments(46, 7, 0)}"
    if evol=="Baja mucho":
        valor= "MN"
        just= f"Según su sector -> Defensa:\n\n{sc.scrap_excel_coments(46, 7, 0)}"
    elif evol=="Se mantiene":
        valor= "E"
        just= "Irrelevante, no presenta ninguna variación."
    return valor, just