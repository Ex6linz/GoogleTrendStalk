import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import BytesIO
import base64


def create_matplotlib_plot(df, keywords):
    plt.figure(figsize=(10, 5))
    for keyword in keywords:
        plt.plot(df.index, df[keyword], label=keyword)
    plt.title(f"Google Trends: {', '.join(keywords)}")
    plt.xlabel("Date")
    plt.ylabel("Search Interest")
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def create_interactive_plot(df, keywords):
    fig = go.Figure()
    for keyword in keywords:
        fig.add_trace(go.Scatter(x=df.index, y=df[keyword], name=keyword))
    return fig.to_json()