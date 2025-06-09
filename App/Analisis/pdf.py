import datetime
from BD.gestor_inds import Indicador as i
from BD.gestor_perfiles import Perfil as p
import Analisis.helpers as h
from fpdf import FPDF
import io, os
from PIL import Image

class PDF_logo(FPDF):
    def header(self):
        self.image("Paginas/Logo.png", x=2, y=2, w=13)

    # Crear pdf con las justificaciones
    def crear_pdf(sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, fuentes, cliente_obj, fecha=datetime.date.today(), perfil="", verPerfil=False, nombre_titulo="Perfil Estratégico"):
        alt= 6
        pag_uno= False
        # Crear pdf
        pdf = PDF_logo()
        pdf.add_page()
        # Añadir fuente
        pdf.add_font('normal', '', "/home/anabel/DATSI/TFG/App/Fonts/DejaVuSansCondensed.ttf", uni=True)
        pdf.add_font('negrita', '', "/home/anabel/DATSI/TFG/App/Fonts/DejaVuSansCondensed-Bold.ttf", uni=True)
        # Imprimir gráfica del perfil a la izquierda
        img = Image.open("Graf_perfil.png")
        ancho_real_px, alto_real_px = img.size
        alto_en_pdf = (120 * alto_real_px) / ancho_real_px
        pag_disp= pdf.h - pdf.b_margin - pdf.t_margin
        if (alto_en_pdf <= pag_disp):
            y_final_imagen = 15 + alto_en_pdf
            # Imprimir gráfico y luego logo para que no se superponga
            pdf.image("Graf_perfil.png", x=10, y=15, w=120)
            pdf.image("Paginas/Logo.png", x=2, y=2, w=13)
            # Título
            pdf.set_font('negrita', size=24)
            pdf.cell(0, 8, f"{nombre_titulo}", align="C")
            # Imprimir información relevante a la derecha del gráfico
            pdf.set_left_margin(120)
            pdf.set_font('negrita', size=14)
            pdf.write(alt, "\n\nFecha de creación:\n")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{fecha}\n")
            pdf.set_font('negrita', size=14)
            pdf.write(alt, "\nFuentes de los datos:\n")
            pdf.set_font('normal', size=10)
            for fuente in fuentes:
                pdf.write(alt, f"{fuente}\n")
            pdf.set_font('negrita', size=14)
            pdf.write(alt, "\nCaracterísticas de la empresa:\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Sector: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{sector}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Tamaño: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{tamaño}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Propiedad del capital: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{tipo}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Ámbito geográfico: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{ambito}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Importación: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{importacion}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Exportación: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{exportacion}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Sostenibilidad: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{sostenibilidad}\n")
            pdf.set_font('negrita', size=10)
            pdf.write(alt, "Cliente objetivo: ")
            pdf.set_font('normal', size=10)
            pdf.write(alt, f"{cliente_obj}\n")
        else:
            alto_fragmento_px = int(pag_disp / (120 / ancho_real_px))
            num_partes = (alto_real_px + alto_fragmento_px - 1) // alto_fragmento_px
            for j in range(num_partes):
                y_inicio_px = j * alto_fragmento_px
                y_fin_px = min((j + 1) * alto_fragmento_px, alto_real_px)
                bbox = (0, y_inicio_px, ancho_real_px, y_fin_px)
                fragmento = img.crop(bbox)
                nombre_temp = f"temp_parte_perfil_{j}.png"
                fragmento.save(nombre_temp)
                if pag_uno:
                    pdf.add_page()
                pdf.image(nombre_temp, x=10, y=15, w=120)
                pdf.image("Paginas/Logo.png", x=2, y=2, w=13)
                if not pag_uno:
                    pag_uno= True
                    # Título
                    pdf.set_font('negrita', size=24)
                    pdf.cell(0, 8, f"{nombre_titulo}", align="C")
                    # Imprimir información relevante a la derecha del gráfico
                    pdf.set_left_margin(120)
                    pdf.set_font('negrita', size=14)
                    pdf.write(alt, "\n\nFecha de creación:\n")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{fecha}\n")
                    pdf.set_font('negrita', size=14)
                    pdf.write(alt, "\n\nFuentes de los datos:\n")
                    pdf.set_font('normal', size=10)
                    for fuente in fuentes:
                        pdf.write(alt, f"{fuente}\n")
                    pdf.set_font('negrita', size=14)
                    pdf.write(alt, "\nCaracterísticas de la empresa:\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Sector: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{sector}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Tamaño: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{tamaño}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Propiedad del capital: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{tipo}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Ámbito geográfico: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{ambito}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Importación: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{importacion}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Exportación: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{exportacion}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Sostenibilidad: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{sostenibilidad}\n")
                    pdf.set_font('negrita', size=10)
                    pdf.write(alt, "Cliente objetivo: ")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{cliente_obj}\n")
                y_final_imagen = y_final_imagen = 15 + (120 * (y_fin_px - y_inicio_px)) / ancho_real_px
                os.remove(nombre_temp)
        img.close()
        # Imprimir indicadores y sus justificaciones, empezando en otra página
        pdf.set_left_margin(17)
        if y_final_imagen > 140:
            pdf.set_y(y_final_imagen)
        else:
            pdf.set_y(140)
        if verPerfil:
            inds_selec_num= p.get_inds(perfil)
            inds_selec= [i.get_Indicador(ind_n) for ind_n in inds_selec_num]
        else:
            inds_selec= i.obtener_seleccionados("BD/indicadores.db")
        inds_nombres= [i.get_name(indicador[0]) for indicador in inds_selec]
        inds_nombres.sort()
        for indicador in inds_nombres:
            indicador_info= i.get_Indicador_name(indicador)
            pdf.set_font('negrita', size=14)
            pdf.write(alt, f"{indicador_info[1]}\n")
            pdf.set_font('normal', size=10)
            l, sector_just, car_just= i.valores_perfil(indicador_info[0], sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, True, perfil, verPerfil)
            if i.sube_o_baja(indicador_info[0], perfil, verPerfil) == "Sube" or i.sube_o_baja(indicador_info[0], perfil, verPerfil) == "Sube mucho":
                pdf.write(alt, f"{i.sube_o_baja(indicador_info[0], perfil, verPerfil)} -> {indicador_info[11]}")
            elif i.sube_o_baja(indicador_info[0], perfil, verPerfil) == "Baja" or i.sube_o_baja(indicador_info[0], perfil, verPerfil) == "Baja mucho":
                pdf.write(alt, f"{i.sube_o_baja(indicador_info[0], perfil, verPerfil)} -> {indicador_info[13]}")
            else:
                pdf.write(alt, f"{i.sube_o_baja(indicador_info[0], perfil, verPerfil)}")
            pdf.set_font('negrita', size=10)
            pdf.write(alt,f"\n{h.valor_letras(l)} ({l})\n")
            if l=="E":
                pdf.set_font('normal', size=10)
                pdf.write(alt, "Irrelevante, no afecta.\n")
            else:
                if sector_just!="":
                    pdf.set_font('normal', 'U', size=10)
                    pdf.write(alt, "Según su sector:\n")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{sector_just}\n")
                if car_just!="":
                    pdf.set_font('normal', 'U', size=10)
                    pdf.write(alt, "Según sus características:\n")
                    pdf.set_font('normal', size=10)
                    pdf.write(alt, f"{car_just}\n")
            pdf.write(alt, "\n\n")
        # Generar pdf
        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer