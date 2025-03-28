import tkinter as tk
from tkinter import messagebox, scrolledtext, StringVar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Função para buscar as informações com base na carga total e demanda
def buscar_informacoes(carga_total, demanda_calculada=None):
    tabela = [
        {"categoria": "A1", "carga": (0, 8), "demanda": "Sem Demanda", "disjuntor": 40, "fases": 1, "fios": 2, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 10, "pvc": 10, "cobre_2": 10, "diametro_aparente": 3/4, "diametro_subterraneo": 1, "tensao": "Monofásico 220 V"},
        {"categoria": "A2", "carga": (8, 11), "demanda": "Sem Demanda", "disjuntor": 50, "fases": 1, "fios": 2, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 10, "pvc": 10, "cobre_2": 10, "diametro_aparente": 3/4, "diametro_subterraneo": 1, "tensao": "Monofásico 220 V"},
        {"categoria": "A3", "carga": (11, 13), "demanda": "Sem Demanda", "disjuntor": 63, "fases": 1, "fios": 2, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 16, "pvc": 16, "cobre_2": "10(16)³", "diametro_aparente": "3/4(1)5", "diametro_subterraneo": 1, "tensao": "Monofásico 220 V"},
        {"categoria": "B1", "carga": (13, 20), "demanda": "Sem Demanda", "disjuntor": 50, "fases": 2, "fios": 3, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 10, "pvc": 10, "cobre_2": 10, "diametro_aparente": 1, "diametro_subterraneo": 1.5, "tensao": "Bifásico 380/220 V"},
        {"categoria": "B2", "carga": (20, 25), "demanda": "Sem Demanda", "disjuntor": 63, "fases": 2, "fios": 3, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 16, "pvc": 16, "cobre_2": "10(16)³", "diametro_aparente": 1, "diametro_subterraneo": 1.5, "tensao": "Bifásico 380/220 V"},
        {"categoria": "C1", "carga": (25, 50), "demanda": (0, 20), "disjuntor": 40, "fases": 3, "fios": 4, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 10, "pvc": 10, "cobre_2": 10, "diametro_aparente": 1, "diametro_subterraneo": 1.5, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C2", "carga": (25, 50), "demanda": (20, 30), "disjuntor": 50, "fases": 3, "fios": 4, "cabo_multiplexado": 10, "cobre": 10, "aluminio": 10, "epr": 16, "pvc": 16, "cobre_2": 10, "diametro_aparente": 1, "diametro_subterraneo": 1.5, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C3", "carga": (25, 50), "demanda": (30, 38), "disjuntor": 63, "fases": 3, "fios": 4, "cabo_multiplexado": 10, "cobre": 16, "aluminio": 16, "epr": 16, "pvc": 16, "cobre_2": "10(16)³", "diametro_aparente": 1.25, "diametro_subterraneo": 2, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C4", "carga": (25, 50), "demanda": (38, 45), "disjuntor": 70, "fases": 3, "fios": 4, "cabo_multiplexado": 16, "cobre": 25, "aluminio": 25, "epr": 25, "pvc": 25, "cobre_2": 25, "diametro_aparente": 1.5, "diametro_subterraneo": 2, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C5", "carga": (50, 75), "demanda": (45, 55), "disjuntor": "80/90^1,6", "fases": 3, "fios": 4, "cabo_multiplexado": 25, "cobre": 35, "aluminio": 25, "epr": 35, "pvc": 35, "cobre_2": 35, "diametro_aparente": 1.5, "diametro_subterraneo": 2, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C6", "carga": (50, 75), "demanda": (55, 65), "disjuntor": "100¹", "fases": 3, "fios": 4, "cabo_multiplexado": 25, "cobre": 35, "aluminio": 25, "epr": 35, "pvc": 35, "cobre_2": 35, "diametro_aparente": 1.5, "diametro_subterraneo": 2, "tensao": "Trifásico 380/220 V"},
        {"categoria": "C7", "carga": (50, 75), "demanda": (65, 75), "disjuntor": "125¹", "fases": 3, "fios": 4, "cabo_multiplexado": 35, "cobre": 50, "aluminio": 35, "epr": "50(70)³", "pvc": "70(50)³", "cobre_2": "35(50/70)³", "diametro_aparente": 2, "diametro_subterraneo": 3, "tensao": "Trifásico 380/220 V"}
    ]
    
    for item in tabela:
        if item["carga"][0] < carga_total <= item["carga"][1]:
            if demanda_calculada is not None:
                if item["demanda"] != "Sem Demanda" and item["demanda"][0] < demanda_calculada <= item["demanda"][1]:
                    return item
            else:
                if item["demanda"] == "Sem Demanda":
                    return item
    
    return None

# Função para processar os dados selecionados e gerar o PDF
def processar_carga_selecionada():
    try:
        carga = float(selected_carga.get().split("< C ≤ ")[-1])
        
        if 25 < carga <= 50 or 50 < carga <= 75:
            demanda_window()
        else:
            info = buscar_informacoes(carga)
            if info:
                atualizar_tela(info)
                gerar_pdf(info)
            else:
                messagebox.showwarning("Atenção", "Nenhuma informação encontrada para os valores selecionados.")
        
    except ValueError:
        messagebox.showerror("Erro", "Selecione uma carga válida.")

# Função para selecionar a demanda e gerar o PDF
def selecionar_demanda():
    try:
        demanda = float(selected_demanda.get().split("< D ≤ ")[-1])
        carga = float(selected_carga.get().split("< C ≤ ")[-1])
        
        info = buscar_informacoes(carga, demanda)
        if info:
            atualizar_tela(info)
            gerar_pdf(info)
        else:
            messagebox.showwarning("Atenção", "Nenhuma informação encontrada para os valores selecionados.")
        
    except ValueError:
        messagebox.showerror("Erro", "Selecione uma demanda válida.")

# Função para abrir uma janela para selecionar a demanda
def demanda_window():
    demanda_win = tk.Toplevel()
    demanda_win.title("Selecionar Demanda")
    
    demanda_label = tk.Label(demanda_win, text="Selecione a demanda calculada:")
    demanda_label.pack()
    
    global selected_demanda
    selected_demanda = StringVar(demanda_win)
    selected_demanda.set(demanda_opcoes[0])
    
    demanda_menu = tk.OptionMenu(demanda_win, selected_demanda, *demanda_opcoes)
    demanda_menu.pack()
    
    confirmar_demanda_btn = tk.Button(demanda_win, text="Confirmar Demanda", command=lambda: [selecionar_demanda(), demanda_win.destroy()])
    confirmar_demanda_btn.pack()

# Função para atualizar a tela com as informações selecionadas
def atualizar_tela(info):
    texto_box.config(state=tk.NORMAL)
    texto_box.delete(1.0, tk.END)
    info_texto = (
        f"Categoria: {info['categoria']}\n"
        f"Disjuntor: {info['disjuntor']} A\n"
        f"Fases: {info['fases']}\n"
        f"Fios: {info['fios']}\n"
        f"Cabo Multiplexado: {info['cabo_multiplexado']} mm²\n"
        f"Cobre: {info['cobre']} mm²\n"
        f"Alumínio: {info['aluminio']} mm²\n"
        f"EPR: {info['epr']} mm²\n"
        f"PVC: {info['pvc']} mm²\n"
        f"Cobre 2: {info['cobre_2']} mm²\n"
        f"Diâmetro Aparente: {info['diametro_aparente']} pol\n"
        f"Diâmetro Subterrâneo: {info['diametro_subterraneo']} pol\n"
        f"Tensão: {info['tensao']}\n"
    )
    texto_box.insert(tk.END, info_texto)
    texto_box.config(state=tk.DISABLED)

# Função para gerar e salvar o PDF com as informações selecionadas
def gerar_pdf(info):
    if info:
        # Cria o documento PDF
        doc = SimpleDocTemplate("relatorio.pdf", pagesize=letter)
        
        # Cria uma lista de elementos
        elementos = []
        
        # Define o estilo para o texto
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos['Title']
        estilo_subtitulo = estilos['Heading1']
        estilo_normal = estilos['Normal']
        
        # Adiciona o título ao documento
        elementos.append(Paragraph("Dimensionamento padrão de entrada coletivo", estilo_titulo))
        elementos.append(Spacer(1, 12))
        
        # Adiciona a seção de informações
        elementos.append(Paragraph("Padrão Adotado:", estilo_subtitulo))
        elementos.append(Spacer(1, 6))
        
        # Adiciona informações ao documento
        elementos.append(Paragraph(f"<b>Categoria:</b> {info['categoria']}", estilo_normal))
        elementos.append(Paragraph(f"<b>Disjuntor:</b> {info['disjuntor']} A", estilo_normal))
        elementos.append(Paragraph(f"<b>Fases:</b> {info['fases']}", estilo_normal))
        elementos.append(Paragraph(f"<b>Fios:</b> {info['fios']}", estilo_normal))
        elementos.append(Paragraph(f"<b>Cabo Multiplexado:</b> {info['cabo_multiplexado']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>Cobre:</b> {info['cobre']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>Alumínio:</b> {info['aluminio']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>EPR:</b> {info['epr']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>PVC:</b> {info['pvc']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>Cobre 2:</b> {info['cobre_2']} mm²", estilo_normal))
        elementos.append(Paragraph(f"<b>Diâmetro Aparente:</b> {info['diametro_aparente']} pol", estilo_normal))
        elementos.append(Paragraph(f"<b>Diâmetro Subterrâneo:</b> {info['diametro_subterraneo']} pol", estilo_normal))
        elementos.append(Paragraph(f"<b>Tensão:</b> {info['tensao']}", estilo_normal))
        
        # Adiciona espaçamento
        elementos.append(Spacer(1, 12))
        
        # Cria o PDF
        doc.build(elementos)
        
        messagebox.showinfo("Sucesso", "Relatório PDF gerado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Nenhuma informação encontrada para os valores selecionados.")


# Opções de carga e demanda
carga_opcoes = ["0 < C ≤ 8", "8 < C ≤ 11", "11 < C ≤ 13", "13 < C ≤ 20", "20 < C ≤ 25", "25 < C ≤ 50", "50 < C ≤ 75"]
demanda_opcoes = ["0 < D ≤ 20", "20 < D ≤ 30", "30 < D ≤ 38", "38 < D ≤ 45", "45 < D ≤ 55", "55 < D ≤ 65", "65 < D ≤ 75"]

# Configuração da janela principal
janela = tk.Tk()
janela.title("Seleção de Carga e Demanda")

carga_label = tk.Label(janela, text="Selecione a carga total:")
carga_label.pack()

selected_carga = StringVar(janela)
selected_carga.set(carga_opcoes[0])

carga_menu = tk.OptionMenu(janela, selected_carga, *carga_opcoes)
carga_menu.pack()

confirmar_btn = tk.Button(janela, text="Confirmar Carga", command=processar_carga_selecionada)
confirmar_btn.pack()

texto_box = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED)
texto_box.pack()

janela.mainloop()
