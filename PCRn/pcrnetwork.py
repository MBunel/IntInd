from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from random import randint
import networkx as nx
from .views import articles


def pcrnetwork(request):

    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0

    mycache = randint(1000, 10000)
    n1 = 10
    n2 = 10
    nedges = 50
    isolated_nodes = []
    isolated_nodes_number = 0
    evacuated_nodes = []
    evacuated_nodes_number = 0

    try:
        mycache = randint(1000, 10000)
        n1 = escape(request.POST['n1'])
        n2 = escape(request.POST['n2'])
        nedges = escape(request.POST['nedges'])
        n1 = int(n1)
        n2 = int(n2)
        nedges = int(nedges)

        if 2 <= n1 <= 10 and 2 <= n2 <= 10 and 2 <= nedges <= 50:

            # edges and vertices
            N = n1+n2
            Nbad = n1
            badnodes = range(Nbad)
            Ngood = n2
            goodnodes = range(Nbad, Nbad+Ngood)

            edges = []
            for k in range(nedges):
                a, b = 0, 0
                while a==b:
                    a, b = randint(0, N-1), randint(0, N-1)
                c = randint(1, 2)
                if c==1:
                    edges = edges + [(a,b)]
                else:
                    edges = edges + [(b,a)]

            # connectivity matrix
            A = np.array([[0 for i in range(N)] for j in range(N)])
            for edge in edges:
                j = edge[1]
                i = edge[0]
                A[j][i] = 1
            for i in range(N):
                A[i][i] = -sum(A[j][i] for j in range(N) if j!= i)

            # Creating graph
            Graph = nx.DiGraph()
            Graph.add_nodes_from(badnodes)
            Graph.add_nodes_from(goodnodes)
            Graph.add_edges_from(edges)

            # Pathfinding

            isolated_nodes = []
            isolated_nodes_number = 0
            evacuated_nodes = []
            evacuated_nodes_number = 0
            for k in range(Nbad):
                connection = 0
                for j in range(Nbad, Nbad+Ngood):
                    if nx.has_path(Graph, k, j):
                        connection = connection + 1
                        evacuated_nodes_number = evacuated_nodes_number + 1
                        evacuated_nodes = evacuated_nodes + [[k, nx.shortest_path(Graph, k, j)]]
                if connection==0:
                    isolated_nodes_number = isolated_nodes_number + 1
                    isolated_nodes = isolated_nodes + [k]

            # Figure 1
            fig, ax = plt.subplots()
            pos = {}
            for i in goodnodes:
                pos.update({i: [2*np.cos(i)+0.02*randint(-10, 10), 2.5*np.sin(i)+0.02*randint(-10, 10)]})
            pos2 = {}
            for i in badnodes:
                pos2.update({i: [0.1*randint(-10, 10), 0.1*randint(-10, 10)]})
            pos.update(pos2)
            plt.axis('off')
            nx.draw_networkx_nodes(Graph, pos, nodelist=goodnodes, node_color='g')
            nx.draw_networkx_nodes(Graph, pos, nodelist=badnodes, node_color='r')
            nx.draw_networkx_edges(Graph, pos, edge_color='gray', alpha=0.5)
            nx.draw_networkx_labels(Graph, pos)
            title = r'$ n_1 = '+str(n1)+r', n_2 = '+str(n2)+r', n_e = '+str(nedges)+r' $'
            ax.set_title(title)
            ax.text(0.02, -0.1, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/pcrnetwork1.png')
            plt.close(fig)

            # PCR network
            eps = 0.2
            def network(X, t):
                dX = [0 for k in range(4*N)]
                for i in range(Nbad):
                    [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0) + np.array([eps*sum(A[i][j]*X[0+4*j] for j in range(N)), eps*sum(A[i][j]*X[1+4*j] for j in range(N)), eps*sum(A[i][j]*X[2+4*j] for j in range(N)), 0])
                for i in range(Nbad, N):
                    [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0.3) + np.array([eps*sum(A[i][j]*X[0+4*j] for j in range(N)), eps*sum(A[i][j]*X[1+4*j] for j in range(N)), eps*sum(A[i][j]*X[2+4*j] for j in range(N)), 0])
                return dX

            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1

            # Solve with scipy
            time = np.arange(0, 60, 0.1)
            orbit = odeint(network, X0, time)
            solution = orbit.T
            P = sum(solution[2+4*i] for i in range(N))
            R = sum(solution[0+4*i] for i in range(N))
            C = sum(solution[1+4*i] for i in range(N))

            # Figure 2
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(time, R)
            ax.plot(time, C)
            ax.plot(time, P)
            ax.set_title(title)
            ax.text(0.02, -0.1, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            plt.legend((r"$R(t)$", r"$C(t)$", r"$P(t)$"),
                shadow = True,
                prop={'size':20},
                loc = (0.7, 0.5))
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/pcrnetwork2.png')
            plt.close(fig)

            result = "You can make many simulations."
        else:
            result = "You must respect the constraints: $2 \leq n_1 \leq 10$, $2 \leq n_2 \leq 10$, $2 \leq n_e \leq 50$."
            n1 = 10
            n2 = 10
            nedges = 50
            isolated_nodes = []
            isolated_nodes_number = 0
            evacuated_nodes = []
            evacuated_nodes_number = 0

    except:
        mycache = randint(1000, 10000)
        result = "You must respect the constraints: $2 \leq n_1 \leq 10$, $2 \leq n_2 \leq 10$, $2 \leq n_e \leq 50$."
        n1 = 10
        n2 = 10
        nedges = 50
        isolated_nodes = []
        isolated_nodes_number = 0
        evacuated_nodes = []
        evacuated_nodes_number = 0
        return render(request, 'simulation/pcrnetwork.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'isolated_nodes': isolated_nodes,
            'isolated_nodes_number': isolated_nodes_number,
            'evacuated_nodes': evacuated_nodes,
            'evacuated_nodes_number': evacuated_nodes_number,
            'islogged': islogged
        })
    return render(request, 'simulation/pcrnetwork.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'isolated_nodes': isolated_nodes,
        'isolated_nodes_number': isolated_nodes_number,
        'evacuated_nodes': evacuated_nodes,
        'evacuated_nodes_number': evacuated_nodes_number,
        'islogged': islogged
    })
