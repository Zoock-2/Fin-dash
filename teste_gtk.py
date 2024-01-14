import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, Gdk, WebKit2
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
import tempfile
import os

class PlotlyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="GTK com Plotly Express")
        self.set_default_size(1600, 600)
        style = {'title': {"text":"Gráfico barras","x":0.5},'font':{'color':"black","size":20}}
        # Criar dados para o primeiro gráfico de barras horizontais
        y_data_bar1 = ['A', 'B', 'C', 'D']
        x_data_bar1 = [10, 11, 12, 13]

        # Criar o primeiro gráfico de barras horizontais
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(y=y_data_bar1, x=x_data_bar1, orientation='h'))
        fig1.update_layout(style)

        # Salvar o primeiro gráfico como um arquivo HTML temporário
        plot_filename1 = os.path.join(tempfile.gettempdir(), "temp_plot1.html")
        pio.write_html(fig1, file=plot_filename1)

        # Criar uma visualização web do arquivo HTML para o primeiro frame
        webview1 = WebKit2.WebView()
        webview1.load_uri(f"file://{plot_filename1}")
        frame1 = Gtk.Frame()
        frame1.add(webview1)

        # Criar dados para o segundo gráfico de barras
        x_data_bar2 = ['E', 'F', 'G', 'H']
        y_data_bar2 = [14, 15, 16, 17]

        # Criar o segundo gráfico de barras
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=x_data_bar2, y=y_data_bar2, marker=dict(color='red')))

        # Salvar o segundo gráfico como um arquivo HTML temporário
        plot_filename2 = os.path.join(tempfile.gettempdir(), "temp_plot2.html")
        pio.write_html(fig2, file=plot_filename2)

        # Criar uma visualização web do arquivo HTML para o segundo frame
        webview2 = WebKit2.WebView()
        webview2.load_uri(f"file://{plot_filename2}")
        frame2 = Gtk.Frame()
        frame2.add(webview2)

        # Criar uma caixa para conter os frames
        hbox = Gtk.HBox(spacing=10)
        hbox.pack_start(frame1, True, True, 0)
        hbox.pack_start(frame2, True, True, 0)

        # Adicionar a caixa à janela
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(hbox)
        self.add(scrolled_window)

def main():
    win = PlotlyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
