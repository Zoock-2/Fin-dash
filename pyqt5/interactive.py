import sys
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class InteractiveBarGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gráfico de Barras Interativo com Tooltips')
        self.canvas = self.create_chart()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_annot(self, index):
        x, y = self.bars[index].get_xy()
        width = self.bars[index].get_width()
        height = self.bars[index].get_height()
        self.annot.xy = (x + width / 2, y + height)
        text = f'Categoria: {self.categorias[index]}\nValor: {self.valores[index]}'
        self.annot.set_text(text)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            for i, bar in enumerate(self.bars):
                cont, ind = bar.contains(event)
                if cont:
                    self.update_annot(i)
                    self.annot.set_visible(True)
                    self.figure.canvas.draw_idle()
                    return
            if vis:
                self.annot.set_visible(False)
                self.figure.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes == self.ax:
            for i, bar in enumerate(self.bars):
                cont, ind = bar.contains(event)
                if cont:
                    if self.bar_selecionada is not None:
                        self.bars[self.bar_selecionada].set_alpha(0.7)  # Voltar a transparência ao normal
                    self.bars[i].set_alpha(1.0)  # Tornar a barra clicada mais opaca
                    self.bar_selecionada = i  # Atualizar a barra selecionada
                    self.figure.canvas.draw_idle()
                    return

        # Clicou fora das barras, restaurar a transparência ao normal para todas as barras
        if self.bar_selecionada is not None:
            self.bars[self.bar_selecionada].set_alpha(0.7)
            self.bar_selecionada = None
            self.figure.canvas.draw_idle()

    def create_chart(self):
        self.categorias = ['A', 'B', 'C', 'D', 'E']
        self.valores = [10, 15, 13, 17, 12]
        self.info = [f'Categoria: {cat}\nValor: {val}' for cat, val in zip(self.categorias, self.valores)]
        self.bar_selecionada = None

        self.figure, self.ax = plt.subplots()
        self.bars = self.ax.bar(self.categorias, self.valores, color='green', alpha=0.7)

        # Remover linhas laterais, superior e inferior
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        self.ax.set_xticks(range(len(self.categorias)))
        self.ax.set_xticklabels(self.categorias)
        #self.ax.set_ylabel('Valores')

        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                      textcoords="offset points",
                                      bbox=dict(boxstyle="round4", fc="green", alpha=0.7),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        canvas = FigureCanvas(self.figure)
        canvas.mpl_connect("motion_notify_event", self.hover)
        canvas.mpl_connect("button_press_event", self.on_click)

        return canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InteractiveBarGraph()
    window.show()
    sys.exit(app.exec_())
