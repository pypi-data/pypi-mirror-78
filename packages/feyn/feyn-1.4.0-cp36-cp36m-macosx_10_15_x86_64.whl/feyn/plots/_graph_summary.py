import itertools
import svgwrite
import io
import numpy as np
import matplotlib.colors as clr

def plot_graph_summary(graph, dataframe):
    """
    Plot a graph displaying the signal path and summary metrics for the provided feyn.Graph and DataFrame.

    Arguments:
        graph -- A feyn.Graph
        dataframe -- a Pandas DataFrame.
    """
    from IPython.display import SVG
    return SVG(_rendergraph(graph, dataframe))


color_list = [('low', '#ff1ec8'), ('mid', '#FAFAFA'),('high', '#00F082')]


def _layout_2d(graph):
    # This layout algo moves nodes to the latest layer possible (graphs are wide in the middle)
    lmap = {}
    layers = []
    out = graph[-1]
    layers.insert(0, [out])
    while True:
        layer = []
        for node in layers[0]:
            for ix in reversed(node.sources):
                if ix!=-1:
                    pred = graph[ix]
                    if pred in lmap:
                        lmap[pred].remove(pred)

                    layer.append(pred)
                    lmap[pred] = layer

        if layer == []:
            break
        layers.insert(0,layer)

    locs = [None]*len(graph)
    for layer, interactions in enumerate(layers):
        sz = len(interactions)
        center = (sz-1) / 2
        for ix, interaction in enumerate(interactions):
            locs[interaction._index] = (layer, ix-center)

    return locs


def _information_gain(graph, interaction, df):
    from sklearn.metrics import mutual_info_score
    #This addition calculates the mutual information between given interaction in graph and output
    activations = []
    
    for i in range(len(df)):
        
        graph.predict(df.iloc[i:i+1])
        activations.append(interaction.activation[0])
    
    c_xy = np.histogram2d(activations, df[graph[-1].name], 10)[0]
    
    mi = mutual_info_score(None, None, contingency=c_xy)
    
    return mi


def _rendergraph(graph, df, label=None):
    from sklearn.metrics import roc_auc_score
    locs = _layout_2d(graph)

    # Move y values so the smallest is 0
    min_y = min([loc[1] for loc in locs])
    locs = [(1+loc[0]*120, (loc[1]-min_y)*60+20) for loc in locs]
    
    max_x = max([loc[0] for loc in locs])
    max_y = max([loc[1] for loc in locs])

    nodew = 80
    nodeh = 30
    
    h = max_y+nodeh+40
    w = max(max_x+nodew+150, 450)
    drawing = svgwrite.Drawing(
        profile="tiny", 
        size=(w, h)
    )

    
    #Summary information, output-type specific
    
    summary_names = ["R2:", "RMSE:", "MAE:"]
    summary_metrics = [np.round(graph.r2_score(df),3),
                        np.round(graph.rmse(df),3),
                        np.round(np.mean(graph.absolute_error(df)),3)]
    
    
    if graph[-1].spec.startswith("out:lr"):
        summary_names = ["Accuracy:", "AUC:", "MAE:"]
        summary_metrics = [np.round(graph.accuracy_score(df),3),
                            np.round(roc_auc_score(df[graph[-1].name], graph.predict(df)),3),
                            np.round(np.mean(graph.absolute_error(df)),3)]
    
    
    summaryw = 110
    summaryh = len(summary_names)*12 + 5
    
    summary_loc = (w-summaryw -10, locs[-1][1] +nodeh/2-summaryh/2)
    
    # The summary information rect
    rect = drawing.rect(
        (summary_loc[0], summary_loc[1]), 
        (summaryw,summaryh),
        fill = "#FAFAFA",
        stroke = "#ff1ec8"
    )
    drawing.add(rect)  

    # Draw summary information in rectangle
    for i in range(len(summary_names)):
        txt = drawing.text(summary_names[i],
                        insert=(summary_loc[0]+3, summary_loc[1]+12*(i+1)), 
                        fill='#202020', 
                        text_anchor="start", 
                        font_size=11, 
                        font_family="monospace")
        drawing.add(txt)
    
    for i in range(len(summary_metrics)):
        txt = drawing.text(summary_metrics[i],
                        insert=(summary_loc[0]-3+summaryw, summary_loc[1]+12*(i+1)), 
                        fill='#202020', 
                        text_anchor="end", 
                        font_size=11, 
                        font_family="monospace")
        drawing.add(txt)
    
    # Calculate mutual information on all activations
    mutual_informations = []

    n_samples = 5000
    if len(df) < 5000:
        n_samples = len(df)
    
    df_samples = df.sample(n_samples)
    
    for ix, interaction in enumerate(graph):   
        
        mutual_informations.append(_information_gain(graph, interaction, df_samples))
        #colors.append(matplotlib.colors.rgb2hex(cmap(norm(mutual_informations[ix]))[:3]))
    
    cmap = clr.LinearSegmentedColormap.from_list('random', 
                                            [(0,   color_list[0][1]),
                                            (0.5, color_list[1][1]),
                                            (1,   color_list[2][1])], N=256) #abzu_cmap_partial
    
    norm = clr.Normalize(vmin=min(mutual_informations), vmax=max(mutual_informations)) 
    
    #Colorbar
    
    bar_w = 50
    bar_h = 20
    colorbar_loc = (w/2-bar_w*1.5, h-20)
    
    for i in range(len(color_list)):
        
        color = color_list[i][1]
        signal_name = color_list[i][0]
        
        # The node rect
        rect = drawing.rect(
            (colorbar_loc[0]+i*bar_w, colorbar_loc[1]), 
            (bar_w,bar_h), 
            fill=color, 
            #stroke=stroke, 
            stroke_width=1
        )
        drawing.add(rect)
        
    
    #Text on signal
        txt = drawing.text(signal_name, 
                        insert=(colorbar_loc[0]+i*bar_w+bar_w/2, colorbar_loc[1]+bar_h/2+3), 
                        fill='#202020', 
                        text_anchor="middle", 
                        font_size=11, 
                        font_family="monospace")
        drawing.add(txt)
    
    txt = drawing.text("Signal capture", 
            insert=(colorbar_loc[0]+bar_w*1.5, colorbar_loc[1]-5), 
            fill='#202020', 
            text_anchor="middle", 
            font_size=11, 
            font_family="monospace")
    drawing.add(txt)
        
    #Nodes
    
    for ix, interaction in enumerate(graph):    
        
        loc = locs[ix]
        
        color = clr.rgb2hex(cmap(norm(mutual_informations[ix]))[:3])
        
        stroke = "#808080"

        # The node rect
        rect = drawing.rect(
            (loc[0], loc[1]), 
            (80,30), 
            fill=color, 
            stroke=stroke, 
            stroke_width=1
        )
        tooltip = svgwrite.base.Title(interaction.name+"\n"+interaction._tooltip)
        rect.add(tooltip)
        drawing.add(rect)

        # The node text
        l = interaction.name
        if not l:
            l = interaction.spec.split(":")[1].split("(")[0]

        if len(l) > 10:
            l = l[:10]+".."
        txt = drawing.text(l, 
                        insert=(loc[0]+nodew/2, loc[1]+nodeh/2+4), 
                        fill='#202020', 
                        text_anchor="middle", 
                        font_size=11, 
                        font_family="monospace")
        drawing.add(txt)
        
        # The index markers
        txt = drawing.text(interaction._index, 
                        insert=(loc[0]+nodew-5, loc[1]+7), 
                        fill='#202020', 
                        text_anchor="middle", 
                        font_size=7, 
                        font_family="monospace")
        drawing.add(txt)
        
        # The mutual information markers
        txt = drawing.text(np.round(mutual_informations[ix],2), 
                        insert=(loc[0]+nodew/2, loc[1]-5), 
                        fill='#202020', 
                        text_anchor="middle", 
                        font_size=9, 
                        font_family="monospace")
        drawing.add(txt)
        
        # The type text
        interaction_type = interaction.name
        if not interaction_type:
            interaction_type = ""
        if interaction.spec.startswith("in:cat"):
            interaction_type = "cat"
        elif interaction.spec.startswith("in:lin"):
            interaction_type = "num"
        elif interaction.spec.startswith("out"):
            interaction_type = "out"
            
        txt = drawing.text(interaction_type, 
                        insert=(loc[0]+8, loc[1]+9), 
                        fill='#202020', 
                        text_anchor="middle", 
                        font_size=8, 
                        font_family="monospace")
        drawing.add(txt)

        
        for ord, src_ix in enumerate(interaction.sources):
            if src_ix == -1:
                continue

            src_loc = locs[src_ix]
            x0 = src_loc[0]+nodew
            y0 = src_loc[1]+nodeh/2
                
            x1 = loc[0]
            y1 = loc[1]+nodeh/2
            if len(interaction.sources)==2:
                y1 += 9-(ord*18)
                
            # Connecting lines
            line = drawing.line(
                (x0,y0),(x1, y1), 
                stroke="#c0c0c0"
            )
            drawing.add(line)
            
            if interaction.spec.startswith("out"):
                continue

            # The ordinal markers
            txt = drawing.text(f"x{ord}", 
                            insert=(x1+5, y1+3), 
                            fill='#202020', 
                            text_anchor="middle", 
                            font_size=7, 
                            font_family="monospace")
            drawing.add(txt)

    f = io.StringIO()
    drawing.write(f)
    return f.getvalue()