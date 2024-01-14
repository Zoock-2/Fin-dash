import pandas as pd
import yfinance as yf
from dataclasses import dataclass
from plotly.subplots import make_subplots
import plotly.graph_objs as go

@dataclass
class acao:
    name: str
    history: any = None
    data_inicio: str = None
    data_fim: str = None
    normalizado: pd.DataFrame = None
    

    def __post_init__(self):
        self.history = yf.download(self.name, start=self.data_inicio, end=self.data_fim)
        self.normalizado = pd.DataFrame(self.history["Close"] / self.history["Close"].iloc[0])
        self.layout_properties = {
            "title_text": self.name,
            "title_x": 0.5,
            "title_font": {"size": 10, "color": "blue"},
        }

    def normalizado_graph(self, graph_type):
        if graph_type.lower() == "box":
            return self.box_graph()
        elif graph_type.lower() == "barras":
            return self.barras_graph(normal=True)
        elif graph_type.lower() == "pizza":
            return self.pizza_graph()
        elif graph_type.lower() == "linha":
            return self.linha_graphs()
        elif graph_type.lower() == "histograma":
            return self.histogram_graph()
        else:
            raise ValueError(f"Tipo de gráfico não suportado: {graph_type}")

    def barras_graph(self, vertical=False, normal=False):
        fig = make_subplots()
        
        if normal:
            data = self.normalizado["Close"]
            
        else:
            data = self.history["Close"]
            
        if vertical:
            # Gráfico de barras verticais
            fig.add_trace(go.Bar(x=data, y=data.index, orientation='h'))
            
        else:
            # Gráfico de barras horizontais
            fig.add_trace(go.Bar(x=self.history.index, y=data))
        fig.update_layout(self.layout_properties)
        return fig

    def pizza_graph(self):
        fig = make_subplots()
        # Gráfico de pizza
        fig.add_trace(go.Pie(labels=self.history.index, values=self.history["Close"], hole=0.3))
        fig.update_layout(self.layout_properties)

        return fig

    def linha_graphs(self):
        fig = make_subplots()

        # Gráfico de linha
        fig.add_trace(go.Scatter(x=self.history.index, y=self.history["Close"], mode='lines', name='Linha'))

        # Gráfico de área
        fig.add_trace(go.Scatter(x=self.history.index, y=self.history["Close"],
                                 fill='tozeroy', mode='none', fillcolor='rgba(0,100,80,0.2)', name='Área'))
        fig.update_xaxes(showticklabels=False,)
        fig.update_yaxes(tickfont=dict(size=10))
        fig.update_layout(self.layout_properties)
        return fig

    def box_graph(self):
        fig = make_subplots()
        fig.add_trace(go.Box(x=self.history["Close"]))
        fig.update_layout(self.layout_properties)
        return fig

    def histogram_graph(self):
        fig = make_subplots()
        fig.add_trace(go.Histogram(x=self.history["Close"], y=self.history.index, nbinsx=10))
        fig.update_layout(self.layout_properties)
        return fig

if __name__ == '__main__':
    b = acao("SAPR3.SA", data_inicio="2020-01-01")
    j = b.barras_graph()
    j.show()
    c = b.normalizado_graph(graph_type="barras")

    # Exibir o gráfico
    c.show()
