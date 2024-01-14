from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the first layout
        layout1 = QtWidgets.QVBoxLayout()
        self.setLayout(layout1)

        # Create and add web view for the scatter plot
        scatter_view = QtWebEngineWidgets.QWebEngineView(self)
        layout1.addWidget(scatter_view)
        self.show_scatter_plot(scatter_view)

        # Create the second layout (horizontal)
        layout2 = QtWidgets.QHBoxLayout()
        layout1.addLayout(layout2)

        # Create and add web view for the bar chart
        bar_view = QtWebEngineWidgets.QWebEngineView(self)
        layout2.addWidget(bar_view)
        self.show_bar_chart(bar_view)
        a = 1
        # Create and add web view for the line chart
        line_view = QtWebEngineWidgets.QWebEngineView(self)
        layout2.addWidget(line_view)
        self.show_line_chart(line_view)

    def show_graph(self, fig, web_view):
        # Render the HTML representation of the plot
        html = fig.to_html(include_plotlyjs='cdn')

        # Set the HTML content to the web view
        web_view.setHtml(html)

    def show_scatter_plot(self, web_view):
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
        self.show_graph(fig, web_view)

    def show_bar_chart(self, web_view):
        df = px.data.tips()
        fig = px.bar(df, x="day", y="total_bill", color="sex", barmode="group")
        self.show_graph(fig, web_view)

    def show_line_chart(self, web_view):
        df = px.data.gapminder().query("country=='Canada'")
        fig = px.line(df, x="year", y="gdpPercap", title='Life expectancy in Canada')
        self.show_graph(fig, web_view)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()

