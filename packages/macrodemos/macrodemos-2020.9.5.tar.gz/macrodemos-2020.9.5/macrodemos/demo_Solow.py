





from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import webbrowser

import numpy as np
import pandas as pd



# Esta parte controla asuntos de estética de la página
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': 'SteelBlue',
    'text': 'White',
    'controls': '#DDDDDD',
    'buttons': 'Orange'
}






class SolowSwan:
    names = dict(
        A='total productivity of factors',
        s='marginal rate of savings',
        α='marginal product of capital',
        δ='depreciation rate',
        n='population growth rate',
        k='Capital Stock (per capita)',
        y='Output per capita',
        sy='Savings per capita',
        c='Consumption per capita',
        Δk='Change in capital stock',
        gy='Output growth rate'
    )

    def __init__(self, A, s, α, δ, n):
        """

        :param A: float, total productivity of factors
        :param s: float, marginal rate of savings
        :param α: float, marginal product of capital
        :param δ: float, depreciation rate
        :param n: float, population growth rate
        """
        self.A = A
        self.s = s
        self.α = α
        self.δ = δ
        self.n = n
        self.data = None
        self.steady_state = dict()
        self.compute_steady_state()

    def parameters(self):
        A, s, α, δ, n = self.A, self.s, self.α, self.δ, self.n
        return dict(A=A, s=s, α=α, δ=δ, n=n)

    def sameparameter(self, param, value):
        return self.__getattribute__(param) if value is None else value

    def f(self, k):
        return self.A * k** self.α

    def compute_steady_state(self):
        A, s, α, δ, n = self.A, self.s, self.α, self.δ, self.n

        k = ((n+δ) / (s*A)) ** (1/(α - 1))
        y = self.f(k)
        i = (n + δ) * k
        c = y - i

        for name, value in zip('ykic', [y,k,i,c]):
            self.steady_state[name] = value

        self.steady_state['Δk'] = 0.0
        self.steady_state['gy'] = 0.0
        self.steady_state['sy'] = s*y

    def shock(self, T, A=None, s=None, α=None, δ=None, n=None):
        A = self.sameparameter('A', A)
        s = self.sameparameter('s', s)
        α = self.sameparameter('α', α)
        δ = self.sameparameter('δ', δ)
        n = self.sameparameter('n', n)

        K, S, Y = np.zeros([3, T+1], dtype=float)
        K[0], S[0], Y[0] = [self.steady_state[var] for var in ['k','sy','y']]

        for t in range(T):
            K[t+1] = ((1 - δ)*K[t] + S[t]) / (1 + n)
            Y[t+1] = A * K[t+1]**α
            S[t+1] = s*Y[t+1]

        datos = pd.DataFrame({'k':K, 'y':Y, 'sy': S})
        datos['c'] = Y - S
        datos['Δk'] = (S - (n+δ)*K) / (1 + n)
        datos.loc[0, 'Δk'] = (S[0] - (self.n + self.δ)*K[0]) / (1 + self.n)
        datos['gy'] = datos['Δk']*datos['k']

        self.data = datos

    def plot_field(self, ser):
        y = self.data[ser]
        ss = self.steady_state[ser]
        t = np.arange(y.size)
        results = dict()
        results['data'] = [{'x': t, 'y': y, 'type': 'line','name': 'scenario'},
                           {'x': t, 'y': ss + np.zeros_like(y), 'type':'line','name':'baseline'}]
        results['layout'] = {'title': self.names[ser], 'legend':{'orientation':'h'}}
        return results


#=======================================================================================================================
#
#  APP STARTS HERE
#
#_______________________________________________________________________________________________________________________
mathjax = ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"]  # to display math
omega = np.linspace(0, np.pi, 121)  # frequencies for spectral plot

def app_model_parameter(label, base_value, scen_value): # to make input parameter
    txt = html.Th(label)
    param1 = html.Th(dcc.Input(id='base_' + label, type='text', value=base_value, size='10'))
    param2 = html.Th(dcc.Input(id='scen_' + label, type='text', value=scen_value, size='10'))
    return html.Tr([txt, param1, param2])



app = JupyterDash(__name__,external_stylesheets=external_stylesheets, external_scripts=mathjax)

#======DESIGN THE APP===============

app.layout = html.Div(children=[
    html.H2(id='title',
            children='The Solow-Swan Model',
            style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(children=[html.H4("Parameters"),
                       html.Table(children=[
                           app_model_parameter('α', 0.35, 0.35),
                           app_model_parameter('δ', 0.06, 0.06),
                           app_model_parameter('n', 0.02, 0.02)]
                       ),
                       html.Hr(),
                       html.H4("Exogenous variables"),
                       html.Table(children=[
                           app_model_parameter('A', 1.0, 1.0),
                           app_model_parameter('s', 0.2, 0.2)]
                       ),
                       html.Hr(),
                       html.H4("Figure parameter"),
                       html.Table(children=[
                           html.Tr([html.Th('Number of periods'), dcc.Input(id='horizon', type='text', value=60, size='10')])]
                       ),
                       html.Button('PLOT', id='execute',style={'textAlign': 'center', 'backgroundColor': colors['buttons']}),
                       html.P('Solow-Swan-DEMO', style={'textAlign': 'center', 'color': colors['text'],'marginTop':250}),
                       ],
             style={'textAlign': 'center', 'color': colors['controls'], 'width': '25%', 'display': 'inline-block'}),

    html.Div(style={'width': '75%', 'float': 'right', 'display': 'inline-block'},
             children=[
                 # --PLOT 1a:  capital stock----------------------------------------------------------------------------
                 dcc.Graph(id='plot-capital',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 1b:  output per capita ------------------------------------------------------------------------------
                 dcc.Graph(id='plot-output',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 1c: savings---------------------------------------------------------------------------
                 dcc.Graph(id='plot-savings',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 # --PLOT 2a:  consumption----------------------------------------------------------------
                 dcc.Graph(id='plot-consumption',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2b: change in capital--------------------------------------------------------------------------
                 dcc.Graph(id='plot-delta-capital',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2c:  Growth rate -------------------------------------------------------------------------------
                 dcc.Graph(id='plot-growth',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 # --PLOT 3b:  IMPULSE RESPONSE FUNCTION----------------------------------------------------------------
                 html.A(children='Randall Romero Aguilar', href='http://randall-romero.com', style={'textAlign': 'center', 'color': colors['text'],'marginBottom':60}),
             ]),
],
    style={'backgroundColor': colors['background']})


@app.callback(
    [Output('plot-capital', 'figure'),
     Output('plot-output', 'figure'),
     Output('plot-savings', 'figure'),
     Output('plot-consumption', 'figure'),
     Output('plot-delta-capital', 'figure'),
     Output('plot-growth', 'figure'),
     ],
    [Input('execute', 'n_clicks')],
    [State('horizon','value'),
     State('base_α', 'value'),
     State('base_δ', 'value'),
     State('base_n', 'value'),
     State('base_A', 'value'),
     State('base_s', 'value'),
     State('scen_α', 'value'),
     State('scen_δ', 'value'),
     State('scen_n', 'value'),
     State('scen_A', 'value'),
     State('scen_s', 'value')])
def update_ARMA_parameters(n_clicks,T, α, δ, n, A, s, α1, δ1, n1, A1, s1):
    modelo = SolowSwan(*[float(xx) for xx in (A, s, α, δ, n)])
    modelo.shock(int(T), *[float(xx) for xx in [A1, s1, α1, δ1, n1]])
    return [modelo.plot_field(ser) for ser in ['k','y','sy','c','Δk','gy']]



def Solow_demo(colab=True):
    if colab:
        app.run_server(mode='external')
    else:
        webbrowser.open('http://127.0.0.1:8050/')
        app.run_server(debug=False)

if __name__ == '__main__':
    Solow_demo()