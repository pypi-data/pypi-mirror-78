from plotly.subplots import make_subplots
import plotly.graph_objs as go

def create_ohlc_figure(data_df, underlying):
    fig = go.Figure(data=go.Ohlc(x=data_df.index,
                                 open=data_df['open'],
                                 high=data_df['high'],
                                 low=data_df['low'],
                                 close=data_df['close']))
    fig.update_layout(height=600, width=1600, title_text=f'Live minute {underlying}')
    return fig




def create_quote_signal_figure(data_df, signals_df, strategy_name):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.9, 0.1])
    fig.add_trace(
        go.Scatter(x=data_df.index, y=data_df['close'], name=f'quotes {strategy_name}'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=data_df.index, y=signals_df['value'], name=f'signals {strategy_name}'),
        row=2, col=1
    )
    fig.update_layout(height=600, width=1600, title_text=f'Live strategy {strategy_name}')
    return fig



def plot_multiple_time_series(data_df):
    fig = make_subplots(rows=1, cols=1)
    constituents = [col for col in data_df.columns if col not in ['date','Date']]
    for me_constituent in constituents:
        trace_sig = go.Scatter(
            x=data_df.index,
            y=data_df[me_constituent],
            name=me_constituent,
            opacity=0.8)
        fig.append_trace(trace_sig, row=1, col=1)

    fig.update_layout(height=600, width=1600, title_text="Strategy performances",showlegend=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig

def plot_multiple_turnover(data_df, ma = None):
    fig = make_subplots(rows=1, cols=1)
    constituents = [col for col in data_df.columns if col not in ['date','Date']]
    for me_constituent in constituents:
        if ma is not None:
            data_df[me_constituent] = data_df[me_constituent].rolling(ma).mean()

        trace_sig = go.Scatter(
            x=data_df.index,
            y=data_df[me_constituent],
            name=me_constituent,
            opacity=0.8)
        fig.append_trace(trace_sig, row=1, col=1)

    fig.update_layout(height=600, width=1600, title_text="Strategy performances",showlegend=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig


def plot_correlation(data_df):
    static_correlation_df = data_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=static_correlation_df.values,
        x=static_correlation_df.index,
        y=static_correlation_df.columns,
        colorscale='Viridis'))

    fig.update_layout(
        title='Signal correlation matrix',
        xaxis_nticks=36)
    return fig


