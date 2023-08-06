#!/usr/bin/env python
# coding: utf-8

# In[8]:


from io import StringIO
import os
import sys
from datetime import date
import re
import random
import math
from collections import Counter, namedtuple
import gc
import threading
import time
from itertools import cycle, chain, combinations
import itertools
import warnings
import kaleido 
from contextlib import suppress

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import cross_validate
 
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn import preprocessing

#import pprint
import pandas_profiling
from pandas_profiling.config import config
from pandas_profiling.model.base import Variable
import phik
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box
from ipywidgets import interact, interact_manual
from IPython.display import display, clear_output, HTML
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

from plotly.subplots import make_subplots
#from plotly.graph_objs import graph_objs as go 



import ipyfilechooser
from ipyfilechooser import FileChooser
import dill
from IPython.core.display import display, HTML

import shap

from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness
from aequitas.plotting import Plot
from aequitas.preprocessing import preprocess_input_df

from scipy import stats
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from typing import Callable, Dict, List, Optional, Union

import benfordslaw as bl
import missingno as msno

class helper_methods():

    def __init__(self):
        self.text_color = "green"
        get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')
        
    
    
        self.worldview = """
                            <b>Worldview:</b> In the context of this framework a "Worldview" is a set of assumptions about a
                            physical and social reality pertaining to a human feature or attribute, or to the measurement of same. 
                            As context must be taken into consideration there is no one fundamentally correct worldview but rather 
                            a reflection of a particular philosophy of life, or a conception of the world, as it relates to each of an
                            individuals' apparently quantifiable features or attributes. In the case of this framework, the focus is, in particular, on the worldview
                            held concerning any disparities in features or attributes that might be detected across groups within protected
                            features such as race, gender, age etc.
                            A disparity may, for example, refer to a non-proportionate representation or a significant difference in 
                            distribution. <br><br>
                            Two worldviews have been defined for this purpose: <br>
                        """
        
        self.worldview_biological = """
                        
                        <b>Inherent or biological worldview: </b>This worldview postulates that either chance or innate, 
                        inherent physiological, biochemical, neurological, cultural and/or genetic factors influence any
                        disparities in features or attributes that might be detected across groups (categorised by race, gender,
                        age etc).

                        This worldview could be quite easily applied to the measurements of weight, height, BMI or similar easily
                        quantifiable features to be used as predictors for a specific outcome. The worldview, however, becomes 
                        more complex for those human attributes or features which are harder to quantify, such as grit, determination,
                        intelligence, cognitive ability, self-control, growth mindset, reasoning, imagination, reliability etc. 

                        This Inherent or biological worldview is closely aligned with the concept of <b>individual fairness</b>,
                        where the fairness goal is to ensure that people who are ‘similar’ concerning a combination of the specific
                        observable and measurable features or attributes deemed relevant to the task or capabilities at hand, 
                        should receive close or similar rankings and therefor achieve similar outcomes.  

                        With this worldview, observable and measurable features are considered to be inherently objective
                        with no adjustments deemed necessary albeit with the knowledge that the human attributes or features
                        considered critical to success may have been identified as such by the dominant group. Notwithstanding 
                        that a significant amount of the measurements used to gauge and/or measure these human features or attributes
                        have been conceptualised, created or implemented by that same dominant group or that those historic 
                        outcomes may also have been influenced by prejudice towards a protected groups, or via favouritism 
                        towards the dominant group. 

                        This worldview might lead one to accept the idea that race, gender or class gaps are due to group 
                        shortcomings, not structural or systemic ones, and therefore the outcome “is what it is”, such that
                        individuals should be ranked with no consideration to differences in outcome across groups.

                        According to this worldview structural inequalities often perpetuated byracism, sexism and other prejudices 
                        <b>are not considered</b> to have any causal influence on outcomes.  

                        This worldview may also lead one to believe that representation of certain groups in specific fields
                        (such as STEM) are disproportionate to the representation in the population due to inherently different
                        preferences and/or abilities as opposed to the influence of social factors such as the exclusion, 
                        marginalisation, and undermining of the potential of the underrepresented group or to the favouritism 
                        (manifested through cognitive biases such as similarity bias etc) shown to other members of the dominant group.
                        This worldview might lead one to conclude that certain groups of individuals do not avoid careers in certain 
                        sectors due to lack of mentorship or the existence of (or the perception of the existence of)an exclusionary
                        workplace culture but rather because of their individual and inherent characteristics. 

                        """
        
        self.worldview_social = """
                        <b>Social and environmental worldview: </b> This worldview postulates that  social
                        and environmental factors, such as family income, parental educational backgrounds,
                        school, peer group, workplace, community, environmental availability of nutrition, 
                        correct environment for sleep, stereotype threat(and other cognitive biases ) 
                        often perpetuated by racism, sexism and other prejudices have influenced outcomes 
                        in terms of any detected disparities across groups. Differences in outcome may be 
                        a reflection of inequalities in a society which has led to these 
                        outcome. Identifying this has important
                        implications for the financial, professional, and social futures of particular 
                        protected groups within the population. Discrimination, privilege, institutional 
                        racism , sexism, ablism are examples of causal influences which may impact outcomes
                        or representation. Disparities may have been caused by intentional,explicit 
                        discrimination against a protected group or by subtle, unconscious, 
                        automatic discrimination as the result of favoritism towards the reference group,
                        or by other social and systemic factors. The term "affirmative action" is often 
                        used to justify the offering of opportunities to members of protected groups who 
                        do not otherwise appear to merit the opportunity. The offering of the opportunity is
                        often based upon personal qualities that are usually hard to quantify in an entirely
                        objective way. However it is important to note that due to social and environmental 
                        factors many measurements relating to human performance, merit, ability, etc
                        are also not necessarily objective. 

                        """
    def display_html(self, text, color, size):
        content = "<" + size + ">"  + "<text style='color:" + color + "'>" + text + "</text>" + "</" + size + ">" 
        display (widgets.HTML(content, layout=Layout(width='100%'))) 
    #################################################################################################
    #  VIEW Group representation in the data and display in the output area provided
    # 
    #################################################################################################
    def display_group_representation(self, data_frame, protected_features_list, output_area, _w=600, _h=600):
        try:

            with  output_area:
                clear_output(wait = True)
                fig_wig_a, fig_wig_b = self.plot_donut(protected_features_list,
                                                       data_frame,
                                                       w=_w, h=_h,
                                                       title = "Representation of Protected group(s) in the data");
                    
                    
                accordion = widgets.Accordion(children=[fig_wig_b, fig_wig_a])
                accordion.set_title(0, 'Tree Map View')
                accordion.set_title(1, 'Donut View')
                display(accordion)
                del fig_wig_a
                del fig_wig_b
        except:
            print ("Error in display_group_representation")
                    
    
    
    #################################################################################################
    #  VIEW analysis of NUMERIC features across protected groups, also used to show outcome distributio
    #  across groups
    #################################################################################################
    def numeric_feature_analysis_across_groups(self, 
                                       df, 
                                       feature,
                                       protected_attributes_list,
                                       label_y,
                                       group_descriptions_dict,#will remove after refactor
                                       label_encoding_dict,#will remove after refactor
                                       reference_groups_dict,#will remove after refactor
                                       _w=600, _h=600,
                                       high_range_pos = True,
                                       feature_data_dict = None):
        
        local_layout = {'width': 'auto', 'visibility':'visible'}
        local_layout_hidden  = {'width': 'auto', 'visibility':'hidden'}
        local_style = {'description_width':'initial'}
        HIGH_RANGE_POSITIVE = high_range_pos
        
        #If any of the protected features have a description replace the entry in the data-frame
        #with the description so it is easier to read.
        
      
        
        def show_analysis(selected_protected, label, curve_type, remove_outliers): 
            #local method 
            #plot the representation of data in the dataframe per protected group
            if selected_protected != "--select--": 
                #define a progress bar thread
                data_frame = df.copy()
                
                #########TO REFACTOR- OBTAINING THE ORIGINAL PROTECTED FOR ANALYSIS#########
                
                
                #label_encoding_dict only used here.
                
                # if group_descriptions_dict.get(selected_protected, False) != False:
                #   print("Descriptions have been saved for the Feature values")
                    
                
                #if label_encoding_dict.get(selected_protected, False) != False:
                    #print("Feature has been label encoded. view with pre-encoded values?")
                
                #if selected_protected+"_bm" in data_frame.columns:
                    #print ("feature has had values merged, view analysis with pre-merged valies?")
                
                if feature_data_dict == None: #refactor to only use a feature_data_dict
                    for feat in protected_attributes_list:
                        #get_feature_info returns _choice_dict_for_drop, original_values, label_encoded_values, descriptions
                        mapping = self.get_feature_info(feat, 
                                                data_frame[feat].dropna().unique(), 
                                                group_descriptions_dict,
                                                label_encoding_dict,
                                                {},
                                                {})[0]
                        keys = list( mapping.keys())
                        values = list (mapping.values())
                        reverse_mapping = dict(zip(values, keys))
                        data_frame[feat] = data_frame[feat].map(reverse_mapping)###
                        #now the dataframe has the description.
                
                elif feature_data_dict != None:#HERE we will keep this after refactoring
                    mapped_cols_df = self.map_values (data_frame, 
                                                      protected_attributes_list,
                                                      feature_data_dict)
                    #swap original cols with mapped cols...
                    for feat in protected_attributes_list:
                        data_frame[feat] = mapped_cols_df[feat]
                
                
                #########END TO REFACTOR-OBTAINING THE ORIGINAL PROTECTED FOR ANALYSIS END#########
                
                
                #data_frame[feat] now contains the values in the way we want to analyse.
                #ie merged, not-merged, encoded or not, with descriptions or not.
                
                progress = widgets.FloatProgress(value=0.0, 
                                                 min=0.0, 
                                                 max=1.0)
                progress.layout.width = '100%'
                finished = False
                def work(progress):
                    total = 200
                    for i in range(total):
                        if finished != True:
                            time.sleep(0.2)
                            progress.value = float(i+1)/total
                        else:
                            progress.value = 200
                            progress.style.bar_color = "green"
                            break

                thread = threading.Thread(target=work, args=(progress,))
                display(progress)
                #start the progress bar thread
                thread.start()
                #If a description was saved, use the desc rather than the actual values
                #to achieve this we change the contents of the column to reflect the
                #description, not the value.

                
                groups = data_frame[selected_protected].dropna().unique()
                
                tab = widgets.Tab()
                widget_html_arr = []
                tab_titles = []
                for group in groups:
                    filtered = data_frame[data_frame[selected_protected]==group]
                    
                    html_summary, outliers = self.detect_outlier_and_describe(filtered[feature],
                                                                              3, 
                                                                              data_type = "numeric")
                    
                    widget_html_arr.append(widgets.HTML(html_summary))
                    tab_titles.append(str(group))
                    if remove_outliers == True:
                        for val in outliers:
                            indexNames = data_frame[ (data_frame[selected_protected] == group) & (data_frame[feature] == val) ].index
                            data_frame.drop(indexNames , inplace=True) 
                tab.children = widget_html_arr
                for x in range(len(tab_titles)):
                    tab.set_title(x, tab_titles[x])

                if curve_type == "normal":       
                    text = ''' <b>Normal distribution:</b> A parametric approach which represents the behavior of most of the situations in 
                                   the universe. It's characterised by a bell shaped. The diameter, weight, strength, 
                                   and many other characteristics of natural, human or machine-made items are normally distributed.
                                   In humans, performance, outcomes, grade point averages etc. are all normally distributed. 
                                   The normal distribution really is a normal occurrence. If we compare the normal distribution
                                   of training data outcomes across two groups we can preform statistical test (such as the one below)
                                   to determine if there is a <b>significant variance</b> between groups'''


                if curve_type == "kde":         
                    text = ''' <b>Kernel Density estimate:</b> is a nonparametric approach. Parametric estimation requires a 
                                    parametric family of distributions to be assumed(e.g Normal distribution). 
                                    If you have a basis to believe the model is approxiamtely correct it is advantageous to do parametric 
                                    inference. On the other hand it is possible that the data does not fit well to any member of the family.
                                    In that case it is better to use kernel density estimation because it will construct a density that 
                                    reasonably fit the data. It does not require any assumption regarding parametric families.'''


                fig_wig_dist, dist_output_per_group, groups = self.plot_distribution(selected_protected,
                                                                                     feature, 
                                                                                     data_frame, 
                                                                                     w=_w, h=_h, 
                                                                                     y_high_positive = HIGH_RANGE_POSITIVE,
                                                                                     curve_type = curve_type)
                distOut = widgets.Output(layout={})
                with distOut:
                    display(fig_wig_dist)#as this returns an array of widgets
                    display(HTML("""Interactive version available <a href="output_dist.html" target="_blank"> here</a>"""))
                    self.display_html(text, "grey", "p")
                
                #########TO REFACTOR- OBTAINING THE Priviliged/Reference group#########
                #reference_groups_dict and group_descriptions_dict only used here
                #reference_group for t_test is the actual value in the dataframe (not the description)
                reference_group_to_use = ''
                if feature_data_dict == None:
                    reference_group = reference_groups_dict[selected_protected]
                    #Now if there is a description we should convert to the description
                    try:
                        reference_group_to_use = group_descriptions_dict [selected_protected][reference_group]
                    except:
                        reference_group_to_use = reference_group  
                else:
                    if feature_data_dict != None: #Here, keep this one after refactoring
                        reference_group_to_use = feature_data_dict[selected_protected]['privileged_description']
                        if reference_group_to_use == '':
                            reference_group_to_use = feature_data_dict[selected_protected]['original_privileged'] 
                        #'label_enc_privileged'
                #########TO REFACTOR END#########
                
                #Now add the two tailed T-test*************
                t_testOut = widgets.Output(layout={})
                with t_testOut:
                    clear_output(wait = True)
                    self.get_t_test_info(dist_output_per_group, groups, reference_group_to_use) 

                #Now add correlation matrix*************
                correlationOut = widgets.Output(layout={})               
                with correlationOut:
                    clear_output(wait = True)
                    
                    self.feature_analysis_plot_correlation(data_frame[[feature]+[selected_protected]+[label_y]],
                                                           label_y,
                                                           feature,
                                                           selected_protected)
                    

                #Now add scatter plot*************
                scatterPlotOut = widgets.Output(layout={})                        
                if label_y != feature:
                    with scatterPlotOut:
                        tab_scat = widgets.Tab()
                        clear_output(wait = True)
                        wig1 = go.FigureWidget(px.scatter_3d(data_frame[[feature]+[selected_protected]+[label_y]], x=label_y, y=feature, z=selected_protected,
                                        color=selected_protected,
                                        width=600, height=600,
                                        title=label_y+" "+feature+ " " + selected_protected))
        

                        wig2 = go.FigureWidget(px.scatter(data_frame[[feature]+[selected_protected]+[label_y]], x=label_y, y=feature, 
                                     color=selected_protected,
                                     width=600, height=600,
                                     title=label_y+" "+feature))
    
                        
                        tab_scat.children = [wig1,wig2]
                        tab_scat.set_title(0, "3D view")
                        tab_scat.set_title(1, "2D view")
                        display(tab_scat)
                          
                BenfordsLawOut = widgets.Output(layout={}) 
                with BenfordsLawOut:
                    benHTML = widgets.HTML("""
                    Also known as the Law of First Digits or the Phenomenon of Significant Digits, 
                    this law is the finding that the first numerals of the numbers found in series
                    of records of the most varied sources do not display a uniform distribution,
                    but rather are arranged in such a way that the digit “1” is the most frequent,
                    followed by “2”, “3”...in a successively decreasing manner down to “9”. This
                    can be a useful way of analysing data for fraud detection for example. 
                    <br><b>Note:</b> The law is not applicable to all numeric series but rather to those:<br>
                    <b>*</b> With a high order of magnitude.<br>
                    <b>*</b> No pre-established min or max <br>
                    <b>*</b> Not numbers used as identifiers, e.g social security, identity, bank acc.<br>
                    <b>*</b> Have a mean which is less than the median.<br>
                    <b>*</b> Data is not concentrated around the mean.<br>
                    """)
                    display(benHTML)
                    display (self.Benfords_law(data_frame[[feature]+[selected_protected]+[label_y]], 
                                               feature, 
                                               selected_protected))
                    
                if label_y != feature:
                    accordion = widgets.Accordion(children=[distOut,
                                                        tab,
                                                        t_testOut,
                                                        correlationOut,
                                                        scatterPlotOut,
                                                        BenfordsLawOut])
                    accordion.set_title(0, 'Distribution of ' + feature + ' grouped by '+selected_protected)
                    accordion.set_title(1, 'Describe (min/max/mean/outliers) for  ' + feature + ' grouped by '+selected_protected)
                    accordion.set_title(2, 'Two tailed T-test for ' + feature + ' based on ' + selected_protected)
                    accordion.set_title(3, 'Correlation between ' + feature + ", " + label_y + ' and '+ selected_protected)
                    accordion.set_title(4, 'Scatter plot ' + feature + ' and ' + label_y)
                    accordion.set_title(5, 'Benfords_law for ' + feature + ' based on ' + selected_protected )
                    accordion.selected_index=0 
                    
                if label_y == feature:
                    accordion = widgets.Accordion(children=[distOut,
                                                        tab,
                                                        t_testOut,
                                                        correlationOut,
                                                        BenfordsLawOut])
                    accordion.set_title(0, 'Distribution of ' + feature + ' grouped by '+selected_protected)
                    accordion.set_title(1, 'Describe (min/max/mean/outliers) for  ' + feature + ' grouped by '+selected_protected)
                    accordion.set_title(2, 'Two tailed T-test for ' + feature + ' based on ' + selected_protected)
                    accordion.set_title(3, 'Correlation between ' + feature + ' and '+ selected_protected)
                    accordion.set_title(4,'Newcomb/Benford law for ' + feature + ' based on ' + selected_protected )
                    accordion.selected_index=0  
                display (accordion)
                finished = True
                del data_frame
        
                
        if feature == label_y:
            self.display_html("Analysis of the distribution of the target ("+ feature + ") across groups", "black", "h4")
        else:
            display(HTML("<h4>Select the protected feature:</h4> "))
            
  
        interact(show_analysis, 
                     selected_protected = widgets.Dropdown(description = "Protected Feature",
                                                options = ["--select--"] + protected_attributes_list,
                                                layout = local_layout,
                                                style = local_style),
                    label = widgets.HTML(description=f"<b><font color='black'>{'Density estimation configuration :'}</b>",
                                         style = {'description_width': 'initial'},
                                         layout=Layout(width='90%')
                                        ),
                    curve_type = widgets.Dropdown(description = "Density Estimation",
                                                  options = {"Normal Distribution":"normal", "Kernel Density Estimation":"kde"},
                                                  layout = local_layout,
                                                  style = local_style),
                    remove_outliers = widgets.Checkbox(value=False,
                                                       description='Remove outliers (per group) for analysis',
                                                       disabled=False,
                                                       layout = local_layout,
                                                       style = local_style,
                                                       indent=False),
                                                );


    
    
    #################################################################################################
    #  VIEW analysis of CATEGORIC features across protected groups, also used to show outcome distributio
    #  across groups
    #################################################################################################
    def categoric_feature_analysis_across_groups(self, 
                                       df, 
                                       feature,
                                       protected_attributes_list,
                                       label_y,
                                       group_descriptions_dict,
                                       encoding_dict,
                                       reference_groups_dict,
                                       _w=600, _h=600,
                                       high_range_pos = True):
        
        local_layout = {'width': 'auto', 'visibility':'visible'}
        local_layout_hidden  = {'width': 'auto', 'visibility':'hidden'}
        local_style = {'description_width':'initial'}
        HIGH_RANGE_POSITIVE = high_range_pos
        
        
        
        def show_analysis(selected_protected): #local method
            #choose is the protected attribute we will analyze against
            if selected_protected != "--select--":
                #If a description was saved, use the desc rather than the actual values
                #to achieve this we change the contents of the column to reflect the
                #description, not the value.
                data_frame = df.copy()
                for feat in protected_attributes_list:
                    
                    mapping = self.get_feature_info(feat, 
                                    data_frame[feat].dropna().unique(), 
                                    group_descriptions_dict,
                                    encoding_dict,
                                        {},{})[0]
                    keys = list( mapping.keys())
                    values = list (mapping.values())
                    reverse_mapping = dict(zip(values, keys))
                    data_frame[feat] = data_frame[feat].map(reverse_mapping)
                    
                ####
                #set up a threaded progress bar
                progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
                progress.layout.width = '100%'
                finished = False
                def work(progress):
                    total = 200
                    for i in range(total):
                        if finished != True:
                            time.sleep(0.2)
                            progress.value = float(i+1)/total
                        else:
                            progress.value = 200
                            progress.style.bar_color = "green"
                            break

                thread = threading.Thread(target=work, args=(progress,))
                display(progress)
                #start the progress bar
                thread.start()

                groups = data_frame[selected_protected].dropna().unique()
                output_values = data_frame[feature].dropna().unique()
                layout = go.Layout(xaxis=dict(type='category'))
                fig_hist_count = go.FigureWidget(layout=layout)  
                fig_hist_percent = go.FigureWidget(layout=layout)
                with fig_hist_count.batch_update():
                    for group in groups:
                        temp = data_frame[[selected_protected, feature]].fillna("@Unknown")
                        temp = temp[temp[selected_protected]==group]
                        if feature == label_y:
                            if high_range_pos == True:
                                temp.loc[(temp[feature] == 1)] = "1(Positive impact)"
                                temp.loc[(temp[feature] == 0)] = "0(Negative impact)"
                                
                            elif high_range_pos == False:
                                temp.loc[(temp[feature] == 0)] = "0(Positive impact)"
                                temp.loc[(temp[feature] == 1)] = "1(Negative impact)"

                        fig_hist_count.add_trace(go.Histogram(
                                                    x=temp[feature],
                                                    name = selected_protected +":"+group,
                                                    histfunc="count",
                                                    opacity=0.75))
        
                        fig_hist_percent.add_trace(go.Histogram(
                                                    x=temp[feature],
                                                    name = selected_protected +":"+group,
                                                    histnorm = 'percent',
                                                    opacity=0.75))
                        
                    fig_hist_count.update_layout(
                                        title_text='Count across groups', # title of plot
                                        xaxis_title_text=feature, # xaxis label
                                        yaxis_title_text='Count', # yaxis label
                                        bargap = 0.2, # gap between bars of adjacent location coordinates
                                        bargroupgap = 0.1, # gap between bars of the same location coordinates
                                        legend_title = selected_protected,
                                        autosize = False
                                        )
                    fig_hist_percent.update_layout(
                                        title_text='Percentage across groups', # title of plot
                                        xaxis_title_text = selected_protected, # xaxis label
                                        yaxis_title_text='Percent', # yaxis label
                                        bargap=0.2, # gap between bars of adjacent location coordinates
                                        bargroupgap=0.1, # gap between bars of the same location coordinates
                                        legend_title = selected_protected,
                                        autosize=False
                                        )
                
                
                ####get information about each group, such as the count, num unique values.
                describe_tab = widgets.Tab()
                widget_html_arr = []
                tab_titles = []
                for group in groups:
                    filtered = data_frame[data_frame[selected_protected]==group]
                    html_summary = self.detect_outlier_and_describe(filtered[feature], 
                                                                    3, 
                                                                    data_type = "categoric")[0]

                    widget_html_arr.append(widgets.HTML(html_summary))
                    tab_titles.append(str(group))
                describe_tab.children = widget_html_arr
                for x in range(len(tab_titles)):
                    describe_tab.set_title(x, tab_titles[x])
                histOut = widgets.Output(layout={})
                with histOut:
                    hist_tab = widgets.Tab()
                    hist_tab.children = [fig_hist_count,fig_hist_percent]
                    hist_tab.set_title(0, "Count")
                    hist_tab.set_title(1, "Percentage")
                    display(hist_tab)
                       
                describeOut = widgets.Output(layout={})
                with describeOut:
                    display(describe_tab)
                
                sigOut = widgets.Output(layout={})
                with sigOut:
                    #reference_group for t_test is the actual value in the dataframe (not the description)
                    reference_group = reference_groups_dict[selected_protected]
                    #Now if there is a description we should convert to the description
                    try:
                        reference_group_to_use = group_descriptions_dict [selected_protected][reference_group]
                    except:
                        reference_group_to_use = reference_group 
                        
                    self.get_chi_square_test_info(data_frame[[feature]+[selected_protected]], 
                                                   feature, 
                                                   selected_protected, 
                                                   reference_group_to_use) 
 
                    
                correlationOut = widgets.Output(layout={})
                with correlationOut:
                    self.feature_analysis_plot_correlation(data_frame[[feature]+[selected_protected]+[label_y]],
                                                           label_y,feature,
                                                           selected_protected)
                    
                
                accordion = widgets.Accordion(children=[histOut,
                                                        describeOut,
                                                        sigOut,
                                                        correlationOut,
                                                        ])
                accordion.set_title(0, 'Count of ' + feature + ' grouped by '+ selected_protected)
                accordion.set_title(1, 'Describe ' + feature + ' grouped by '+ selected_protected)
                accordion.set_title(2, 'Pearson’s chi-squared significance test  ' + feature + ' based on ' + selected_protected)
                accordion.set_title(3, 'Correlation between ' + feature + ", " + label_y + ' and '+ selected_protected)
                accordion.selected_index=0 
                display(accordion)
                #end the progress bar thread
                finished = True
                del data_frame

        if feature == label_y:
            self.display_html("Analysis of the distribution of the target ("+ feature + ") across groups.", "black", "h4")
        else:
            self.display_html("Analysis of input feature: "+ feature + " across groups.", "black", "h4")
            
        
        interact(show_analysis, 
                 selected_protected = widgets.Dropdown(description = "Protected Feature",
                                            options = ["--select--"] + protected_attributes_list,
                                            layout = local_layout,
                                            style = local_style),
                )

    
    
    ################################################################################################
    # Correlation plot for protected group and all values
    # 
    ################################################################################################
    def plot_correlation_per_group(self, data_frame, protected_feature):
        widget_dict = {}
        plt.figure(figsize=(8, 8)) 
        for group in data_frame[protected_feature].dropna().unique():
            print(group)
            temp_df = data_frame[data_frame[protected_feature]== group]
            temp_df.drop(protected_feature, axis=1, inplace = True )
            corr = self.phi_k_correlation(temp_df)
            corr.reset_index(drop=True, inplace=True)
            corr["index"] = pd.Series(list(corr.columns))
            corr = corr.set_index("index")

            heatmap = go.FigureWidget(go.Heatmap(z=corr,
                         zmin=0, 
                         zmax=1,
                         x=corr.columns,
                         y=corr.columns,
                        xgap=1, ygap=1,
                        colorscale= px.colors.sequential.Blues,
                        colorbar_thickness=20,
                        colorbar_ticklen=3))

            title = 'Correlation Matrix'               
            with heatmap.batch_update():
                heatmap.update_layout(go.Layout(title_text=title, title_x=0.5, 
                                        width=300, height=300,
                                        xaxis_showgrid=False,
                                        yaxis_showgrid=False,
                                        yaxis_autorange='reversed'
                                        ))
            widget_dict[group] = heatmap
        return widget_dict
        box = widgets.HBox(widget_dict.values)
        display(box )
       
        
    #################################################################################################
    # Correlation plot for feature or label vs protected feature
    # 
    ################################################################################################
    def feature_analysis_plot_correlation(self, data_frame, label_y, feature, protected_feature):
        #remove any duplicate column that might occur when feature is the label
        data_frame = data_frame.loc[:,~data_frame.columns.duplicated()]
        html = widgets.HTML("""<b>Phik (φk)</b><br>
                        Phik (φk) is a new and practical correlation coefficient that
                        works consistently between categorical, ordinal and interval
                        variables, captures non-linear dependency and reverts to 
                        the Pearson correlation coefficient in case of a bivariate 
                        normal input distribution. There is extensive documentation
                        available here https://phik.readthedocs.io/en/latest/index.html""")

        display(html)
       
        plt.figure(figsize=(6, 6)) 
        
            
        if label_y != feature:
            corr = self.phi_k_correlation(data_frame[[feature]+[protected_feature]+[label_y]])
            res1 = corr.loc[ feature , : ][protected_feature]
            res2 = corr.loc[ feature , : ][label_y]
            text = "Correlation value for " + feature + " and " + protected_feature + " is " + str (res1)
            text = text + "<br>Correlation value for " + feature + " and " + label_y + " is " + str (res2)

        elif label_y == feature:
            corr = self.phi_k_correlation(data_frame[[label_y]+[protected_feature]])
            res1 = corr.loc[ feature , : ][protected_feature]
            text = "Correlation value for " + feature + " and " + protected_feature + " is " + str (res1)

        corr.reset_index(drop=True, inplace=True)
        corr["index"] = pd.Series(list(corr.columns))
        corr = corr.set_index("index")

        heatmap = go.FigureWidget(go.Heatmap(z=corr, 
                         x=corr.columns,
                         y=corr.columns,
                        xgap=1, ygap=1,
                        colorscale= px.colors.sequential.Blues,
                        colorbar_thickness=20,
                        colorbar_ticklen=3))

        title = 'Correlation Matrix'               
        with heatmap.batch_update():
            heatmap.update_layout(go.Layout(title_text=title, title_x=0.5, 
                                        width=300, height=300,
                                        xaxis_showgrid=False,
                                        yaxis_showgrid=False,
                                        yaxis_autorange='reversed'
                                        ))
        display(heatmap)
        display (HTML(text))
      
    #################################################################################################
    #  VIEW Counts of categorical features or output
    #  view_categorical_counts(data_frame, feature, high_range_pos)
    ################################################################################################
    def view_categorical_counts (self, data_frame, feature, high_range_pos = True ):
        layout = go.Layout(xaxis=dict(type='category'))
        if high_range_pos == True:
            data_frame.loc[(data_frame[feature] == 1),feature] = "1(Positive impact)"
            data_frame.loc[(data_frame[feature] == 0),feature] = "0(Negative impact)"

        elif high_range_pos == False:
            data_frame.loc[(data_frame[feature] == 0),feature] = "0(Positive impact)"
            data_frame.loc[(data_frame[feature] == 1),feature] = "1(Negative impact)"
            
        count = go.FigureWidget(layout=layout)  
        pcnt = go.FigureWidget(layout=layout)  

        count.add_trace(go.Histogram(
                    x=data_frame[feature],
                    histfunc="count",
                    opacity=0.75))

        pcnt.add_trace(go.Histogram(
                     x=data_frame[feature],
                    histnorm = 'percent',
                    opacity=0.75))

        

        count.update_layout(
                        title_text='Count of total', # title of plot
                        xaxis_title_text=feature, # xaxis label
                        yaxis_title_text='Count', # yaxis label
                        bargap = 0.2, # gap between bars of adjacent location coordinates
                        bargroupgap = 0.1, # gap between bars of the same location coordinates
                        autosize = False
                        )
        pcnt.update_layout(
                        title_text='Percent of total', # title of plot
                        xaxis_title_text=feature, # xaxis label
                        yaxis_title_text='Percent', # yaxis label
                        bargap=0.2, # gap between bars of adjacent location coordinates
                        bargroupgap=0.1, # gap between bars of the same location coordinates
                        autosize=False
                        )
        return count, pcnt
    
     #################################################################################################
    #  VIEW Counts of categorical features or output
    #  view_categorical_counts(data_frame, selected_protected, feature, high_range_pos)
    #################################################################################################  
    def view_categorical_counts_for_protected(self, 
                                data_frame, 
                                protected_feature,
                                feature,
                                label_y,
                                high_range_pos = True):
        

        groups = data_frame[protected_feature].dropna().unique()
        output_values = data_frame[protected_feature].dropna().unique()

        
        layout = go.Layout(xaxis=dict(type='category'))
        fig_hist_count = go.FigureWidget(layout=layout)  
        fig_hist_percent = go.FigureWidget(layout=layout)
        with fig_hist_count.batch_update():
            for group in groups:
                temp = data_frame[[protected_feature, feature]].fillna("@Unknown")
                temp = temp[temp[protected_feature]==group]
                if feature == label_y:
                    if high_range_pos == True:
                        temp.loc[(temp[feature] == 1),feature] = "1(Positive impact)"
                        temp.loc[(temp[feature] == 0),feature] = "0(Negative impact)"

                    elif high_range_pos == False:
                        temp.loc[(temp[feature] == 0),feature] = "0(Positive impact)"
                        temp.loc[(temp[feature] == 1),feature] = "1(Negative impact)"

                fig_hist_count.add_trace(go.Histogram(
                                            x=temp[feature],
                                            name = protected_feature +":"+group,
                                            histfunc="count",
                                            opacity=0.75))

                fig_hist_percent.add_trace(go.Histogram(
                                            x=temp[feature],
                                            name = protected_feature +":"+group,
                                            histnorm = 'percent',
                                            opacity=0.75))

            fig_hist_count.update_layout(
                                title_text='Count across groups', # title of plot
                                xaxis_title_text=feature, # xaxis label
                                yaxis_title_text='Count', # yaxis label
                                bargap = 0.2, # gap between bars of adjacent location coordinates
                                bargroupgap = 0.1, # gap between bars of the same location coordinates
                                legend_title = protected_feature,
                                autosize = False
                                )
            fig_hist_percent.update_layout(
                                title_text='Percentage across groups', # title of plot
                                xaxis_title_text = feature, # xaxis label
                                yaxis_title_text='Percent', # yaxis label
                                bargap=0.2, # gap between bars of adjacent location coordinates
                                bargroupgap=0.1, # gap between bars of the same location coordinates
                                legend_title = protected_feature,
                                autosize=False
                                )

        return fig_hist_count, fig_hist_percent


        
        
    #################################################################################################
    #  Convert encoded or merged features back to original values to allow for more 
    #  intuitive analysis of fairness.
    #################################################################################################  
    def convert_feature_column(self, 
                               df,
                               feature,
                               feature_data):
        
       # one-hot-encode (done)
       # label_encode (done)
       # merged (done)
       # merged and one-hot-encode (TODO)
       # merged and label_encode (TODO)
        if len(feature_data['values_description']) == 0:
            feature_data['values_description'] = feature_data['original_values']
    
        
        # If the feature was one_hot_encoded but not merged, de-encode and return the original col, 
        # and original vals with description(if exists)
        if feature_data['one_hot_enc'] == True and feature_data['values_merged'] == False:
            df[feature] = self.de_hot_encode_feature (df, 
                                                      feature_data['one_hot_enc_col_before'], 
                                                      feature_data['one_hot_enc_cols_after'])
            mapping_dict = dict(zip(feature_data['original_values'], 
                                    feature_data['values_description']))
            df[feature] = df[feature].map(mapping_dict)
            return df[feature]
        
        # If the feature was label encoded but not merged, return the original col, 
        # and original vals with description(if exists)
        elif feature_data['label_enc'] == True and feature_data['values_merged'] == False:
            
            mapping_dict = dict(zip(feature_data['label_enc_values'], 
                                    feature_data['values_description']))
            
            df[feature] = df[feature].map(mapping_dict)
            return df[feature]
        
        # If the feature was merged but not one-hot encoded or label encoded
        elif feature_data['values_merged'] == True:
            print ("merged!")
            df[feature] = df[feature_data['before_merge_col']]
            mapping_dict = dict(zip(feature_data['original_values'], 
                                    feature_data['values_description']))
            df[feature] = df[feature].map(mapping_dict)
            return df[feature]
        
    
        else:
            return df[feature]
    
    #################################################################################################
    #  VIEW STATISTICS AROUND. THE PROTECTED FEATURES/ATTRIBUTES
    # 
    #################################################################################################       
    def set_decision_boundary(self, df, data_summary):
        #if the function was already called, remove the generated column to start again.
        if data_summary.y_value +'_binary' in df.columns:
            df.drop(data_summary.y_value +'_binary', axis = 1, inplace = True)
            
        #copy the input data_frame to avoid permanent changes as we will de-encode etc.    
        data_frame = df.copy()
        out1 = widgets.Output(layout={})
        local_layout = {'width': 'auto', 'visibility':'visible'}
        local_layout_hidden  = {'width': 'auto', 'visibility':'hidden'}
        local_style = {'description_width':'initial'}
        display (out1)
        layout = go.Layout(xaxis=dict(type='category'))
        try:
            with out1:
                clear_output(wait = True)
                self.display_html("Description of Target", self.text_color, "h3")
                if data_summary.Y_BINARY == True:
                    self.display_html("The target is a binary value(1 or 0)", "black", "p")
                    if data_summary.HIGH_RANGE_POSITIVE == True:
                        impactTxt = "<b>Positive</b>"
                    if data_summary.HIGH_RANGE_POSITIVE == False:
                        impactTxt = "<b>Negative</b>"
                    x = "An output of 1 has a <b>" + impactTxt + "</b> impact on an individual" 
                    self.display_html(str(x), self.text_color, "h4")
                
                elif data_summary.Y_CONTINUOUS == True:
                    self.display_html("The target is a continuous value", "black", "p")
                    y_Min = round(data_frame[data_summary.y_value].min(), 3)
                    y_Mean = round(data_frame[data_summary.y_value].mean(), 3)
                    y_Max = round(data_frame[data_summary.y_value].max(), 3)
                    text = ""
                    text = text + "Minimum: " + str(y_Min) + "<br>"
                    text = text + "Mean: " +str(y_Mean)+ "<br>"
                    text = text + "Max: " +str(y_Max)+ "<br>"
                    self.display_html(text, "black", "p")
                    if data_summary.HIGH_RANGE_POSITIVE == True:
                        impactTxt = "<b>Positive</b>"
                    if data_summary.HIGH_RANGE_POSITIVE == False:
                        impactTxt = "<b>Negative</b>"

                    x = "The Impact of a high output(ranking) on an individual or group is <b>" + impactTxt + ".</b>"
                    self.display_html(str(x), "black", "p")
                    
                    self.display_html("Select the decision boundary between a positive and negative outcome for logistic regression training.", "black", "h4")
                    text = """Logistic regression is a predictive modelling algorithm that is used when the target (Y )
                            is binary categorical. That is, it can take only two values e.g 1 or 0.
                            The goal is to determine a mathematical equation that can be used to predict the probability 
                            of event 1, if you wish to use logistic regression to predict a successful outcome in terms of """ + data_summary.y_value + """, 
                            you must select a decision boundary after which the continuous value  will represent 1"""
                    self.display_html(text, "black", "p")
                
                    
                    #revert to thevalues as we wish to see them
                   
                    for protected_feat in data_summary.protected_before_transform:
                        data_frame[protected_feat] = self.convert_feature_column(
                                                                 data_frame,
                                                                 protected_feat,
                                                                 data_summary.feature_data_dict[protected_feat])
                        
                    
                    def select_boundary(choose): #local method
                        #plot the representation of data in the dataframe per protected group
                        slider = widgets.IntSlider()
                        
                        def set_outcome (s):
                            #data_summary.y_value
                            if slider.description == "Select Percentile":
                                try:
                                     data_frame.drop(data_summary.y_value +'_binary', axis = 1, inplace = True)
                                except:
                                    pass 
    
                                s = s/100
                                data_frame[data_summary.y_value +'_Percentile_Rank'] = data_frame[data_summary.y_value].rank(pct = True)
                                data_frame.loc[data_frame[data_summary.y_value +'_Percentile_Rank'] >= s, data_summary.y_value+'_binary'] = 1
                                data_frame.loc[data_frame[data_summary.y_value +'_Percentile_Rank'] < s, data_summary.y_value+'_binary'] = 0
                                data_frame.drop(data_summary.y_value +'_Percentile_Rank', axis = 1, inplace = True)
                                #self.display_html(_text, self.text_color, "p")
                                #total = data_frame[[data_summary.y_value, data_summary.y_value+'_binary']].groupby(data_summary.y_value+'_binary').count().reset_index()
                                
                                fig_widget_arr = []
                                tab_titles = []
                                hist_tab = widgets.Tab()
                                
                                count, pcnt = self.view_categorical_counts(data_frame.copy(),
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.HIGH_RANGE_POSITIVE)
                                
                                
                                tab_titles.append("Total count")
                                fig_widget_arr.append(count)
                                tab_titles.append("Total percentage")
                                fig_widget_arr.append(pcnt) 
                                
                                for protected_feat in data_summary.protected_before_transform:
                                    #protected_total = data_frame[[data_summary.y_value, data_summary.y_value+'_binary', protected_feat]].groupby([data_summary.y_value+'_binary',protected_feat]).count().reset_index()
                                    #view_categorical_counts returns go.FigureWidget type.
                                    count, pcnt = self.view_categorical_counts_for_protected(data_frame.copy(),
                                                                 protected_feat, 
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.HIGH_RANGE_POSITIVE)
                                    tab_titles.append(str(protected_feat) + " count")
                                    fig_widget_arr.append(count)
                                    tab_titles.append(str(protected_feat) + " percentage")
                                    fig_widget_arr.append(pcnt)    
                                hist_tab.children = fig_widget_arr
                                for x in range(len(tab_titles)):
                                    hist_tab.set_title(x, tab_titles[x])
                                display(hist_tab)
                                #Now apply the modification to the original input df
                                df[data_summary.y_value+'_binary'] = data_frame[data_summary.y_value+'_binary']
                        
                            elif slider.description == "Select n for Top_n":
                                try:
                                     data_frame.drop(data_summary.y_value +'_binary', axis = 1, inplace = True)
                                except:
                                    pass 
                                #Ascending means smallest to largest, go from smallest to largest, take the value in position s.
                                yDivPoint = data_frame.sort_values(data_summary.y_value,ascending = False).head(s).min()[data_summary.y_value]
                                data_frame.loc[data_frame[data_summary.y_value ] >= yDivPoint, data_summary.y_value+'_binary'] = 1
                                data_frame.loc[data_frame[data_summary.y_value ] < yDivPoint, data_summary.y_value+'_binary'] = 0
                                self.display_html("""The """ + str(s) + """th position has value of <b>""" + str(yDivPoint) + """</b>, any value equal to or above
                                                   this will be set to <b>1</b>. Any value below this will be set to <b>0</b>""", "black", "p")

                                fig_widget_arr = []
                                tab_titles = []
                                hist_tab = widgets.Tab()
                                
                                count, pcnt = self.view_categorical_counts(data_frame.copy(),
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.HIGH_RANGE_POSITIVE)
                                
                                
                                tab_titles.append("Total count")
                                fig_widget_arr.append(count)
                                tab_titles.append("Total percentage")
                                fig_widget_arr.append(pcnt) 
                                
                                for protected_feat in data_summary.protected_before_transform:
                                    #protected_total = data_frame[[data_summary.y_value, data_summary.y_value+'_binary', protected_feat]].groupby([data_summary.y_value+'_binary',protected_feat]).count().reset_index()
                                    #view_categorical_counts returns go.FigureWidget type.
                                    count, pcnt = self.view_categorical_counts_for_protected(data_frame.copy(),
                                                                 protected_feat, 
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.y_value+'_binary',
                                                                 data_summary.HIGH_RANGE_POSITIVE)
                                    tab_titles.append(str(protected_feat) + " count")
                                    fig_widget_arr.append(count)
                                    tab_titles.append(str(protected_feat) + " percentage")
                                    fig_widget_arr.append(pcnt)    
                                hist_tab.children = fig_widget_arr
                                for x in range(len(tab_titles)):
                                    hist_tab.set_title(x, tab_titles[x])
                                display(hist_tab)
                                #Now apply the modification to the original input df
                                df[data_summary.y_value+'_binary'] = data_frame[data_summary.y_value+'_binary']
                                
                        if choose == "Mean":
                            try:
                                data_frame.drop(data_summary.y_value +'_binary', axis = 1, inplace = True)
                            except:
                                pass 
                            text = "Values between " + str(y_Min) + " and " + str(y_Mean) + " will be converted to <b>0</b><br>"
                            text = text + "Values between " + str(y_Mean) + " and " + str(y_Max) + " will be converted to <b>1</b>"
                            self.display_html(text, "black", "p")
                            
                            data_frame.loc[data_frame[data_summary.y_value] >= y_Mean, data_summary.y_value+'_binary'] = 1
                            data_frame.loc[data_frame[data_summary.y_value] <  y_Mean, data_summary.y_value+'_binary'] = 0
                            
                            fig_widget_arr = []
                            tab_titles = []
                            hist_tab = widgets.Tab()

                            count, pcnt = self.view_categorical_counts(data_frame.copy(),
                                                             data_summary.y_value+'_binary',
                                                             data_summary.HIGH_RANGE_POSITIVE)


                            tab_titles.append("Total count")
                            fig_widget_arr.append(count)
                            tab_titles.append("Total percentage")
                            fig_widget_arr.append(pcnt) 

                            for protected_feat in data_summary.protected_before_transform:
                                #protected_total = data_frame[[data_summary.y_value, data_summary.y_value+'_binary', protected_feat]].groupby([data_summary.y_value+'_binary',protected_feat]).count().reset_index()
                                #view_categorical_counts returns go.FigureWidget type.
                               
                                count, pcnt = self.view_categorical_counts_for_protected(data_frame.copy(),
                                                             protected_feat, 
                                                             data_summary.y_value+'_binary',
                                                             data_summary.y_value+'_binary',
                                                             data_summary.HIGH_RANGE_POSITIVE)
                                tab_titles.append(str(protected_feat) + " count")
                                fig_widget_arr.append(count)
                                tab_titles.append(str(protected_feat) + " percentage")
                                fig_widget_arr.append(pcnt)    
                            hist_tab.children = fig_widget_arr
                            for x in range(len(tab_titles)):
                                hist_tab.set_title(x, tab_titles[x])
                            display(hist_tab)
                            #Now apply the modification to the original input df
                            df[data_summary.y_value+'_binary'] = data_frame[data_summary.y_value+'_binary']
                              

                        if choose == "Percentile":
                            slider = widgets.IntSlider(
                                    description = "Select Percentile", 
                                    min=0, max=100,
                                    step=1, value=80, 
                                    continuous_update=False,
                                    style = local_style)
                            interact(set_outcome, s = slider)
                            
                        if choose == "Top-n":
                            slider = widgets.IntSlider(
                                    description = "Select n for Top_n", 
                                    min=10, max=1000,
                                    step=10, value=100, 
                                    continuous_update=False,
                                    style = local_style) 
                            interact(set_outcome, s = slider)
                            
                    _choose = widgets.Dropdown(
                                    description = "Decision boundary determined by", 
                                    options = ["Mean","Top-n","Percentile"],
                                    layout = local_layout,
                                    style = local_style)

                    interact(select_boundary, choose = _choose)
                    

                    change = widgets.Button(description="View dataframe head")
                    button_output = widgets.Output()
                    def on_button_clicked(b):
                        with button_output:
                            clear_output(wait = True)
                            display(df.head(5))
                    change.on_click(on_button_clicked)
                    display(change, button_output)
                
        except Exception as e:
            self.display_html("Something went wrong in method", self.text_color, "h4")
            print (e)
        
          
    #################################################################################################
    #  
    # 
    #################################################################################################         
    def create_label (self, row):
            
            names = list (row.index)
            values = list( row.values)
            text = ""
            for i in range (len(names)):
                text = text + ":" + names[i] + "_" + str(values[i])
            text = text[1:]            
            return text       
    #################################################################################################
    #  
    # 
    #################################################################################################       
    def plot_donut(self, attributes_list, data_frame, w=800, h=800, title = "Result"):
    
        num_of_donuts = len(attributes_list)
        if num_of_donuts > 6:
            num_of_donuts = 6
            display (HTML("showing only the first 6 attributes"))
        
        sequential_color_list = [
            px.colors.sequential.Blues,
            px.colors.sequential.Greens, 
            px.colors.sequential.Oranges, 
            px.colors.sequential.Purples,
            px.colors.sequential.Reds,
            px.colors.sequential.Greys,
            px.colors.sequential.algae,
            px.colors.sequential.amp]
    
        color_pool = cycle(sequential_color_list)
    
        pie_list = []    
        labels_arr = []
        values_arr = []
        color_arr = []
        annotations_arr = []
        annotate = dict(text='woops', 
            x=0.5, y=0.6, 
            font_size=15, 
            showarrow=False)
        
        attribute_hierarchy = []
        for a, pos in zip (attributes_list, range(len(attributes_list))):
            attribute_hierarchy.append(a)
            annotate['text'] = a
            annotate['y'] = annotate['y']-0.05
            annotations_arr.append(annotate.copy())
            data_frame["count"] = 0
            df = data_frame[attribute_hierarchy+["count"]].fillna("@Unknown").groupby(attribute_hierarchy).count().reset_index().rename(columns={"count": "values"})
            df['labels'] =  df.apply(lambda row : self.create_label(row[attribute_hierarchy]), axis = 1) 
            df['values'].fillna(0,inplace=True)
            c = []
            s = []
            if pos == 0:
                for l in range (len(df['labels'].to_numpy())):
                    c.append(next(color_pool)[0])
                    if l >= len(sequential_color_list):
                        l = l - len(sequential_color_list)
                    s.append(l)
                df['colors'] = c
                df['color_pool_pos'] = s
                
            else:
                temp_list = list(df['values'].to_numpy())#changed from .list
                for count, color_index in zip(prev_counts, prev_color_pool) :
                    match = 0
                    for value, pos in zip (temp_list, range(len(temp_list))):
                        s.append(color_index)
                        try:
                            c.append (sequential_color_list[color_index][pos+1])
                        except:
                            c.append (sequential_color_list[color_index][2])
                        match = match + value
                        if match == count:
                            del temp_list[0:pos+1]
                            break
                df['colors'] = c
                df['color_pool_pos'] = s
            labels_arr.append (df['labels'])
            values_arr.append (df['values'])
            color_arr.append (df['colors'])
        
            prev_counts = df['values'].values
            prev_color_pool = df['color_pool_pos'].values
        hole = 0.8
        x1 = 0
        x2 =1
        y1 = 0
        y2 = 1
        adjust = round((1.0 - hole)* 0.5,2) 
        for x in range (num_of_donuts):
            pie_list.append(go.Pie(
            hole=hole, #Sets the fraction of the radius to cut out of the pie. Use this to make a donut chart
            sort=False,
            direction='clockwise',
            domain={'x': [x1, x2], 'y': [y1, y2]},
            values=values_arr[x],
            labels=labels_arr[x],
            textinfo='label+percent',
            textposition='inside',
            name=attributes_list[x],
            marker={'colors': color_arr[x],'line': {'color': 'black', 'width': 1}}
            ))
            hole= round(hole - adjust, 2)
            x1 = round (x1 + adjust, 2)
            x2 = round (x2 - adjust, 2)
            y1 = round (y1 + adjust, 2)
            y2 = round (y2 - adjust, 2)
         
        
        fig = go.FigureWidget(data=pie_list);#need to reverse the order?
        fig.update_layout(autosize=False,
                          width=w,
                          height=h,
                          margin=dict(l=50,r=50,b=100, t=100,pad=4),
                          title=str(attribute_hierarchy),
                          #Add annotations in the center of the donut pies.
                          annotations=annotations_arr,
                          legend_orientation="h",
                           #paper_bgcolor='rgba(113, 136, 136, 1)', #for transparent set to (0,0,0,0)
                          #plot_bgcolor='rgba(113, 136, 136, 1)',
                    );

        fig.update_traces(textposition='inside');
        fig.update(layout_title_text=title,
               layout_showlegend=False );
        df["all"] = "all"
        fig_2 = px.treemap(df, 
                           path=["all"]+attributes_list, 
                           values='values',  
                          )
        
        fig_2.data[0].textinfo = 'current path+ label+value+percent parent+percent root'
         # # # # # Now create one donut per protected attribute for a clearer view if the call specifies this# # # # # # 
        fig_2.update(layout_title_text=title,
               layout_showlegend=True );
        fig_wig_2 = go.FigureWidget(fig_2);

        #as this can be a pointer to the input, clean it up
        data_frame.drop(["count"], axis=1, inplace = True)
        gc.collect()
        return fig, fig_wig_2
        
    #################################################################################################
    # Pearson’s Chi-Squared Test....
    # METHOD USED TO Perform Independent chi_square_test. can be used as a test for independance
    # between categorical variables
    #################################################################################################
    #################################################################################################
    def get_chi_square_test_info(self, df, feature, protected_feature, ref_group): 
        '''A categorical variable is a variable that may take on one of a set of labels.
           Here we will examine a categorical variable as they pertain to another categorical label, 
           specifically a protected feature such as Gender(Male, Female), or Race(Black, White)
           as it pertains to another variable such as Score, Success etc,
            Large values of X^2 indicate that observed and expected frequencies are far apart. 
            Small values of X^2 indicate that observed are close to expecteds.
            X^2 give a measure of the distance between observed and expected frequencies.
            expected frequency is that there will be no difference between observed and expected
            above what would be expected by chance (no statistically significant difference)'''
        try:
            groups = df[protected_feature].dropna().unique()
            table = pd.crosstab(df[protected_feature], df[feature])
            prob = 0.95
            

            #can be used to create multiple plots, however we only call it with attribute_list of len 1.            
            def test_res(group_1, group_2):
                filter_table  = table[table.index.isin([group_1,group_2])]
                for col in filter_table.columns:
                    if filter_table[col].sum() == 0:
                        filter_table.drop(col, inplace=True)
                chi2_stat, p_value, dof, expected = chi2_contingency(filter_table)
                ######
                #Interprert the critical value
                # critical = chi2.ppf(prob, dof)
                #print ("critical(chi2.ppf(prob, dof)): ", critical)
                #if abs(chi2_stat) >= critical:
                     #print('Dependent (reject H0)')
                #else:
                   #print('Independent (fail to reject H0)')
                #######

                # interpret p-value for consistency with other test
                     #alpha = 1.0 - prob
                    #print('significance=%.3f, p=%.3f' % (alpha, p_value))

                     #if  p_value <= alpha:
                     #    print('Dependent (reject H0)')
                     #else:
                     #    print('Independent (fail to reject H0)')

                ####

                matrix_twosample = [
                                    ['', 'Chi-2 Test Statistic(T-Value)', 'P-value'],
                                    ['Sample Data', abs(chi2_stat), p_value]
                                    ]

                wig2 = go.FigureWidget(ff.create_table(matrix_twosample, index=True))
                display (wig2)
                text = "There is a "+ str (round ((p_value*100),3)) +  "% probability that a difference of " + str(chi2_stat)
                text = text + """ occured by chance. A usual interpretation is that a p-value of less than 0.05 (5% probability)
                is deemed to indicate that the difference has not occured by chance (rejecting H0)"""

                self.display_html(text, self.text_color, "p")

            self.display_html("Chi-Squared T-Test ", "black", "h3")
            text = ''' <b>Significant variance:</b> The statistic test will tell us if there is a significant difference in the 
                        distribution of categories, if this difference is due to chance, or how likely it is that it is not due to chance but
                        rather to an unobserved factor. <br>


                        <b>T-Value:</b>This value represents the distance between the observed distribution
                        and the expected distribution in a fair world. 
                        The larger the value of T, the greater the evidence against the difference
                        occuring by chance in a fair world. <br>'''
            self.display_html(text, "black", "p")

            interact(test_res, 
                        group_1 = widgets.Dropdown(description = "Reference Group", 
                                                   options =  groups, 
                                                   value = ref_group,
                                                   style = {'description_width': 'initial'}),
                        group_2 = widgets.Dropdown(description = "Focal Group", 
                                                   options =  groups)
                );

        except Exception as e:
            self.display_html("Something went wrong generating the distribution, change the distribution type and ensure group is represented sufficiently to generate dist", 
                              self.text_color, "h4")
            print (e)  

            
            
            
            
            
    #################################################################################################
    #  
    # METHOD USED TO Perform Independent t-Test. A t-test is a type of inferential statistic which is used to
    # determine if there is a significant difference between the means of two groups which may be 
    # related in certain features
    #################################################################################################
    def get_t_test_info(self, dist_output_per_group, groups, ref_group):
        try:
            #can be used to create multiple plots, however we only call it with attribute_list of len 1.            
            def test_res(group_1, group_2):
                group_index_1 = list(groups).index(group_1)
                group_index_2 = list(groups).index(group_2)

                twosample_results = stats.ttest_ind(dist_output_per_group[group_index_1],  dist_output_per_group[group_index_2])
                matrix_twosample = [
                                    ['', 'Test Statistic(T-Value)', 'P-value'],
                                    ['Sample Data', twosample_results[0], twosample_results[1]]
                                    ]

                wig2 = go.FigureWidget(ff.create_table(matrix_twosample, index=True))
                display (wig2)
                text = "There is a "+ str (round ((twosample_results[1]*100),3)) +  "% probability that a difference of " +str(twosample_results[0]) +" occured by chance."
                self.display_html(text, self.text_color, "p")
           
            self.display_html("Two-Tailed T-Test ", "black", "h3")
            text = ''' <b>Significant variance:</b> The statistic test will tell us if there is a significant variance in the distribution 
                        and if this variance is due to chance, or how likely it is that it is not due to chance but
                        rather to an unobserved factor. <br>
                        
                        
                        <b>T-Value:</b>This value represents the distance between the observed distribution
                        and the expected distribution in a fair world. 
                        The larger the value of T, the greater the evidence against the difference
                        occuring by chance in a fair world. <br>'''
            
            self.display_html(text, "black", "p")    
            interact(test_res, 
                        group_1 = widgets.Dropdown(description = "Reference Group", 
                                                   options =  groups, 
                                                   value = ref_group,
                                                   style = {'description_width': 'initial'}),
                        group_2 = widgets.Dropdown(description = "Focal Group", 
                                                   options =  groups)
                );
                 
                            

        except Exception as e:
            self.display_html("Something went wrong generating the distribution, change the distribution type and ensure group is represented sufficiently to generate dist", 
                              self.text_color, "h4")
            print (e)

           
        
    #################################################################################################
    #  
    # METHOD USED TO PLOT THE DISTRIBUTION OF THE OUTCOME ACROSS GROUPS
    #################################################################################################
    
    def plot_distribution(self, 
                          attribute, 
                          y, 
                          data_frame, 
                          w=800, h=800, 
                          y_high_positive = True, 
                          curve_type = "kde"):
        try:
            #can be used to creatr multiple plots, however we only call it with attribute_list of len 1.
            dist_output_per_group = []
            group_labels = []
            groups = data_frame[attribute].dropna().unique()
            #For every group in the protected feature
            
            
            for group in range(len(groups)):
                group_df = data_frame[data_frame[attribute] == groups[group]]
                dist_output_per_group.append(group_df[y])
                group_labels.append(attribute + "-" + str(groups[group]))
                # Add histogram data
                # Group data together
                
            #Add the dist of all combined groups
            dist_output_per_group.append(data_frame[y])
            group_labels.append("All")
            
            # Create distplot with custom bin_size
            
            # Add title
            
            wig = go.Figure(ff.create_distplot(dist_output_per_group, 
                                           group_labels, 
                                           curve_type = curve_type, 
                                           show_hist=False) )#, bin_size=[.1, .25, .5, 1])
    
            with wig.batch_update():
                wig.update_layout(autosize=False,
                              width=900,
                              height=500,
                              #margin=dict(l=50,r=50,b=100, t=100,pad=4),
                              #paper_bgcolor="LightSteelBlue",
                              title=y +' distribution across ' + attribute,
                              xaxis=dict(range=[data_frame[y].min(), data_frame[y].max()])
                            )
            
            img_bytes = wig.to_image(format="png", engine="kaleido")
            wig.write_html("output_dist.html")

            image_wig = widgets.Image(value=img_bytes,
                                   format='png',
                                   width=800,
                                   height=500)
            

            del wig
            return image_wig, dist_output_per_group, groups

        except Exception as e:
            self.display_html("Something went wrong generating the distribution, change the distribution type and ensure group is represented sufficiently to generate dist", 
                              self.text_color, "h4")
            print (e)

        
    
    #################################################################################################
    #  #NOT FULLY IMPLEMENTED
    # 
    #################################################################################################
    def plot_output_ratios( ):
        sequential_color_list = [
            px.colors.sequential.Greens, 
            px.colors.sequential.Greys]

        df_ratios = data_frame[attributes_list+[impact_col_name]+[y_value]].groupby(attributes_list+[impact_col_name]).count().reset_index().rename(columns={y_value: "values"})     
        
        _total =  df_ratios['values'].sum()
        _total_pos =  df_ratios[(df_ratios[impact_col_name]=="Pos")]['values'].sum()
        _total_neg =  df_ratios[(df_ratios[impact_col_name]=="Neg")]['values'].sum()
        one, isto = self.ratio(_total_pos, _total_neg)
        df_ratios['labels'] =  df_ratios.apply(lambda row : self.create_label(row[attributes_list]), axis = 1) 
        df_ratios['labels'].fillna(0,inplace=True)
        attr_list = []
        attr_list.append("All")
        isto_list = []
        isto_list.append(isto)
        pcnt_list = []
        pcnt_list.append((_total_pos/(_total_pos+_total_neg))*100)
        for label in df_ratios['labels'].dropna().unique():
            pos = df_ratios[(df_ratios['labels']==label) & (df_ratios[impact_col_name]=="Pos")]['values']
            neg = df_ratios[(df_ratios['labels']==label) & (df_ratios[impact_col_name]=="Neg")]['values']
            one, isto = self.ratio(pos.values[0], neg.values[0])
            attr_list.append(label)
            isto_list.append(isto)
            pcnt = (pos.values[0]/(pos.values[0]+neg.values[0]))*100
            if math.isnan(pcnt):
                pcnt_list.append(0)
            else:
                pcnt_list.append(pcnt)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
                            x=attr_list,
                            y=isto_list,
                            marker_color='indianred'
                        ))


            # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig1.update_layout(xaxis_tickangle=-45, 
                           title = "Ratio of Positive to Negative (for each 1 positive effect)",
                          autosize=False,
                          width=900,
                          height=400,)
        
        fw = go.FigureWidget(fig1)
    

    #################################################################################################
    #  
    # 
    ################################################################################################# 
    def label_encoding(self, attributes_list, data_frame):
        # creating initial dataframe
        labelencoder = LabelEncoder()
        return_dict = {}
        for attribute in attributes_list:
            categories = data_frame[attribute].dropna().unique()
            temp_df = pd.DataFrame(categories, columns=[attribute])
            # Assigning numerical values and storing in another column
            temp_df[attribute+"_benc"] = temp_df[attribute]
            temp_df[attribute] = labelencoder.fit_transform(temp_df[attribute])
            # Convert this Temp_df into a dictionary
            temp_df.set_index(attribute+"_benc", inplace=True)
            return_dict.update(temp_df.to_dict())
            data_frame[attribute+"_benc"] = data_frame[attribute]
            data_frame[attribute] = labelencoder.fit_transform(data_frame[attribute])
        return return_dict
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################   
    def gcd(self, p, q): 
        if (q == 0): 
            return p
        else:
            return min(q, p)

    def ratio(self, a,b):
        _gcd = self.gcd(a,b)
        one = round(a/_gcd, 2)
        isto = round(b/_gcd, 2)
        if one != 1:
            isto = round (1/one, 2)
            one = 1.0
        return one, isto

    
    #################################################################################################
    #  VIEW FAIRNESS MATRICS AEQUITAS
    # 
    #################################################################################################
    """Difference in means: The difference between the probability for a member of group-a be selected and 
        the probability for a member of group-b to be selected.

        Disparate Impact: the Probability of a member of group-a be selected to be selected divided by
        the probability of a member of group-b to be selected

        False positive rate Ratio of false positive ratio's among protected groups

       False negative rate: Ratio of false negative ratio's among protected groups"""
            
    #################################################################################################
    #  VIEW FAIRNESS MATRICS AEQUITAS
    # 
    #################################################################################################
    """Difference in means: The difference between the probability for a member of group-a be selected and 
        the probability for a member of group-b to be selected.

        Disparate Impact: the Probability of a member of group-a be selected to be selected divided by
        the probability of a member of group-b to be selected

        False positive rate Ratio of false positive ratio's among protected groups

       False negative rate: Ratio of false negative ratio's among protected groups"""
            
    def view_aequitas_fairness_metrics(self, 
                                       X_df, 
                                       y_target, 
                                       y_pred,
                                       data_summary):
        #copying it here so we do not make any modifications to the original
        X_data_frame = X_df.copy()
        y_column_name = y_target.name
        _w=600
        _h=600
        protected_attributes_list = data_summary.protected_before_transform
        feature_data_dict = data_summary.feature_data_dict
        y_high_positive = data_summary.HIGH_RANGE_POSITIVE
        aeq_Plot = Plot()
        aeq_Group = Group()
        aeq_Bias = Bias()
        aeq_Fairness = Fairness()

        out1 = widgets.Output(layout={})
        out2 = widgets.Output(layout={})
        out3 = widgets.Output(layout={})
        out4 = widgets.Output(layout={})
        out5 = widgets.Output(layout={})
        out6 = widgets.Output(layout={})
        out7 = widgets.Output(layout={})
        tab_contents = [out1, out2, out3, out4, out5, out6,out7]
        
        children = tab_contents
        tab = widgets.Tab(style={'description_layout':'auto', 'title_layout':'auto'})
        tab.children = children
        
        tab.set_title(0, "Confusion Matrix")
        tab.set_title(1, "False Positive")
        tab.set_title(2, "False Negative")
        tab.set_title(3, "All Metrics")
        tab.set_title(4, "Disparate Impact")
        tab.set_title(5, "Fairness")
        tab.set_title(6, "Metrics reminder")
        
        local_layout = {'width': 'auto', 'visibility':'visible'}
        local_layout_hidden  = {'width': 'auto', 'visibility':'hidden'}
        local_style = {'description_width':'initial'}
        
        #Convert the protected feature columns back to their values
        #before label encoding or one-hot encoding
        for feature in protected_attributes_list:
            X_data_frame[feature] = self.convert_feature_column(X_data_frame,
                                        feature,
                                        feature_data_dict[feature])
        
        _choose_a = widgets.Dropdown(description = "Select protected feature", 
                                     options = protected_attributes_list,
                                     layout = local_layout,
                                     style = local_style)
          
        _choose_b = widgets.Dropdown(description = "Select protected group", 
                                             options = X_data_frame[_choose_a.value].dropna().unique(),
                                             layout = local_layout,
                                             style = local_style)
        
        _choose_measure = widgets.Dropdown(description = "Select metric", 
                                             options = {'False Omission Rate' : 'for',
                                                        'False Discovery Rate' :'fdr',
                                                        'False Positive Rate': 'fpr',
                                                        'False Negative Rate': 'fnr',
                                                        'Negative Predictive Value': 'npv',
                                                        'Precision': 'precision',
                                                        'Predicted Positive Ratio_k' :'ppr',
                                                        'Predicted Positive Ratio_g': 'pprev',
                                                        'Group Prevalence':'prev'},
                                             layout = local_layout,
                                             value = 'precision',
                                             style = local_style)
    
        
        _choose_disparity_measure = widgets.Dropdown(description = "Select disparity metric", 
                                             options = {'False Positive Rate disparity': 'fpr_disparity',
                                                        'False Negative Rate disparity': 'fnr_disparity',
                                                        'Predicted Positive Ratio_k' : 'ppr_disparity',
                                                        'Predicted Positive Ratio_g disparity' :'pprev_disparity',
                                                        'Precision Disparity': 'precision_disparity',
                                                        'False Discovery Rate disparity': 'fdr_disparity',
                                                        'False Omission Rate disparity': 'for_disparity',
                                                        'True Positive Rate disparity': 'tpr_disparity',
                                                        'True Negative Rate disparity': 'tnr_disparity',
                                                        'npv_disparity': 'npv_disparity',},
                                             layout = local_layout,
                                             value = 'fpr_disparity',
                                             style = local_style)
        
        html = '''<h3>Aequitas fairness via Machnamh: </h3> Aequitas is an open source bias audit toolkit for
        machine learning developers, analysts, and  policymakers to audit machine learning models for discrimination
        and bias, and make informed and equitable decisions around developing and deploying predictive risk-assessment 
        tools.<br>The Machnamh framework provides a dynamic interface to Aequitas API allowing for quick analysis and a useful
        user interface to help facilitate the translation of results'''
        display (HTML(html))
        display(tab)
        
        df_aequitas = pd.concat([X_data_frame[protected_attributes_list],
                                        y_target,
                                        pd.DataFrame(y_pred, 
                                        index=X_data_frame.index)],
                                        axis=1, sort=False);
        
    
        #Aequitas needs the true-y_value column to be called 'label_value'
        # and the prediction to be called 'scire'
        df_aequitas.rename(columns={y_column_name: 'label_value',
                                    0: 'score'}, 
                           inplace=True);
        
        df_aequitas[df_aequitas.columns.difference(['label_value', 'score'])] = df_aequitas[
                                                    df_aequitas.columns.difference(['label_value', 'score'])].astype(str);
                
        
        cross_tab, _ =  aeq_Group.get_crosstabs(df_aequitas)
        cross_tab.fillna(0, inplace = True)
        absolute_metrics = aeq_Group.list_absolute_metrics(cross_tab) 
        #columns not in absolute Matrix
        counts_metrics = list (cross_tab[[col for col in cross_tab.columns if col not in absolute_metrics]].columns.values)
        counts_metrics.remove('model_id') 
        counts_metrics.remove('score_threshold') 
        counts_metrics.remove('k') 
        
        ## Read images from file (because this is binary, maybe you can find how to use ByteIO) but this is more easy
        path = os.path.dirname(sys.modules[__name__].__file__)
        img2 = open(path + '/data/count.png', 'rb').read()
        img1 = open(path + '/data/absolute.png', 'rb').read()
        ## Create image widgets. You can use layout of ipywidgets only with widgets.
        ## Set image variable, image format and dimension.
        wi1 = widgets.Image(value=img1, format='png', width=300, height=400)
        wi2 = widgets.Image(value=img2, format='png', width=300, height=400)
        ## Side by side thanks to HBox widgets
        sidebyside = widgets.HBox([wi1, wi2])
        ## Finally, show.
        
        with out1:
            clear_output(wait = True)
            tab = widgets.Tab()
            tab_names = []
            output_arr = {}
            for feature in protected_attributes_list:
                priv = str(feature_data_dict[feature]['privileged_description'])
                output_arr[feature] = widgets.Output(layout={})
                
                with output_arr[feature]:
                    beneficial = ""
                    punative = ""
                    if  y_high_positive == True:
                        html = """You have indicated that a high ranking is beneficial to an individual or 
                                        group, therefor <font color='red'><b>false negatives</b></font> can be particularally harmful.
                                        in terms of fairness!"""
                        beneficial = ['tp','fp']
                        punitive =   ['tn','fn']
                        equal_oppertunity = '''In this case a high outcome(or binary one) is <font color='green'>beneficial </font>so we are quantifying the equal oppertunity to have an apparently deserved <font color='green'>beneficial outcomes</font> (TPR)'''
                        
                        equal_odds = ''', and to have an apparently undeserved<font color='green'> beneficial outcome</font>'''
                        
                        equal_oppertunity_2 = ''

                    
                    elif y_high_positive == False:
                        html = """You have indicated that a low ranking is beneficial to an individual or 
                                        group, therefor <font color='red'><b>false positives</b></font> can 
                                        be particularally harmful in terms of fairness!"""
                        beneficial = ['tn','fn']
                        punitive =   ['tp','fp']
                        equal_oppertunity = '''In this case a high outcome(or binary one) is <font color='red'>not beneficial </font>so we are quantifying the equal oppertunity to have <font color='red'>an
                          apparently deserved non-beneficial outcome</font> '''
                        equal_odds = ''', and to have an apparently undeserved<font color='green'> non-beneficial outcome.</font>'''
                        
                        equal_oppertunity_2 = ''' Rectifying any discrepencies in
                          oppertunity to a non-benificial outcome will cause negative outcomes for additional individuals.'''
                    widgHTML = widgets.GridBox(children=[widgets.HTML(html)],
                        layout=Layout(
                        width='90%',
                        )
                   )  
                    display (widgHTML)
                    one = widgets.Output(layout={})
                    two = widgets.Output(layout={})
                    three = widgets.Output(layout={})
                    
                    accordion1 = widgets.Accordion(children=[one, two, three])
                    accordion1.set_title(0, "Absolute Metrics across " + feature  + " groups")  
                    accordion1.set_title(1, "Group counts across " + feature + " groups")  
                    accordion1.set_title(2, "Metrics description ")  
                    with one:
                        included = ['attribute_name', 'attribute_value'] + absolute_metrics
                        display ( cross_tab[included][ cross_tab[included]['attribute_name'] == feature].round(2))
                    with two:
                        display (cross_tab[counts_metrics][ cross_tab[counts_metrics]['attribute_name'] == feature] )
                    with three:
                        display(sidebyside)
                    accordion1.selected_index = None
                    display(accordion1)
                    self.make_confusion_matrix(cross_tab[counts_metrics], 
                                              feature,
                                              group_names = ['True Neg','False Pos','False Neg','True Pos'],
                                              categories='auto',
                                              count=True,
                                              percent=True,
                                              cbar=True,
                                              xyticks=True,
                                              xyplotlabels=True,
                                              sum_stats=True,
                                              figsize=(3,3),
                                              cmap='Blues',
                                              title=None)
                   
                
                    fairness_measures_pd = cross_tab[counts_metrics][ cross_tab[counts_metrics]['attribute_name'] == feature]
                    
                    ###### Proportional parity#########                 
                    fairness_measures_pd["Beneficial outcome percentage"] = fairness_measures_pd.apply(lambda row: ((row[beneficial[0]] + row[beneficial[1]])/row["group_size"])*100, axis=1)
                    fairness_measures_pd["Beneficial outcome percentage"]  = round(fairness_measures_pd["Beneficial outcome percentage"],2)
                     
                    fairness_measures_pd["Punative outcome percentage"] = fairness_measures_pd.apply(lambda row: ((row[punitive[0]] + row[punitive[1]])/row["group_size"])*100, axis=1)
                    fairness_measures_pd["Punative outcome percentage"] = round(fairness_measures_pd["Punative outcome percentage"],2) 
                    display (HTML("""<h2><font color='green'>Proportional parity</h2><font color='black'>
                                    <b>Proportional parity:</b> 
                                    Proportional parity is a representational based group fairness metric
                                    which states that each group should have the same proportion of
                                    beneficial(non-punative) outcomes. A desire to correct for the 
                                    absence of proportional parity (when no biological or inherent
                                    reason accounts for its' absence) reflects a worldview which recognises
                                    the existance of prejudice and a wish to create a "decision maker" 
                                    willing to apply corrective measures to counter historical discrimination
                                    against a particular group or groups and ensure that all groups are 
                                    proportionately represented in beneficial outcomes. The "decision maker" is
                                    aware that such intervention may be reflected in a reduction of perceived utility
                                    of <i>current</i> model accuracy.<br>
                                    <b>Note</b> These values are calculated based on the group
                                                representation in the sample which does not necessarally match that of 
                                                the population or the domain in which the model will be used.<br>"""))
                                                
                    display (HTML("The privileged group has been set as: " + priv))
                    display(fairness_measures_pd[["attribute_value","Beneficial outcome percentage","Punative outcome percentage"]].rename(columns = {'attribute_value': 'Group'}))
        
                    ####### Demographic parity (TP+FP) or (TN+FN) should be the same######### 
                    fairness_measures_pd["Beneficial outcome count"] = fairness_measures_pd.apply(lambda row: (row[beneficial[0]] + row[beneficial[1]]), axis=1)
                    fairness_measures_pd["Punative outcome count"] = fairness_measures_pd.apply(lambda row: (row[punitive[0]] + row[punitive[1]]), axis=1)
                    display (HTML("""<h2><font color='green'>Demographic parity</h2><font color='black'>
                                <b>Demographic parity:</b> (also known as Independence or Statistical Parity,) is a 
                                representation based group fairness metric which states that each group
                                should have an equal number of beneficial(non-punative) outcomes. 
                                A desire to correct for the absence of demographic parity (when no biological 
                                or inherent reason accounts for its' absence) reflects a worldview which recognises
                                the existance of prejudice and a wish to create a "decision maker" willing to apply
                                corrective measures to counter historical discrimination against a particular group
                                or groups and ensure that all groups are proportionately represented in beneficial
                                outcomes. The "decision maker" is aware that such intervention may be reflected in a
                                reduction of perceived utility of <i>current</i> model accuracy. """))
                                
                    display (HTML("The privileged group has been set as: " + priv))
                    display(fairness_measures_pd[["attribute_value","Beneficial outcome count","Punative outcome count"]].rename(columns = {'attribute_value': 'Group'}))
                    
                    ####### Equal oppertunity############################### 
                    def tpr(row):
                      try: 
                        row = row["tp"] / (row["tp"] + row["fn"])
                      except: 
                        row = "0"
                      return round(row * 100,2)
                    fairness_measures_pd["True positive rate percentage"] = fairness_measures_pd.apply(lambda row: tpr(row),axis=1)
                    
                    fairness_measures_pd["Proportional to "+priv] = fairness_measures_pd.apply(lambda row: tpr(row),axis=1)

                    
                    display (HTML("""<h2><font color='green'>Equality of oppertunity</h2><font color='black'>
                    <b>Equality of opportunity:</b> is an accuracy related fairness that
                    is satisfied if the model correctly predicts class 1 
                    outcomes at equal rates across groups. A desire by a 'decision maker' to
                    satisfy equality of oppertunity reflects a worldview belief that we 
                    should ensure that those who appear to deserve a certain outcome(assistive or punitive )
                    should obtain that outcome independant of the group they belong to and that this outcome should be
                    the same rate across groups, the desire is to ensure that no further prejudice or unfairness 
                    occurs although there is no consideration to actively apply corrective measures to counter 
                    historical discrimination reflected in the features used to determine the outcome.
                    There is also no concern given to those situations where an outcome is incorrectly
                    given when not deserved(which may indicate favoritism towards a particular group)<br> """ + equal_oppertunity + equal_oppertunity_2 +'''<br><br>The True Positive Rate (TPR) should be the same for each group, to satisfy Equality of opportunity.'''))
                   
                    display (HTML("The privileged group has been set as: " + priv))
                    display(fairness_measures_pd[["attribute_value","True positive rate percentage"]].rename(columns = {'attribute_value': 'Group'}))
                    
                    ######################Equalized odds ######################
                    def fpr(row):
                      try: 
                        row = row["fp"] / (row["fp"] + row["tn"])
                      except: 
                        row = "0"
                      return round(row * 100,2)
                    fairness_measures_pd["False positive rate percentage"] = fairness_measures_pd.apply(lambda row: fpr(row),axis=1)

                    display (HTML("""<h2><font color='green'>Equalized odds</h2><font color='black'>
                    <b>Equalized odds:</b> is an accuracy related fairness that
                    is satisfied if the model correctly predicts true class 1 
                    outcomes at equal rates across groups. A desire by a 'decision maker' to
                    satisfy equality of oppertunity reflects a worldview belief that we 
                    should ensure that those who appear to deserve a certain outcome(assistive or punitive )
                    should obtain that outcome independant of the group they belong to, and that those who
                    do not deserve the outcome, should not obtain it(should not be mis-classified) and this should be the
                    same rate across groups, the desire is to ensure that no further prejudice or unfairness occurs either through prejudice or favoritism, although there is no consideration to actively apply corrective measures to counter historical discrimination reflected in the features used to determine the outcome.
                    )<br> """ + equal_oppertunity + equal_odds + equal_oppertunity_2 +'''<br><br>The True Positive Rate (TPR) and False Positive Rate (FPR) should be the same for each group to satisfy Equalised odds.'''))
                    
                    display (HTML("The privileged group has been set as: " + priv))
                    display(fairness_measures_pd[["attribute_value","True positive rate percentage", "False positive rate percentage"]].rename(columns = {'attribute_value': 'Group'}))
                    
                    
                    
            
            tab.children = list(output_arr.values())
            for i in range(len(protected_attributes_list)):
                tab.set_title(i, protected_attributes_list[i])

            display (tab)
            
        with out2: #False Positive
            clear_output(wait = True)
            html = """<b>False Positive Rate:</b> The model predicted the subjects outcome 
            was positive when in fact it was not, in other words <b>an incorrect decision to 
            recommend for action!</b>"""

            if  y_high_positive == True:
                html = html + '''You have indicated that a high outcome (ranking) has a positive impact on an individual
                                therefore a high false positive rate will have a <font color='green'><b>positive impact</b></font>  on an individual or group.
                                '''
            elif y_high_positive == False:
                html = html + '''You have indicated that a high outcome (ranking) has a negative impact on an individual
                                therefore a high false positive rate will have a <font color='red'><b>negative impact</b></font> on an individual or group.
                                '''
            
            
            
            widgHTML = widgets.GridBox(children=[widgets.HTML(html)],
                        layout=Layout(
                        width='90%',
                        )
                   )      
            display (widgHTML)
            fig1, (ax1) = plt.subplots(nrows=1, figsize=(10 ,5));
            ax1 = aeq_Plot.plot_group_metric(cross_tab,'fpr', ax1);
            plt.tight_layout();
            ax1.set_title('False Positive ratios');
            plt.show();
            plt.close(fig1);
            plt.clf();
        
        
        with out3:#False Negative
            clear_output(wait = True)
            html = """<b>False Negative Rate:</b> The model predicted the subjects outcome was negative
            when in fact it was not, in other words <b>an incorrect decision not to recommend for action!</b> """
            if  y_high_positive == True:
                html = html +  '''You have indicated that a high outcome (ranking) has a positive impact on an individual
                                therefore a high false negative rate will have a<font color='red'> <b>negative impact </b></font> on an individual or group.
                                '''
            elif y_high_positive == False:
                html = html + '''You have indicated that a high outcome (ranking) has a negative impact on an individual
                                therefore a high false negative rate will have a <font color='green'><b>positive impact </b></font> on an individual or group.
                                '''
            widgHTML = widgets.GridBox(children=[widgets.HTML(html)],
                        layout=Layout(
                        width='90%',
                        )
                   )      
            display (widgHTML)
            fig1, (ax1) = plt.subplots(nrows=1, figsize=(10 ,5));
            ax1 = aeq_Plot.plot_group_metric(cross_tab,'fnr', ax1);
            plt.tight_layout();
            ax1.set_title('False Negative ratios');
            plt.show()
            plt.close(fig1);
            plt.clf();
            
        with out4:#ALL metrics
            clear_output(wait = True)
            
            if  y_high_positive == True:
                html =  '''You have indicated that a <b>high outcome(ranking)</b> has a<font color='green'> <b>positive impact</b></font> on an individual.
                                '''
            elif y_high_positive == False:
                html =  '''You have indicated that a <b>high outcome(ranking)</b> has a <font color='red'></b>negative impact</b></font> on an individual.
                               '''
            display (HTML(html))
            def show_any(choose_measure):
                fig1, (ax1) = plt.subplots(nrows=1);
                ax1 = aeq_Plot.plot_group_metric(cross_tab, choose_measure, ax1)
                plt.tight_layout()
                ax1.set_title(choose_measure)
                plt.show()
                plt.close(fig1)
                plt.clf()
            interact(show_any, choose_measure = _choose_measure);
   
        with out5: #Disparate 
            clear_output(wait = True)
            dict_of_controls = {}
            
            dis_imp_html = '''<b>Disparate Impact:</b> A decision-making process suffers from disparate impact if the outcome 
            of the decision disproportionately benefits one group or disproportionately hurts another group.
            It generally results from unintentional discrimination in decision-making systems.
            Disparities are calculated as a ratio of a metric for a group of interest compared to a reference group. 
            For example, the False Negative Rate Disparity for Group-A compared to a reference Group-B is: FNR-B/FNR-A
            The calculated disparities are in relation to a reference group, which will always 
            have a disparity of 1.0. Disparate impact is often measured by the eighty percent or four-fifths rule. '''
            
            widgHTML = widgets.GridBox(children=[widgets.HTML(dis_imp_html)],
                        layout=Layout(
                        width='90%',
                        )
                   )  
            display (widgHTML)
        
        
            for feature in protected_attributes_list:
                dict_of_controls[feature] = widgets.Dropdown(description = "Reference group for "+feature, 
                                             options = X_data_frame[feature].dropna().unique(),
                                             value = feature_data_dict[feature]['privileged_description'],
                                             layout = local_layout,
                                             style = local_style)
            
                display(dict_of_controls[feature])
                
                
            def show_disparity(button, space, choose_disparity_measure): #local method
                _ref_groups_dict = {}   
                for c in dict_of_controls:
                    _ref_groups_dict[c] = str(dict_of_controls[c].value)
                
                disparity = aeq_Bias.get_disparity_predefined_groups(cross_tab, 
                                                                     original_df=df_aequitas,
                                                                     ref_groups_dict=_ref_groups_dict, 
                                                                     alpha=0.05,
                                                                     mask_significance=True); 
                num_rows = math.ceil( (len(protected_attributes_list))/2)
                
                fig = plt.figure(figsize=(12 ,6*num_rows))
                plt.tight_layout()
                ax_dict = {}
                for x, num in zip (protected_attributes_list, range(len(protected_attributes_list))):
                    ax_dict[x] = plt.subplot(1, 2, num+1)
                    ax_dict[x] = aeq_Plot.plot_disparity(disparity, 
                                             group_metric=choose_disparity_measure, 
                                             attribute_name=x,
                                             significance_alpha=0.05,
                                             fig = fig,
                                             ax = ax_dict[x]);
                   
                if  y_high_positive == True:
                    html =   '''<b></b>You have indicated that a high outcome (ranking) has a <font color='green'><b>positive</b> </font> impact on a group or individual.
                                <br>
                                '''
                elif y_high_positive == False:
                    html = '''<b></b>You have indicated that a high outcome (ranking) has a <font color='red'><b>negative impact</b></font> on a group or individual.
                                '''
                display(HTML(html))
                
                plt.show()
                display(HTML('''Sized based on group size, color based on disparity magnitude<br>
                                Reference groups are displayed in grey with disparity = 1. <br>
                                Disparities greater than 10x will show as 10x.<br>
                                Disparities less than 0.1x will show as 0.1x.<br>
                                Statistical siginificance(default 0.05) will show as ** on square.'''))
                plt.close(fig1)
                plt.clf()
                
                one = widgets.Output(layout={})
                accordion1 = widgets.Accordion(children=[one])
                accordion1.set_title(0, "All Calculated values ")  
                with one:
                    pd.set_option('display.max_columns', None)
                    display (disparity)
                accordion1.selected_index = None
                display(accordion1)
                
                
                with out6:
                    clear_output(wait = True)
                    for ref in _ref_groups_dict:
                        display(HTML("Reference group is " +_ref_groups_dict[ref] + " for " + ref))
                    display(HTML("Green bar indicates Fair.<br>Red bar indicates unfair."))
                    group_val_fairness= aeq_Fairness.get_group_value_fairness(disparity)
                    parity_detrminations = aeq_Fairness.list_parities(group_val_fairness)
                    aeq_Plot.plot_fairness_group_all(group_val_fairness, ncols=5, metrics = "all")
                    
                    one = widgets.Output(layout={})
                    accordion1 = widgets.Accordion(children=[one])
                    accordion1.set_title(0, "All Calculated values ")  
                    with one:
                        display (group_val_fairness[['attribute_name', 'attribute_value']+parity_detrminations])
                    accordion1.selected_index = None
                    display(accordion1)
                    

            interact(show_disparity, 
                     button = widgets.ToggleButton(
                         description='Apply selected Reference group',
                         layout = local_layout,
                         style = local_style),
                         space = widgets.Label('  ', layout=widgets.Layout(width='100%')),
                     choose_disparity_measure = _choose_disparity_measure
                     
                     )

        with out7:
            html = '''<table class="wikitable" align="center" style="text-align:center; border:none; background:transparent;">
                    <tbody><tr>
                    <td style="border:none;" colspan="2">
                    </td>
                    <td style="background:#eeeebb;" colspan="2"><b>True condition</b>
                    </td></tr>
                    <tr>
                    <td style="border:none;">
                    </td>
                    <td style="background:#dddddd;"><a href="https://en.wikipedia.org/wiki/Statistical_population" title="Statistical population">Total population</a>
                    </td>
                    <td style="background:#ffffcc;">Condition positive
                    </td>
                    <td style="background:#ddddaa;">Condition negative
                    </td>
                    <td style="background:#eeeecc;font-size:90%;"><a href="https://en.wikipedia.org/wiki/Prevalence" title="Prevalence">Prevalence</a> <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931;&#160;Condition positive</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Total population</span></span></span>
                    </td>
                    <td style="background:#cceecc;border-left:double silver;font-size:90%;" colspan="2"><a href="https://en.wikipedia.org/wiki/Accuracy_and_precision" title="Accuracy and precision">Accuracy</a> (ACC) = <span style="font-size:118%;"><span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931;&#160;True positive + &#931; True negative</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Total population</span></span></span>
                    </td></tr>
                    <tr>
                    <td rowspan="2" class="nowrap unsortable" style="line-height:99%;vertical-align:middle;padding:.4em .4em .2em;background-position:50% .4em !important;min-width:0.875em;max-width:0.875em;width:0.875em;overflow:hidden;background:#bbeeee;"><div style="-webkit-writing-mode: vertical-rl; -o-writing-mode: vertical-rl; -ms-writing-mode: tb-rl;writing-mode: tb-rl; writing-mode: vertical-rl; layout-flow: vertical-ideographic;display: inline-block; -ms-transform: rotate(180deg); -webkit-transform: rotate(180deg); transform: rotate(180deg);;-ms-transform: none ;padding-left:1px;text-align:center;"><b>Predicted condition</b></div>
                    </td>
                    <td style="background:#ccffff;">Predicted condition<br />positive
                    </td>
                    <td style="background:#ccffcc;"><span style="color:#006600;"><b><a href="https://en.wikipedia.org/wiki/True_positive" class="mw-redirect" title="True positive">True positive</a></b></span>
                    </td>
                    <td style="background:#eedddd;"><span style="color:#cc0000;"><b><a href="https://en.wikipedia.org/wiki/False_positive" class="mw-redirect" title="False positive">False positive</a></b>,<br /><a href="https://en.wikipedia.org/wiki/Type_I_error" class="mw-redirect" title="Type I error">Type I error</a></span>
                    </td>
                    <td style="background:#ccffee;border-top:double silver;font-size:90%;"><a href="https://en.wikipedia.org/wiki/Positive_predictive_value" class="mw-redirect" title="Positive predictive value">Positive predictive value</a> (PPV), <a href="https://en.wikipedia.org/wiki/Precision_(information_retrieval)" class="mw-redirect" title="Precision (information retrieval)">Precision</a> = <span style="font-size:118%;white-space:nowrap;"><span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; True positive</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Predicted&#160;condition&#160;positive</span></span></span>
                    </td>
                    <td style="background:#cceeff;border-top:double silver;font-size:90%;" colspan="2"><a href="https://en.wikipedia.org/wiki/False_discovery_rate" title="False discovery rate">False discovery rate</a> (FDR) = <span style="font-size:118%;white-space:nowrap;"><span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; False positive</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Predicted&#160;condition&#160;positive</span></span></span>
                    </td></tr>
                    <tr>
                    <td style="background:#aadddd;">Predicted condition<br />negative
                    </td>
                    <td style="background:#ffdddd;"><span style="color:#cc0000;"><b><a href="https://en.wikipedia.org/wiki/False_negative" class="mw-redirect" title="False negative">False negative</a></b>,<br /><a href="https://en.wikipedia.org/wiki/Type_II_error" class="mw-redirect" title="Type II error">Type II error</a></span>
                    </td>
                    <td style="background:#bbeebb;"><span style="color:#006600;"><b><a href="https://en.wikipedia.org/wiki/True_negative" class="mw-redirect" title="True negative">True negative</a></b></span>
                    </td>
                    <td style="background:#eeddee;border-bottom:double silver;font-size:90%;"><a href="https://en.wikipedia.org/wiki/False_omission_rate" class="mw-redirect" title="False omission rate">False omission rate</a> (FOR) = <span style="font-size:118%;white-space:nowrap;"><span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; False negative</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Predicted&#160;condition&#160;negative</span></span></span>
                    </td>
                    <td style="background:#aaddcc;border-bottom:double silver;font-size:90%;" colspan="2"><a href="https://en.wikipedia.org/wiki/Negative_predictive_value" class="mw-redirect" title="Negative predictive value">Negative predictive value</a> (NPV) = <span style="font-size:118%;white-space:nowrap;"><span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; True negative</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Predicted&#160;condition&#160;negative</span></span></span>
                    </td></tr>
                    <tr style="font-size:90%;">
                    <td style="border:none;vertical-align:bottom;padding:0 2px 0 0;color:#999999;" colspan="2" rowspan="2">
                    </td>
                    <td style="background:#eeffcc;"><a href="https://en.wikipedia.org/wiki/True_positive_rate" class="mw-redirect" title="True positive rate">True positive rate</a> (TPR), <a href="https://en.wikipedia.org/wiki/Recall_(information_retrieval)" class="mw-redirect" title="Recall (information retrieval)">Recall</a>, <a href="https://en.wikipedia.org/wiki/Sensitivity_(tests)" class="mw-redirect" title="Sensitivity (tests)">Sensitivity</a>, probability&#160;of&#160;detection, <a href="https://en.wikipedia.org/wiki/Statistical_power" class="mw-redirect" title="Statistical power">Power</a> <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; True positive</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Condition&#160;positive</span></span></span>
                    </td>
                    <td style="background:#eeddbb;"><a href="https://en.wikipedia.org/wiki/False_positive_rate" title="False positive rate">False positive rate</a> (FPR), <a href="https://en.wikipedia.org/wiki/Information_retrieval" title="Information retrieval"><span class="nowrap">Fall-out</span></a>, probability&#160;of&#160;false&#160;alarm <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; False positive</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Condition&#160;negative</span></span></span>
                    </td>
                    <td style="background:#eeeeee;"><a href="https://en.wikipedia.org/wiki/Positive_likelihood_ratio" class="mw-redirect" title="Positive likelihood ratio">Positive likelihood ratio</a> <span class="nowrap">(LR+)</span> <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">TPR</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">FPR</span></span></span>
                    </td>
                    <td style="background:#dddddd;" rowspan="2"><a href="https://en.wikipedia.org/wiki/Diagnostic_odds_ratio" title="Diagnostic odds ratio">Diagnostic odds ratio</a> (DOR) <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">LR+</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">LR−</span></span></span>
                    </td>
                    <td style="background:#ddffdd;border-left:double silver;line-height:2;" rowspan="2"><a class="mw-selflink selflink">F<sub>1</sub> score</a> = <span style="font-size:118%;white-space:nowrap;">2 · <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">Precision · Recall</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">Precision + Recall</span></span></span>
                    </td></tr>
                    <tr style="font-size:90%;">
                    <td style="background:#ffeecc;"><a href="https://en.wikipedia.org/wiki/False_negative_rate" class="mw-redirect" title="False negative rate">False negative rate</a> (FNR), Miss&#160;rate <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; False negative</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Condition&#160;positive</span></span></span>
                    </td>
                    <td style="background:#ddeebb;"><a href="https://en.wikipedia.org/wiki/Specificity_(tests)" class="mw-redirect" title="Specificity (tests)">Specificity</a> (SPC), Selectivity, <a href="https://en.wikipedia.org/wiki/True_negative_rate" class="mw-redirect" title="True negative rate">True negative rate</a> (TNR) <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">&#931; True negative</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">&#931;&#160;Condition&#160;negative</span></span></span>
                    </td>
                    <td style="background:#cccccc;"><a href="https://en.wikipedia.org/wiki/Negative_likelihood_ratio" class="mw-redirect" title="Negative likelihood ratio">Negative likelihood ratio</a> <span class="nowrap">(LR−)</span> <span style="font-size:118%;white-space:nowrap;">= <span role="math" class="sfrac nowrap tion" style="display:inline-block; vertical-align:-0.5em; font-size:85%; text-align:center;"><span class="num" style="display:block; line-height:1em; margin:0 0.1em;">FNR</span><span class="slash visualhide">/</span><span class="den" style="display:block; line-height:1em; margin:0 0.1em; border-top:1px solid;">TNR</span></span></span>
                    </td></tr></tbody></table>'''
            display(HTML("<b>Wikipedia Metrics overview</b>"))
            display(HTML(html))
        gc.collect()
    def visualise_RMSE_model_eval(self, y_train, y_test, y_pred_train, y_pred_test):
        y_predictedTrain = y_pred_train
        y_predictedTest = y_pred_test
        y_test = y_test
        y_train = y_train
        '''We will be using Root mean squared error(RMSE) and Coefficient of Determination(R² score) to evaluate our model.
        RMSE is the square root of the average of the sum of the squares of residuals. 
        The RMSE is the square root of the variance of the residuals. 
        #It indicates the absolute fit of the model to the data–how close the observed data points are to the model’s
        #predicted values. Whereas R-squared is a relative measure of fit, RMSE is an absolute measure of fit. 
        #As the square root of a variance, RMSE can be interpreted as the standard deviation of the unexplained variance, 
        #and has the useful property of being in the same units as the response variable. 
        #Lower values of RMSE indicate better fit. 
        #RMSE is a good measure of how accurately the model predicts the response, and it is the most important criterion
        #for fit if the main purpose of the model is prediction.

        #Coefficient of Determination(R² score) - The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse). 
        #A constant model that always predicts the expected value of y, disregarding the input features, 
        #would get a R^2 score of 0.0. #R-squared is between 0 and 1, Higher values are better because it means 
        #that more variance is explained by the model.'''

        display("*****EVALUATING MODEL WITH TRAINING DATA:***")
        rmse = mean_squared_error(y_train, y_predictedTrain)
        r2 = r2_score(y_train, y_predictedTrain)
        display(' Root mean squared error: '+ str(rmse))
        display(' R2 score: '+ str(r2))

        display("*****EVALUATING MODEL WITH TEST DATA:******")
        rmse = mean_squared_error(y_test, y_predictedTest)
        r2 = r2_score(y_test, y_predictedTest)
        display(' Root mean squared error: ' + str(rmse))
        display(' R2 score: '+ str(r2))

        n_train = len(y_train)

        plt.figure(figsize=(20, 10))
        plt.plot(range(n_train), y_train, label="train")
        plt.plot(range(n_train, len(y_test) + n_train), y_test, '-', label="test")
        plt.plot(range(n_train), y_predictedTrain, '--', label="prediction train")

        plt.plot(range(n_train, len(y_test) + n_train), y_predictedTest, '--', label="prediction test")
        plt.legend(loc=(1.01, 0))
        plt.xlabel("Score")
        plt.ylabel("prediction")
        return plt
        
        
        
    def reload_data (self, pickle_path, data_frame_path, print_summary = True):
    # Reload the file
        data_summary = dill.load(open(pickle_path, "rb"))
        data_frame = pd.read_csv(data_frame_path)
        html = ""  
        protected = []
        non_protected = []
        y_value = ""
        if print_summary == True:
            display(HTML("<b>Number of samples in dataset:</b> " + str(data_frame.shape[0])))
            display (HTML("<b>All columns in data frame:</b> "+ str(data_frame.columns)))
            display(HTML("<b>Target:</b> "+ str (data_summary.y_value)))
            if data_summary.Y_CONTINUOUS == True:
                display(HTML("<b>Target type: </b>continuous"))
                display(HTML("<b>Num of unique values in target</b>: " + str ( len(data_frame[data_summary.y_value].dropna().unique()))))
                display(HTML("<b>Min:</b> " + str (data_frame[data_summary.y_value].min())))
                display(HTML("<b>Max </b>: "+ str ( data_frame[data_summary.y_value].max())))
            
            if data_summary.Y_BINARY == True:
                display(HTML("Output is binary"))
            if data_summary.HIGH_RANGE_POSITIVE == True:
                display(HTML("Output in high range has positive effect"))
            if data_summary.HIGH_RANGE_POSITIVE == False:
                display(HTML("Output in high range has negative effect"))
            
            
            
            display(HTML("<h3>Summary of Data transformation per feature:</h3>"))
            
            feature_data = data_summary.feature_data_dict 

            html = html + "<ul>"       
            for feature in feature_data:#in order of target, protected, other.
                html = html +"<li><b>"+feature+"</b><br>"
                html = html + "<ul>"
                html = html + "<li>Type: " + str(feature_data[feature]['type']) + "<br>"
                if feature_data[feature]['target'] == True:
                    html = html + "<li>This is the target(y)<br>"
                    y_value = feature
                elif feature_data[feature]['protected'] == True:
                    html = html + "<li>This is a protected feature<br>"
                    protected.append(feature)
                else:
                    non_protected.append(feature)
                if feature_data[feature]['type'] == "categorical":
                    html = html + "<li>Original Values: " + str(feature_data[feature]['original_values']) + "<br>"
                    html = html + "<li>Value descriptions: " + str(feature_data[feature]['values_description']) + "<br>"
                if feature_data[feature]['label_enc'] == True:
                    html = html + "<li>Label encoding was applied to this feature." + "<br>"
                    html = html + "<li>Label encoded values: " + str(feature_data[feature]['label_enc_values']) + "<br>"
                if feature_data[feature]['one_hot_enc'] == True:
                    html = html + "<li>One-Hot-Encoding was applied to this feature" + "<br>"
                    html = html + "<li>The new columns are:" + str(feature_data[feature]['one_hot_enc_cols_after']) + "<br>"
                    html = html + "<li>The original column before one-hot encoding:" + str(feature_data[feature]['one_hot_enc_col_before']) + "<br>"
                
                if feature_data[feature]['values_merged'] == True:
                    html = html + "<li>Some values within the feature were merged." + "<br>"
                    html = html + "<li>The values before the merge were: " + str(feature_data[feature]['before_merge_values']) + "<br>"
                    html = html + "<li>The values after the merge are: " + str(feature_data[feature]['original_values']) + "<br>"
                
                if feature_data[feature]['scaled_using'] != "":
                    html = html + "<li>Scaled/Normalised using: " + feature_data[feature]['scaled_using'] + "<br>"
            
                
                html = html + "<br>"
                html = html + "</ul>"
            html = html + "</ul>"
            display (HTML(html))
        
        
        return data_frame, data_summary
    
    

    #################################################################################################
    # Detect outliers and return for one column in dataset.
    # We find the z score for each of the data point in the dataset 
    # and if the z score is greater than 3 than we can classify that point as an outlier. 
    # Any point outside of "thresh" = 3 standard deviations would be an outlier.
    # 
    #################################################################################################
    def detect_outlier_and_describe(self, series, thresh = 3, data_type = "numeric"):
        outliers=[]
        threshold=thresh
        size = series.count()
        missing =  series.isnull().sum()
        unique = len(series.unique())
        pcnt_missing = missing/size *100
        html = ""
        if data_type == "numeric":
            mean_1 = np.mean(series)
            std_1 =np.std(series)
        
            html = "Outlier is defind as any point outside " + str(thresh) + " standard deviations<br>" 
            html = html + "Min: " + str(np.min(series)) + "<br>"
            html = html + "Max: " + str( np.max(series)) + "<br>"
            html = html + "Mean: " + str( mean_1) + "<br>"
            html = html + "Standard Deviation: "+ str( std_1) + "<br>"
            for y in series:
                z_score= (y - mean_1)/std_1 
                if np.abs(z_score) > threshold:
                    outliers.append(y)
            html = html + "Number of outliers: "+ str( len(outliers)) + "<br>"
            html = html + "Outliers: "+ str(outliers) + "<br>"
        

         
        html = html + "Number of observations: "+ str( size) + "<br>"
        html = html + "Num of unique values: "+ str(unique) + "<br>"
        html = html + "Missing cells: "+ str( missing) + "<br>"
        html = html + "Missing cells%: "+ str( missing) + "<br>"
        
        
        return html, outliers
    
        
    #################################################################################################
    #  This function will return  a Features dataframe, a Series with the Target and a list of the 
    # features that will be used to train the model. The Features dataframe may contain additional features
    # such as the protected features(when not used for training), and tcolumns containing values before 
    # any kind of merge of the data.
    #################################################################################################
    
    def get_features_and_target(self, 
                                data_frame, 
                                data_summary, 
                                include_protected,
                                continuous_to_binary_target = False):

        if include_protected == True:
            cols = data_summary.protected_after_transform + data_summary.non_protected_after_transform
        else:
            cols = data_summary.non_protected_after_transform
        
        if data_summary.y_value in cols:
            cols.remove(data_summary.y_value)
        
        if continuous_to_binary_target == True:
            if not data_summary.y_value + "_binary" in list(data_frame.columns):
                display(HTML("""<font style='color:orange;'>You have set <b>'continuous_to_binary_target = True'</b>, but no translation from continuous to binary was detected!<br> 
                                <font style='color:black;'>If the label is a
                                continuous number then run the helper method 
                                <b>set_decision_boundary(data_frame, data_summary)</b> 
                                to convert a binary label to a  continuous label 
                                before calling <b>get_features_and_target</b>. 
                             """))
                return data_frame.drop(data_summary.y_value, axis = 1), data_frame[data_summary.y_value], cols
       
            else:
                return  data_frame.drop([data_summary.y_value, data_summary.y_value + "_binary"], axis = 1), data_frame[data_summary.y_value + "_binary"], cols
        return  data_frame.drop(data_summary.y_value, axis = 1), data_frame[data_summary.y_value], cols
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def shap_analysis(self, shap_values, explainer, x, data_summary):
        try:
            shap.initjs()
        except:
            print ( 'shap.initjs() failed to load javascript')
        
        outOverview = widgets.Output(layout={})
        out1 = widgets.Output(layout={})
        out2 = widgets.Output(layout={})
        out3 = widgets.Output(layout={})
        out4 = widgets.Output(layout={})
        out5 = widgets.Output(layout={})
        tab_contents = [out1, out2, out3, out4, out5]
        
        children = tab_contents
        tab = widgets.Tab(style={'description_layout':'auto', 'title_layout':'auto'})
        tab.children = children
        
        tab.set_title(0, "Summary Importance plot")
        tab.set_title(1, "Importance plot")
        tab.set_title(2, "Dependence plot")
        tab.set_title(3, "Individual force plot")
        tab.set_title(4, "Collective force plot")
        
        local_layout = {'width': 'auto', 'visibility':'visible'}
        local_layout_hidden  = {'width': 'auto', 'visibility':'hidden'}
        local_style = {'description_width':'initial'}
        display(outOverview)
        display(tab)
        
        
 
        _choose = widgets.Dropdown(description = "Select Feature", 
                                    options = list(x.columns),
                                    layout = local_layout,
                                    style = local_style)
        all_comb = {}
        for f in data_summary.protected_after_transform:
            for a in  x[f].unique():
                all_comb[(f+":"+ str(a))] = a
        
        _protected = widgets.Dropdown(description = "Filter by Protected Feature", 
                                     options = all_comb,
                                     layout = local_layout,
                                     style = local_style)
        
        toggle = widgets.ToggleButton(
                            value=False,
                            description='Generate',
                            disabled=False,
                            button_style='', # 'success', 'info', 'warning', 'danger' or ''
                            
                            )
        
        with outOverview:
            display (HTML('''<h3>SHAP interpretability via Machnamh</h3>(SHapley Additive exPlanations) KernelExplainer is a 
            model-agnostic method which builds a weighted linear regression by using training/test data, 
            training/test predictions, and whatever function that predicts the predicted values. 
            SHAP values represent a feature's responsibility for a change in the model output.
            It computes the variable importance values based on the Shapley values from game theory, 
            and the coefficients from a local linear regression. </br>
            see: https://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf <br>

            It offer a high level of interpretability for a model, through two distinct approaches:

            <br><b>Global interpretability</b> — the SHAP values can show how much each predictor contributes, 
            either positively or negatively, to the target variable. Similar to a variable importance plot however it also indicates the positive or negative relationship between each feature and the target output.

            <br><b>Local interpretability</b> — each observation is assigned it's own SHAP value. 
            This provides a very granular level of transparency and interpretability where we can 
            determine why an individual cases receive a specific prediction  and the contribution of 
            each feature to the prediction. Generally speaking variable importance algorithms usually 
            only show the results across the entire dataset but not on each individual case.'''))
            
        with out1:
          
            html_desc = '''
            <b>Summary importance plot </b><br><b>Feature importance:</b> Variables are ranked in descending order. The top variables contribute more to the model than the bottom ones and thus have high predictive power.<br>
            ''' 
            wi1 = widgets.Output(layout=Layout(width='60%'))
            with wi1:
                shap.summary_plot(shap_values, x, plot_type="bar"); 
            wi2 = widgets.HTML(value=html_desc,layout=Layout(width='30%') ) ; 
            sidebyside = widgets.HBox([wi1, wi2])
            display (sidebyside)
        with out2:
            display (HTML('''<b>Importance plot:</b> lists the most significant variables in descending order. 
                          The top variables contribute more to the model than the bottom ones and thus have high predictive power.'''))
            html_desc = '''
            <b>Feature importance:</b> Variables are ranked in descending order.<br>
            <b>Impact:</b> Horizontal location indicates if effect of feature is associated with a higher or lower prediction.<br>
            <b>Original value:</b> Colour indicates if feature variable is high(red) or low(blue) for the particular observation.<br>
            <b>Correlation:</b> A high or low impact(indicated by colour), a positive or negative impact(indicated by position on x-axis)
                '''  
            wi1 = widgets.Output(layout={})
            with wi1:
                shap.summary_plot(shap_values, x);
            wi2 = widgets.HTML(value=html_desc,layout=Layout(width='30%') )  
            sidebyside = widgets.HBox([wi1, wi2])
            display (sidebyside)
                
        with out3:
            
            display (HTML ("The decision variable is " + str(data_summary.y_value)))
            display (HTML ('''To understand how a single feature effects the output of the model a 
                             dependency plot plots the SHAP value of  that feature vs. the value of 
                             the feature for all the examples in a dataset.'''))
            def show_dependancy_plot(choose):
                html_desc = '''The dependency plots show relationship between the target ('''+ data_summary.y_value +  ''') 
                   and the selected feature ('''+ choose + ''') to review if it is linear, monotonic or 
                  more complex.  The additionla variable is the variable that the selected feature (''' + choose + ''') 
                  interacts with the most frequently. Vertical dispersion at a single value represents interaction 
                  effects with the other features.  '''
                display (HTML(html_desc))
                display (shap.dependence_plot(choose, shap_values, x))
            interact(show_dependancy_plot, choose = _choose);
    
        with out4:
            display (HTML ("The decision variable is " + str(data_summary.y_value)))
            display (HTML ('''<b>Individual Force plot</b> shows the features which each contribute to push the model output 
                            from the base value (the average model output over the dataset passed) to the
                            model output. Features pushing the prediction higher are shown in red, 
                            those pushing the prediction lower are shown in blue.'''))
            # visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
            display (HTML ("<b>Generate random sample to investigate:</b>"))
            def show_individual_force_plot(protected, toggle):
                feat = _protected.label.split(':')[0]
                index = x[x[feat] == _protected.value].sample(1).index[0]
                display (shap.force_plot(explainer.expected_value, 
                                     shap_values[index,:], 
                                     x.iloc[index,:],
                                     matplotlib=True))
            
            interact(show_individual_force_plot, protected = _protected, toggle = toggle);
         
        with out5:
            display (HTML ("The decision variable is " + str(data_summary.y_value)))
            display (HTML ('''<b>Collective Force plot</b> A combination of all individual force plots, each rotated 90 degrees, and stacked
                                horizontally, to explanation an entire dataset.'''))
            display (shap.force_plot(explainer.expected_value, 
                                     shap_values, 
                                     x))

    #################################################################################################
    #  
    # 
    #################################################################################################
    def get_protected (self, summary):
        return summary.protected_before_transform

    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    #def get_protected_before_merge (self, summary):
    #    return summary.all_columns_in_x
    #   print (list([all_columns_in_x.contains('_bm')]))
    #   print (list(X_train.columns[X_train.columns.str.contains('_benc')]))

    
    #################################################################################################
    #  
    # 
    #################################################################################################
    #def get_protected_before_transform (self, summary):
    #    all_cols = summary.all_columns_in_x
    #    prot = summary.protected_x

    #    new_prot = []
    #    for f in prot:
    #        found = False
    #        if f+'_bm' in all_cols:
    #           new_prot.append(f+'_bm')
    #           found = True
    #       if f+'_benc' in all_cols:
    #           new_prot.append(f+'_benc')
    #            found = True
    #        if f.endswith('_oh_benc'):
    #            new_prot.append(f)
    #            found = True
    #    
    #        if found == False:
    #            new_prot.append(f)
    #    return new_prot
    
    
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def serialise_ranked_list(self, X, y, y_prob_actual, y_prob_1, y_pred, save_to_path = './', name = ""):
        
        ranked_dict = {}
        ranked_dict['X'] = X
        ranked_dict['y'] = y
        ranked_dict['y_prob_actual'] = y_prob_actual
        ranked_dict[ 'y_prob_1'] =  y_prob_1
        ranked_dict['y_pred'] =  y_pred
        path =  save_to_path + name + "_ranked_data.pickle"
        dill.dump(ranked_dict, file = open(path, "wb"))
        display (HTML("Serialised data to dictionary 'ranked_dict', at " + path))
        return path
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def reload_ranked_list (self, _path):
        path = _path
        ranked_dict = dill.load(open(path, "rb"))
        X = ranked_dict['X']
        y = ranked_dict['y'] 
        y_prob_actual = ranked_dict['y_prob_actual']
        y_prob_1 = ranked_dict[ 'y_prob_1']
        y_pred = ranked_dict['y_pred']
        return  X, y, y_prob_actual, y_prob_1, y_pred

    #################################################################################################
    #  
    # 
    #################################################################################################
    def run_shap_and_serialise_response(self, X_in, 
                                       model_predict,
                                       count = 100, 
                                       save_to_path = './'):
        x = shap.sample( X_in, count)
        x = x.reset_index(drop=True)
        explainer = shap.KernelExplainer(model_predict, x ) # The second argument is the "background" dataset; a size of 100 rows is gently encouraged by the code
        shap_values = explainer.shap_values(x, l1_reg="num_features(10)")
        print(f'length of SHAP values: {len(shap_values)}')
        print(f'Shape of each element: {shap_values[0].shape}')
        path =  save_to_path + "shap_values.pickle"
        print ("Shap_values saved to", path)
        dill.dump(shap_values, file = open(path, "wb"))
        path =  save_to_path + "shap_explainer.pickle"
        print ("Shap_explainer saved to", path)
        dill.dump(explainer, file = open(path, "wb"))
        path =  save_to_path +"shap_x.pickle"
        print ("Shap_explainer saved to", path)
        dill.dump(x, file = open(path, "wb"))
        display (HTML ("The model-agnostic SHAP explainer <b>'KernelExplainer'</b> has been used."))
        return explainer, shap_values, x

    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def reload_shap_data (self, _path):
        path = _path 
        shap_values_path = path + "/shap_values.pickle"
        explainer_path = path + "/shap_explainer.pickle"
        x_path = path + "/shap_x.pickle"
        shap_values = dill.load(open(shap_values_path, "rb"))
        explainer = dill.load(open(explainer_path, "rb"))
        x = dill.load(open(x_path, "rb"))
        # Reload the file
        return shap_values, explainer, x
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def get_features_type(self, df, unique_max):
        numeric_cat = []
        obj = []
        cat = []
        boo = []
        #pandas data types.
        # datetime64 - currently not supported by the tool
        # timedelta[ns] - currently not supported by the tool
        # object
        # int64
        # float64
        # bool
        # category
        
        for col in df.select_dtypes(include='number').columns:
            if len(df[col].dropna().unique()) <= unique_max:
                numeric_cat.append(col)
                
        for col in df.select_dtypes(include='object').columns:
            if len(df[col].dropna().unique()) <= unique_max:
                obj.append(col)
                
        for col in df.select_dtypes(include='category').columns:
            if len(df[col].dropna().unique()) <= unique_max:
                cat.append(col)
                
        for col in df.select_dtypes(include='bool').columns:
            if len(df[col].dropna().unique()) <= unique_max:
                boo.append(col)

        all_categorical = cat + obj + numeric_cat + boo
        all_numeric = list (df.columns)
        all_numeric = [ele for ele in all_numeric if ele not in all_categorical] 
        return all_categorical, all_numeric
    
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def get_feature_info (self, feature, unique_values, group_descriptions_dict, label_encoding_dict, oh_encoding_dict, merged_dict, trace = False):
        values = unique_values
        decoded_values = []
        original_values = []
        label_encoded_values = []
        
        keys = []
        
        if feature in oh_encoding_dict:
            original_feature_bohe = oh_encoding_dict[feature]["Original_col"]
            original_value_bohe = oh_encoding_dict[feature]["Original_val"]
            if trace == True:
                print ("One Hot Encoded from feature:", original_feature_bohe, "value:",original_value_bohe)
                print ("One Hot Encoded values:", values)
            _choice_dict_for_drop = dict(zip(values, values))
            original_values = values
            label_encoded_values = []
            descriptions = values
            return _choice_dict_for_drop, original_values, label_encoded_values, descriptions
            
        def get_key(val): #local method in get_feature_info
            for key, value in label_encoding_dict[feature].items(): 
                if val == value: 
                    return key 
            return None
        
        #if feature is already encoded then unique_values will be the encoded versions
        #If feature does not have a description saved then return {x:x, y:y etc} as
        #the key value pairs for any dropdown. regardless of encoded or not.
        if feature not in group_descriptions_dict:
            original_values = values 
            if feature in label_encoding_dict:
                for value in values:
                    decoded_values.append(get_key(value))
                    original_values = decoded_values
                    label_encoded_values = values 
                descriptions = original_values
                _choice_dict_for_drop = dict(zip(original_values, label_encoded_values))
                
            else:
                
                _choice_dict_for_drop = dict(zip(values, values))
                descriptions = values
            
            if trace == True:
                print ("Original values ", original_values)
                print ("Label Encoded values ", label_encoded_values )
                print ("Description ",  descriptions )
                print ("Key/Value for dropdown: ", _choice_dict_for_drop)
            
            return _choice_dict_for_drop, original_values, label_encoded_values, descriptions
        
        
        if feature in group_descriptions_dict:
            #first check if the input feature unique_values are the result of an Encode
            if feature in label_encoding_dict:
                for value in values:
                    decoded_values.append(get_key(value))
                original_values = decoded_values
                label_encoded_values = values
                if trace == True:
                    print ("Original values ", original_values)
                    print ("Label Encoded values ", label_encoded_values )
             
            if feature not in label_encoding_dict:
                original_values = values
                label_encoded_values = []
                if trace == True:
                    print ("Original values ", original_values)
                    print ("Label Encoded values ", label_encoded_values )
                
            for key in original_values:
                if key not in group_descriptions_dict[feature]:
                    keys.append(key)
                else:
                    keys.append(group_descriptions_dict[feature][key])
        # using zip() 
        # to convert lists to dictionary 
            _choice_dict_for_drop = dict(zip(keys,values))
            descriptions = keys
            if trace == True:
                print ("Description: ", keys)
                print ("Key/Value for dropdown: ", _choice_dict_for_drop)
                if feature in merged_dict:
                    print ("Merged Values: ", merged_dict[feature])
        return _choice_dict_for_drop, original_values, label_encoded_values, descriptions


    
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def phi_k_correlation(self, df):
        intcols = []
        selcols = []
        for col in df.columns.tolist():
            try:
                tmp = (
                        df[col]
                        .value_counts(dropna=False)
                        .reset_index()
                        .dropna()
                        .set_index("index")
                        .iloc[:, 0]
                    )
                if tmp.index.inferred_type == "mixed":
                    continue

                if pd.api.types.is_numeric_dtype(df[col]):
                    intcols.append(col)
                    selcols.append(col)
                elif df[col].nunique() <= config[
                    "categorical_maximum_correlation_distinct"
                ].get(int):
                    selcols.append(col)
            except (TypeError, ValueError):
                continue

        if len(selcols) > 1:
            correlation = df[selcols].phik_matrix(interval_cols=intcols)

            return correlation
        else:
            return None

    #################################################################################################
    #  
    # 
    #################################################################################################
    def Benfords_law(self, df, feature, protected):
        groups = df[protected].dropna().unique()
        tab = widgets.Tab()
        widget_arr = {}
        tab_titles = []
        fit_output = widgets.Output(layout={})       
                    
        for group in groups:
            filtered = df[df[protected]==group]
            X = filtered[feature].values
            # # Make fit
            with fit_output:
                out = bl.fit(X)
            # # Plot
            widget_arr[group] = widgets.Output(layout={})
            with widget_arr[group]:
                display(bl.plot(out,
                        title='Benfords law for '+ str(feature) + ' and group '+ str(group),  
                        figsize=(8,4)));
            tab_titles.append(str(group))
        widget_arr["Output"] = fit_output
        tab.children = list(widget_arr.values())
        
        for x in range(len(tab_titles)):
            tab.set_title(x, tab_titles[x])
        tab.set_title(x+1,"Output Trace")
        return tab
    
    
    def de_hot_encode_feature (self, df, original_col, hot_encoded_cols):
        num_chars = len(original_col) + 1
        df[original_col] = 0
        for col in hot_encoded_cols:
            map_to = col[num_chars:]
            df.loc[df[col] == 1, original_col] = map_to

        return df[original_col]


    def map_values (self, data_frame, protected_attributes_list, feature_data_dict):
        for feat in protected_attributes_list:
            #create a dictionary out of two lists..
            if feature_data_dict[feat]['values_merged'] == True:
                display ("the feature was merged")
                display ("column before merge is ", feature_data_dict[feat]['before_merge_col'])
                #data_frame[feat] = data_frame['before_merge_col']

            if feature_data_dict[feat]['one_hot_enc'] == True:
                #One_hot was applied
                original_col = feature_data_dict[feat]['one_hot_enc_col_before']
                hot_encoded_cols = feature_data_dict[feat]['one_hot_enc_cols_after']
                data_frame[feat] = self.de_hot_encode_feature(data_frame, original_col, hot_encoded_cols)

                #now if there are descriptions use the descriptions
                if len(feature_data_dict[feat]['values_description']) != 0:
                    map_dictionary = dict(zip(feature_data_dict[feat]['original_values'], 
                                              feature_data_dict[feat]['values_description']))
                    data_frame[feat] = data_frame[feat].map(map_dictionary)


            elif feature_data_dict[feat]['label_enc'] == True:
                #Label encoding was applied
                #if there are descriptions use the descriptions otherwise use the non-label encoded values
                if len(feature_data_dict[feat]['values_description']) != 0:
                    map_dictionary = dict(zip(feature_data_dict[feat]['label_enc_values'], 
                                          feature_data_dict[feat]['values_description']))
                else:
                    map_dictionary = dict(zip(feature_data_dict[feat]['label_enc_values'], 
                                          feature_data_dict[feat]['original_values']))
                data_frame[feat] = data_frame[feat].map(map_dictionary)


            else:
                #No encoding was applied
                if len(feature_data_dict[feat]['values_description']) != 0:
                    map_dictionary = dict(zip(feature_data_dict[feat]['original_values'], 
                                              feature_data_dict[feat]['values_description']))
                    data_frame[feat] = data_frame[feat].map(map_dictionary)


        return data_frame[protected_attributes_list]
    
    #################################################################################################
    #  copied from Medium article, will use it as a
    # 
    #################################################################################################
    def make_confusion_matrix(self, 
                              conf_matrix, 
                              feature,
                              group_names=None,
                              categories='auto',
                              count=True,
                              percent=True,
                              cbar=True,
                              xyticks=True,
                              xyplotlabels=True,
                              sum_stats=True,
                              figsize=None,
                              cmap='Blues',
                              title=None):
        
        cm_all = conf_matrix.copy()
        '''
        This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
        Arguments
        ---------
        conf_matrix:   Aequitas entire confusion matrix to be passed in
        feature        The protected feature to view
        group_names:   List of strings that represent the labels row by row to be shown in each square.
        categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
        count:         If True, show the raw number in the confusion matrix. Default is True.
        normalize:     If True, show the proportions for each category. Default is True.
        cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                       Default is True.
        xyticks:       If True, show x and y ticks. Default is True.
        xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
        sum_stats:     If True, display summary statistics below the figure. Default is True.
        figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
        cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                       See http://matplotlib.org/examples/color/colormaps_reference.html

        title:         Title for the heatmap. Default is None.
        '''
        
        out_dict = {} 
       
        cm_all = cm_all[cm_all['attribute_name'] == feature] 
        groups = cm_all['attribute_value'].unique()
        for group in groups:
            cm_group = cm_all[cm_all['attribute_value'] == group].squeeze() #squeese changes it to series
            tn = cm_group['tn']
            fp = cm_group['fp']
            fn = cm_group['fn']
            tp = cm_group['tp']

            cf =  np.array([[tn,  fp],
                  [ fn, tp]])
            
            out_dict[group] = widgets.Output(layout = {'border': 'solid 1px white', 'padding': '25px'})

            # CODE TO GENERATE TEXT INSIDE EACH SQUARE
            blanks = ['' for i in range(cf.size)]

            if group_names and len(group_names)==cf.size:
                group_labels = ["{}\n".format(value) for value in group_names]
            else:
                group_labels = blanks

            if count:
                group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
            else:
                group_counts = blanks

            if percent:
                group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]
            else:
                group_percentages = blanks

            box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
            box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])


            # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
            if sum_stats:
                #Accuracy is sum of diagonal divided by total observations
                accuracy  = np.trace(cf) / float(np.sum(cf))

                #if it is a binary confusion matrix, show some more stats
                if len(cf)==2:
                    #Metrics for Binary Confusion Matrices
                    precision = cf[1,1] / sum(cf[:,1])
                    recall    = cf[1,1] / sum(cf[1,:])
                    f1_score  = 2*precision*recall / (precision + recall)
                    stats_text = """\n\nAccuracy={:0.3f}
                                      \nPrecision/Positive predictive value(PPV)={:0.3f}
                                      \nRecall/True Positive Rate/Sensitivity={:0.3f}
                                      \nF1 Score={:0.3f}""".format(
                        accuracy,precision,recall,f1_score)
                    html = '<font style="font-family:sans-serif; font-size:10px;color:black;">'
                    html = html + "Accuracy: " + str(round(accuracy,2)) + "<br>"
                    html = html + "Precision/Positive predictive value(PPV): " + str(round(precision,2)) + "<br>"
                    html = html + "Recall/True Positive Rate/Sensitivity: " + str(round(recall,2)) + "<br>"
                    html = html + "F1 Score=: " + str(round(f1_score,2)) + "<br>"
                          
                else:
                    stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)
            else:
                stats_text = ""

            stats_text = ''#Going to use the HTML instead
            # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
            if figsize==None:
                #Get default figure size if not set
                figsize = plt.rcParams.get('figure.figsize')

            if xyticks==False:
                #Do not show categories if xyticks is False
                categories=False


            # MAKE THE HEATMAP VISUALIZATION
            plt.figure(figsize=figsize)
            sns.heatmap(cf,annot=box_labels,
                        fmt="",
                        cmap=cmap,
                        cbar=cbar,
                        xticklabels=categories,
                        yticklabels=categories
                       )

            if xyplotlabels:
                plt.ylabel('True label')
                plt.xlabel('Predicted label' + stats_text)
            else:
                plt.xlabel(stats_text)

            if title:
                plt.title(title)
            with out_dict[group]:
                display(HTML(group))
                plt.show()
                display(HTML(html))
                
        l = list(out_dict.values())
        n = 3
        outList = []
        for i in range(n, len(l) + n, n):
            outList.append(l[i-n:i])

        for chunk_of_3 in outList:
            display (widgets.HBox([*chunk_of_3], layout = Layout(
                                                            padding = '10px',
                                                            width='100%',
                                                            display='flex',
                                                            align_items='stretch',
                                                            align_content='space-between',
                                                            )
                                 ))


# In[ ]:

