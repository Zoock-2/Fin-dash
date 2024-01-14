import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MinhaApp:
    def __init__(self):
        # Carregar a interface do arquivo .ui
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Dashboad/ui/interface.ui")

        # Obter referências para os widgets definidos no Glade
        self.janela_principal = self.builder.get_object("main")
        self.janela_principal.connect("destroy", self.on_main_destroy)

        # Obter a referência para o GtkBox usando o ID
        vbox = self.builder.get_object("gtkbox")

        # Criar um botão
        botao = Gtk.Button(label="Meu Botão")
        # Conectar um manipulador de evento ao botão
        botao.connect("clicked", self.on_botao_clicked)

        # Adicionar o botão ao GtkBox
        vbox.pack_start(botao, True, True, 0)

        # Exibir todos os widgets
        self.janela_principal.show_all()

    def on_botao_clicked(self, widget):
        print("Botão Clicado!")

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
