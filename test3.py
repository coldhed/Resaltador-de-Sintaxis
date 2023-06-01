# Script copied from https://gist.github.com/HiroNakamura/4650385

import numpy as np
import pandas as pd

class waterfall():
    def __init__(self, data, shap_values, 
                       base_value, 
                       path = "",
                       green_color ='#29EA38' , 
                       red_color = '#FB3C62', 
                       n=8,
                       title="The Prediction " ,
                       x_lab="",
                       y_lab="The predicted value",
                       formatting = "{:,.2f}",
                       rotation_value = 90,
                       figsize = (7,5)
                
                ):
        self.data        = data
        self.shap_values = shap_values
        self.base_value  = base_value
        self.green_color = green_color
        self.red_color   = red_color
        self.n           = n
        self.title       = title
        self.x_lab       = x_lab
        self.y_lab       = y_lab
        self.formatting  = formatting
        self.rotation_value = rotation_value
        self.figsize     = figsize
        self._plot       = pd.DataFrame()
        self.path        = path

    def obs_to_explain(self):
        '''
          - data: the observation. It is a Pandas series. The index contains the variable names 
          - shap_values: the shap_values for the above observation 
          - base_value: the base_value, which is the expected value or the mean of the target value of the training set
          - green_color: the color for the up bar
          - red_color: the color for the down bar
          - for_plot: a sorted data frame by the absolute value of shape in descending order
          - n: show the top n (default) variables. The rest variables are summed up into "others"
        '''
        for_plot = pd.DataFrame({'data':np.round(self.data,2),
                                 'shap':self.shap_values,
                                 'shap_abs': np.abs(self.shap_values),
                                 'label': self.data.index
                                })
        for_plot = for_plot.sort_values(by='shap_abs',ascending=False)

        # Split the variables into n and the rest. Only show the top n
        for_plot1 = for_plot.iloc[0:self.n,:]
        for_plot2 = for_plot.iloc[self.n:,:]

        # Sum up the rest as 'others'
        rest = pd.DataFrame({'data': '','shap':for_plot2['shap'].sum(), 'label': 'Others'},index=['others'])
        for_plot = for_plot1.append(rest)

        # Sum up the rest into 'others'
        base = pd.DataFrame({'data': np.round(self.base_value,2),'shap':self.base_value, 'label': 'Base value'},index=['base_value'])
        for_plot = base.append(for_plot)

        for_plot['blank'] = for_plot['shap'].cumsum().shift(1).fillna(0) # +  base_value
        for_plot['label'] = + for_plot['label'] + " =" + for_plot['data'].map(str) 
        for_plot['color'] = np.where(for_plot['shap']>0,self.green_color,self.red_color)
        for_plot = for_plot.drop(['data','shap_abs'],axis=1)
        
        self.for_plot = for_plot
        
        return(for_plot ) 
    
    def plt_plot(self):
        '''
          - x_lab, y_lab: the x label and y label
          - formatting: show the value of each bar 
        '''

        fig, ax = plt.subplots(figsize=self.figsize)

        # Plot the waterfall    
        plt.bar(range(0,len(self.for_plot.index)), self.for_plot['shap'], width=0.6,
              bottom=self.for_plot['blank'],     color=self.for_plot['color'])     

        #axis labels
        plt.xlabel("\n" + self.x_lab)
        plt.ylabel(self.y_lab + "\n")

        #Get the y-axis position for the labels
        y_height = self.for_plot.shap.cumsum().shift(1).fillna(0)

        plot_max = self.for_plot['shap'].max()
        plot_min = self.for_plot['shap'].min()
        pos_offset = plot_max / 40
        plot_offset = plot_max / 15 
        total = self.for_plot.sum().shap 

        # label the shap values
        loop = 0
        for index, row in self.for_plot.iterrows():
            # For the last item in the list, we don't want to double count
            if row['shap'] == total:
                    y = y_height[loop]
            else:
                    y = y_height[loop] + row['shap']

            if row['shap'] > 0:
                    y += (pos_offset*2)
                    plt.annotate(self.formatting.format(row['shap']),(loop,y),ha="center", color = self.green_color, fontsize=10)
            else:
                    y -= (pos_offset*4)
                    plt.annotate(self.formatting.format(row['shap']),(loop,y),ha="center", color = self.red_color, fontsize=10)
            loop+=1

        # Range of the ylim
        plt.ylim(plot_min-round(3.6*plot_offset, 7) ,plot_max+round(3.6*plot_offset, 7))

        #Rotate the labels
        plt.xticks(range(0,len(self.for_plot)), self.for_plot['label'], rotation=self.rotation_value)

        #add the base value line and title
        #plt.axhline(base_value, color='black', linewidth = 0.6, linestyle="dashed")
        plt.title(self.title)

        import matplotlib.patches as mpatches
        red_patch = mpatches.Patch(color=self.red_color, label='Down')
        green_patch = mpatches.Patch(color=self.green_color, label='Up')
        plt.legend(handles=[red_patch,green_patch],bbox_to_anchor=[1, 1], loc='upper left')

        #plt.tight_layout()
        #return(fig)
    
    def plotly_plot(self):
        import plotly.graph_objects as go
        import numpy as np

        ys = self.for_plot['shap'].round(2)
        ms = list(np.repeat('relative',len(ys)))
        xs = list(self.for_plot['label'].values)
        texts = self.for_plot['shap'].round(2)

        fig = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ms,
            x = xs,
            textposition = "outside",
            text = texts,
            y = ys,
            connector = {"line":{"color":"rgb(63, 63, 63)"} },
           ) )


        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        fig.update_layout(
            template="plotly_white",
            title ="The prediction of this observation is " ,
            margin=dict(l=120, r=120, t=60, b=60),
            yaxis=dict(
                title_text="The predicted value" 
            ),
            xaxis =dict(
                tickangle = -90,
                title_text = "Variables")
        )
        fig.write_html(self.path + "/f.html", auto_open=True)