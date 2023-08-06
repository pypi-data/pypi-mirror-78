
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import webbrowser
from warnings import warn


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




class MarkovChain:

    def __init__(self, P, pi0=None, z=None):
        """

        Parameters
        ----------
        P   transition probability matrix, n.n
        pi0 initial distribution, n vector
        z   stochastic outcomes, n vector
        """
        P = np.atleast_2d(P)
        n, n2 = P.shape
        assert n == n2, "P must be a square array"
        assert np.all(P >= 0), "P elements must be nonnegative"
        assert np.allclose(P.sum(1), 1), "The rows of P must sum to 1"

        self.P = P
        self.n = n
        self.cdf = P.cumsum(1)

        if pi0 is None:
            self.pi0 = self.stationary_distribution if self.has_unique_stationary_distribution else np.ones((n) ) /n
        else:
            pi0 = np.asarray(pi0)
            assert pi0.ndim == 1 and pi0.size == n, "pi0 must be a vector with %d elements" % n
            assert np.all(pi0 >= 0), "pi0 elements must be nonnegative"
            assert np.allclose(pi0.sum(), 1), "The elements of pi0 must sum to 1"
            self.pi0 = pi0

        if z is None:
            self.outcomes = np.arange(n)
        else:
            z = np.asarray(z)
            assert z.ndim == 1 and z.size == n, "z must be a vector with %d elements" % n
            self.outcomes = z

        self.string_outcomes = isinstance(self.outcomes[0], str)

    @property
    def stationary_distribution(self):
        if self.has_unique_stationary_distribution:
            A = np.vstack((np.eye(self.n ) -self.P.T, np.ones((1 ,self.n))))
            b = np.hstack((np.zeros(self.n), np.ones((1))))
            return np.linalg.lstsq(A ,b)[0]
        else:
            warn("This Markov process does not have a unique stationary distribution")

    @property
    def has_unique_stationary_distribution(self):  # fixme: ugly implementation
        pn = self.P
        for it in range(50):
            if np.any(pn == 0.0):
                pn = pn @ self.P
            else:
                return True

        return False

    def rand(self, j):
        """
        Draw next state
        Parameters
        ----------
        j current state, integer = 0, 1,...,n-1

        Returns
        -------
        Integer: next state
        """
        return (np.random.rand() > self.cdf[j]).sum()

    def simulate(self, T: int = 120, j: int = 0):
        """
        Simulate the Markov process
        Parameters
        ----------
        T
        j

        Returns
        -------
        Vector: array of simulated values
        """
        assert j in range(self.n), 'Initial state must be a nonnegative integer less than %d' % self.n

        y = np.empty((1 + T))
        y[0] = j if self.string_outcomes else self.outcomes[j]
        for t in range(T):
            j = self.rand(j)
            y[t + 1] = j if self.string_outcomes else self.outcomes[j]

        return y

    def unconditional_distribution(self, T=24):
        prob = np.empty(( T +1, self.n))
        prob[0] = self.pi0
        for t in range(T):
            prob[t + 1] = np.dot(prob[t], self.P)
        return prob


    def plot(self, T=120):

        j = (np.random.rand() > self.pi0.cumsum()).sum()

        y = self.simulate(T, j)
        t = np.arange(y.size)
        results = dict()
        results['data'] = [{'x': t, 'y': y, 'type': 'line' ,'name': 'path' ,'line': {'shape': 'hv'}}]
        results['layout'] = {'title': 'Simulated path',
                             'legend' :{'orientation' :'h'},
                             'yaxis' :{'tickvals' :np.arange(self.n),
                                      'ticktext' :self.outcomes,
                                      'range' :[self. n -0.8, -0.2]
                                      }
                             }
        return results



    def plot_probability(self, T=24):

        p = self.unconditional_distribution(T).T
        tt = np.arange( 1 +T)
        results = dict()
        results['data'] = [{'x': tt, 'y': yy, 'type': 'bar' ,'name': state} for yy, state in zip(p, self.outcomes)]
        results['layout'] = {'title': 'Unconditional probability', 'legend' :{'orientation' :'h'}, 'barmode' :'stack'}
        return results


    def __repr__(self):
        txt = 'A Markov Chain process with transition probability\n'
        txt += self.P.__str__()
        txt += '\n\nand possible outcomes\n'
        txt += self.outcomes.__str__()
        return txt

    # =======================================================================================================================
#
#  APP STARTS HERE
#
# _______________________________________________________________________________________________________________________
mathjax = ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"]  # to display math
omega = np.linspace(0, np.pi, 121)  # frequencies for spectral plot

def app_model_parameter(label, base_value, scen_value): # to make input parameter
    txt = html.Th(label)
    param1 = html.Th(dcc.Input(id='base_' + label, type='text', value=base_value, size='10'))
    param2 = html.Th(dcc.Input(id='scen_' + label, type='text', value=scen_value, size='10'))
    return html.Tr([txt, param1, param2])




def make_the_app(states):
    n_states = len(states)

    app = JupyterDash(__name__ ,external_stylesheets=external_stylesheets, external_scripts=mathjax)

    # ======DESIGN THE APP===============

    app.layout = html.Div(children=[
        html.H2(id='title',
                children=f'Markov Chain with {n_states} states',
                style={'textAlign': 'center', 'color': colors['text']}),
        html.Div(children=[html.H4("Transition matrix"),
                           dash_table.DataTable(
                               id='table-row-headers',
                               columns=([{'id': 'Estado', 'name': 'Estado'}]),
                               data=[dict(Estado=param) for param in states],
                               editable=False,
                               style_table={'width' :'20%', 'float' :'left'}
                           ),
                           dash_table.DataTable(
                               id='table-transition-matrix',
                               columns=([{'id': p, 'name': p} for p in states]),
                               data=[dict(**{param: x for param, x in zip(states, fila)})
                                     for fila in np.identity(n_states)],
                               editable=True,
                               style_table={'width' :'75%'}
                           ),
                           html.Hr(),
                           html.H4("Initial probability"),
                           dash_table.DataTable(
                               id='table-states0',
                               columns=([{'id': 'Estado', 'name': 'Estado'},
                                         {'id': 'Prob0',  'name': 'Probabilidad'}]),
                               data=[dict(Estado=param, Prob0=x) for param, x in zip(states ,np.ones(n_states ) /n_states)],
                               editable=True,
                               style_table={'width' :'50%'}
                           ),
                           html.Hr(),
                           html.H4("Figure parameter"),
                           html.Table(children=[
                               html.Tr([html.Th('Number of periods, simulations'), dcc.Input(id='horizon', type='text', value=120, size='10')]),
                               html.Tr([html.Th('Number of periods, distribution'), dcc.Input(id='horizon2', type='text', value=32, size='10')]),
                           ]),
                           html.Button('PLOT', id='execute'
                                       ,style={'textAlign': 'center', 'backgroundColor': colors['buttons']}),
                           html.P('Markov-Chain-DEMO', style={'textAlign': 'center', 'color': colors['text'] ,'marginTop' :250}),
                           ],
                 style={'textAlign': 'center', 'color': colors['controls'], 'width': '25%', 'display': 'inline-block'}),

        html.Div(style={'width': '75%', 'float': 'right', 'display': 'inline-block'},
                 children=[
                     # --PLOT 1a:  capital stock----------------------------------------------------------------------------
                     dcc.Graph(id='plot-capital',
                               style={'width': '100%', 'display': 'inline-block'}),
                     # --PLOT 1b:  output per capita ------------------------------------------------------------------------------
                     dcc.Graph(id='plot-output',
                               style={'width': '100%',  'display': 'inline-block'}),
                     html.A(children='Randall Romero Aguilar', href='http://randall-romero.com', style={'textAlign': 'center', 'color': colors['text'] ,'marginBottom' :60}),
                 ]),
    ],
        style={'backgroundColor': colors['background']})


    @app.callback(
        [Output('plot-capital', 'figure'),
         Output('plot-output', 'figure'),
         ],
        [Input('execute', 'n_clicks')],
        [State('horizon' ,'value'),
         State('horizon2' ,'value'),
         State('table-transition-matrix', 'data'),
         State('table-states0', 'data') ,])
    def update_Markov_parameters(n_clicks, T, T2, data, pi0data):


        P = pd.DataFrame(data).astype(float)
        states = P.columns
        pi0 = pd.DataFrame(pi0data).iloc[: ,1].astype(float).values
        markov = MarkovChain(P, pi0, states)

        return [markov.plot(int(T)), markov.plot_probability(int(T2))]

    return app

def Markov_demo(*states, colab=True):
    app = make_the_app([str(x) for x in states])
    if colab:
        app.run_server(mode='external')
    else:
        webbrowser.open('http://127.0.0.1:8050/')
        app.run_server(debug=False)

if __name__ == '__main__':
    Markov_demo('state 0', 'state 1')