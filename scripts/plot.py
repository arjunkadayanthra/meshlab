import glob

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from scipy.stats import mstats

# Global constants
BITRATE = 'bitrate'
PLOTS_DIR = 'plots'
TIME_SECONDS = 'Time (seconds)'
BIT_RATE_MBPS = "Bit rate (Mbps)"
PREFIX_AGGREGATED = 'aggregated_'
EXT_HTML = 'html'
EXT_PNG = 'png'
PREFIX_FIGURE = 'figure_'

modes = [
    {'code': 'ip', 'desc': 'IP'},
    {'code': 'sw', 'desc': 'Software Offloading'},
    {'code': 'hw', 'desc': 'Hardware Offloading'},
    {'code': 'tc', 'desc': 'eBPF (TC)'}
]

protocols = [
    {'code': 'tcp', 'desc': 'TCP'},
    {'code': 'udp', 'desc': 'UDP'}
]

num_cols = 4
df_all_modes = pd.DataFrame()


# Function definitions
def plot_mode_subs(cur_mode, cur_prot):
    bitrate_all = []
    desc = cur_mode["desc"]
    m_code = cur_mode["code"]
    files = glob.glob(f'extracted/data/{cur_prot}_{m_code}-*.csv')
    num_files = len(files)
    num_rows = (num_files + num_cols - 1) // num_cols
    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(5 * num_cols, 4 * num_rows),
                            constrained_layout=True)
    fig.suptitle(f"Bit rate v/s time for mode : {desc} ({cur_prot.upper()})")
    fig.supylabel(BIT_RATE_MBPS)
    fig.supxlabel(TIME_SECONDS)
    for i, file in enumerate(files):
        df = pd.read_csv(file)

        df[BITRATE] = df[BITRATE] / 1e6
        bitrate_all.extend(df[BITRATE])
        mean = df[BITRATE].mean()
        median = df[BITRATE].median()
        std_dev = df[BITRATE].std()

        r = i // num_cols
        c = i % num_cols
        axs[r, c].plot(df[BITRATE], marker='o')
        axs[r, c].grid(True)
        axs[r, c].axhline(y=mean, color='r', linestyle='-', label=f'Mean: {mean:.2f}')
        axs[r, c].axhline(y=median, color='g', linestyle='--', label=f'Median: {median:.2f}')
        axs[r, c].fill_between(range(len(df)), (mean - std_dev), (mean + std_dev),
                               color='b', alpha=.1, label=f'SD: {std_dev:.2f}')
        axs[r, c].legend(mode="expand", ncols=3, fancybox=True, framealpha=0.5)

    min_bitrate = min(bitrate_all) - 5
    max_bitrate = max(bitrate_all) + 5
    for ax in axs.flatten():
        ax.set_ylim(min_bitrate, max_bitrate)

    # Remove empty subplots
    for i in range(num_files, num_rows * num_cols):
        fig.delaxes(axs.flatten()[i])

    # plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/{PREFIX_FIGURE}{cur_prot}_{m_code}.{EXT_PNG}')
    # plt.show()
    return bitrate_all


def plot_mode_aggregates(cur_mode, cur_prot, bitrate_all):
    code = cur_mode['code']
    desc = cur_mode['desc']
    aggregated_df = clean_df(bitrate_all)
    dim = f'{cur_prot}_{code}'
    df_all_modes[dim] = aggregated_df
    agg_mean = aggregated_df[0].mean()
    agg_median = aggregated_df[0].median()
    agg_std_dev = aggregated_df[0].std()
    fig = go.Figure()
    y_std_dev_upper = [agg_mean + agg_std_dev] * len(aggregated_df.index)
    y_std_dev_lower = [agg_mean - agg_std_dev] * len(aggregated_df.index)

    fig.add_trace(go.Scatter(x=aggregated_df.index.tolist() + aggregated_df.index.tolist()[::-1],
                             y=y_std_dev_upper + y_std_dev_lower[::-1],
                             fill='toself', fillcolor='rgba(63, 213, 132, 0.28)',
                             line=dict(color='rgba(63, 213, 132, 0.28)'),
                             showlegend=True, name=f'SD:{agg_std_dev:.2f}'))
    fig.add_shape(type="line", x0=aggregated_df.index[0], y0=agg_mean, x1=aggregated_df.index[-1], y1=agg_mean,
                  line=dict(color="deeppink", width=2),
                  label=dict(text=f"Mean:{agg_mean:.2f}", yanchor="top"), showlegend=True)
    fig.add_shape(type="line", x0=aggregated_df.index[0], y0=agg_median, x1=aggregated_df.index[-1], y1=agg_median,
                  line=dict(color="papayawhip", width=2),
                  line_dash="dot",
                  label=dict(text=f"Median:{agg_median:.2f}", yanchor="bottom"),
                  showlegend=True)
    fig.add_trace(
        go.Scatter(x=aggregated_df.index, y=aggregated_df[0], mode='lines+markers', name='Aggregated Bit Rate'))

    fig.update_layout(title=f'Aggregated bit rate over time for {desc} ({cur_prot.upper()})',
                      xaxis_title=TIME_SECONDS,
                      yaxis_title=BIT_RATE_MBPS,
                      xaxis=dict(title_standoff=20),
                      yaxis=dict(title_standoff=20),
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                      ))

    pio.write_html(fig, f'{PLOTS_DIR}/{PREFIX_AGGREGATED}{cur_prot}_{code}.html', auto_open=False)


def clean_df(bitrate_all):
    return pd.DataFrame(mstats.winsorize(pd.Series(bitrate_all), limits=[0.02, 0.02]))


def get_box_xlabels():
    result_dict = {}
    for protocol in protocols:
        for m in modes:
            key = f"{protocol['code']}_{m['code']}"
            value = f"{m['desc']} ({protocol['desc']})"
            result_dict[key] = value
    return result_dict


def plot_protocol_summary():
    fig = px.box(df_all_modes, title='Bit rates for different protocol-mode combinations', labels=get_box_xlabels())
    labels_dict = get_box_xlabels()
    fig.update_xaxes(tickvals=list(range(len(labels_dict))), ticktext=list(labels_dict.values()), title='Variant')
    fig.update_yaxes(title=BIT_RATE_MBPS)
    # fig.show()
    pio.write_html(fig, f'{PLOTS_DIR}/summary.html', auto_open=True)


# Driver code
for p in protocols:
    for mode in modes:
        bitrates = plot_mode_subs(mode, p['code'])
        plot_mode_aggregates(mode, p['code'], bitrates)
plot_protocol_summary()
