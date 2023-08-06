newline = '\n'
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, NavigableString, Comment # To get everything
import chart_studio.plotly as py
from plotly.graph_objs import *
import pandas as pd
import re
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

width=800
height=800
layout=Layout(title= "Just Checking",
    font= dict(size=12),
    showlegend=False,
    autosize=False,
    width=width,
    height=height,
    xaxis=layout.XAxis(axis),
    yaxis=layout.YAxis(axis),
    margin=layout.Margin(
        l=40,
        r=40,
        b=85,
        t=100,
    ),
    hovermode='closest',
    )

def painter(node_color_list,the_color):
  diff_color_x = []
  diff_color_y = []
  diff_color_label = []
  Nodes = list(G.nodes)

  for ttc in node_color_list:
    ttcl = len(ttc)
    for i in range(len(labels)):
      if(ttc == str(Nodes[i][:ttcl])):
        diff_color_y.append(Yv[i])
        diff_color_x.append(Xv[i])
        diff_color_label.append(labels[i])

  trace=Scatter(x=diff_color_x,
                 y=diff_color_y,
                 mode='markers',
                 name='net',
                 marker=dict(symbol='circle-dot',
                               size=10,
                               color=the_color,
                               line=dict(color='rgb(50,50,50)', width=0.5)
                               ),
                 text=diff_color_label,
                 hoverinfo='text'
                 )

  return trace


G = None
g = None
parents = None
labels = None
edges = None
pos = None
trace3 = None
trace4 = None
Xv = None
Yv = None

def init_global_variables(website):
  r = requests.get(website)
  #r = requests.get("https://www.autocarindia.com")
  output = r.text

  soup = BeautifulSoup(output, 'lxml')

  #The below two lines of code will extract the comments out of the code
  for element in soup(text=lambda text: isinstance(text, Comment)):
    element.extract()
  result = soup.findAll("html") #The result will point to the top node <html>

  G = nx.DiGraph() #Empty Graph with no nodes and no edges.

  G.add_node(result[0].name)  # result[0].name --> html
  parent = result[0]      #<html><head></head><body><div></div><p></p></body></html>
  parents = [parent]      #[<html><head></head><body><div></div><p></p></body></html>]
  labels=[parent.name]    #['html']
  edges = []
  i = 0
  for parent in parents:
    if hasattr(parent, 'contents'):
      for child in parent.contents:
        #These 2 lines will take out the extra string present as a node
        if isinstance(child, NavigableString):
          continue

        if child.name != None:
          node_name = child.name+str(i)
        else:
          node_name = 'string'+str(i)
        i = i + 1
        G.add_node(node_name)
        G.add_edge(parent.name,node_name)
        x = (parent.name,node_name)
        #print(parent.name,node_name)
        #print("")
        #print(str(child.name) + " ---> " + str(child.contents))
        toadd = ""
        for abc in child.contents:
          #print(str(type(abc)) +" -----> " + str(abc.string))
          if isinstance(abc, NavigableString):
            #print("TOADD ----> " +  str(abc.string))
            toadd = toadd + str(abc.string)
       
        if child.name != None:
          element1 = str(child.name) + ': ' + node_name
          child.name = node_name
        else:
          element1 = toadd
        if hasattr(child, 'attrs'):
          for item in child.attrs:
            # print(item,child.attrs[item])
            # input()
            element1 = element1 + '<br>' + '&nbsp; &nbsp;' + item+':' + '&nbsp;' + str(child.attrs[item])
        
        if child.string != None:
          element1 = element1 + '<br>' + '&nbsp; &nbsp;' + 'string'+':' + '&nbsp;' + str(child.string)
        elif toadd != "":
          element1 = element1 + '<br>' + '&nbsp; &nbsp;' + 'string'+':' + '&nbsp;' + toadd
        labels.append(element1)
        edges.append(x)
        parents.append(child)
        #print(parent.name,node_name)
  pos = nx.spiral_layout(G)

  # nx.draw(G,pos,with_labels=True, font_weight='bold')
  # print(parents)
  # plt.show()

  g=nx.Graph()
  g.add_nodes_from(parents)
  g.add_edges_from(edges) # E is the list of edges

  pos=nx.fruchterman_reingold_layout(g)

  # This part of code eliminates the extra nodes that are present in the graph
  # I didnt know if you want those extra nodes or not..

  N = len(parents) # ?
  counter = 0
  Xv = []
  Yv = []
  for k in pos.keys():
    if(counter>=N):
      Xv.append(pos[k][0])
      Yv.append(pos[k][1])
    counter+=1

  Xed=[]
  Yed=[]
  for edge in edges:
    Xed+=[pos[edge[0]][0],pos[edge[1]][0],None]
    Yed+=[pos[edge[0]][1],pos[edge[1]][1],None]




  trace3=Scatter(x=Xed,
                 y=Yed,
                 mode='lines',
                 line=dict(color='rgb(210,210,210)', width=1),
                 hoverinfo='text'
                 )
  trace4=Scatter(x=Xv,
                 y=Yv,
                 mode='markers',
                 name='net',
                 marker=dict(symbol='circle-dot',
                               size=5,
                               color='#6959CD',
                               line=dict(color='rgb(50,50,50)', width=0.5)
                               ),
                 text=labels,
                 hoverinfo='text'
                 )

  globals()['trace3']=trace3
  globals()['trace4']=trace4
  globals()['G']=G
  globals()['g']=g
  globals()['pos']=pos
  globals()['parents']=parents
  globals()['labels']=labels
  globals()['edges']=edges
  globals()['Xv']=Xv
  globals()['Yv']=Yv


def get_figure(find_node,text):
  # output = '''
  # <html>
  # 	<head>Some head
  # 	</head>
  # 	<body class='jc' id='id1'>
  # 		<div class='jc jc1 jc2'>
  # 			String in Div tag with nested p tag
  # 			<p> Hello </p>
  # 		</div>
  # 		<div>
  # 			Verumdigrtah
  # 		</div>
  # 		<p>Hi There!</p>
  # 	</body>
  # </html>
  # '''
  # output = "<html><head><script></script><title>Some</title></head><body class='jc' id='id1'><div class='jc jc1 jc2'>String in Div tag with nested p tag<div>Div kulla Div</div><p> Hello </p></div><div>summa</div><p>Hi There!</p></body></html>" #Output to be processed
  

  # Couldn't find any different code in google : ( Sed Lyf... 
  # So modified our own code to color some nodes differently 
  # This code colors the nodes given in the shortest_lenth list
  # Given that our shortest length calculator, calculates the length from the child_nodes ... so that the return name is p5, p3 similar to that 
  print(find_node)
  shortest_path = (nx.shortest_path(G,source="html",target=find_node))
  shortest_length = ['html']
  
  # Checking Tag Attributes
  if text!= None:
    for i in range(len(labels)):
      x = re.search(text,labels[i])
      if x:
        shortest_length.append(parents[i].name)
  # Checking if not found searching raw html code
  res = [] 
  for val in shortest_length: 
      if val != None : 
          res.append(val)
      else:
      	counter = 0
      	for item in reversed(parents):
        	item = str(item)
        	x = re.search(text,item)
        	if x:
        		res.append(item)
        		counter += 1
        		if(counter==2):
        			break
  
  # Matching Raw HTML code to parent for target node
  res2 = []
  for item1 in res:
    for item2 in parents:
      if str(item1)==str(item2):
        res2.append(item2.name)
        break

  res2_2 = []
  for val in res2:
    if val != None:
      res2_2.append(val)

  res = res + res2_2


  print(res)
  trace5 = painter(shortest_path,'#FFA500')
  trace6 = painter(res,'#00FF00')



  # diff_color_x = []
  # diff_color_y = []
  # diff_color_label = []
  # Nodes = list(G.nodes)

  # for ttc in shortest_length:
  #   ttcl = len(ttc)
  #   for i in range(len(labels)):
  #     if(ttc == str(Nodes[i][:ttcl])):
  #       diff_color_y.append(Yv[i])
  #       diff_color_x.append(Xv[i])
  #       diff_color_label.append(labels[i])

  # trace5=Scatter(x=diff_color_x,
  #                y=diff_color_y,
  #                mode='markers',
  #                name='net',
  #                marker=dict(symbol='circle-dot',
  #                              size=5,
  #                              color='#FFA500',
  #                              line=dict(color='rgb(50,50,50)', width=0.5)
  #                              ),
  #                text=diff_color_label,
  #                hoverinfo='text'
  #                )





  # annot="This networkx.Graph has the Fruchterman-Reingold layout<br>Code:"+  # "<a href='http://nbviewer.ipython.org/gist/empet/07ea33b2e4e0b84193bd'> [2]</a>"

  # axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
  #           zeroline=False,
  #           showgrid=False,
  #           showticklabels=False,
  #           title=''
  #           )

  # width=800
  # height=800
  # layout=Layout(title= "HTML Tree (WEBTREE)",
  #     font= dict(size=12),
  #     showlegend=False,
  #     autosize=False,
  #     width=width,
  #     height=height,
  #     xaxis=layout.XAxis(axis),
  #     yaxis=layout.YAxis(axis),
  #     margin=layout.Margin(
  #         l=40,
  #         r=40,
  #         b=85,
  #         t=100,
  #     ),
  #     hovermode='closest',
  #     annotations=[
  #            dict(
  #            showarrow=False,
  #             text='Displaying website as graph. Refresh for different layout',
  #             xref='paper',
  #             yref='paper',
  #             x=0,
  #             y=-0.1,
  #             xanchor='left',
  #             yanchor='bottom',
  #             font=dict(
  #             size=14
  #             )
  #             )
  #         ]
  #     )

  # data1=[trace3, trace4]
  data1=[trace3, trace4, trace5, trace6]
  fig1=Figure(data=data1, layout=layout)

  fromX=[]
  fromY=[]
  toX=[]
  toY=[]
  for edge in edges:
    fromX.append(pos[edge[0]][0])
    fromY.append(pos[edge[0]][1])
    toX.append(pos[edge[1]][0])
    toY.append(pos[edge[1]][1])

  list_len = len(fromX)
  list_of_arrows = []
  for i in range(list_len):
    list_of_arrows+=([dict(   x=toX[i],  # arrows' head
                    y=toY[i],  # arrows' head
                    ax=fromX[i],  # arrows' tail
                    ay=fromY[i],  # arrows' tail
                    xref='x',
                    yref='y',
                    axref='x',
                    ayref='y',
                    text='',  # if you want only the arrow
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=2,
                    arrowwidth=1,
                    arrowcolor='black')])
  annotations=[
             dict(
              showarrow=False,
              text='To change layout of graph, refresh page',
              xref='paper',
              yref='paper',
              x=0,
              y=-0.1,
              xanchor='left',
              yanchor='bottom',
              font=dict(
              size=14
              )
              )
          ]
  fig1.update_layout(
    annotations = annotations + list_of_arrows,
  )
  n = "Nodes in green are:" + newline
  for item in res:
    n = n + str(item) + newline
  return [fig1,n]


#fig1 = get_figure("html")

available_indicators = ["html","span208"]
app.layout = html.Div([

    html.Div([
        dcc.Input(
            id="text_input".format("text"),
            type="text",
            placeholder="search text",
            debounce=True,
        )
    ]),

    html.Div([
      html.Div(id='textarea', style={'whiteSpace': 'pre-line'}),
            dcc.Input(
            id="node".format("text"),
            type="text",
            placeholder="search node",
            debounce=True,
        )],
        style={'width': '49%', 'display': 'inline-block'}), 

    html.Div(children='''
        Enter the Node to search for in the above Textbox and see the path from HTML tag
    '''),

    dcc.Graph(
        id='graph1',
    ),

])

@app.callback(
    [Output('graph1', 'figure'),
    Output('textarea','children')],
    [Input('node', 'value'),
    Input('text_input','value')]
)
def callback(arg1,arg2):
    return get_figure(arg1,arg2)

if __name__ == '__main__':
    init_global_variables('http://www.google.com')
    app.run_server(debug=True)
  