import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
import tempfile
import os
from model import acao


class MinhaApp:
    def __init__(self):
        # Carregar a interface do arquivo .ui
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./ui/interface.ui")
        # Obter referências para os widgets definidos no Glade
        self.janela_principal = self.builder.get_object("main")
        self.janela_principal.connect("destroy", self.on_main_destroy)
        
        self.box1 = self.builder.get_object("Graph_vbox1")  # GtkBox
        self.frame1 = Gtk.Frame()
        self.frame2 = Gtk.Frame()  # Criar GtkFrame
        self.box1.pack_start(self.frame1, True, True, 0)  # Adicionar GtkFrame à GtkBox
        self.box1.pack_start(self.frame2, True, True, 0)
        
        self.box2 = self.builder.get_object("Graph_vbox2") 
        self.frame_graph1 = Gtk.Frame()
        self.frame_graph2 = Gtk.Frame()
        self.frame_graph3 = Gtk.Frame()
        self.box2.pack_start(self.frame_graph1, True, True, 0)
        self.box2.pack_start(self.frame_graph2, True, True, 0)
        self.box2.pack_start(self.frame_graph3, True, True, 0)

        # Obter a referência para o GtkBox usando o ID
        vbox = self.builder.get_object("gtkbox")
        
        # Adicionar gráfico Plotly ao GtkFrame
        acoes_nomes = ["SAPR3.SA", "KLBN3.SA", 'SUZB3.SA', 'MGLU3.SA', 'HYPE3.SA']
        acoes = [acao(nome) for nome in acoes_nomes]
        
        for acao_instancia in acoes:
            # Criar um botão
            botao = Gtk.Button(label=acao_instancia.name)
            botao.connect("clicked", self.on_botao_clicked, acao_instancia)
            vbox.pack_start(botao, True, True, 0)
            
    def adicionar_grafico_plotly(self, frame, acao_graph): 
        # criar uma situação de direta ou esquerda para uma estilização para cada lado
        self.frame = frame
        fig = acao_graph
        
        # Ajustar margens e tamanho do gráfico
        fig.update_layout(
            margin=dict(l=30, r=0, t=25, b=5),  # Definir as margens desejadas em pixels
            width=600,  # Definir a largura desejada em pixels
            height=200  # Definir a altura desejada em pixels
        )
        
        # Salvar o gráfico como um arquivo HTML temporário
        import random
        numero_aleatorio = random.randint(1, 100)
        plot_filename = os.path.join(tempfile.gettempdir(), f"{numero_aleatorio}.html")
        pio.write_html(fig, file=plot_filename)

        # Criar uma visualização web do arquivo HTML
        webview = WebKit2.WebView()
        webview.load_uri(f"file://{plot_filename}")

        # Adicionar a visualização web ao GtkFrame
        self.frame.add(webview)
        webview.show()

    def on_botao_clicked(self, widget, acao_instancia):
        # Limpar os gráficos existentes nos frames antes de adicionar os novos
        for child in self.frame1.get_children():
            self.frame1.remove(child)

        for child in self.frame2.get_children():
            self.frame2.remove(child)

        for child in self.frame_graph1.get_children():
            self.frame_graph1.remove(child)

        for child in self.frame_graph2.get_children():
            self.frame_graph2.remove(child)

        for child in self.frame_graph3.get_children():
            self.frame_graph3.remove(child)

        # Adicionar novos gráficos com base na ação selecionada
        self.adicionar_grafico_plotly(self.frame1, acao_instancia.barras_graph())
        self.adicionar_grafico_plotly(self.frame2, acao_instancia.normalizado_graph(graph_type="barras"))
        self.adicionar_grafico_plotly(self.frame_graph1, acao_instancia.histogram_graph())
        self.adicionar_grafico_plotly(self.frame_graph2, acao_instancia.box_graph())
        self.adicionar_grafico_plotly(self.frame_graph3, acao_instancia.linha_graphs())

    def run(self):
        # Exibir a janela principal
        self.janela_principal.show_all()
        # Iniciar o loop principal do GTK
        Gtk.main()

    def on_main_destroy(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    minha_app = MinhaApp()
    minha_app.run()
