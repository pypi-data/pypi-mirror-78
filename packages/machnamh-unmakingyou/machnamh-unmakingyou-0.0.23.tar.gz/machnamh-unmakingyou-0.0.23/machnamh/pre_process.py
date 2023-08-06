#!/usr/bin/env python
# coding: utf-8

# In[3]:


from machnamh import helper
from machnamh import demo_data
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

class self_info_class():
            def _init(self):
                self.df_url
                self.feature_data_dict = {}
                self.HIGH_RANGE_POSITIVE
                self.Y_BINARY = False
                self.Y_CONTINUOUS = False
                self.GT_VALIDITY
                self.y_value
                self.protected_before_transform
                self.non_protected_before_transform
                self.protected_after_transform
                self.non_protected_after_transform
            
            def describe(self):
                display (HTML ("<h3>Description of varialbes in class data_summary:</h3>"))
                
                display (HTML ('<b>feature_data_dict:</b> dictionary to describe all features'))
                display (HTML('<b>HIGH_RANGE_POSITIVE:</b> True if high label value (or 1) is of benefit to individual'))
                display (HTML ('<b>Y_BINARY:</b> True if label is binary'))
                display (HTML ('<b>y_value:</b> The target variable'))
                display (HTML ('<b>Y_CONTINUOUS:</b> True if label is continuous'))
                display (HTML ('<b>protected_before_transform:</b> list of protected feature columns before any transformation applied'))
                display (HTML ('<b>non_protected_before_transform:</b> list of non-protected features columns before any transformation applied'))
                display (HTML ('<b>protected_after_transform:</b> list of protected feature columns after any transformations applied'))
                display (HTML ('<b>non_protected_after_transform:</b> list of non-protected feature columns after any transformations applied'))
                

class data_pre_process_UI():
    
    def __init__(self):
        
        get_ipython().run_cell_magic('html', '', '<style>\n.box_style{\n    width:40%;\n    border : 2px solid red;\n    height: auto;\n    background-color:#34abeb;\n}\n.title_style{\n    width:40%;\n    border : 2px solid red;\n    height: auto;\n    background-color:green;\n}\n</style>')
        self.helper_methods = helper.helper_methods()
        pd.set_option('display.max_colwidth', None)
        self.df = pd.DataFrame() # Original Dataframe uploaded
        self.df_url = None
        
        self.y_label_df = pd.DataFrame() # Dataframe containing label(score) and also the range(upper or lower)
        self.non_protected_feature_set_df = pd.DataFrame() # Dataframe containing features except protected
        self.protected_feature_set_df = pd.DataFrame() # Dataframe containing features except protected

        self.text_color = "#34abeb"
        # A dictionary, mapping feature encoding values
        
        self.HIGH_RANGE_POSITIVE = True
        self.GT_VALIDITY = 0
        self.Y_BINARY = False
        self.Y_CONTINUOUS = False
        self.y_min_rank = 0
        self.y_mid_rank = 0.5
        self.y_max_rank = 1
        
        
        self.group_descriptions_dict = {} #refactor later to remove these
        self.reference_groups_dict= {} #refactor later to remove these
        self.label_encoding_dict = {} #refactor later to remove these
        self.oh_encoding_dict = {} #refactor later to remove these
        self.merged_dict = {} #refactor later to remove these
        self.apply_scale_norm = {} #refactor later to remove these
        
        self.feature_data_dict = {}#refactor to use this to replace the individula dictionaries
        
        self.default_desc = {
                       'type': '',
                       'target': False,
                       'protected': False,
                       'original_values' : [],
                       'values_description': [],
                       'original_choice_dict': {},
                       'original_privileged': '',
                       'privileged_description': '',
                       'one_hot_enc': False,
                       'one_hot_enc_col_before':'',
                       'one_hot_enc_cols_after': [],
                       'label_enc': False,
                       'label_enc_values': [],
                       'label_enc_choice_dict': {},
                       'label_enc_privileged': {},
                       'values_merged': False,
                       'before_merge_col': '',
                       'before_merge_values': [],
                       'scaled_using':'',
                       'renamed':False,
                       'renamed_from':"",
                    }
        
        
        
        
        
        #For creating report on group representation in data
        self.group_under_represented_pop_dict   = {} 
        self.group_under_represented_domain_dict   = {} 
        self.group_under_represented_world_view_dict   = {}
        self.group_under_represented_data_ok_dict = {}
        self.group_represented_free_text= {}
        
        #For creating report on output distribution in data with respect to protected groups
        self.group_output_distribution_dict   = {} 
        self.group_output_distribution_world_view_dict   = {} 
        self.group_output_distribution_data_ok_dict  = {}
        self.group_output_distribution_free_text = {}
        
        
        #For creating report on input feature with respect to protected groups
        self.proxy_features_audit_dict = {}
        self.dependant_features_audit_dict = {}
        
        self.worldview = self.helper_methods.worldview
        
        self.worldview_biological = self.helper_methods.worldview_biological
        
        self.worldview_social = self.helper_methods.worldview_social
                        
        self.ground_truth_zero_text = """
                                     <b>An inherently subjective human decision: </b>
                                     In some cases this target is a human decision, rather than an epistemological or actual 
                                     ground truth and therefor may reflect human prejudice and propensity to discriminate. If you suspect 
                                     that the target reflects a subjective decision and accept that all humans are prone to prejudice,
                                     then the ground truth can only be assumed to be true. There is no concept of counterfactual regret,
                                     or what would have happened had prejudice not existed (would particular groups have a higher
                                     representation in the dataset, or have been approved for more mortgages, offered more jobs, 
                                     been rewarded with more promotions, been stopped by the police less, been arrested less etc.) </br>    
            
                                """
        
        self.ground_truth_one_text = """<b>An intentional proxy for the ground truth: </b>
                            In some cases, if there is no (or poor) measurement of the ground-truth
                            a proxy might have been used. A proxy is an observation or set of observations assumed to correlate 
                            to the actual ground-truth. The target(y) is extrapolated from these observations. 
                            The intentional use of such a proxy is sometimes necessary but may result in bias against 
                            certain groups.
        
                        """
        
        self.ground_truth_two_text = """<b> An apparently objective and measurable ground truth: </b>
                                    In some cases this label is an apparently objective and measurable value which reflects 
                                    a real world outcome(e.g loan repaid/loan defaulted, reoffence/noreoffence, exam score). 
                                    The target is an objective and measurable value which has not been the subjective decisions 
                                    of a possibly prejudiced human."""
        
        

        
        
        self.style = {'description_width': 'initial'}
        self.layout = {'width': 'auto'}
        self.layout_short = {'width': 'auto'}
        
        self.auto_width_layout = {'width': 'auto'}     # override the default width of the button to 'auto' to let the button grow

        self.fileUploader = widgets.FileUpload(accept='.csv',
                                       multiple=False,
                                       disabled=False,
                                       button_style='success',
                                       compress_level=9
                                       )
        
        
        self.selectYFeature = widgets.Dropdown(
            options=  self.df.columns.values,
            value=None,
            description='Target(y):',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
        

        self.selectXFeatures = widgets.SelectMultiple(
            options = self.df.columns.values,
            description='Features',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout,
            continuous_update=False
        )
        

        self.selectProtectedAttributes = widgets.SelectMultiple(
            options=self.df.columns.values,
            description='Protected Feature(s)',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout,
            continuous_update=False
        )
        
        self.theSelectedInputFeaturesChoice = widgets.SelectMultiple(
            options = [],
            description='Features',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
        
        
        self.theSelectedNumericFeaturesChoice = widgets.SelectMultiple(
            options = [],
            description='Features',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
           
        
        self.theSelectedCategoricalFeaturesDropDown = widgets.Dropdown(
            options = [],
            description='Categorical Feature',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
    
    
        self.selectImpact = widgets.RadioButtons(
            options={'A positive or assistive impact on an individual': 1,
                     'A negative or punitive impact on an individual': 0},
            description='A prediction in the high range (or binary 1) will have:',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
        
        
        self.gtAssumption = widgets.RadioButtons(
            options={'An inherently subjective human decision': 0,
                     'An intentional proxy for the ground truth': 1,
                     'An apparently objective and measurable ground truth': 2,},
            description='The target (y) is:',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
        
        self.analyze_missing_data_button = widgets.Button(
            description='Run missing data analysis',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Review missing data and apply resolution',
            icon='',
            layout = self.auto_width_layout
        )

        
        self.newNameForValue = widgets.Text(
            description='New Value Name',
            disabled=False,
            tooltip='enter the new value name',
            style = self.style,
            layout = self.auto_width_layout
        )
        

        self.choosenFeatureValues = widgets.SelectMultiple(
            description='Select value(s)',
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )
        

        self.view_representation_button = widgets.Button(
            description='View representation of groups in the sample',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='view the representation of various groups in the data',
            icon='',
            layout = self.auto_width_layout
        )
        
        
        self.view_output_distribution_button = widgets.Button(
            description='View distribution of output per protected group',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='view the distribution of output for the protected groups',
            icon='',
            layout = self.auto_width_layout
        )
        
        
        self.merge_values_button = widgets.Button(
            description='Merge',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Merge feature values',
            icon='',
            layout = self.auto_width_layout
        )

        self.descriptionText = widgets.Text(
            description='Description of value',
            disabled=False,
            tooltip='Save a description for the value e.g "protected" or the original name',
            style = self.style,
            layout = self.auto_width_layout
        )

        self.save_description_button = widgets.Button(
            description='Save',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            icon='check',
            layout = self.auto_width_layout
        )
        
        
        self.profile_data_button = widgets.Button(
            description='Generate feature visualisation for analysis',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='view data',
            layout = self.auto_width_layout
            
        )
        
    
        self.drop_features_button = widgets.Button(
            description='Drop',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Drop the selected features',
            layout = self.auto_width_layout
            
        )
        

        self.label_encode_button = widgets.Button(
            description='Label Encode',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='click to apply label encoding',
            layout = self.auto_width_layout
        )
        

        self.one_hot_encode_button = widgets.Button(
            description='One-Hot Encode',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='click to apply one-hot-encoding',
            layout = self.auto_width_layout
            
        )
        
        self.selectScaleType = widgets.Dropdown(
            description='Method to use',
            options ={"Standard Scalar":"STANDARD_SCALAR",
                      "Min Max Scalar": "MIN_MAX_SCALAR",
                      "Robust Scalar":"ROBUST_SCALAR",
                      "Normalise": "NORMALIZER"},
            value="STANDARD_SCALAR",
            disabled=False,
            style=self.style,
            layout = self.auto_width_layout
        )

        
        self.apply_scale_button = widgets.Button(
            description='Apply scaling/normalisation',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            layout = self.auto_width_layout     
        )
        
        self.view_scale_button = widgets.Button(
            description='View effect of scaling/normalisation',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            layout = self.auto_width_layout     
        )
        
        
        
        self.save_file_button = widgets.Button(
            description='Save Transformed data',
            disabled=False,
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save the transformed data to csv',
            layout = self.auto_width_layout   
        )
        
        
        
        self.progressBar = widgets.FloatProgress(
            value=0.0, 
            min=0.0, 
            max=1.0,
            layout = self.auto_width_layout,
        )
        
        

        self.ref_name_box = widgets.Checkbox(False, description='Use group descriptions')
        self.pre_encode_box = widgets.Checkbox(False, description='Use pre-encoded group names')
        self.pre_merge_box =  widgets.Checkbox(False, description='Use pre-merged groups')

        
        #functions called on buttons clicked
        self.analyze_missing_data_button.on_click(self.on_analyze_missing_data_button_clicked)
        self.view_representation_button.on_click(self.on_view_representation_button_clicked)
        self.merge_values_button.on_click(self.on_merge_button_clicked)
        self.save_description_button.on_click(self.on_save_description_button_clicked)
        
        self.label_encode_button.on_click(self.on_label_encode_button_clicked)
        self.one_hot_encode_button.on_click(self.on_one_hot_encode_button_clicked)
        self.apply_scale_button.on_click(self.on_apply_scale_button_clicked)
        self.view_scale_button.on_click(self.on_view_scale_button_clicked)
        self.profile_data_button.on_click(self.on_profile_data_button_clicked)
        self.drop_features_button.on_click(self.on_drop_features_button_clicked)
        self.save_file_button.on_click(self.on_save_file_button_clicked)
        
        
        self.uploadFileOutput = widgets.interactive_output(self.upload_new_file_function, {
                                'fileUploader_value': self.fileUploader})
        
        
        
        
        self.selectLabelYOutput = widgets.interactive_output(self.selectLabelYFunction, {
                                'selectYFeature_values': self.selectYFeature})
  

        self.selectLabelXOutput = widgets.interactive_output(self.selectLabelXFunction, {
                                'selectXFeatures_values': self.selectXFeatures,
                                'selectProtectedAttributes_values': self.selectProtectedAttributes})
        
        self.analyzeMissingDataOutput = widgets.Output(layout={})
        self.missingDataProcessedOutput = widgets.Output(layout={})
        
        self.selectReferenceGroupsOutput = widgets.interactive_output(self.selectReferenceGroupsFunction, {
                                'selectProtectedAttributes_values': self.selectProtectedAttributes})            
    
        self.auditRepresentationOut = widgets.interactive_output(self.viewGroupRepresentationFunction, {
                                'selectProtectedAttributes_values': self.selectProtectedAttributes})
         
        self.viewRepresentationOut  = widgets.Output(layout={})
        
        self.viewOutputDistributionOut  = widgets.interactive_output(self.viewOutputDistributionFunction, {
                                'selectProtectedAttributes_values': self.selectProtectedAttributes,
                                'selectYFeature_values': self.selectYFeature})
        
        self.auditOutputDistributionOut  =  widgets.Output(layout={}) 
        
        
        self.selectFeatureAuditOutput = widgets.interactive_output(self.selectFeatureAuditFunction, {
                                'selectXFeatures_values': self.selectXFeatures,
                                'selectProtectedAttributes_values': self.selectProtectedAttributes})
        
        self.selecImpactOutput = widgets.interactive_output(self.selectImpactFunction, {
                                'selectImpact_values': self.selectImpact})
        
        self.selecGTOutput = widgets.interactive_output(self.selectGTFunction, {
                                'gtAssumption_values': self.gtAssumption})
        
        self.workInProgressOut = widgets.Output(layout={})
        
        self.mergeOut = widgets.interactive_output(self.set_selected_categorical_values, {
                        'theSelectedCategoricalFeaturesDropDown_value': self.theSelectedCategoricalFeaturesDropDown,})
        
        self.saveDescriptionOut  = widgets.Output(layout={})
        
        self.descriptionChoiceOut = widgets.Output(layout={})
        
        self.theSelectedInputFeaturesChoiceOut = widgets.interactive_output(self.selected_features_choice, {
                        'theSelectedInputFeaturesChoice_value': self.theSelectedInputFeaturesChoice,})
             
        self.LEOut = widgets.Output(layout={})

        self.HotEncodeOut = widgets.Output(layout={})

        self.scaleNormaliseOut = widgets.Output(layout={})

        self.correlationsOut = widgets.Output(layout={})
        self.profileDataOut = widgets.Output(layout={})
        self.dropColOut = widgets.Output(layout={})           

       
    
        #Create and display a FileChooser widget with path = current path
        self.fcOut = widgets.Output(layout={})
        self.fc = FileChooser()
        
            
            
        
    ################################################################################################
    #  Use the sample LSAT data 
    #
    #################################################################################################     
    def use_sample_dataset(self):
    #   self.__init__()
    
        
        with self.uploadFileOutput:
            path = os.path.dirname(sys.modules[__name__].__file__)
            file = open( path + "/data/law_data.csv", "rb")
            file_bytes = file.read()
            demo_file_dict = {'law_data.csv': 
                             {'metadata': 
                                {'name': 'law_data.csv', 
                                 'type': 'text/csv', 
                                 'size': 981371, 
                                 'lastModified': 1563733119625}, 
                                 'content':file_bytes}}
            self.uploadFileFunction(demo_file_dict)
            
            demo = demo_data.demo_data()
            html = widgets.HTML(demo.html)
            accordion = widgets.Accordion(children=[html])

            accordion.set_title(0, 'Law School, Sample data overview')
            accordion.selected_index=None
            display(accordion)
            
        
    
    ################################################################################################
    #  When a new file is upliaded refresh everything to start again
    #
    ################################################################################################# 
    def upload_new_file_function(self, fileUploader_value):
        if bool(fileUploader_value) != False: 
            self.uploadFileFunction(fileUploader_value)
            
       
    #################################################################################################
    #  Upload the Training/Test/Validate .csv file for analysis
    # 
    #################################################################################################     
    def uploadFileFunction(self, fileUploader_value):
        try:
            
            for key in fileUploader_value:
                text = "File uploaded: " + fileUploader_value[key]['metadata']['name']
                self.df_url = fileUploader_value[key]['metadata']['name']
                dl = date.today().strftime("%d_%m_%Y")
                _filename = 'transformed_' + dl + '_' + str(self.df_url)
                #updating the File chooser that is displated at end of the process
                #so that it already defaults to current working dir.
                self.fc = FileChooser(os.getcwd()+ '/transformed_data', 
                                      filename=_filename,
                                      select_default=True,
                                      show_hidden = True,
                                      use_dir_icons = True,
                                    )
                self.helper_methods.display_html (text, self.text_color, "h4")
                with self.fcOut:
                    clear_output(wait = True)
                    display (self.fc, self.save_file_button)
                try:
                    csvInBytes = fileUploader_value[key]['content']
                    s = str(csvInBytes, 'utf-8')
                    data = StringIO(s)
                    self.df = pd.read_csv(data)
                    if self.df.columns[0] ==  "Unnamed: 0":
                        self.df = self.df.drop(["Unnamed: 0"], axis=1)
                    del csvInBytes
                    del data
                    del s
                    self.helper_methods.display_html ("Snapshot of data",self.text_color, "h3")
                    dbOut = widgets.Output(layout={})
                    with dbOut:
                        display (self.df.head(4))
                        old = widgets.Dropdown(description = "Column", options = self.df.columns)
                        new = widgets.Text(value=list(self.df.columns)[0], description='New Name:', disabled=False)
                        display (old, new)
                    display (dbOut)
                    #self.selectColumnWithMissingData.options = self.df.columns[self.df.isnull().any()]
                    _button = widgets.ToggleButton(value=True, 
                                                   description='Rename',
                                                   button_style='success')
                    def rename_col( button):
                        if _button.value == False:
                            self.df = self.df.rename(columns={old.value: new.value})  
                            self.helper_methods.display_html ("Column '" + old.value + "' renamed to '" + new.value + "'!",self.text_color, "p") 
                            with dbOut:
                                clear_output(wait = True)
                                display (self.df.head(4))
                                self.helper_methods.display_html ("Note: Any columns should be renamed at beginning of process!","orange", "p") 
                                old.options = self.df.columns
                                display (old, new)
                                self.selectXFeatures.options = self.df.columns.values
                                self.selectProtectedAttributes.options = self.df.columns.values
                                self.selectYFeature.options = self.df.columns.values
                                old.value = new.value
                                new.value = ""
                                
                        _button.value = False
                    interact(rename_col, button = _button)
     
                except BaseException as error:      
                    text = "Error reading file - upload new file"
                    self.helper_methods.display_html (text, "red")
                    display('An exception occurred: {}'.format(error))
        except BaseException as error:
            display("Error uploading file - upload again")
            display('An exception occurred: {}'.format(error))
        display()    
        self.selectXFeatures.options = self.df.columns.values
        self.selectProtectedAttributes.options = self.df.columns.values
        self.selectYFeature.options = self.df.columns.values
        gc.collect()

   
                    
    #################################################################################################
    #  
    # 
    #################################################################################################                 
    def selectLabelYFunction(self, selectYFeature_values):    
        if not self.df.empty:       
            #Once we select a label, remove it from possible input features dropdown
            try:
                #store the entire label column in its own dataframe
                self.y_label_df = self.df[selectYFeature_values].copy().to_frame()
                listx = list(self.df.columns.values) 
                #use different ways to remove an item of the list
                listx.remove(selectYFeature_values) 
                #converting the tuple to list
                tuplex = tuple(listx)
                self.selectXFeatures.options =tuplex
                self.selectProtectedAttributes.options =tuplex
            except:
                self.selectXFeatures.options = self.df.columns.values
                self.selectProtectedAttributes.options = self.df.columns.values
            
            if selectYFeature_values == None:
                self.helper_methods.display_html ("None Selected!", self.text_color, "h5")
   
            
            if selectYFeature_values != None:
                colType = self.df[selectYFeature_values].dtype
                unique_vals = self.df[self.selectYFeature.value].dropna().unique()
                #If the output label has only 2 unique values then convert to binary
                if len(self.df[self.selectYFeature.value].dropna().unique()) == 2:
                    result =  all(elem in [1,0]  for elem in list(self.df[self.selectYFeature.value].dropna().unique()))
                    #if already binary
                    if result == True :
                        text = "The data to predict is Binary."
                        self.helper_methods.display_html (text, self.text_color, "p")
                        yMin = round(
                        self.df[selectYFeature_values].min(), 3)
                        yMean = round(
                        self.df[selectYFeature_values].mean(), 3)
                        yMax = round(
                        self.df[selectYFeature_values].max(), 3)
                        self.Y_BINARY = True
                        self.Y_CONTINUOUS  = False
                    #else convert to binary    
                    elif result == False :
                        self.helper_methods.display_html ("Converted the label values to Binary(0/1) to continue.", self.text_color, "p")
                        values = unique_vals

                        convert_val = widgets.Dropdown(description="Convert Label '" + str(values[0]) + "' to ",
                                                        options=[0, 1],
                                                        style=self.style)
                        new_values = [0,1]
                        
                        #inner function, local to outer funct
                        def convert_to_bin (convert_val):
                            if convert_val == 0:
                                text = "Convert Label '" + str(values[1]) + "' to 1"
                                self.helper_methods.display_html(text, "black", "p")
                                new_values = [0,1]    
                            else:
                                text = "Convert Label '" + str(values[1]) + "' to 0"
                                self.helper_methods.display_html(text, "black", "p")
                                new_values = [1,0]   
                            #inner inner function,   
                            def convert(button):
                                self.df[self.selectYFeature.value].replace({values[0]: new_values[0], 
                                                                        values[1]: new_values[1]}, 
                                                                       inplace=True)
                                text = "Converted " + str(values[0]) + " to " + str(new_values[0])
                                self.helper_methods.display_html(text, self.text_color, "p")
                                text = "Converted " + str(values[1]) + " to " + str(new_values[1])
                                self.helper_methods.display_html(text, self.text_color, "p")
                                self.Y_BINARY = True
                                self.Y_CONTINUOUS  = False
                                yMin = round(
                                self.df[selectYFeature_values].min(), 3)
                                yMean = round(
                                self.df[selectYFeature_values].mean(), 3)
                                yMax = round(
                                self.df[selectYFeature_values].max(), 3)
                                
                                self.y_label_df = self.df[selectYFeature_values].copy().to_frame()

   
                            convert_button = widgets.Button(description='Convert to Binary',
                                                        layout = self.auto_width_layout)
                            
                            convert_button.on_click(convert)
                            #button to convert values to new_values
                            display (convert_button)
   
                        interact(convert_to_bin, convert_val = convert_val )
                        
                #If the output label has more tham 2 unique values.....      
                elif colType != str and colType != object: #There are more than 2 unique values.
                    text = "The data to predict is a continuous value, "
                    self.Y_BINARY = False
                    self.Y_CONTINUOUS  = True
                    yMin = round(
                    self.df[selectYFeature_values].min(), 3)
                    yMean = round(
                    self.df[selectYFeature_values].mean(), 3)
                    yMax = round(
                    self.df[selectYFeature_values].max(), 3)
                    text = text + "between " + str(yMin) + " and "+ str(yMax) +", with a mean of " + str(yMean)
                    self.helper_methods.display_html (text, self.text_color, "p")
                    
                else:
                    clear_output(wait=True)
                    self.helper_methods.display_html ("The selected output label is not numeric or binary! Only Binary or Continuous Numerical outputs are currently supported by the tool", "orange", "p")
                    unique_vals = list(self.df[self.selectYFeature.value].dropna().unique())
                                      
       
    #################################################################################################
    #  
    # 
    #################################################################################################           
    def selectImpactFunction(self, selectImpact_values):
        #Default value is High
        if selectImpact_values == 1:
            self.HIGH_RANGE_POSITIVE = True
            self.helper_methods.display_html ("Your choice indicates that the <b>higher</b> the predicted score the better the outcome for the individual", self.text_color,  "p")
        else:
            self.HIGH_RANGE_POSITIVE = False
            self.helper_methods.display_html ("Your choice indicates that the <b>lower</b> the predicted score the better the outcome for the individual",  self.text_color, "p")
     
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################           
    def selectGTFunction(self, gtAssumption_values):       
        select_zero = self.ground_truth_zero_text
        
        
        select_zero_ex_0 = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" >
            <b>Example 1</b>: Policing in the UK. Between April 2018 and March 2019, 
            there were 4 stop and searches for every 1,000 White people, compared with 38 for 
            every 1,000 Black people. This figure has decreased year on year from 2009 where 
            there were 19 stop and searches for every 1000 White people compared to 117 for 
            every 1000 Black people. Black people also had the highest stop and search rates 
            in every police force area for which there was data. A police officer may stop and 
            search on the subjective proviso that “the officer has a reasonable cause to suspect 
            they will find something”.  Only 9% of stops and searches resulted in an arrest at the 
            peak of its use in 2008/9. This number has increased since 2009 and was 17% in 2017/18. 
            Offence detections are similar regardless of ethnicity, such that around 25% of searches 
            result in some form of action being taken. Black people are almost ten times more likely 
            to be stopped yet the likelihood of offence detection is similar regardless of ethnicity 
            with a higher offence detection for white people compared to black people. If this historic
            data from 2008 to 2019 were to be used to train a model to predict the “reasonable cause”, 
            It is possible that this disproportionate rate may result in the model reflecting the subjective
            grounds for “reasonable cause” used by historic and current members of the police force. <br>

            <font style="font-family:sans-serif; font-size:12px;color:black;">
            <br><a href="https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/stop-and-search/latest
             " target="_blank">Stop-and-search - latest, gov.uk </a>
             
             <br><a href="https://fullfact.org/crime/stop-and-search-england-and-wales/
             " target="_blank">Stop and Search - England and Wales, fullfact.org </a>
             <br><a href=https://www.theguardian.com/law/2019/jan/26/met-police-disproportionately-use-stop-and-search-powers-on-black-people
             " target="_blank">Met police disproportionately use stop and search powers on black people, theguardian.com </a>
            
             <br><br>
             <br>""")
        select_zero_ex_1 = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" > 
            <b>Example 2</b>: Prior to the passage of the 1974 Equal Credit Opportunity Act in the USA, 
            banks often had explicit policies to treat women less favorably than men. 
            As documented by several surveys in the 1970s, mortgage lenders often discounted a wife's 
            income by 50 percent or more when evaluadng mortgage applications and banks were more likely
            to discount the wife's income if she was of child-bearing age or if the family included 
            pre-school children. The Equal Credit Opportunity Act of 1974 prohibited sex-based 
            classificadons and income discounting(Schafer and Ladd, 1981; Ladd,1982). <br>
            """ )

        select_zero_ex_2 = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" >       
            <b>Example 3:</b> In the 1930's whole neighborhoods in the US were subject to "redlining" where they were classified
            according to their "credit characteristics". Green for “best,” blue for “still desirable,” yellow 
            for “definitely declining” and red for “hazardous.” The Humans responsible for approving mortgages
            often discounted an individual’s chances of receiving a mortgage based on this geographic status. 
            Low rating neighbourhoods ("redlined" as hazardous) were frequently poor or dominated by racial 
            and ethnic minorities and thetefor residents were frequently rejected for mortgage approval based largely
            on this fact. It is thought that this lead to continued segregation, keeping minorities out of predominately
            white "Green" neighbourhoods. This practice continued legally until 1968 however this does not necessarally
            mean the practice was eradicated as for years after it fell largely to local civil rights groups to
            highlight the problem. 
            """)
        
        
        attend_zero = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" >
             - Pay attention to the representation of protected groups in the dataset, are some groups represented more than
             others? why? <br>
             - Pay attention to any differences in distribution of the target outcome across the groups,
             are there statistically significant differences in the distribution? why?
             - Pay attention to any differences in distribution of input feature values across the groups,
             are there statistically significant differences in the distribution? why?
             """)
        
        select_one = self.ground_truth_one_text
        
        select_one_ex_1 = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" >
            <b>Example 1:</b>When training a model to detect homelessness, because of varying definitions of 
            homelessness and the transient nature of homeless populations it is difficult
            to definitively say if a person is homeless or not. The legal definition of homeless also varies 
            from country to country, examples include living on the streets, moving between temporary shelters,
            moving between houses of friends, family and emergency accommodation,
            living in private boarding houses without a private bathroom. A homeless(yes/no) might be used as the
            target to train a model however the yes or no label might actually be extrapolated from other features which
            can be objectively observed and measured. This is therefor an intentional proxy which may 
            not necessarily reflect the ground truth outcome and may result in bias against certain protected groups.
            """)
        
        select_one_ex_2 = widgets.HTML("""
           <font style="font-family:sans-serif; font-size:15px;color:grey;" >
           <b>Example 2: </b>When training a model to detect "at risk" children,
            “at risk” might be extrapolated from a variety of different indicators, including 
            having limited reading proficiency, having experienced abuse or trauma, having a disability
            or illness, having exhibited behavior problems. Measures of family risk include
            poverty, a low level of parental education, a large number of children, not owning a home, 
            single parenthood, welfare dependence, family dysfunction, abuse, parental mental illness, 
            parental substance use, and family discord or illness. Therefor a target which defines 'at
            risk' with a label (yes/no) might have been extrapolated from features that can be 
            observed and measured, but which may not necessarally represent the ground truth in terms of "at risk". 
            This intentional use of a proxy may result in bias against certain protected groups. 
            """)
        
        attend_one = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;" >
            Add some information here.
            """)

        select_two = self.ground_truth_two_text
        
        attend_two =  widgets.HTML(
            """<font style="font-family:sans-serif; font-size:15px;color:grey;">
            Remember, this does not imply that there is no prejudice reflected in the ground-truth or that the 
            resulting model will not be unfair. Even when our ground truth is confirmed to be true i.e a real-world outcomes 
            (e.g. loan repayment/default, exam score, reoffence/no reoffend) prejudice can still be 
            reflected in the target. 
            
            Example: If a borrower was historically judged to be 'high risk' due solely to their membership of
            a protected group, it could happen that a loan or mortgage might have been approved but with a higher
            interest rate and therefor a higher repayment rate which in turn could increase the liklihood of 
            defaulting on the loan. We have no way to determine what the outcome might have been
            had a 'low risk' interest rate been objectively applied without prejudice. 
            """)
        
        out = widgets.Output()
        #local method
        def display_ex_0 (exa): #subjective representation
            with out:
                out.clear_output(False)
                if exa.tooltip == "Show":
                    if exa.description == 'Watch out for':
                        display (attend_zero)
                        wf.tooltip = "Hide"
                        ex0.tooltip = "Show"
                        ex1.tooltip = "Show"
                        ex2.tooltip = "Show"
                    elif exa.description == 'Example 1':
                        display ( select_zero_ex_0)
                        wf.tooltip = "Show"
                        ex0.tooltip = "Hide"
                        ex1.tooltip = "Show"
                        ex2.tooltip = "Show"
                    elif exa.description == "Example 2":
                        display ( select_zero_ex_1) 
                        wf.tooltip = "Show"
                        ex0.tooltip = "Show"
                        ex1.tooltip = "Hide"
                        ex2.tooltip = "Show"
                        
                    elif exa.description == "Example 3":
                        display ( select_zero_ex_2) 
                        wf.tooltip = "Show"
                        ex0.tooltip = "Show"
                        ex1.tooltip = "Show"
                        ex2.tooltip = "Hide"
                                        
                elif exa.tooltip == "Hide":
                    if exa.description == 'Watch out for':
                        wf.tooltip = "Show"
                    elif exa.description == 'Example 1':
                        ex0.tooltip = "Show"
                    elif exa.description == "Example 2":
                        ex1.tooltip = "Show"
                    elif exa.description == "Example 3":
                        ex2.tooltip = "Show"
        #local method
        def display_ex_1 (exa):
            with out:
                out.clear_output(False)
                if exa.tooltip == "Show":
                    if exa.description == 'Watch out for':
                        display (attend_one)
                        wf.tooltip = "Hide"
                        ex1.tooltip = "Show"
                        ex2.tooltip = "Show"
                    elif exa.description == 'Example 1':
                        display ( select_one_ex_1)
                        wf.tooltip = "Show"
                        ex1.tooltip = "Hide"
                        ex2.tooltip = "Show"
                    elif exa.description == "Example 2":
                        display ( select_one_ex_2) 
                        wf.tooltip = "Show"
                        ex1.tooltip = "Show"
                        ex2.tooltip = "Hide"    
                elif exa.tooltip == "Hide":
                    if exa.description == 'Watch out for':
                        wf.tooltip = "Show"
                    elif exa.description == 'Example 1':
                        ex1.tooltip = "Show"
                    elif exa.description == "Example 2":
                        ex2.tooltip = "Show"
        #local method           
        def display_ex_2 (exa):
            with out:
                out.clear_output(False)
                if exa.tooltip == "Show":
                    if exa.description == 'Watch out for':
                        display (attend_two)
                        wf.tooltip = "Hide"
                        #ex1.tooltip = "Show"
                        #ex2.tooltip = "Show"
                    #elif exa.description == 'Example 1':
                         #display ( select_two_ex_1)
                         #wf.tooltip = "Show"
                         #ex1.tooltip = "Hide"
                         #ex2.tooltip = "Show"
                     #elif exa.description == "Example 2":
                         #display ( select_two_ex_2) 
                         #wf.tooltip = "Show"
                         #ex1.tooltip = "Show"
                         #ex2.tooltip = "Hide"
                        
                elif exa.tooltip == "Hide":
                    if exa.description == 'Watch out for':
                        wf.tooltip = "Show"
                    #elif exa.description == 'Example 1':
                         #ex1.tooltip = "Show"
                    #elif exa.description == "Example 2":
                        #ex2.tooltip = "Show"
        
        if gtAssumption_values == 0:
            self.GT_VALIDITY = select_zero
            display (widgets.GridBox(children=[widgets.HTML("""<font style="font-family:sans-serif; 
                                                               font-size:15px;color:grey;">
                                                            """ + select_zero)],
                        layout=Layout(
                        width='100%',
                        )
                    ))
            
            ex0 =  widgets.Button(
                                description='Example 1',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )
            ex1 = widgets.Button(
                                description='Example 2',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )

            ex2 = widgets.Button(
                                description='Example 3',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )
            wf = widgets.Button(
                                description='Watch out for',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' ,# (FontAwesome names without the `fa-` prefix)
                                )
            
            
            display (widgets.HBox([ex0, ex1,ex2, wf]))
            display (out)
            ex0.on_click(display_ex_0)
            ex1.on_click(display_ex_0)
            ex2.on_click(display_ex_0)
            wf.on_click(display_ex_0)
    
        elif gtAssumption_values == 1:
            self.GT_VALIDITY = select_one
            display (widgets.GridBox(children=[widgets.HTML("""<font style="font-family:sans-serif; 
                                                               font-size:15px;color:grey;">
                                                            """ + select_one)],
                        layout=Layout(
                        width='100%',
                        )
                    ))
            
            ex1 = widgets.Button(
                                description='Example 1',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )
            
            ex2 = widgets.Button(
                                description='Example 2',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )

            wf = widgets.Button(
                                description='Watch out for',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )
            
            
            display (widgets.HBox([ex1,ex2, wf]))
            display (out)
            ex1.on_click(display_ex_1)
            ex2.on_click(display_ex_1)
            wf.on_click(display_ex_1)
                
        elif gtAssumption_values == 2:
            self.GT_VALIDITY = select_two
            display (widgets.GridBox(children=[widgets.HTML("""<font style="font-family:sans-serif; 
                                                               font-size:15px;color:grey;">
                                                            """ + select_two)],
                        layout=Layout(
                        width='100%',
                        )
                    ))
            
           
            wf = widgets.Button(
                                description='Watch out for',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                                icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                                )
            
            
            display (widgets.HBox([wf]))
            display (out)
            wf.on_click(display_ex_2)

    
    #################################################################################################
    #  Select the columns that represent possible input features and identify protected
    #  features
    ################################################################################################# 
    def selectLabelXFunction(self, selectXFeatures_values, selectProtectedAttributes_values):
        self.helper_methods.display_html ("- No input features (X) selected!", self.text_color, "p")
        self.helper_methods.display_html ("- No Protected Features Selected!", self.text_color, "p") 
        protected = []
        non_protected = []
        if not self.df.empty:
            with self.selectLabelXOutput:
                clear_output(wait=True) 
                self.non_protected_feature_set_df = self.df
                #drop list contains all the Features not yet selected as X value.
                drop_list = set(selectXFeatures_values).symmetric_difference(
                    self.selectXFeatures.options)

                if len(selectXFeatures_values) == 0:
                    self.helper_methods.display_html ("- No input features (X) selected", self.text_color, "p")
                else:
                    self.helper_methods.display_html ("- Selected Features (X): " + str(list(selectXFeatures_values)), self.text_color, "p")
                    protected = list(selectXFeatures_values)

                if len(selectProtectedAttributes_values ) == 0:
                    self.helper_methods.display_html ("- No Protected Features Selected", self.text_color, "p")
                else:
                    self.helper_methods.display_html ("- Selected Protected Features: " + str(list(selectProtectedAttributes_values)), self.text_color, "p")
            
                for c in drop_list:
                    try:
                        self.non_protected_feature_set_df = self.df.drop(columns = c, axis=1)
                    except:
                        print(c + "not a selected feature")
                self.non_protected_feature_set_df = self.non_protected_feature_set_df.drop(columns = self.selectYFeature.value, axis=1) 
        
            
                if len(selectProtectedAttributes_values) != 0:
                    for c in list(selectProtectedAttributes_values):
                        try:
                            self.non_protected_feature_set_df = self.non_protected_feature_set_df.drop(columns = c, axis=1) 
                        except:
                            print(c + "not a selected feature")
                    self.protected_feature_set_df = self.df[list(selectProtectedAttributes_values)].copy()
                    non_protected = list(selectProtectedAttributes_values) 
                    
                #Refactor later to use protected[] and non_protected[] and y_value to populate self.feature_data_dict
                
                #get/refresh a list of protected and non-protected based on the data frame 
                self.get_all_engineered_features()[2]#we only want 3d output of funct
            
        wf = widgets.Button(description='Watch out for',
                        disabled=False,
                        tooltip = "Show",
                        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                        icon='fa-eye' ,# (FontAwesome names without the `fa-` prefix)
                        )

        _xml = widgets.HTML("""
                        <font style="font-family:sans-serif; font-size:15px;color:grey;">
                        <b>Fairness and Disparate Treatment (Direct Bias)</b> — A decision-making process suffers 
                        from disparate treatment if the decision or outcom is in any way dependant on a protected Feature. 
                        It generally involves an intent to discriminate, in the case of ML this can occur when the model 
                        detects a correlation between the feature in question(such as gender, race, religion or age) 
                        and the historic outcomes/decisions specified in the training data.

                        While protected features should not necessarally be used as an input feature to train a model
                        it is important to retain/track this information rather than simply taking a "blind" approach 
                        because as we will see later we need to consider the possibility that proxies for protected 
                        features may exist in the non-protected features(e.g. postcode). 
                        We also need to measure fairness based upon these explicitly protected 
                        features. Imposing a willful blindness by removing and then ignoring the protected feature 
                        makes it harder to detect, prevent, and reverse bias. 

                        As stated by Dwork et al. being <b>“colorblind”</b> or simply ignoring protected 
                        attributes will not ensure fairness in decision making by algorithms.  
                        """)
        out = widgets.Output()
        def watch_out_for (_button):    
            if wf.tooltip == "Show":
                with out:
                    clear_output(wait = False)
                    display(_xml)
                wf.tooltip = "Hide"
            elif wf.tooltip == "Hide":
                with out:
                    clear_output(wait = False)
                    wf.tooltip = "Show"


        wf.on_click(watch_out_for)
        display (wf)
        display (out)
            
            
            
            
    #################################################################################################
    #  
    # 
    ################################################################################################# 
    def on_analyze_missing_data_button_clicked (self, b):
        with self.analyzeMissingDataOutput:
            clear_output(wait=True)
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
                        progress.style.bar_color = self.text_color
                        break

            thread = threading.Thread(target=work, args=(progress,))
            display(progress)
            #start the progress bar thread
            thread.start()
            
            
            self.on_display_missing_data_info(self.selectProtectedAttributes.value, 
                                              self.get_dataframe(True, True)[0])
            
             
            finished = True
            
        
    #################################################################################################
    #  
    # 
    ################################################################################################# 
    def on_display_missing_data_info(self, protected_features_list, df ):

        null_columns=df.columns[df.isnull().any()]
        all_columns=df.columns.values
        style = {'description_width': 'initial'}
        layout = {'width': 'auto'}
        # There is some missing data, display information on the missing data
        # broken down by total, and then by protected feature.
        if len(null_columns) != 0:
            missing_data_tab = widgets.Tab()
            tab_one_output_area = widgets.Output(layout={})
            tab_two_output_area = widgets.Output(layout={})
            missing_data_tab.children = [tab_one_output_area, tab_two_output_area]
            missing_data_tab.set_title(0, "Total Missing Data")
            missing_data_tab.set_title(1, "Per Protected")

            with tab_one_output_area:
                total = df.shape[0] 
                text = "Number of Records: "+ str(total)
                missing = df.isnull().any(axis=1).sum() 
                percent = (missing/total)*100
                text = text + ", Number with missing data: "+ str(missing) + " (" + str(round(percent,2)) + "%)"
                self.helper_methods.display_html (text, "black", "p")

                num_cols = df.shape[1] 
                text = "Number of Columns: "+ str(num_cols)
                selectColumnWithMissingData_options = df[null_columns].isnull().sum().index
                missing = len(selectColumnWithMissingData_options)
                text = text + ", Number with missing data: " + str(missing)
                self.helper_methods.display_html (text, "black", "p")
                html ="""Nullity correlation ranges from:<br>
                <b>-1 :</b> If one variable appears the other definitely does not)<br>
                <b> 0 :</b> Variables appearing or not appearing have no effect on one another)<br>
                <b> 1 :</b> If one variable appears the other definitely also does.<br>

                Variables that are always full or always empty have no meaningful correlation are 
                not visualized """
                display(HTML(html))

                fig = plt.figure(figsize=(14,7));
                ax1 = fig.add_subplot(1,2,1);
                msno.bar(df, color="dodgerblue", sort="ascending", fontsize = 12, ax = ax1) ;
                ax2 = fig.add_subplot(1,2,2);
                msno.heatmap(df, fontsize = 12, ax = ax2);
                plt.tight_layout();
                plt.show()

                for col in selectColumnWithMissingData_options:
                    missing = df[col].isnull().sum()
                    pcnt_missing = (missing/total)*100
                    if col in protected_features_list:
                        text = '<b>Protected Feature: </b>'
                    else:
                         text = '<b>Feature: </b>'
                    display (widgets.HBox([widgets.HTML(text + col + ", "), 
                                   widgets.HTML("    <b>Number missing:</b> " + str(missing) + ", "),
                                   widgets.HTML("    <b>Percent missing:</b> "+ str(round(pcnt_missing,1)) + '%')
                                          ]))

                missingDataRowsThresholdSlider = widgets.IntSlider(
                                    value=70,
                                    description= "Row threshold(percent)" ,
                                    max=100,
                                    min=0,
                                    style=style,
                                    layout = layout
                                    )

                missingDataColumnsThresholdSlider = widgets.IntSlider(
                                    value=70,
                                    description= "Column threshold(percent)" ,
                                    max=100,
                                    min=0,
                                    style= style,
                                    layout = layout
                                    )

                remove_rows_button = widgets.Button(description='Remove Rows',
                                                    tooltip='Remove rows or columns where x% of data is missing',
                                                    layout = layout
                                                    )

                remove_cols_button = widgets.Button(description='Remove Columns',
                                                    tooltip='Remove rows or columns where x% of data is missing',
                                                    layout = layout
                                                    )

                def missing_row_protected(row_pcnt):
                    rows = df.loc[df.isnull().mean(axis=1)*100 > row_pcnt]
                    text = str(len(rows))+ " rows have more than " + str(row_pcnt) + "% missing data." 
                    self.helper_methods.display_html (text, "black", "p")
                    if rows.shape[0] > 0:
                        display (rows)

                def missing_column_protected(col_pcnt):
                    columns = df[df.columns[df.isnull().mean()*100 > col_pcnt]].columns
                    columns = list(columns)
                    if len(columns) > 0:
                        text = "Features " + str(columns) + " have more than " + str (col_pcnt) + "% missing records."
                    else:
                        text = "No Features have more than " + str (col_pcnt) + "% missing records."
                    self.helper_methods.display_html (text, "black", "p")

                def remove_rows_button_clicked(b):
                    #Dropping rows with missing value rate higher than threshold
                    row_index_to_remove = df.loc[df.isnull().mean(axis=1)*100 > missingDataRowsThresholdSlider.value].index
                    text = "Removed rows " + str(list(row_index_to_remove))
                    with self.missingDataProcessedOutput:
                        self.helper_methods.display_html (text, "black", "p")
                    
                    #Refresh the 3 seperate DataFrames, should rewrite code base to only use one!
                    self.y_label_df = df[self.selectYFeature.value]
                    non_prot_list = set(self.selectXFeatures.value).symmetric_difference(set(self.selectProtectedAttributes.value))
                    self.non_protected_feature_set_df = df[list(non_prot_list)]
                    self.protected_feature_set_df = df[list(self.selectProtectedAttributes.value)]
                    
                    #Call this outer function recursively to see the changes applied.
                    self.on_analyze_missing_data_button_clicked(self.analyze_missing_data_button)
                    return

                def remove_cols_button_clicked(b):
                    display(df.head())
                    #Dropping columns with missing value rate higher than threshold
                    to_drop = df[df.columns[df.isnull().mean()*100 > missingDataColumnsThresholdSlider.value]]
                    to_drop = list(to_drop)
                    df.drop(to_drop, axis = 1, inplace = True)
                    text = "removed columns " + str(to_drop)
                    with self.missingDataProcessedOutput:
                        self.helper_methods.display_html (text, "black", "p")
                        
                    #Refresh the 3 seperate DataFrames, should rewrite code base to only use one!
                    self.y_label_df = df[self.selectYFeature.value]
                    non_prot_list = set(self.selectXFeatures.value).symmetric_difference(set(self.selectProtectedAttributes.value))
                    self.non_protected_feature_set_df = df[list(non_prot_list)]
                    self.non_protected_feature_set_df.drop(to_drop, axis = 1, inplace = True)
                    self.protected_feature_set_df = df[list(self.selectProtectedAttributes.value)]
                    
                    #Call this outer function recursively to see the changes applied.
                    self.on_analyze_missing_data_button_clicked(self.analyze_missing_data_button)
                    return


                text = "Delete Rows with a significant amount of missing data:"
                self.helper_methods.display_html (text, "black", "h3")
                interact(missing_row_protected, row_pcnt = missingDataRowsThresholdSlider)
                remove_rows_button.on_click(remove_rows_button_clicked)
                display (remove_rows_button)


                text = "Delete Columns with a significant amount of missing data:"
                self.helper_methods.display_html (text, "black", "h3")
                interact(missing_column_protected, col_pcnt = missingDataColumnsThresholdSlider)

                remove_cols_button.on_click(remove_cols_button_clicked)
                display (remove_cols_button)
                
            #Now review per protected feature, by choosing the feature in tab 2
            with tab_two_output_area:
                selectProtectedDropDown = widgets.Dropdown(
                                                    options = protected_features_list,
                                                    description='Protected Feature',
                                                    disabled=False,
                                                    style=style,
                                                    layout = layout
                                                    )

                impute_dd_dict = {} 
                impute_protected = False
                
                def view_missing_per_protected(selected_protected):
                    #choice box will appear here in UX
                    if len(protected_features_list) == 0:
                        print ("No protected features selected!")
                        return
                    per_protected_tab = widgets.Tab()
                    out_dict = {}
                    tab_contents = []

                    box_layout = Layout(display='flex',
                    flex_flow='column',
                    align_items='stretch',
                    width='33%')

                    outer_box_layout = Layout(
                    border='solid 2px #34baeb',
                    padding = '5px',
                    width='100%')
                    
                    
                    impute_button = widgets.Button(description='Impute',
                                                    tooltip='Apply imputations as defined in tabs',
                                                    #layout = self.auto_width_layout
                                                    )
                    #######
                    #Check if there is missing data in the selected protected
                    if selected_protected in df[null_columns].isnull().sum().index:#There is missing data in the selected protected.
                        missing = df[selected_protected].isnull().sum()
                        pcnt_missing = (missing/df.shape[0] )*100 
                        _options = {}
                        most_frequent = df[selected_protected].value_counts().idxmax() 
                        _options["Most Frequent"] = most_frequent
                        unique_values = list(df[selected_protected].dropna().unique())
                        for _val in unique_values:
                            _options[_val] = _val
                            
                        num_values = len(unique_values)
                        impute_protected = True
                        impute_protected_choice  = widgets.Dropdown(description='Replace missing with:',
                                                             options = _options,         
                                                              style=style, 
                                                              layout = layout)
                        self.helper_methods.display_html (selected_protected, self.text_color, "h3")
                        display (widgets.HBox([
                             widgets.VBox([
                             widgets.HTML("<b>Type:</b> Categoric" ),  
                             widgets.HTML("    <b>Number Missing:</b> " + str(missing)),
                             widgets.HTML("    <b>Percent Missing:</b> "+ str(round(pcnt_missing,1)) + '%'),
                             ],layout = box_layout),
                             widgets.VBox([
                             widgets.HTML("    <b>Number Unique:</b> "+ str(num_values)),
                             widgets.HTML("    <b>Values:</b> "+ str(unique_values)),
                             widgets.HTML("    <b>Most Frequent:</b> "+ str(most_frequent)),
                             ],layout = box_layout),
                             widgets.VBox([
                             impute_protected_choice,
                            ],layout = box_layout),
                            ],layout = outer_box_layout))    
                                    
                    
                    #######
                    #Now check missing data broken down by the protected feature groups.
                    unique_vals = list(df[selected_protected].dropna().unique())
                    
                    
                    for value in unique_vals:
                        impute_dd_dict[value] = {}
                        temp = df.loc[df[selected_protected] == value]
                        out_dict[value] = widgets.Output(layout={})
                        with out_dict[value]:
                            num_rows = temp.shape[0] 
                            text = "Number of Records: "+ str(num_rows)
                            missing = temp.isnull().any(axis=1).sum() 
                            percent = (missing/num_rows) * 100
                            text = text + ", Number with missing data: "+ str(missing) + " (" + str(round(percent,2)) + "%)"
                            self.helper_methods.display_html (text, "black", "p")


                            selectColumnWithMissingData_options = temp[null_columns].isnull().sum().index
                            num_cols = len(selectColumnWithMissingData_options)
                            text = "Number of Columns with missing data: " + str(num_cols)
                            self.helper_methods.display_html (text, "black", "p")
                            
                            
                            #create UX for all of the other columns with missing data
                            #broken down per value in the selected protected.
                            categorical_list, numeric_list = self.helper_methods.get_features_type( df, 20)
                            for col in selectColumnWithMissingData_options:   
                                if col != selected_protected:
                                    if col in protected_features_list:
                                        text = '<b>Protected Feature: </b>'
                                    else:
                                         text = '<b>Feature: </b>'
                                    missing = temp[col].isnull().sum()
                                    pcnt_missing = (missing/total)*100
                                    
                                    if col in numeric_list:
                                        median = df[col].median()
                                        minimum = df[col].min()
                                        maximum = df[col].max()
                                        num_values = len(list(df[col].dropna().unique()))
                                        impute_dd_dict[value][col] = widgets.Dropdown(
                                                              description='Replace missing with:',
                                                              options = {"Median":median,
                                                                         "Minimum":minimum,
                                                                         "Maximum":maximum },          
                                                                         style=style, 
                                                                         layout = layout
                                                             )

                                  
                                        self.helper_methods.display_html (text + col, self.text_color, "h3")
                                        display (widgets.HBox([
                                             widgets.VBox([
                                             widgets.HTML("<b>Type:</b> Numeric" ), 
                                             widgets.HTML("    <b>Number Missing:</b> " + str(missing)),
                                             widgets.HTML("    <b>Percent Missing:</b> "+ str(round(pcnt_missing,1)) + '%'),
                                             ], layout = box_layout),
                                             widgets.VBox([
                                             widgets.HTML("    <b>Number Unique:</b> "+ str(num_values)),
                                             widgets.HTML("    <b>Median:</b> "+ str(median)),
                                             widgets.HTML("    <b>Min:</b> "+ str(minimum)),
                                             widgets.HTML("    <b>Max:</b> "+  str(maximum)),
                                             ],layout = box_layout),
                                             widgets.VBox([
                                                 impute_dd_dict[value][col]
                                             ],layout = box_layout),
                                            ],layout = outer_box_layout))


                                    elif col in categorical_list:#Categoric
                                        _options = {}
                                        most_frequent = df[col].value_counts().idxmax() 
                                        _options["Most Frequent"] = most_frequent
                                        unique_values = list(df[col].dropna().unique())
                                        for _val in unique_values:
                                            _options[_val] = _val
                                        num_values = len(unique_values)
                                        impute_dd_dict[value][col]  = widgets.Dropdown(
                                                                     description='Replace missing with:',
                                                                     options = _options,         
                                                                      style=style, 
                                                                      layout = layout
                                                                     )
                                        self.helper_methods.display_html (text + col, self.text_color, "h3")
                                        display (widgets.HBox([
                                             widgets.VBox([
                                             widgets.HTML("<b>Type:</b> Categoric" ),  
                                             widgets.HTML("    <b>Number Missing:</b> " + str(missing)),
                                             widgets.HTML("    <b>Percent Missing:</b> "+ str(round(pcnt_missing,1)) + '%'),
                                             ],layout = box_layout),
                                             widgets.VBox([
                                             widgets.HTML("    <b>Number Unique:</b> "+ str(num_values)),
                                             widgets.HTML("    <b>Values:</b> "+ str(unique_values)),
                                             widgets.HTML("    <b>Most Frequent:</b> "+ str(most_frequent)),
                                             ],layout = box_layout),
                                             widgets.VBox([
                                             impute_dd_dict[value][col]
                                            ],layout = box_layout),
                                            ],layout = outer_box_layout))


                    per_protected_tab.children = list(out_dict.values())
                    for title, x in zip(list(out_dict.keys()), range(len(list(out_dict.keys())))):
                        per_protected_tab.set_title(x, title)
                    display(per_protected_tab)


                    def on_apply_imputation_button_clicked(b):
                        #Filling all missing values with 0
                        protected = selectProtectedDropDown.value
                        with self.missingDataProcessedOutput:
                            clear_output (wait = True)
                            #Impute any missing values for the selected protected value
                            if impute_protected == True:
                                impute_value = impute_protected_choice.value
                                text = "convert missing values for "+ protected + " to " + str(impute_value)
                                df[protected].fillna(impute_value, inplace = True)
                            #impute all other missing values based on tab contents. 
                            for val in impute_dd_dict:
                                for col in impute_dd_dict[val]:
                                    impute_value = impute_dd_dict[val][col].value
                                    text = "convert missing values for "+ protected +":" + str(val) + " within col: " + str(col) + " to " + str(impute_value)
                                    self.helper_methods.display_html (text, self.text_color, "p")
                                    m1 = (df[protected] == val) 
                                    df.loc[m1,col] = df.loc[m1,col].fillna(impute_value)
                                    
                      
                        #Refresh the 3 seperate DataFrames, should rewrite code base to only use one!
                        self.y_label_df = df[self.selectYFeature.value]
                        non_prot_list = set(self.selectXFeatures.value).symmetric_difference(set(self.selectProtectedAttributes.value))
                        self.non_protected_feature_set_df = df[list(non_prot_list)]
                        self.protected_feature_set_df = df[list(self.selectProtectedAttributes.value)]
                        #Recursively refresh to see the new situation after the impute!
                        self.on_analyze_missing_data_button_clicked(self.analyze_missing_data_button)
                                    
                    impute_button.on_click(on_apply_imputation_button_clicked)
                    display (impute_button)
                    text = "Note: This will apply changes to " + str(unique_vals)
                    self.helper_methods.display_html (text, self.text_color, "p")
                    

                interact(view_missing_per_protected, selected_protected = selectProtectedDropDown)

            display(missing_data_tab)

        else:#If there is no missing data in the datafile
            num_rows = df.shape[0] 
            text = "Total Number of Rows: "+ str(num_rows)
            self.helper_methods.display_html (text, self.text_color, "p")

            num_cols = df.shape[1] 
            text = "Total Number of Columns: "+ str(num_cols)
            self.helper_methods.display_html (text, self.text_color, "p")
            text = "No missing data has been detected!"
            self.helper_methods.display_html (text, self.text_color, "p")
            with self.missingDataProcessedOutput:
                clear_output (wait = True)

      
    #################################################################################################
    #  
    # 
    #################################################################################################        
    def on_save_description_button_clicked(self, b):
        with self.saveDescriptionOut:
            clear_output(wait=True)
            if self.theSelectedCategoricalFeaturesDropDown.value not in self.group_descriptions_dict:
                    self.group_descriptions_dict[self.theSelectedCategoricalFeaturesDropDown.value] = {}
            for value in self.choosenFeatureValues.value:
                text = "Saving description of: " + str(value) + " as "+ str(self.descriptionText.value) 
                self.helper_methods.display_html (text, self.text_color, "p")
                self.group_descriptions_dict[self.theSelectedCategoricalFeaturesDropDown.value][value] = self.descriptionText.value
                self.set_selected_categorical_values(self.theSelectedCategoricalFeaturesDropDown.value)
            with self.selectReferenceGroupsOutput:
                clear_output(wait=True)
                self.selectReferenceGroupsFunction(self.selectProtectedAttributes.value)
        self.descriptionText.value = ""
        
     
    #################################################################################################
    #  
    # 
    #################################################################################################          
    def selectReferenceGroupsFunction (self, selectProtectedAttributes_values):
        feat_widg_arr = {}
        if self.protected_feature_set_df.empty:
            self.helper_methods.display_html ("No protected features selected", self.text_color, "p")
        def selected_group(val, feat):
            self.reference_groups_dict[feat] = val #sets the value not the description.
            chk_arr = [''] * len(feat_widg_arr[feat].options)
            pos = list(feat_widg_arr[feat].options.values()).index(val)
            chk_arr[pos] = "check"
            feat_widg_arr[feat].icons=chk_arr         
        if not self.protected_feature_set_df.empty:
            self.helper_methods.display_html ("Select privileged group for:", "black", "h4")
            for feature in selectProtectedAttributes_values:
                #adding this incase we accidentally select an incorrect protected feature such as
                #a continuous feature with multiple values.
                if len(self.protected_feature_set_df[feature].dropna().unique()) <= 20:
                    feat_widg_arr[feature] = widgets.ToggleButtons(
                                                options = self.helper_methods.get_feature_info(feature, 
                                                                                            self.protected_feature_set_df[feature].dropna().unique(),
                                                                                            self.group_descriptions_dict, 
                                                                                            self.label_encoding_dict,
                                                                                            self.oh_encoding_dict, 
                                                                                            self.merged_dict)[0],
                                                description=  feature + ":",
                                                button_style = "info",
                                                #layout = self.layout,
                                                style= {'button_width':'200px','description_width':'70px'},
                                                disabled=False)
                    if feature in self.reference_groups_dict:
                        feat_widg_arr[feature].value = self.reference_groups_dict[feature]  
                    interact(selected_group, 
                             val = feat_widg_arr[feature], 
                             feat = widgets.Text(
                                    value=feature,
                                    disabled=True,
                                    layout =  {'visibility':'hidden'})
                            )
      
    
    #################################################################################################
    # View the representation of the protected groups in the data, 
    # 
    #################################################################################################
    def on_view_representation_button_clicked(self, button):
            data_frame = self.get_dataframe(True, True)[0]
            for feat in list(self.selectProtectedAttributes.value):
                mapping = self.helper_methods.get_feature_info(feat, 
                                                data_frame[feat].dropna().unique(), 
                                                self.group_descriptions_dict,
                                                self.label_encoding_dict,
                                                self.oh_encoding_dict, 
                                                self.merged_dict)[0]
                keys = list( mapping.keys())
                values = list (mapping.values())
                reverse_mapping = dict(zip(values, keys))
                data_frame[feat] = data_frame[feat].map(reverse_mapping)                                   
            self.helper_methods.display_group_representation(data_frame, 
                                                             list(self.selectProtectedAttributes.value), 
                                                             self.viewRepresentationOut)
            
  


    ################################################################################################
    #  View the representation of the protected groups in the data,
    # 
    #################################################################################################
    def viewGroupRepresentationFunction (self, selectProtectedAttributes_values): 
        if self.protected_feature_set_df.empty:
            self.helper_methods.display_html ("No protected features selected", self.text_color, "p")
        if not self.protected_feature_set_df.empty:
            with self.auditRepresentationOut:
                clear_output(wait=True)
                
                #Add the samples and "watch out for here."
                ex1_html = widgets.HTML("""
                <font style="font-family:sans-serif; font-size:15px;color:grey;">
                <b>Example 1: </b>If a company historically hired significantly more men than women, and 
                therefor women are not represented in the training data set, the resulting trained model
                may learn to associate "success" with factors found in male applicants — or to reject applications 
                that have factors associated with female applicants. This is what happened in the
                famous Amazon recruiting tool case. The gender feature(or proxy for it) had too much
                weight on the outcome due to a lack of Female representation in the data used to 
                train the model.
                <br> See:  add link
                """)
            
                ex2_html = widgets.HTML("""
                <font style="font-family:sans-serif; font-size:15px;color:grey;">
                <b>Example 2: </b>If a crime prediction model were to be trained with historical crime data
                there may be an imbalanced representation between race and historic criminality. 
                Criminological research has shown that police databases relating to people, neighbourhoods
                and police contact are not a “complete census of all criminal offenses, nor do they 
                constitute a representative sample". In the US Black and Hispanic people are more likely
                to have contact with the police which can be directly correlate with racist police practices
                as opposed to any higher propensity for criminality.
                <br> See: "CHALLENGING RACIST PREDICTIVE POLICING ALGORITHMS UNDER THE EQUAL PROTECTION CLAUSE- 
                RENATA M. O’DONNELL"
                """)

      
                ex3_html = widgets.HTML("""
                <font style="font-family:sans-serif; font-size:15px;color:grey;">
                <b>Example 3: </b>Harassment, bigotry, casual racism and sexism have historically permeated 
                environments where underrepresentation is rampant. The result is the possible exclusion,
                marginalisation, and undermining of the potential of anyone who isn't a wealthy, male, 
                white, straight, able-bodied individual. This may account for an imbalanced representation of 
                groups within the domain and therefor within the protected feature as certain groups may 
                avoid careers in certain sectors due to lack of mentorship, the existence of 
                (or the perception of the existence of) an exclusionary workplace culture 
                <br>See: "Did this really happen" https://didthisreallyhappen.net/category/strips/
                """)
                #layout = widgets.Layout(flex='1 1 0%', width='auto') 
                layout = widgets.Layout() 
                ex1 = widgets.Button(description='Example 1',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', 
                                icon='fa-eye',
                                layout = layout
                                )
            
                ex2 = widgets.Button(description='Example 2',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', 
                                icon='fa-eye',
                                layout = layout
                                )
                
                ex3 = widgets.Button(description='Example 3',
                                disabled=False,
                                tooltip = "Show",
                                button_style='warning', 
                                icon='fa-eye',
                                layout = layout
                                )

                out = widgets.Output()
                
                def view_hide_example (b):  
                    with out:
                        clear_output(wait = False)
                        if b.description== 'Example 1':
                            if b.tooltip == 'Show':
                                display(ex1_html)
                                ex1.tooltip = 'Hide'
                                ex2.tooltip = 'Show'
                                ex3.tooltip = 'Show'
                            else:
                                ex1.tooltip = 'Show'
                        
                        elif b.description== 'Example 2':
                            if b.tooltip == 'Show':
                                display(ex2_html)
                                ex2.tooltip = 'Hide'
                                ex1.tooltip = 'Show'
                                ex3.tooltip = 'Show'
                            else:
                                ex2.tooltip = 'Show'
                            
                            
                        elif b.description== 'Example 3':
                            if b.tooltip == 'Show':
                                display(ex3_html)
                                ex3.tooltip = 'Hide'
                                ex2.tooltip = 'Show'
                                ex1.tooltip = 'Show'
                            else:
                                ex3.tooltip = 'Show'
            
                
                ex1.on_click(view_hide_example)
                ex2.on_click(view_hide_example)
                ex3.on_click(view_hide_example)
                
                box_layout = Layout(display='flex',
                    flex_flow='row',
                    align_items='stretch',
                    align_content='stretch',
                    width='100%')
                display (widgets.HBox ([ex1, ex2, ex3],layout = box_layout))
                display (out)

                
                text = """Reflections related to group representation:"""
                self.helper_methods.display_html (text, "black", "h3") 
                
              
                
                def audit_features(l1, q1, space1, 
                                   l2, q2, space2, 
                                   wvl, wvq, space3, 
                                   okl, okq, 
                                   feature, 
                                   free_text_label, free_text):
                    if q1 == 1:
                        self.group_under_represented_pop_dict[feature] = """An imbalance of group representation within the sample <b>has</b> been observed 
                                                                            compared to that within the general population. """
                    elif q1 == 0:
                        self.group_under_represented_pop_dict[feature] = """An imbalance of group representation within the sample <b>has not</b> been observed 
                                                                            compared to that within the general population. """
                    if q2 == 1:
                        self.group_under_represented_domain_dict[feature] = """An imbalance of group representation within the sample <b>has</b> been observed 
                                                                            compared to that within the population the model will be used in. """
                    elif q2 == 0:
                        self.group_under_represented_domain_dict[feature] = """An imbalance of group representation within the sample <b>has not</b> been observed 
                                                                            compared to that within the population the model will be used on. """
                    elif q2 == 2:
                        self.group_under_represented_domain_dict[feature] = """An imbalance of group representation within the sample 
                                                                            compared to that within the population the model will be used on has
                                                                            been observed as <b>not applicable</b>."""
                   
                    if wvq == 1:
                        self.group_under_represented_world_view_dict[feature]   =  1 
                    elif wvq == 0:
                        self.group_under_represented_world_view_dict[feature]   =  0
                    
                    if  okq == 1:
                        self.group_under_represented_data_ok_dict[feature]    = """The belief is that using this data will result in a fair model
                                                                                    that <b>does</b> reflect the selected worldview.""" 
                    elif  okq == 0:
                        self.group_under_represented_data_ok_dict[feature]    =  """The belief is that using this data will result in a 
                                                                                    model that <b>does not</b> reflect the selected worldview."""
                    
                    elif  okq == 2:
                        self.group_under_represented_data_ok_dict[feature]    =  """The belief is that <b>further discussion is required</b>
                                                                                    to decide if using this data will result in a fair model that 
                                                                                    reflect the selected worldview."""
                   
                    self.group_represented_free_text[feature] = free_text

                    chk_arr1 = [''] * len(q1_dict[feature].options)
                    pos = list(q1_dict[feature].options.values()).index(q1)
                    chk_arr1[pos] = "check"
                    q1_dict[feature].icons=chk_arr1  
                    
                    chk_arr2 = [''] * len(q2_dict[feature].options)
                    pos = list(q2_dict[feature].options.values()).index(q2)
                    chk_arr2[pos] = "check"
                    q2_dict[feature].icons=chk_arr2 
                    
                    chk_arr3 = [''] * len(wvq_dict[feature].options)
                    pos = list(wvq_dict[feature].options.values()).index(wvq)
                    chk_arr3[pos] = "check"
                    wvq_dict[feature].icons=chk_arr3 
                    
                    chk_arr4 = [''] * len(data_ok_dict[feature].options)
                    pos = list(data_ok_dict[feature].options.values()).index(okq)
                    chk_arr4[pos] = "check"
                    data_ok_dict[feature].icons=chk_arr4 
                        
                l1_dict = {}
                q1_dict = {}
                l2_dict = {}
                q2_dict = {}
                wvl_dict = {}
                wvq_dict = {}
                data_ok_label_dict = {}
                data_ok_dict = {}
                free_text_dict = {}
                free_text_label_dict  = {}
               
                
                for feat in list(self.selectProtectedAttributes.value):
                    text =  feat
                    self.helper_methods.display_html (text.capitalize(), "black", "h5") 
                    text = "Do you observe any significant disparity in '<b>" + feat + "</b>' group representation between the sample population and the general population in the geographical region of use?"
                    #self.helper_methods.display_html (text, "grey", "p") 
                    l1_dict[feat] = widgets.HTML(value = text,
                                                description= "Q: ",
                                                layout=Layout(width='95%'),# height='70px'
                                                style = {'description_width': 'initial'})

                    
                    q1_dict[feat]  = widgets.ToggleButtons(
                                                options={'Yes, significant':1,
                                                         'No, not significant':0
                                                         },
                                                tooltip = feat,
                                                button_style = "info",
                                                layout = {'padding':'4px'},
                                                style= {'button_width':'415px','description_width':'0px'},
                                                disabled=False)
                    
                   
  
                    text = "Do you observe any significant disparity in  '<b>" + feat + "</b>' group representation between the sample population and the population that the machine learning model will make predictions about after deployment?"
                    #self.helper_methods.display_html (text, "grey", "p")             
                    l2_dict[feat] = widgets.HTML(value = text,
                                                description= "Q: ",
                                                layout=Layout(width='95%'),# height='70px'
                                                style = {'description_width': 'initial'})
 
                    
                    q2_dict[feat] = widgets.ToggleButtons(
                                                options={'Yes, significant':1,
                                                         'No, not significant':0,
                                                         'Not Applicable':2
                                                        },
                                                button_style = "info",
                                                layout = {'padding':'4px'},
                                                style= {'button_width':'272px','description_width':'0px'},
                                                disabled=False)
                    
                    text = """What worldview do you believe should be applied to any significant disparity in  '<b>""" + feat + """</b>' group representation?.
                        Any disparity in representation is likely caused by:"""
                    
                    wvl_dict[feat] = widgets.HTML(value = text,
                                                description= "Q: ",
                                                layout=Layout(width='95%'),# height='70px'
                                                style = {'description_width': 'initial'})
                    
                    wvq_dict[feat] =  widgets.ToggleButtons(options={
                                                            'An inherent characteristic of the protected group':0, 
                                                            'An external, unobserved causal influence':1
                                                            },
                                                        button_style = "info",
                                                        layout = {'padding':'4px'},
                                                        style= {'button_width':'415px','description_width':'0px'},
                                                        disabled=False)
                    
                    
                    text = """In your opinion should this data be used if the objective is to train a fair ML
                    model which will reflect the worldview selected for disparities in <b>"""  + feat + """?</b>"""
                    
                    data_ok_label_dict[feat] = widgets.HTML(value = text,
                                                            description= "Q: ",
                                                            layout=Layout(width='95%'),# height='70px'
                                                            style = {'description_width': 'initial'})
                    
                    data_ok_dict[feat] =  widgets.ToggleButtons(options={
                                                                        'Yes':1, 
                                                                        'No':0,
                                                                        'Discussion required':2
                                                                        },
                                                                button_style = "info",
                                                                layout = {'padding':'4px'},
                                                                style= {'button_width':'272px','description_width':'0px'},
                                                                disabled=False)
                    
                    space1 =  widgets.Text(value="empty",
                                            disabled=True,
                                            layout =  {'visibility':'hidden', 
                                                        'height':'14px', 
                                                        'overflow':'scroll hidden'},
                                            )
                    space2 =  widgets.Text(value="empty",
                                            disabled=True,
                                            layout =  {'visibility':'hidden', 
                                                        'height':'14px', 
                                                        'overflow':'scroll hidden'},
                                            )
                    space3 =  widgets.Text(value="empty",
                                            disabled=True,
                                            layout =  {'visibility':'hidden', 
                                                        'height':'14px', 
                                                        'overflow':'scroll hidden'},
                                            )
                    text = """Enter any notes related to your observations on the representation of protected groups in protected feature '<b>""" + feat + "</b>'?"
                    
                    free_text_label_dict[feat] = widgets.HTML(value = text,
                                                            description= "Q: ",
                                                            layout=Layout(width='95%'),# height='70px'
                                                            style = {'description_width': 'initial'})
                    
                    
                    free_text_dict[feat] = widgets.Textarea(description='',
                                                            disabled=False,
                                                            layout=Layout(width='95%'),
                                                            style= {'description_width':'0px'},
                                                        
                                                            )
                    interact(audit_features, 
                             l1= l1_dict[feat], 
                             q1 = q1_dict[feat],
                             space1 = space1,
                             l2= l2_dict[feat], 
                             q2 = q2_dict[feat],
                             space2 = space2,
                             wvl= wvl_dict[feat], 
                             wvq = wvq_dict[feat],
                             space3 = space3,
                             okl = data_ok_label_dict[feat],
                             okq = data_ok_dict[feat],
                             feature = widgets.Text(feat, layout ={'visibility':'hidden'}),
                             free_text_label = free_text_label_dict[feat],
                             free_text = free_text_dict[feat]
                             )
              
               
                
                       
                   
    #################################################################################################
    #  view the controls to see information about the output/label/y
    # 
    #################################################################################################
    def viewOutputDistributionFunction(self, selectProtectedAttributes_values, selectYFeature_values):
    
        if not list(selectProtectedAttributes_values) == [] and not selectYFeature_values == None:
        
            data_frame = self.get_dataframe(True, True)[0] 
            with self.viewOutputDistributionOut:
                clear_output(wait=True)
                if self.Y_BINARY == True:
                    self.helper_methods.categoric_feature_analysis_across_groups(data_frame,
                                                               self.selectYFeature.value,
                                                               list(self.selectProtectedAttributes.value),
                                                               self.selectYFeature.value,
                                                               self.group_descriptions_dict,
                                                               self.label_encoding_dict,
                                                               self.reference_groups_dict,
                                                               _w=600, _h=600,
                                                               high_range_pos = self.HIGH_RANGE_POSITIVE)
                elif self.Y_BINARY == False:
                    self.helper_methods.numeric_feature_analysis_across_groups(data_frame,
                                                               self.selectYFeature.value,
                                                               list(self.selectProtectedAttributes.value),
                                                               self.selectYFeature.value,
                                                               self.group_descriptions_dict,
                                                               self.label_encoding_dict,
                                                               self.reference_groups_dict,
                                                               _w=600, _h=600,
                                                               high_range_pos = self.HIGH_RANGE_POSITIVE)
            
            with self.auditOutputDistributionOut:
                clear_output(wait=True)
                text = """Reflections related to the distribution of the target ( """ + str(self.selectYFeature.value) + """) across groups:"""
                self.helper_methods.display_html (text, "black", "h3") 
                
                
            
            
            
                
                def audit_features(l1, q1, space1, 
                                   wvl, wvq, space2, 
                                   okl, okq, feature,
                                  free_text_label, free_text):
                    if q1 == 1:
                        self.group_output_distribution_dict[feature] = """A significant difference in distribution of the target(y) across groups <b>has</b> been observed. 
                                                                         """
                    elif q1 == 0:
                        self.group_output_distribution_dict[feature] = """A significant difference in distribution of the target(y) across groups <b>has not</b> been observed.
                                                                         """
            
            
                    if wvq == 1:
                        self.group_output_distribution_world_view_dict[feature]   = 1
                    elif wvq == 0:
                        self.group_output_distribution_world_view_dict[feature]   = 0
                    
                    if  okq == 1:
                        self.group_output_distribution_data_ok_dict[feature]    = """The belief is that using this data will 
                                                                                    result in a fair model that <b>does fairly</b> 
                                                                                    reflect the selected worldview.""" 
                    elif  okq == 0:
                        self.group_output_distribution_data_ok_dict[feature]    =  """The belief is that using this data will
                                                                                      result in a model that <b>does not fairly</b>
                                                                                      reflect the selected worldview."""
                    elif  okq == 2:
                        self.group_output_distribution_data_ok_dict[feature]    =  """The belief is that <b>further discussion is required</b>
                                                                                      to determine if using this data will
                                                                                      result in a model that 
                                                                                      reflect the selected worldview."""
                    
                    self.group_output_distribution_free_text[feature] = free_text
                    
                    chk_arr1 = [''] * len(q1_dict[feature].options)
                    pos = list(q1_dict[feature].options.values()).index(q1)
                    chk_arr1[pos] = "check"
                    q1_dict[feature].icons=chk_arr1  
                    
                    chk_arr3 = [''] * len(wvq_dict[feature].options)
                    pos = list(wvq_dict[feature].options.values()).index(wvq)
                    chk_arr3[pos] = "check"
                    wvq_dict[feature].icons=chk_arr3 
                    
                    chk_arr4 = [''] * len(data_ok_dict[feature].options)
                    pos = list(data_ok_dict[feature].options.values()).index(okq)
                    chk_arr4[pos] = "check"
                    data_ok_dict[feature].icons=chk_arr4 
                        
                l1_dict = {}
                q1_dict = {}
                wvl_dict = {}
                wvq_dict = {}
                data_ok_label_dict = {}
                data_ok_dict = {}
                free_text_label_dict = {}
                free_text_dict = {}
               
                
                for feat in list(self.selectProtectedAttributes.value):
                    text =  feat
                    self.helper_methods.display_html (text.capitalize(), "black", "h5") 
                    text = "Using the tools provided do you observe a significant difference in the distribution of the <b>target(y)</b> across groups within the '<b>" + feat.capitalize() + "</b>' protected feature"
                    l1_dict[feat] = widgets.HTML(value = text,
                                                description= "Q: ",
                                                layout=Layout(width='95%'),# height='70px'
                                                style = {'description_width': 'initial'})

                    
                    q1_dict[feat]  = widgets.ToggleButtons(
                                                options={'Yes, significant differences':1,
                                                         'No, not significant':0
                                                         },
                                                tooltip = feat,
                                                button_style = "info",
                                                layout = {'padding':'4px'},
                                                style= {'button_width':'415px','description_width':'0px'},
                                                disabled=False)
                    
                   
  
                    
                    text = """What worldview do you believe should be applied to any significant differences in the distribution of the <b>target(y)</b> across groups for the protected feature  '<b>""" + feat + """'</b>? 
                        Any significant difference in distribution is likely caused by:"""
                    
                    wvl_dict[feat] = widgets.HTML(value = text,
                                                description= "Q: ",
                                                layout=Layout(width='95%'),# height='70px'
                                                style = {'description_width': 'initial'})
                    
                    wvq_dict[feat] =  widgets.ToggleButtons(options={
                                                            'An inherent characteristic of the protected group':0, 
                                                            'An external, unobserved causal influence':1
                                                            },
                                                        button_style = "info",
                                                        layout = {'padding':'4px'},
                                                        style= {'button_width':'415px','description_width':'0px'},
                                                        disabled=False)
                    
                    
                    text = """In your opinion should this data be used if the objective is to train a fair ML
                    model which will reflect the selected worldview for <b>'""" + feat + "</b>'?"
                    
                    data_ok_label_dict[feat] = widgets.HTML(value = text,
                                                            description= "Q: ",
                                                            layout=Layout(width='95%'),# height='70px'
                                                            style = {'description_width': 'initial'})
                    
                    data_ok_dict[feat] =  widgets.ToggleButtons(options={
                                                                        'Yes':1, 
                                                                        'No':0,
                                                                        'Discussion required':2
                                                                        },
                                                                button_style = "info",
                                                                layout = {'padding':'4px'},
                                                                style= {'button_width':'272px','description_width':'0px'},
                                                                disabled=False)
                    
                    space1 =  widgets.Text(value="empty",
                                            disabled=True,
                                            layout =  {'visibility':'hidden', 
                                                        'height':'14px', 
                                                        'overflow':'scroll hidden'},
                                            )
                    space2 =  widgets.Text(value="empty",
                                            disabled=True,
                                            layout =  {'visibility':'hidden', 
                                                        'height':'14px', 
                                                        'overflow':'scroll hidden'},
                                            )
                   
                    text = """Enter any notes related to your observations on the distribution of output across groups in protected feature <b>'""" + feat + "</b>'?"
                    
                    free_text_label_dict[feat] = widgets.HTML(value = text,
                                                            description= "Q: ",
                                                            layout=Layout(width='95%'),# height='70px'
                                                            style = {'description_width': 'initial'})
                    
                    
                    free_text_dict[feat] = widgets.Textarea(description='',
                                                            disabled=False,
                                                            layout=Layout(width='95%'),
                                                            style= {'description_width':'0px'},
                                                        
                                                            )

                    interact(audit_features, 
                             l1= l1_dict[feat], 
                             q1 = q1_dict[feat],
                             space1 = space1,
                             wvl= wvl_dict[feat], 
                             wvq = wvq_dict[feat],
                             space2 = space2,
                             okl = data_ok_label_dict[feat],
                             okq = data_ok_dict[feat],
                             feature = widgets.Text(feat, layout ={'visibility':'hidden'}),
                             free_text_label = free_text_label_dict[feat],
                             free_text = free_text_dict[feat],
                            )
              
              
               
               
          
    #################################################################################################
    # profile the data: visualize the relationship between the features.
    # we need to choose variables that we think will be good predictors — this can 
    # be achieved by checking the correlation(s) between variables, by plotting the data and searching visually
    # for relationship, by conducting preliminary research on what variables are good predictors of y
    #################################################################################################
    def on_profile_data_button_clicked(self, b):
        if not self.df.empty:
            try:
                pandasOut = widgets.Output(layout={})
                bespokeOut = widgets.Output(layout={})
                tab = widgets.Tab()
                tab.children = [pandasOut, bespokeOut] 
                tab.set_title(0, "General analysis of data")
                tab.set_title(1, "Specific analysis per protected Feature")
                feature_set_with_y, df_cols = self.get_dataframe(include_label_y = True, include_protected = True)

                #Check to see if any features are explicitly selected, if not..use all   
                if len(list(self.theSelectedInputFeaturesChoice.value)) > 0: #Default to show all but only show selected if selection exists
                    #to make sure the protected values are included...
                    df_cols = column_list + [self.selectProtectedAttributes.value]
                    #remove dupes if protected was already selected (although better not to even show in dropdown.)
                    df_cols = list(dict.fromkeys(df_cols))

                to_use = []
                values_before_merge = []
                values_before_encoding = []
                for feature in df_cols:
                    #filter out the columns which contain column values before merge or before encoding
                    #later we can review this and give option to analyze original values/original encoding.
                    if not feature.endswith("_bm") and not feature.endswith("_benc"): #_bm, _oh_benc or _benc
                        to_use.append(feature)
                    if feature.endswith("_bm"):
                        values_before_merge.append(feature)
                    if feature.endswith("_benc"):
                        values_before_encoding.append(feature)
                input_feat = widgets.Dropdown(options=to_use,
                                              description='Input Feature:',
                                              disabled=False,
                                              style = {'description_width': 'initial'}) 
                
                        
                categorical_features, numeric_features = self.helper_methods.get_features_type(feature_set_with_y[to_use], 20)
                        

                def describe_features(input_feat):                     
                    if input_feat in categorical_features:
                        self.helper_methods.categoric_feature_analysis_across_groups(feature_set_with_y[to_use],
                                                                            input_feat,
                                                                            list(self.selectProtectedAttributes.value),
                                                                            self.selectYFeature.value,
                                                                            self.group_descriptions_dict,
                                                                            self.label_encoding_dict,
                                                                            self.reference_groups_dict,
                                                                            _w=600, _h=600,
                                                                            high_range_pos = True)
        
                    elif input_feat in numeric_features:
                        self.helper_methods.numeric_feature_analysis_across_groups(feature_set_with_y[to_use],
                                                                            input_feat,
                                                                            list(self.selectProtectedAttributes.value),
                                                                            self.selectYFeature.value,
                                                                            self.group_descriptions_dict,
                                                                            self.label_encoding_dict,
                                                                            self.reference_groups_dict,
                                                                            _w=600, _h=600,
                                                                            high_range_pos = True)
                with self.profileDataOut :
                    clear_output(wait=True)
                    display (tab)    
                with pandasOut:
                    clear_output(wait=True)
                    display(HTML('''<h3>General analysis of data</h3>Generated by pandas profiler'''))
                    profile = pandas_profiling.ProfileReport(feature_set_with_y[to_use])
                    profile.to_widgets()
                        
                        
                with bespokeOut:
                    clear_output(wait=True)
                    display(HTML('''<h3>Analysis of input feature with respect to a protected feature:</h3>'''))
                    display(HTML('''<h4>Select the input feature to analyse:</h4>'''))
                    interact(describe_features, input_feat = input_feat)
            
            except:
                print("No values selected yet")
                
     

    #################################################################################################
    # Drop any columns that will not be used as input feature 
    # 
    #################################################################################################          
    def on_drop_features_button_clicked(self, b):
        if not self.df.empty:
            columns_to_drop = self.theSelectedInputFeaturesChoice.value 
            protected, non_protected, all_features = self.get_all_engineered_features()
            p = set(protected)# for fast reference operation
            with self.dropColOut:
                clear_output(wait=True)
                for selected in columns_to_drop:
                    if selected in p:# if protected
                        #self.protected_feature_set_df.drop(selected, axis=1, inplace=True) 
                        self.helper_methods.display_html ("Protected Feature "+ str (selected)+" not dropped.",self.text_color, "h5")
                    else: 
                        self.non_protected_feature_set_df.drop(selected, axis=1, inplace=True)
                        self.helper_methods.display_html ("Dropped "+ str (selected),self.text_color, "h5")
                
    
        
        
    #################################################################################################
    #  
    # 
    #################################################################################################          
    def selectFeatureAuditFunction (self, selectXFeatures_values, selectProtectedAttributes_values):
        dependantsHTML = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            <b>Dependant on protected group: </b> An input feature may have a statistical association
            with membership of a protected group. For example historic bias may lead to a disparity in 
            generational wealth between groups, which may in turn impact choice of neighbourhood, which
            may impact quality of schooling, living conditions, nutrition, access to resources, 
            availabel support structures, medical care etc. All of these factors, which are outside
            of an individuals control, may have a causal effect upon a test score, such that the test 
            score has a dependancy upon a protected feature. It is important to note that this statistical
            association between group membership and an input feature does not imply a causal relationship
            between group membership and the input feature in question. Depending on your worldview
            you may determine that some non-observed variable might be responsible. 
            When ranking humans it may be wise to consider how for example an individual would have scored
            had the unobserved influence been consistent across all groups, or the advantages some groups
            have had over others. <br>
             """)
        
        
        proxiesHTML = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            
            <b>Proxy for protected group: </b> A proxy is a very strong dependency, such that
            the proxy may be used to infer membership to a protected group.
            Bias often appears through seemingly innocuous features 
            which are strongly correlated to protected features. For example, in some countries, zip or 
            postcodes may be strongly correlated with race or even age. Names may be strongly correlated
            with gender, race, or religion. Height or the reference to an all-girls school on a cv 
            may correlat with gender. Linguistic characteristic or last name may correlate with race.
            In this case removing the protected feature from training
            by applying a "color blind" or "gender blind" approach may not actually remove a 
            correlation between a protected group and any historic prejudices encoded in the outcome. 
            
            
            <font style="font-family:sans-serif; font-size:15px;color:#34baeb;">
            <br><b>Note: </b> Not all proxy are negative, for example, debt-to-income ratio could in 
            certain countries be strongly correlated with race but if debt-to-income ratio can be 
            separately justified as a strong predictor of the ability to repay a loan, then it may 
            be legitimate to use it. At a minimum it is important to be aware of the possibility for
            proxies to  and in case of douby engage a human domain expert to make decisions related 
            to accuracy vs fairness. """)
        feat_widg_arr_dependent = {}
        feat_widg_arr_proxy = {}
        
        if self.protected_feature_set_df.empty:
            self.helper_methods.display_html ("No protected features selected", self.text_color, "p")
        

            
     
        if not self.protected_feature_set_df.empty:
            wf = widgets.Button(description='Watch out for',
                        disabled=False,
                        tooltip = "Show",
                        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
                        icon='fa-eye' # (FontAwesome names without the `fa-` prefix)
                        )

            disparateImpactHTML = widgets.HTML("""
                <font style="font-family:sans-serif; font-size:15px;color:grey;">
                <b>Fairness and Disparate Impact (Indirect bias)</b> — A decision making process suffers from disparate impact if 
                the outcome of a decision disproportionately hurts (or benefits) those within a group. No intent 
                is required. This type of relative discrimination can be detected if there is a difference in the
                fraction of positive (negative) outcomes for the different protected groups.
                <br><b>Note:</b> Disparate impact is often referred to as unintentional discrimination, and is often the
                result of the existance of proxy features, whereas disparate treatment is intentional. 
                """)
        
            out = widgets.Output()
            def watch_out_for (_button):    
                if wf.tooltip == "Show":
                    with out:
                        clear_output(wait = False)
                        display(disparateImpactHTML)
                    wf.tooltip = "Hide"
                elif wf.tooltip == "Hide":
                    with out:
                        clear_output(wait = False)
                        wf.tooltip = "Show"


            wf.on_click(watch_out_for)
        
            
            
            def audit_features_dependent(q, val, feat, protected):
                self.dependant_features_audit_dict[protected][feat] = val 
                chk_arr = [''] * ( len(feat_widg_arr_dependent[protected][feat].options) )
                pos = feat_widg_arr_dependent[protected][feat].options.index(val)
                chk_arr[pos] = "check"
                feat_widg_arr_dependent[protected][feat].icons=chk_arr 

            
            dependency_out = widgets.Output(layout={})
            proxy_out = widgets.Output(layout={})
            tab_contents = [dependency_out, proxy_out]
            tab_audit = widgets.Tab()
            tab_audit.children = tab_contents
            tab_audit.set_title(0, "Dependencies")
            tab_audit.set_title(1, "Proxies")
            
            with proxy_out:
                display (proxiesHTML)
                display (wf)
                display (out)
            with dependency_out:
                display (dependantsHTML)
                display (wf)
                display (out)
            display (tab_audit)
            
            non_protected_features = [x for x in selectXFeatures_values if x not in selectProtectedAttributes_values]
            
            for protected in selectProtectedAttributes_values:
                feat_widg_arr_dependent[protected] = {} #Nested dict
                
                self.dependant_features_audit_dict[protected] = {} #Nested dict
                
            for feature in non_protected_features:
                for protected in selectProtectedAttributes_values:
                    text = "In your opinion select the dependency level between '<b>" + feature  + "</b>' and '<b>" + protected + "</b>':"
                    q1 = widgets.HTML(value = text,
                                      description= "Q: ",
                                      layout=Layout(width='95%'),# height='70px'
                                      style = {'description_width': 'initial'})
                    
                    feat_widg_arr_dependent[protected][feature] = widgets.ToggleButtons(
                                                options=['Not Dependant', 'Somewhat Dependant', 'Dependant', 'A Likely proxy'],
                                                description= "",
                                                tooltip = feature,
                                                layout = self.layout,
                                                button_style = "info",
                                                style= {'button_width':'180px','description_width':'0px'},
                                                disabled=False)
                
        
                    
                    interact(audit_features_dependent, 
                             q = q1,
                             val = feat_widg_arr_dependent[protected][feature], 
                             feat = widgets.Text(value=feature,
                                                disabled=True,
                                                layout =  {'visibility':'hidden', 'height':'7px', 'overflow':'scroll hidden'},
                                                ),
                             protected = widgets.Text(value=protected,
                                                      disabled=True,
                                                      layout =  {'visibility':'hidden', 'height':'7px', 'overflow':'scroll hidden'},
                                                      style= {'width':'10px'}
                                                    ),
                        )

                    
            text = """<b>Keep in mind:</b> Input features that are themselves generated by an ML model may 
            also act as a proxy for protected group. """
            self.helper_methods.display_html (text, "orange", "p") 
    
    
    
    
    
    #################################################################################################
    #  get_dataframe()[0] to only return df
    # get_dataframe()[1] to only return column values
    ################################################################################################# 
    def get_dataframe(self, include_label_y, include_protected):
        df =  self.non_protected_feature_set_df
        if include_protected == True:
            df = pd.concat([df, self.protected_feature_set_df], axis=1)   
        if include_label_y == True:
            df = pd.concat([df, self.y_label_df], axis=1)
        return df, df.columns.values
     
    #################################################################################################
    #  
    # 
    #################################################################################################        
    def work_in_progress(self, progress):
        total = 100
        for i in range(total):
            time.sleep(0.2)
            progress.value = float(i+1)/total
            
            
    #################################################################################################
    #  
    # 
    #################################################################################################
    def get_colums_for_protected (self, all_cols, protected):
        protected_features = []
        for feature in  protected:
            # If any are encoded  
                        
            if (feature + "_bm" in all_cols) and  (self.pre_merge_box.value == True):
                protected_features.append(feature + "_bm")
                            
            elif feature + "_benc" in all_cols and self.pre_encode_box.value == True:
                 protected_features.append(feature + "_benc")
                            
            elif feature + "_oh_benc" in all_cols and self.pre_encode_box.value == True:
                protected_features.append(feature + "oh_benc")
                            
            else:
                protected_features.append(feature)
        return protected_features
                        
    
        
 
    #################################################################################################
    #  Called each time there is a new choice of protected or non-protected.
    # 
    #################################################################################################
    def get_all_engineered_features(self): 
        protected = []
        non_protected = []
        all_features = []
        without_engineered_original = []
        for feature in self.protected_feature_set_df.columns.values:
            protected.append(feature)
            all_features.append(feature)
            if not feature.endswith("_bm") and not feature.endswith("_benc"):
                without_engineered_original.append(feature)
            
        for feature in self.non_protected_feature_set_df.columns.values:
            non_protected.append(feature)
            all_features.append(feature)
            if not feature.endswith("_bm") and not feature.endswith("_benc"):
                without_engineered_original.append(feature)

        
        self.theSelectedInputFeaturesChoice.options = without_engineered_original
        
        all_categorical = self.helper_methods.get_features_type(self.protected_feature_set_df, 20)[0] + self.helper_methods.get_features_type(self.non_protected_feature_set_df, 20)[0]
        
        all_numeric = self.helper_methods.get_features_type(self.protected_feature_set_df, 20)[1] + self.helper_methods.get_features_type(self.non_protected_feature_set_df, 20)[1]
        
        #remove the engineered originals here too, if something is in all_categorical but not in
        #without_engineered_original, then remove it from all_categorical
        result = [x for x in all_categorical if x in without_engineered_original]
        all_categorical  = result
        
        #remove the engineered originals here too, if something is in all_categorical but not in
        #without_engineered_original, then remove it from all_categorical
        result = [x for x in all_numeric if x in without_engineered_original]
        all_numeric  = result
        
        self.theSelectedCategoricalFeaturesDropDown.options = all_categorical 
        self.theSelectedNumericFeaturesChoice.options = all_numeric 

        return protected, non_protected, all_features
        
    #################################################################################################
    #  
    # 
    #################################################################################################
    def set_selected_categorical_values(self, theSelectedCategoricalFeaturesDropDown_value):
        if not self.non_protected_feature_set_df.empty:

            if not self.y_label_df.empty and not self.non_protected_feature_set_df.empty:
                try:

                    protected, non_protected, all_features = self.get_all_engineered_features()
           
                    p = set(protected)# for fast reference operation
                    
                    
                    if theSelectedCategoricalFeaturesDropDown_value in p:# if protected
                        _options =  self.helper_methods.get_feature_info(theSelectedCategoricalFeaturesDropDown_value,
                                                                      self.protected_feature_set_df[theSelectedCategoricalFeaturesDropDown_value].dropna().unique(),
                                                                      self.group_descriptions_dict,
                                                                      self.label_encoding_dict,
                                                                      self.oh_encoding_dict, 
                                                                      self.merged_dict)[0]

                        self.choosenFeatureValues.options = _options
                        colType = self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dtype
                    else: 
                        _options =  self.helper_methods.get_feature_info(theSelectedCategoricalFeaturesDropDown_value,
                                                                      self.non_protected_feature_set_df[theSelectedCategoricalFeaturesDropDown_value].dropna().unique(),
                                                                      self.group_descriptions_dict,
                                                                      self.label_encoding_dict,
                                                                      self.oh_encoding_dict, 
                                                                      self.merged_dict)[0]

                        self.choosenFeatureValues.options = _options
                        colType = self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dtype
                    
                    
                    if len(self.choosenFeatureValues.value) == 1:
                        self.merge_values_button.description = "Change value"
                    else:
                        self.merge_values_button.description = "Merge values"
                        
                    
                    with self.mergeOut:
                        clear_output(wait=True)
                        
                    with self.LEOut:
                        clear_output(wait=False)
                        if theSelectedCategoricalFeaturesDropDown_value in self.label_encoding_dict:
                            self.helper_methods.display_html ("The feature is label encoded.", "orange", "p")
                        if theSelectedCategoricalFeaturesDropDown_value in self.oh_encoding_dict:
                            self.helper_methods.display_html ("This feature is one-hot encoded.", "orange", "p")
                        
                    with self.HotEncodeOut:
                        clear_output(wait=False)
                        if theSelectedCategoricalFeaturesDropDown_value in self.label_encoding_dict:
                            self.helper_methods.display_html ("The feature is label encoded.", "orange", "p")
                        if theSelectedCategoricalFeaturesDropDown_value in self.oh_encoding_dict:
                            self.helper_methods.display_html ("This feature is one-hot encoded.", "orange", "p")
                                                
                    with self.saveDescriptionOut:
                        clear_output(wait=True)
                
                    with self.descriptionChoiceOut:
                        clear_output(wait=True)
                        if theSelectedCategoricalFeaturesDropDown_value in self.label_encoding_dict:
                            self.helper_methods.display_html ("The feature is label encoded.", "orange", "p")
                        if theSelectedCategoricalFeaturesDropDown_value in self.oh_encoding_dict:
                            self.helper_methods.display_html ("This feature is one-hot encoded.", "orange", "p")
                        if theSelectedCategoricalFeaturesDropDown_value in p:
                            text = "The selected Feature is one of your protected Features."
                            self.helper_methods.display_html (text, self.text_color, "p")
                            
                        self.helper_methods.get_feature_info(theSelectedCategoricalFeaturesDropDown_value, 
                                            list(_options.values()), 
                                            self.group_descriptions_dict,
                                            self.label_encoding_dict, 
                                            self.oh_encoding_dict, 
                                            self.merged_dict,
                                            trace = True)
                        
                    
                                
                except Exception as e:
                    
                    self.helper_methods.display_html ("**Protected attribut merge not yet generated**", self.text_color, "h4")
                    print(e)
                    
                    
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def on_merge_button_clicked(self, b):
        with self.mergeOut:
            clear_output(wait=True)
            protected = []
            for feature in self.protected_feature_set_df.columns.values:
                protected.append(feature)
            p = set(protected)# for fast reference operation, to see if we are renaming a protected Feature.
            
            colTypeCast = type(self.choosenFeatureValues.value[0])
            
            if self.theSelectedCategoricalFeaturesDropDown.value not in self.merged_dict:
                self.merged_dict[self.theSelectedCategoricalFeaturesDropDown.value] = {}
                
            for value in self.choosenFeatureValues.value:
                newValue = colTypeCast(self.newNameForValue.value)
                self.merged_dict[self.theSelectedCategoricalFeaturesDropDown.value][value] = newValue
                newValue = colTypeCast(self.newNameForValue.value)
                
                if self.theSelectedCategoricalFeaturesDropDown.value in p:# if protected
                    if not self.theSelectedCategoricalFeaturesDropDown.value+"_bm" in self.protected_feature_set_df.columns:
                        self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value+"_bm"] = self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value]
                    self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].replace(
                        [value], newValue, inplace=True)
                else:
                    if not self.theSelectedCategoricalFeaturesDropDown.value+"_bm" in self.non_protected_feature_set_df.columns:
                        self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value+"_bm"] = self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value]
                    self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].replace(
                        [value], newValue, inplace=True) #######
     
            ####show stats after rename
            display("Statistics after Merge:")
            if self.theSelectedCategoricalFeaturesDropDown.value in p:# if protected
                display(self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].value_counts())
                colType = self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dtype
                self.choosenFeatureValues.options = self.protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dropna().unique()
                
            else:
                display(self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].value_counts())
                colType = self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dtype
                self.choosenFeatureValues.options = self.non_protected_feature_set_df[self.theSelectedCategoricalFeaturesDropDown.value].dropna().unique()
           
            if colType == str or colType == object :
                colType = str
                self.choosenFeatureValues.value = tuple([colType(newValue)])
                
            if colType == int or colType == float:
                self.choosenFeatureValues.value = tuple([newValue,])
                
            self.newNameForValue.value = "" #Reset the new name text box
            
            #Refresh any of the areas on the GUI affected by the change a merge provides
            with self.selectReferenceGroupsOutput:
                clear_output(wait=True)
                self.selectReferenceGroupsFunction (self.selectProtectedAttributes.value)  
            self.viewOutputDistributionFunction(self.selectProtectedAttributes.value, self.selectYFeature.value)
            self.set_selected_categorical_values(self.theSelectedCategoricalFeaturesDropDown.value)
            ###end refresh areas
        
                              
                        
    #################################################################################################
    # called when the theSelectedInputFeaturesChoice_value changes 
    # 
    #################################################################################################
    def selected_features_choice(self, theSelectedInputFeaturesChoice_value):
        if not self.df.empty:
            with self.theSelectedInputFeaturesChoiceOut:
                clear_output(wait=True)
                protected, non_protected, all_features = self.get_all_engineered_features()
                #Show th values when one feature is selected, just for convenience before selecting
                if len (theSelectedInputFeaturesChoice_value) == 1:
                    for selected in theSelectedInputFeaturesChoice_value:
                        text = selected
                        if selected in protected:# if protected
                            text = text + ": values to encode " + str(self.protected_feature_set_df[selected].dropna().unique())
                            self.helper_methods.display_html (text, self.text_color, "h4")
                        else: 
                            text = text + ": values to encode " + str(self.non_protected_feature_set_df[selected].dropna().unique())
                            self.helper_methods.display_html (text, self.text_color, "h4")

    #################################################################################################
    #  
    # 
    #################################################################################################                           
    def on_label_encode_button_clicked(self, b):
         if not self.non_protected_feature_set_df.empty:
            try:
                protected, non_protected, all_features = self.get_all_engineered_features()
                p = set(protected)# for fast reference operation
                prot_list = []
                non_prot_list = []
                prot_dict = {}
                non_prot_dict = {}
                for selected in [self.theSelectedCategoricalFeaturesDropDown.value]:
                    if selected in p:# if protected
                        prot_list.append(selected)   
                    else: 
                        non_prot_list.append(selected)
                
                
                if len(prot_list) > 0:
                    prot_dict = self.helper_methods.label_encoding(prot_list,
                                                                   self.protected_feature_set_df)                  
                    self.label_encoding_dict.update(prot_dict)
                    
                if len(non_prot_list) > 0:
                    non_prot_dict = self.helper_methods.label_encoding(non_prot_list, 
                                                                       self.non_protected_feature_set_df)                  
                    self.label_encoding_dict.update(non_prot_dict)
                
                text = ""
                for v in prot_list:
                    text = text + v + "_benc" + ", "
                for v in non_prot_list:
                    text = text + v + "_benc" + ", "
                with self.LEOut:
                    clear_output(wait=True)
                    text = "Label Encoding applied, original column copied as  " +  text
                    self.helper_methods.display_html (text, self.text_color, "p")
                    self.get_all_engineered_features()  #to refresh the dropdowns with the new cols      
                    self.set_selected_categorical_values(self.theSelectedCategoricalFeaturesDropDown.value)
            except Exception as e:
                with self.LEOut:
                    clear_output(wait=True)
                    self.helper_methods.display_html ("**Error when label encoding**", self.text_color, "h4")
                    display(e)
            
        
    #################################################################################################
    #  
    # 
    ################################################################################################# 
    def on_one_hot_encode_button_clicked(self, b):
        """ One Hot Encoding is used to convert categorical data, or text data, into numbers, 
        which our predictive models can better understand. 
        label encoding (an alternative approach)might introduces a new problems e.g if
        we encoded a set of country names into numerical data. 
        This is actually categorical data and there is no relation, of any kind, between the rows.
        The problem here is, since there are different numbers in the same column, 
        the model will misunderstand the data to be in some kind of order, 0 < 1 < 2. 
        But this isn’t the case at all. To overcome this problem, we use One Hot Encoder.
        One hot encoding is a process by which categorical variables are converted into a form that could be
        provided to ML algorithms to do a better job in prediction. 
        The categorical values start from 0 goes all the way up to N-1 categories.
        What one hot encoding does is, it takes a column which has categorical data, 
        which has been label encoded, and then splits the column into multiple columns. 
        The numbers are replaced by 1s and 0s, depending on which column has what value. 
        We want 7 new columns one for each Race category in our dataset."""
        with self.HotEncodeOut:
            clear_output(wait=True)
            protected, non_protected, all_features = self.get_all_engineered_features()
            p = set(protected)# for fast reference operation
                
            selected = self.theSelectedCategoricalFeaturesDropDown.value
            text = "Applying one hot encoding to feature "+ str(selected)
            self.helper_methods.display_html (text, self.text_color, "p")
            if selected in p:# if protected
                self.protected_feature_set_df[selected] = pd.Categorical(self.protected_feature_set_df[selected])
                dfDummies = pd.get_dummies(self.protected_feature_set_df[selected], prefix=selected)
                self.protected_feature_set_df = pd.concat([self.protected_feature_set_df, dfDummies], axis=1)
                self.helper_methods.display_html("Generated Features: "+  str(dfDummies.columns.values), self.text_color, "h5")
                self.protected_feature_set_df.rename(columns={selected: selected+'_oh_benc'}, inplace=True)
            else: 
                self.non_protected_feature_set_df[selected] = pd.Categorical(self.non_protected_feature_set_df[selected])
                dfDummies = pd.get_dummies(self.non_protected_feature_set_df[selected], prefix=selected)
                self.non_protected_feature_set_df = pd.concat([self.non_protected_feature_set_df, dfDummies], axis=1)
                text = "Generated Features: "+ str(dfDummies.columns.values) + "<br>"
                self.non_protected_feature_set_df.rename(columns={selected: selected+'_oh_benc'}, inplace=True)
            text =  text + "Original column saved as "+ str(selected)+'_oh_benc'
            for col in dfDummies.columns:
                self.oh_encoding_dict[col] = {}
                self.oh_encoding_dict[col]["Original_col"] = selected
                orig_val = col.replace(selected + "_",'')
                self.oh_encoding_dict[col]["Original_val"] = orig_val
           
            self.helper_methods.display_html (text, self.text_color, "p")
            self.get_all_engineered_features()  #to refresh the dropdowns with the new cols
            self.theSelectedCategoricalFeaturesDropDown.value = dfDummies.columns.values[0]


    #################################################################################################
    #  Method to view the scale of the input features. on_apply_scale button calls the same method
    # but with apply set to True for the helper file
    #################################################################################################
    def on_view_scale_button_clicked(self, b):
        if not self.df.empty:
            self.scale_features(_apply = False)     
            
    
    def on_apply_scale_button_clicked(self, b):
        if not self.df.empty:
            self.scale_features(_apply = True)     
             
            
    #################################################################################################
    #  HERE: Have to view when select value, and apply when click button(so need to modify this flow)
    # 
    #################################################################################################
    def scale_features(self, _apply = False):
        with self.scaleNormaliseOut:
            clear_output(wait=True)

            beforeOut = widgets.Output(layout={})
            afterOut = widgets.Output(layout={})

            tab_contents = [beforeOut, afterOut]


            tab = widgets.Tab()
            tab.children = tab_contents

            tab.set_title(0, "View Before")
            tab.set_title(1, "View After")
            display (tab)
            try:
                protected, non_protected, all_features = self.get_all_engineered_features()
                p = set(protected)# for fast reference operation
                prot_list = []
                non_prot_list = []
                attribute_list = []
                
                selected_items = self.theSelectedNumericFeaturesChoice.value
                if len(list(selected_items)) == 0:
                    selected_items = list(self.theSelectedNumericFeaturesChoice.options)
                 
                for selected in selected_items:
                    if selected in p:# if protected
                        prot_list.append(selected) 
                        attribute_list.append(selected) 
                    else: 
                        non_prot_list.append(selected)
                        attribute_list.append(selected)

                data_frame_to_scale = (self.get_dataframe( include_label_y = False, 
                                    include_protected = True)[0][attribute_list])


                s_type = self.selectScaleType.value

                if s_type == "STANDARD_SCALAR":
                    scaler = preprocessing.StandardScaler()    
                elif s_type == "MIN_MAX_SCALAR":
                    scaler = preprocessing.MinMaxScaler()
                elif s_type == "ROBUST_SCALAR":
                    scaler = preprocessing.RobustScaler()
                elif s_type == "NORMALIZER":
                    scaler = preprocessing.Normalizer()


                fig1, (ax1) = plt.subplots(nrows=1, figsize=(14,7));
                fig2, (ax2) = plt.subplots(nrows=1, figsize=(14,7));
                plt.tight_layout()

                modified_df = scaler.fit_transform(data_frame_to_scale)
                modified_df = pd.DataFrame(modified_df, columns=attribute_list)

                with beforeOut:
                    accordion_before = widgets.Accordion(children=[widgets.HTML(data_frame_to_scale.describe().to_html())])
                    accordion_before.set_title(0, 'Description of features before scaling/normalisation')
                    accordion_before.selected_index = None
                    display(accordion_before)                                                                      
                    ax1.set_title('Before Scaling')
                    for attribute in attribute_list:
                        sns.kdeplot(data_frame_to_scale[attribute], ax=ax1);
                    display(fig1)


                with afterOut:
                    display (HTML("View effect of " + s_type + ". This is a view only!"))
                    accordion_after = widgets.Accordion(children=[widgets.HTML(modified_df.describe().to_html())])
                    accordion_after.set_title(0, 'Description of features after scaling/normalisation')
                    accordion_after.selected_index = None
                    display(accordion_after)  
                    ax2.set_title('After '+ s_type)
                    for attribute in attribute_list:
                        sns.kdeplot(modified_df[attribute], ax=ax2);
                    display(fig2)


                plt.close(fig1)
                plt.close(fig2)
                plt.clf()



                if _apply == True:
                    for col in prot_list:
                        self.apply_scale_norm[col] = s_type
                        self.protected_feature_set_df[col] = modified_df[col];
                    for col in non_prot_list:
                        self.apply_scale_norm[col] = s_type
                        self.non_protected_feature_set_df[col] = modified_df[col];
                    self.helper_methods.display_html ("Operation has been applied", self.text_color, "p")

                else:
                    self.helper_methods.display_html ("View only, press 'Apply' button below to apply changes", self.text_color, "p")


                gc.collect()

            except Exception as e:
                    self.helper_methods.display_html ("**Error when applying scale, select only numeric features**", self.text_color, "h4")
                    print(e)

        
    
    
    
    #################################################################################################
    #  
    # 
    #################################################################################################
    def on_save_file_button_clicked(self, b):
        #Combine protected/non protected and y and save to csv
        df = pd.concat([self.non_protected_feature_set_df, self.protected_feature_set_df, self.y_label_df], axis=1)

        all_features = df.columns
        protected_x = []
        non_protected_x = []
        oh_enc = []

        for column in (all_features):
            if column.endswith ("_oh_benc"):
                #[:-8]
                if column in self.protected_feature_set_df.columns:
                    protected_x.append(column)
                else:
                    non_protected_x.append(column)
                oh_enc.append(column)
            if not column.endswith ("_bm") and not column.endswith ("_benc"):
                if column in self.protected_feature_set_df.columns:
                    protected_x.append(column)
                else:
                    non_protected_x.append(column)
        #now we have in protected_x and non_protected_x the original names of the features
        #and any of the new one_hot names which we should now remove.
        rename = []
        for feat in oh_enc:
            remove = []
            
            for f in protected_x:
                if f.startswith(feat[:-8] + "_") and f != feat:
                    remove.append(f)
                elif f == feat:
                    rename.append(f)
            protected_x = [ele for ele in protected_x if ele not in remove]
    
            remove = []
            for f in non_protected_x :
                if f.startswith(feat[:-8] + "_") and f != feat:
                    remove.append(f)
                elif f == feat:
                    rename.append(f)
            non_protected_x = [ele for ele in non_protected_x if ele not in remove]
            

        categorical, numerical = self.helper_methods.get_features_type(df[protected_x + non_protected_x], 20)

        categorical = [x[:-8] if (x in rename) else x for x in categorical]
        numerical = [x[:-8] if (x in rename) else x for x in numerical]

        feature_data = {}
        default_desc = {
                       'type': '',
                       'target': False,
                       'protected': False,
                       'original_values' : [],
                       'values_description': [],
                       'original_choice_dict': {},
                       'original_privileged': '',
                       'privileged_description': '',
                       'one_hot_enc': False,
                       'one_hot_enc_col_before':'',
                       'one_hot_enc_cols_after': [],
                       'label_enc': False,
                       'label_enc_values': [],
                       'label_enc_choice_dict': {},
                       'label_enc_privileged': {},
                       'values_merged': False,
                       'before_merge_col': '',
                       'before_merge_values': [],
                       'scaled_using':''

                    }

        for feature in numerical:
            feature_data[feature] = default_desc.copy()
            feature_data[feature]['type'] = "numeric" 
            if feature == str(self.y_label_df.columns[0]):
                feature_data[feature]['target'] = True
            if feature in self.apply_scale_norm:
                feature_data[feature]['scaled_using'] = self.apply_scale_norm[feature]

        for feature in categorical:
            feature_data[feature] = default_desc.copy()
            feature_data[feature]['type'] = "categorical"
            if feature == str(self.y_label_df.columns[0]):
                feature_data[feature]['target'] = True
            if feature + "_bm" in all_features: 
                feature_data[feature]['values_merged'] = True
                feature_data[feature]['before_merge_col'] = feature+"_bm"
                feature_data[feature]['before_merge_values'] = self.merged_dict[feature]

            if  feature + "_oh_benc" in all_features:

                feature_data[feature]['one_hot_enc'] = True
                feature_data[feature]['one_hot_enc_col_before'] = feature
                oh_cols = []
                for cols in all_features:
                    if cols.startswith(feature+"_"):
                        oh_cols.append(cols)
                oh_cols.remove(feature + "_oh_benc")
                feature_data[feature]['one_hot_enc_cols_after'] = oh_cols

                #Setting this to its pre- one hot encoded column name for the call to get_feature_info
                values = df[feature + "_oh_benc"].unique()
                choice_dict, original_values, label_encoded_values, descriptions = self.helper_methods.get_feature_info (
                                                                 feature + "_oh_benc", 
                                                                 values, 
                                                                 self.group_descriptions_dict, 
                                                                 self.label_encoding_dict, 
                                                                 self.oh_encoding_dict, 
                                                                 self.merged_dict, 
                                                                 trace = False)

            else:
                values = df[feature].unique()

                choice_dict, original_values, label_encoded_values, descriptions = self.helper_methods.get_feature_info (
                                                                 feature, 
                                                                 values, 
                                                                 self.group_descriptions_dict, 
                                                                 self.label_encoding_dict, 
                                                                 self.oh_encoding_dict, 
                                                                 self.merged_dict, 
                                                                 trace = False)


            feature_data[feature]['original_values'] = list(original_values)
            feature_data[feature]['values_description'] = list(descriptions)

            feature_data[feature]['original_choice_dict'] = dict(zip(list(descriptions), list(original_values)))
            reverse_original_choice_dict = dict(zip(list(original_values), list(descriptions)))

            feature_data[feature]['label_enc_values'] = list(label_encoded_values)
            if feature in self.reference_groups_dict:
                feature_data[feature]['original_privileged'] = self.reference_groups_dict[feature]
                feature_data[feature]['privileged_description'] = reverse_original_choice_dict[self.reference_groups_dict[feature]]
            if len (label_encoded_values) > 0:
                feature_data[feature]['label_enc'] = True
                feature_data[feature]['label_enc_choice_dict'] = choice_dict
                feature_data[feature]['label_enc_privileged'] = choice_dict[feature_data[feature]['privileged_description']]
            if feature in protected_x:
                feature_data[feature]['protected'] = True  
            elif feature_data[feature]['original_privileged'] != '':
                feature_data[feature]['protected'] = True  
        

        for col in df.columns:
            if col.endswith("_benc"):
                df.drop(col, axis = 1, inplace=True)
                
        path = self.fc.selected_path + "/" + self.fc.selected_filename
        if not os.path.exists(self.fc.selected_path):
            os.makedirs(self.fc.selected_path)
        df.to_csv(path, index=False)
        text = "<font style='color:orange;'>Transformed CSV file saved to " + str( path)
        display(HTML(text))
        
        #####
        #removed local class
        #####

        save_info = self_info_class()
        save_info.df_url = self.df_url
        save_info.feature_data_dict = feature_data.copy()
        save_info.HIGH_RANGE_POSITIVE = self.HIGH_RANGE_POSITIVE
        save_info.Y_BINARY = self.Y_BINARY
        save_info.Y_CONTINUOUS  = self.Y_CONTINUOUS
        save_info.GT_VALIDITY = self.GT_VALIDITY#0,1 or 2
        save_info.y_value = self.y_label_df.columns[0]

    # Save the file
        path = self.fc.selected_path + "/" + self.fc.selected_filename[:-4] + "_summary.pickle"
        self.run_report(feature_data, path)
        
        protected_before_transform = []
        non_protected_before_transform = []
        protected_after_transform = []
        non_protected_after_transform = []
            
        for feature in feature_data:
            if feature_data[feature]['target'] != True:
                if feature_data[feature]['protected'] == True:
                    protected_before_transform.append(feature)
                    if len (feature_data[feature]['one_hot_enc_cols_after']) != 0:
                        protected_after_transform = protected_after_transform +  feature_data[feature]['one_hot_enc_cols_after']
                    else:
                        protected_after_transform.append(feature)   
                else:
                    non_protected_before_transform.append(feature)
                    if len (feature_data[feature]['one_hot_enc_cols_after']) != 0:
                        non_protected_after_transform =  non_protected_after_transform + feature_data[feature]['one_hot_enc_cols_after']
                    else:
                        non_protected_after_transform.append(feature)
                
        save_info.protected_before_transform = protected_before_transform
        save_info.non_protected_before_transform = non_protected_before_transform
        save_info.protected_after_transform = protected_after_transform
        save_info.non_protected_after_transform = non_protected_after_transform

        dill.dump(save_info, file = open(path, "wb"))
        text = "<font style='color:orange;'>Transformation summary (to be used as input to analysis of trained model) saved to:<br> "+ str(path)
        display(HTML(text))
        
    

    #################################################################################################
    #  
    # 
    #################################################################################################
    def run_report(self, feature_data, pickle_path ):
        protected = []
        non_protected = []
        label = ''
        for feature in feature_data:
            if feature_data[feature]['target'] == True:
                label = feature
            elif feature_data[feature]['protected'] == True:
                protected.append(feature)
            elif feature_data[feature]['protected'] == False and feature_data[feature]['target'] == False:
                non_protected.append(feature)


        def hover(hover_color="#ffff99"):
            return dict(selector="tr:hover",
                        props=[("background-color", "%s" % hover_color)])
        styles = [
            hover(),
            dict(selector="th", props=[("font-size", "150%"),
                                       ("text-align", "center")]),
            dict(selector="caption", props=[("caption-side", "bottom")])
        ]

        html = "<h3><font style='font-family:sans-serif;color:green;'>General information:</h3><font style='color:black;'>" 
        html = html + "<ul><li>The target is <b>" + str(label) + " </b><br>"
        html = html + "<li>The features are <b>" + str(non_protected) + " </b><br>"
        html = html + "<li>The protected features are <b>" + str(protected) + " </b><br>"

        if self.HIGH_RANGE_POSITIVE == True:
            html = html + "<li>It has been observed that a high ranking (or Binary 1) by the model has a <b>POSITIVE</b> effect on an indivudual or group.<br>"
        elif self.HIGH_RANGE_POSITIVE == False:
            html = html + "<li>It has been observed that a high ranking (or Binary 1) by the model has a <b>NEGATIVE</b> effect on an indivudual or group.<br>"

        html = html + "<li>The relationship between the target <b>" + label + "</b> and the ground truth has been observed as " + self.GT_VALIDITY + "<br>"


        for feature in feature_data:
            if feature_data[feature]['protected'] == True:
            #Obtain the group set as privileged for each protected feature.     
                html = html + "<li> The privileged group for <b>" + feature + "</b> was set as <b>" + str(feature_data[feature]['privileged_description']) + "</b><br>"
        
        html = html + "</ul>"#close the list for general

        html = html + "<h3><font style='font-family:sans-serif;color:green;'>Transformations applied:</h3><font style='color:black;'>"
        new_order = []
        for feature in feature_data:
            if feature_data[feature]['target'] == True:
                new_order.append(feature)
        for feature in feature_data:
            if feature_data[feature]['protected'] == True:
                new_order.append(feature)
        for feature in feature_data:
            if feature_data[feature]['protected'] == False and feature_data[feature]['target'] == False:
                new_order.append(feature)
                
        html = html + "<ul>"       
        for feature in new_order:#in order of target, protected, other.
            html = html +"<li><b>"+feature+"</b><br>"
            html = html + "<ul>"
            html = html + "<li>Type: " + str(feature_data[feature]['type']) + "<br>"
            if feature_data[feature]['target'] == True:
                html = html + "<li>This is the target(y)<br>"
            if feature_data[feature]['protected'] == True:
                html = html + "<li>This is a protected feature<br>"
            if feature_data[feature]['type'] == "categorical":
                html = html + "<li>Original Values: " + str(feature_data[feature]['original_values']) + "<br>"
                html = html + "<li>Value descriptions: " + str(feature_data[feature]['values_description']) + "<br>"
            if feature_data[feature]['label_enc'] == True:
                html = html + "<li>Label encoding was applied to this feature." + "<br>"
                html = html + "<li>Label encoded values: " + str(feature_data[feature]['label_enc_values']) + "<br>"
            if feature_data[feature]['one_hot_enc'] == True:
                html = html + "<li>One-Hot-Encoding was applied to this feature" + "<br>"
                html = html + "<li>The new columns are:" + str(feature_data[feature]['one_hot_enc_cols_after']) + "<br>"
            if feature_data[feature]['values_merged'] == True:
                html = html + "<li>Some values within the feature were merged." + "<br>"
                html = html + "<li>The values before the merge were: " + str(feature_data[feature]['before_merge_values']) + "<br>"
                html = html + "<li>The values after the merge are: " + str(feature_data[feature]['original_values']) + "<br>"
            if feature_data[feature]['scaled_using'] != "":
                html = html + "<li>Scaled/Normalised using: " + feature_data[feature]['scaled_using'] + "<br>"
            
            html = html + "<br>"
            html = html + "</ul>"
        html = html + "</ul>"
        
        
        #Group Representation
        for feature in feature_data:
            if feature_data[feature]['protected'] == True:
                html = html + "<h3><font style='font-family:sans-serif;color:green;'>Observations about group representation in sample for protected feature "+ feature.capitalize()+ ":</h3>"
                html = html + "<font style='color:black;'>"
                html = html + "<ul><li>" + self.group_under_represented_pop_dict[feature] + "<br>"
                html = html + "<li>" + self.group_under_represented_domain_dict[feature] + "<br>"
                html = html + "<li>" + self.group_under_represented_data_ok_dict[feature] + "<br>"
                #Worldview
                if self.group_under_represented_world_view_dict[feature] == 0: #bio
                    html = html + "<li><b> Inherent or biological worldview </b> considered applicable to any imbalance in sample representation across groups in feature  "+ feature.capitalize()+ ". (See below for details)<br>"
                elif self.group_under_represented_world_view_dict[feature] == 1: #social
                    html = html + "<li><b> Social or environmental worldview </b> considered applicable to any imbalance in sample representation across groups in feature  "+ feature.capitalize()+ ". (See below for details)<br>"
                html = html + "<li>" + "Additional notes: <font style='font-family:sans-serif;color:blue;'>" + self.group_represented_free_text[feature] + "<br>"
                html = html + "</ul>"#close the list 
        #Group and output distribution
        for feature in feature_data:
            if feature_data[feature]['protected'] == True:
                html = html + "<h3><font style='font-family:sans-serif;color:green;'>Observations about output distribution across groups in the sample for protected feature "+ feature.capitalize()+ ":</h3>"
                html = html + "<font style='color:black;'>"
                html = html + "<ul><li>" + self.group_output_distribution_dict[feature] + "<br>"
                html = html + "<li>" + self.group_output_distribution_data_ok_dict[feature] + "<br>"
                #Worldview
                if self.group_output_distribution_world_view_dict[feature] == 0:
                    html = html + "<li><b> Inherent or biological worldview </b> considered applicable to any differences in output distribution across groups in feature "+ feature.capitalize()+ ". (See below for details)<br>"
                elif self.group_output_distribution_world_view_dict[feature] == 1:
                    html = html + "<li><b> Social or environmental worldview </b> considered applicable to any differences in output distribution across groups in feature "+ feature.capitalize()+ ". (See below for details)<br>"

                html = html + "<li>" +  "Additional notes: <font style='font-family:sans-serif;color:blue;'>" + self.group_output_distribution_free_text[feature]+ "<br>"

                html = html + "</ul>"#close the list 

        df_dep = pd.DataFrame.from_dict(self.dependant_features_audit_dict)
        
        html = html + "<h3><font style='font-family:sans-serif;color:green;'>Observations on liklihood that Features are dependant on or proxys for protected features:</h3>"
        df_html = (df_dep.style.set_table_styles(styles))
        display (HTML(html))
        with open(self.fc.selected_path + "/report_" + self.df_url + ".html", 'w') as f:
            f.write(HTML(html).data)
            f.write(HTML(df_html.render()).data)
            
        display (df_html)
        
        html  = "<h3><font style='font-family:sans-serif;color:green;'>Worldview Descriptions:</h3>"  
        html =  html + "<font style='color:black;'>"
        html = html + self.worldview + "<br>"
        html  = html + self.worldview_biological + "<br><br>"
        html  = html + self.worldview_social + "<br>"
        
        display (HTML(html))
        with open(self.fc.selected_path + "/report_" + self.df_url + ".html", 'a') as f:
            f.write(HTML(html).data)
            f.write (HTML("<br><br><font style='color:orange;'>Transformation summary (to be used as input to analysis of trained model) saved to:<br> "+ str(pickle_path)).data)
       
        display (HTML ("<font style='color:orange;'>Report saved to " + self.fc.selected_path + "/report_" + self.df_url + ".html" ))
        
    
    #################################################################################################
    #  
    # 
    #################################################################################################

    def get_feature_set(self):
        return self.non_protected_feature_set_df.columns.values

    def get_protected(self):
        '''Returns:
        - a list of protected Features
        - a dictionary of renamed groups in a protected Feature
        - a dictionary of descriptions for a protected Feature.'''
        return self.protected_feature_set_df.columns.values
        

    def get_X_y(self):
        return self.non_protected_feature_set_df, self.protected_feature_set_df, self.y_label_df
        
    
    def get_pre_process_info(self):
        return self.label_encoding_dict, self.oh_encoding_dict, self.merged_dict, self.group_descriptions_dict
    

    
    def high_positive(self):
            return self.HIGH_RANGE_POSITIVE
            
    

            
        
    def render(self, use_demo_data = False):
        
        intro_box_layout = widgets.Layout(display='flex',
                                          flex_flow='column',
                                          align_items='stretch',
                                          border='solid',
                                          width='90%')
        
        space = widgets.Label('  ', layout=widgets.Layout(width='100%'))
        
       
        titleHTML = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:white;">
            <h1><center>Machnamh<font style="font-family:sans-serif; font-size:9px;color:white;">
            <a href="https://www.tearma.ie/q/machnamh/" target="_blank">(meaning)  </a>
            <font style="font-family:sans-serif; font-size:15px;color:white;"></h1></center>
            
            Fairness as a philosophy has no objective definition, and as such there is no consensus on a 
            mathematical formulation for fairness. When training a Machine learning model to 
            predict an outcome and hence influence decisions that will have positive or negative
            conseqnence for a person or group it is 
            necessary to reflect on the worldview or philosophy of fairness that the model will reflect.

            The design and functionality of a machine learning model will likely reflect the worldview 
            and values of those responsible for delivering the model. 
            Machnamh
            may be used for
            reflecting upon the risk of introducing prejudice during the creation of a supervised machine learning applications
            for predictive modeling.
            The framework has been developed with a specific focus on those models which rank humans and
            supports either continuous numeric or binary predictions. 
            Reflections prompted by this tool may require discussion, collaboration and agreement
            amongst various stakeholders within the business including relevant domain experts. Answers provided 
            will form part of a report which will reflect the organization’s core values and 
            worldview in relation to fairness. The report will provide a reference point for discussions
            between the producer and the consumer of the model with respect to the potential for these 
            worldviews and values to be reflected in the models output. Would the historic decisions 
            have differed, or would representation of a particular group be different in the data if 
            discrimination was not occuring in the present, or had discrimination not occured in the past.
           
             <br><br> 
            
            """ + self.worldview )
        
        wv_accordion = widgets.Accordion(children=[widgets.HTML(self.worldview_biological) , 
                                                   widgets.HTML(self.worldview_social) 
                                                  ])
        wv_accordion.set_title(0, 'Inherent or biological worldview')
        wv_accordion.set_title(1, 'Social or environmental worldview')
        wv_accordion.selected_index=None
            
        warningHTML = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:yellow;">
            *It is imperative to become familiar with these two worldview definitions before using the tool.
            Gaps in understanding of the ethical implications of poorly considered machine learning models which rank humans can have severe consequences for individuals
            as well as for groups and entire societies.
            """)
        title_box = Box(children=[titleHTML, wv_accordion, warningHTML], layout=intro_box_layout)
        title_box.add_class("box_style")

        

        introHTML = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:black;">
            <h3>Step 1: Data Review and Preparation:</h3> The purpose of this step is to raise awareness amongst 
            developers, domain experts and data scientists as to the potential for bias in the <b>training data</b> used to create
            any machine learning model. The tool provides a framework for reflection and accountability 
            in relation to the data used to train the model. The goal is to promote discussion, collaboration
            and accountability amongst all those involved in delivering or consuming the ML model.
            Data used to train the models should be representative and free of bias, this is an objective which
            all stakeholders should be aware of, reflect upon and be accountable for.
            <br><br>
            """)

        intro_box = Box(children=[introHTML], layout=intro_box_layout)
        intro_box.add_class("intro_box_style")

        uploadHTML = widgets.HTML("<h3><left>Upload the data file to be used to train/test/validate your ML model :</left></h3>")
        
        removeRowsColumnsHTML = widgets.HTML(
            "<h3><left>Review and handle missing data:</left></h3> ")
        
        selectYHTML = widgets.HTML(
            """<h3><left>Select the target (y):</left></h3> """)
        
        selectYHTML_B = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            
            The model will 'learn' how to make new predictions by 
            detecting patterns/correlations between the persons' input features(X0 to Xn) 
            and the historic decisions or outcomes as reflected in the 
            target (y). This target is often 
            considered as the <b>"Ground Truth"</b> and deemed to be the golden standard to 
            which the learning algorithm needs to adapt, and against which accuracy of the 
            final models output (ŷ) is measured.
            """)
        
        selectGTHTML = widgets.HTML(
            """<h3><left>Reflect upon the relationship between the target (y) and the ground-truth:</left></h3>
            <font style="font-family:sans-serif; font-size:15px;color:grey;">

            """)
        
        
        selectImpactHTML = widgets.HTML(
            """<h3><left>Reflect upon the impact the prediction will have on an individual:</left></h3>""")
        
        
        rankingEffectHTML = widgets.HTML(
            "<h4><center>Impact of output value</center></h4>")
        
        
        selectXHTML_h = widgets.HTML(
            """
            <h3><left>Select possible Input features and Protected features:</left></h3>""")
        
        selectXHTML_f = widgets.HTML(
            value = """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            
            <b>Input features: </b>The available and observed features that a decision
            could be based upon. <br>
            <font style="font-family:sans-serif; font-size:13px;color:#34abeb;">
            *These do not necessarily reflect the “true” features 
            of a person which are often not objectively observable. In reality, there may also not 
            be enough observable, measurable features to make fair ranking decisions between 
            individuals.<br>""",
            layout = {'border': 'solid 1px white', 'padding': '10px'})
        
        selectXHTML_pf = widgets.HTML(
            value = """<font style="font-family:sans-serif; font-size:15px;color:grey;">
            <b>Protected features:</b> A protected feature is a sensitive feature or attribute that
            categorises humans into groups of individuals who share certain characteristics. <br>
            <font style="font-family:sans-serif; font-size:13px;color:#34abeb;">
            *To promote social equality we must prevent an unfavorable outcome that is based upon
            the membership of a particular group. Example of protected groups include but are 
            not limited to those of race, sex, national origin, age, religion, disability, or colour.
            Unfavorable outcomes may be as a result of racism, sexism, ageism, homophobia, 
            ableism, classism, xenophobia and other forms of prejudice<br>
            """,
            layout = {'border': 'solid 1px white', 'padding': '10px'})
        
        
        selectXHTML_f.layout.grid_area  = 'left'
        selectXHTML_pf.layout.grid_area  = 'right'

        f_layout=Layout(
                        width='100%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        grid_template_areas='''
                        "left right"
                        ''')

        selectXHTML = widgets.GridBox([selectXHTML_f, 
                            selectXHTML_pf], layout = f_layout)

        selectXHTML_B = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            <b>Fairness and Disparate Treatment (Direct Bias)</b> — A decision-making process suffers 
            from disparate treatment if the decision or outcom is in any way dependant on a protected Feature. 
            It generally involves an intent to discriminate, in the case of ML this can occur when the model 
            detects a correlation between the feature in question(such as gender, race, religion or age) 
            and the historic outcomes/decisions specified in the training data.
            
            While protected features should not necessarally be used as an input feature to train a model
            it is important to retain/track this information rather than simply taking a "blind" approach 
            because as we will see later we need to consider the possibility that proxies for protected 
            features may exist in the non-protected features(e.g. postcode). 
            We also need to measure fairness based upon these explicitly protected 
            features. Imposing a willful blindness by removing and then ignoring the protected feature 
            makes it harder to detect, prevent, and reverse bias. 
           
            As stated by Dwork et al., being <b>“colorblind”</b> or simply ignoring protected 
            attributes will not ensure fairness in decision making by algorithms.  
            """
        )
        
        
        selectReferenceGroupsHTML = widgets.HTML(
            """
            <h3><left>Identify the privileged group for each protected feature:</left></h3>
            """)
            
        selectReferenceGroupsHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            
            <b>Privileged group: </b>Within a protected Feature we have one or more protected groups, 
            the privileged group is a non-protected group and typically refers to the non-protected group 
            which has historically held the majority of political and social power within the population. 
            For example "White" and "Male" are typical choices for the privileged group for 
            the race and gender features respectively. 
            The priviliged group is usually the reference group against which bias is measured, setting it here
            will result in it's use as the default reference group for any later calculations. 
            """)
            
        selectReferenceGroupsHTMLNote = widgets.HTML(
            """<font style="font-family:sans-serif; font-size:15px;color:#34baeb;">
            <b>Note:</b> If you are unsure which group to select, make your best guess. It will be used as the 
            default reference group.
            """)
        
        
        viewGroupRepresentationHTML = widgets.HTML(
            """
            <h3><left>Review and reflect upon the sample in terms of protected group representation:</left></h3>
            """)
        
        viewGroupRepresentationHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            Bias frequently occurs when the training data has an
            disparity in representation of samples across groups within a proteced feature
            (such as race, gender etc). If the population represented in the training dataset
            does not match the population that the machine learning model will make 
            predictions about when deployed then the resulting model may not generalise well for 
            those groups which are under-represented.
            """)
            
            

        
        viewOutputDistributionHTML = widgets.HTML(
            """
            <h3><left>Review and reflect upon the distribution of the target(y) across groups:</left></h3>
            """)
        
        
        viewOutputDistributionHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            An important consideration when training a Machine learning model to rank humans 
            is as to whether there is a statistically significant difference in the target
            being using to train the model with respect to membership of a particular protected group. 
            Training a model to predict differences, without any consideration as to why any
            differences exist, may have a significant impact on the life chances, and oppertunities
            of the humans being ranked, resulting in the transmission of socioeconomic and other
            inequality across generations based on gender, race, ethnicity etc.
            
            
            """)
        
        
        featureAuditForProxiesHTML = widgets.HTML(
            """
            <h3><left>Reflect on the input features relationship with the protected features:</left></h3>
            <font style="font-family:sans-serif; font-size:15px;color:grey;">""")
            


        
        
        
        ProtectedAttributesHTML = widgets.HTML(
            """<h3><left>6. Visualise Features:</left></h3>
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            This analysis can be used to determine if there is an imbalanced representation of protected 
            groups in the dataset, to observe the distribution of outcomes across the protected groups, the distribution of
            input features across groups and to generally examine the outcome across gropus based on a definition of a 
            successful outcome.
            """)

        mergeFeaturesHTML = widgets.HTML(
            """<h3><left>Merge Categorical feature levels (unique values): </left></h3> 
            """)
        mergeFeaturesHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            This functionality can be used to reduce the number of levels(unique values) per categorical 
            feature by merging levels. For example you could merge "race" levels to form {White, Non-White}
            or gender to {Male, Non-Male}. The main motivation for merging levels(unique values) is to make 
            the model more robust and to prevent overfitting, which may occur when one level is
            disproportionately represented in the training data, the model will not understand an 
            underrepresente level very well (nor will it generalize). One option is to make an explicit 
            "other" category for values. There may however be a cost to performance as every time you merge
            levels, you sacrifice information and make your data more regularized. 
            <p style="color:#34baeb">Note: This functionality can also be use to rename a categorical
            feature level.</p>""")
        
        storeReferenceForFeaturesHTML = widgets.HTML(
            """<h3><left>Set a description for categorical feature value(s):</left></h3>
            We consider a categorical feature any feature of type "object" or of type "numeric" with 
            less than 20 unique values.""")
            
        storeReferenceForFeaturesHTML_b = widgets.HTML("""
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            Categorical Input features may already be in a numeric format in your dataset such as 1 = Female, 2 = Male.
            However, if they are not, to allow for a clearer analysis you can apply a description to
            the values of a feature here. Applying a description to the protected groups 
            if the meanings are unclear will be particularally useful while interpreting 
            the results of unfairness detection later.
            """)
            
        storeReferenceForFeaturesHTMLNote = widgets.HTML("""<font style="font-family:sans-serif; font-size:15px;color:#34baeb;">
            <b>Note:</b> These descriptions are for information purposes only, therefore if values are already 
            descriptive this step is not necessary """)
        
        
        profileHTML = widgets.HTML(
            """<h3><left>Input feature analysis:</left></h3>
            <font style = "color:orange;"> This step may take some time to complete as several operations are taking place!
            
            """)
        
        profileHTML_b = widgets.HTML(
            """<font style="font-family:sans-serif; font-size:15px;color:grey;">
            This data visualization step may be used in conjunction with any other
            feature selection methods you typically use. Feature selection methods are intended to 
            reduce the number of input variables to those that are considered most useful to a models prediction.
            This aid will provide preliminary insight into the available input features and help identify <b>fair and accurate</b> predictors of the target(y).
            Generally in Machine learning we need to choose input features which are good predictors of the
            target. From a fairness perspective we may want to avoid features which have strong dependencies on
            the protected feature, or which may act as a proxy( ie. have a very strong dependency) on the protected
            feature. Using an input feature that is a proxy to a protected feature may cause the model to
            infer membership of a protected group even if the protected feature itself is not
            explicitly used. This would result in the same issues as using the protected feature directly. <br>
            
            <b><br>This visualization can be used to: <br></b>
            
            <b>*</b> Detect any dependencies or correlations amongst the input features themselves. <br>
            <b>*</b> Detect any dependencies or correlations between the input features and the target(y).<br> 
            <b>*</b> Detect any dependencies or correlations between the input features and the protected features.<br> 
            <b>*</b> Detect significant differences in the distribution of the input feature values across groups of individuals.<br>
            <b>*</b> Preform significance testing on distribution of feature values across groups of individuals.<br>
            <b>*</b> Preform Pearson, Spearman, Kendall, Phik and Cramer correlation tests.<br>
            <b>*</b> Preform Two-Tailed T-Test, Pearson’s chi-squared, Benfords law of significant digits test. <br>
            <br>
            
            """)
        
         
        profileSelectionHTML = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:12px;color:#34baeb;">
            <b>Note:</b> All features will be available for visualization by default. If you only want to 
            visualise some of the possible input features then make a selection from the 
            box to the left.
            """)
        
        
        
        dropFeaturesHTML = widgets.HTML(
            "<h3><left>Optionally drop input features based on analysis:</left></h3>")
        
        dropFeaturesHTMLNote = widgets.HTML("""
        <font style="font-family:sans-serif; font-size:12px;color:#34baeb;">
        <b>Note:</b> It is not possible to drop protected features at this point. Later
        you can decide if you will use them for training or not, however they will remain 
        in the process for reference purposes and so that model fairness analysis can be preformed later.""" )


        
        selectLEHTML = widgets.HTML(
            """<h3><left>Label-Encode <b>Ordinal</b> categorical features: </left></h3>
            Categorical features are defined by the tool as any feature with dataType Object, or with ten or less unique values.</br>
            """)
        
        selectLEHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            Categorical features are those that contain a finite number of label values rather than 
            numeric values. <br>
            
            <b>Ordinal categories</b> are those that have a natural ordered relationship between 
            each other which a model might understand and harness. Label-Encoding can also 
            be applied to nominal categorical features if there are only two categories, 
            as this is equivalent to One-Hot-Encoding(with "first column drop" applied)""")
        
        
        
        selectHEHTML = widgets.HTML(
            """<h3><left>One-Hot-Encode <b>Nominal</b> categorical features: </left></h3>
            Categorical features are defined by the tool as any feature with dataType Object, or less unique values.</br>
            """)
        
        selectHEHTML_b = widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            Categorical features are those that contain a finite number of label values rather than 
            numeric values. <br>
            <b>Nominal Categories</b> are those that that have NO natural ordered relationship e.g 
            Gender: {Female, Male}, or Race: {Asian, Black, Hispanic, White...}. 
            Keep in mind the concept of Multicollinearity and the "One-Hot-Encoding trap"(Dummy Variable Trap.) in the case of
            gender for example if there are only two genders defined, it would be enough to label encode to 1/0 
            (or 0/1) as this is the equivalent to one-hot encoding except using one input feature instead of 
            two, thus avoiding the "dummy variable trap". When using one-hot encoding, it is common to leave 
            out one of the columns because it can be inferred as being that which is absent 
            (i.e. if all of the other columns in the one-hot encoded dummy variables are 0, 
            then it must be the final category".""")
        

        selectScaleHTML = widgets.HTML(
            """<h3><left>Scale/Normalise numeric input features: </left></h3>""")
        
        selectScaleHTML_b= widgets.HTML(
            """
            <font style="font-family:sans-serif; font-size:15px;color:grey;">
            Many machine learning algorithms work better when features are on a relatively
            similar scale and close to a normal distribution. 
            MinMaxScaler, RobustScaler, StandardScaler, and Normalizer are scikit-learn methods used here
            to scale or normalise the data.<br><br>
            
            <b>Normalisation</b> is a good technique to use when you do not know the distribution of your
            data or when you know the distribution is not Normal or Gaussian. 
            It is useful when your data has varying scales and the algorithm you will use  
            does not make assumptions about the distribution of the data(e.g. knn or neural nets).<br>
            

            <b>Standardisation</b> is more effective when data has a normal or Gaussian (bell curve) distribution. 
            It is useful when your data has varying scales and the algorithm you are using makes 
            assumptions about the distribution (e.g. linear or logistic regression, or linear discriminant analysis)
            <br><br>""")

        
        selectSaveHTML = widgets.HTML(
            "<h3><left>Save transformed data to file.</left></h3>")
        
        
        self.selectYFeature.layout.grid_area = 'topl'
        self.selectXFeatures.layout.grid_area = 'topl' 
        self.selectProtectedAttributes.layout.grid_area = 'topr'
        self.choosenFeatureValues.layout.grid_area  = 'topr'
        self.newNameForValue.layout.grid_area = 'middle'
        self.merge_values_button.layout.grid_area = 'bottom' 
        self.theSelectedCategoricalFeaturesDropDown.layout.grid_area = 'topl'
        self.theSelectedNumericFeaturesChoice.layout.grid_area = 'topl'
        self.descriptionText.layout.grid_area = 'middle'
        self.save_description_button.layout.grid_area = 'bottom'
        self.selectXFeatures.layout.grid_area = 'topl'
        self.theSelectedInputFeaturesChoice.layout.grid_area = 'topl'
        self.label_encode_button.layout.grid_area = "topr"
        self.one_hot_encode_button.layout.grid_area =  "topr"
        self.selectScaleType.layout.grid_area = "topr"
        self.view_scale_button.layout.grid_area = "view"                                                                                    
        self.apply_scale_button.layout.grid_area = "middlel"                      
        self.profile_data_button.layout.grid_area = "middlel"
        self.progressBar.layout.grid_area = "middle"
        self.drop_features_button.layout.grid_area = "bottom"
        self.selectReferenceGroupsOutput.layout.grid_area  = 'top'
        self.selectFeatureAuditOutput.layout.grid_area  = 'top'
        self.gtAssumption.layout.grid_area  = 'top'
        self.selectImpact.layout.grid_area  = 'top'
        self.view_representation_button.layout.grid_area  = 'top'
        self.viewRepresentationOut.layout.grid_area  = 'bottom'
        self.view_output_distribution_button.layout.grid_area  = 'top'
        self.viewOutputDistributionOut.layout.grid_area  = 'bottom'
        self.auditRepresentationOut.layout.grid_area  = 'audit' 
        self.auditOutputDistributionOut .layout.grid_area  = 'audit'
        self.analyze_missing_data_button.layout.grid_area = "top"
        profileSelectionHTML.layout.grid_area = "topr"
        HBox_view_choices = widgets.HBox([self.ref_name_box, self.pre_merge_box, self.pre_encode_box ])
        HBox_view_choices.layout.grid_area = "middle"
        dropFeaturesHTMLNote.layout.grid_area  = 'topr'
        self.selectLabelYOutput.layout.grid_area  = 'bot'
        self.selecImpactOutput.layout.grid_area  = 'bot'
        self.selecGTOutput.layout.grid_area  = 'bot'
        self.selectLabelXOutput.layout.grid_area  = 'bot'
        self.analyzeMissingDataOutput.layout.grid_area  = 'mid'
        self.missingDataProcessedOutput.layout.grid_area  = 'bot'
        selectXHTML.layout.grid_area = 'html'
        self.saveDescriptionOut.layout.grid_area = 'five'
        storeReferenceForFeaturesHTMLNote.layout.grid_area = 'six'
        selectReferenceGroupsHTMLNote.layout.grid_area = 'note'
        self.auditRepresentationOut.layout.grid_area = 'out'
        self.auditOutputDistributionOut.layout.grid_area = 'out'
        self.fileUploader.layout.grid_area = "topl"
        self.uploadFileOutput.layout.grid_area  = 'bot'
        selectYHTML_B.layout.grid_area  = 'html'
        storeReferenceForFeaturesHTML_b.layout.grid_area  = 'html'
        selectReferenceGroupsHTML_b.layout.grid_area  = 'html'
        viewGroupRepresentationHTML_b.layout.grid_area  = 'html'
        viewOutputDistributionHTML_b.layout.grid_area  = 'html'
        profileHTML_b.layout.grid_area  = 'html'
        mergeFeaturesHTML_b.layout.grid_area  = 'html'
        self.mergeOut.layout.grid_area    = "six"
        self.LEOut.layout.grid_area     = "four"
        self.HotEncodeOut.layout.grid_area = "three"            
        selectLEHTML_b.layout.grid_area   = "html"
        selectHEHTML_b.layout.grid_area   = "html"
        selectScaleHTML_b.layout.grid_area = "html"
        self.theSelectedInputFeaturesChoiceOut.layout.grid_area = "four"
        self.scaleNormaliseOut.layout.grid_area = "five"
        self.profileDataOut.layout.grid_area = "out"
        accordion_about_one = widgets.Accordion(children=[self.descriptionChoiceOut])
        accordion_about_one.set_title(0, 'About feature selected... ')
        accordion_about_one.selected_index=None
        accordion_about_two = widgets.Accordion(children=[self.descriptionChoiceOut])
        accordion_about_two.set_title(0, 'About feature selected... ')
        accordion_about_two.selected_index=None
        accordion_about_three = widgets.Accordion(children=[self.descriptionChoiceOut])
        accordion_about_three.set_title(0, 'About feature selected... ')
        accordion_about_three.selected_index=None
        accordion_about_four = widgets.Accordion(children=[self.descriptionChoiceOut])
        accordion_about_four.set_title(0, 'About feature selected... ')
        accordion_about_four.selected_index=None
        accordion_about_one.layout.grid_area  = 'acc'
        accordion_about_two.layout.grid_area  = 'acc'
        accordion_about_three.layout.grid_area  = 'acc'
        accordion_about_four.layout.grid_area  = 'acc'



        display(
            title_box,
            intro_box,
            
            ###########Upload the file)#################
            
            widgets.GridBox(children=[uploadHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),  
            
            widgets.GridBox(children=[self.fileUploader,
                                      self.uploadFileOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "topl ."
                        "bot bot"
                        ''')
                   ), 
             
            ###########Select Label (Y)#################
            space,
            widgets.GridBox(children=[selectYHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),        
            widgets.GridBox(children=[selectYHTML_B, 
                                      self.selectYFeature, 
                                      self.selectLabelYOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl ."
                        "bot bot"
                        ''')
                   ),        

       
            ###########Select Impact of Score#################
            space,
            widgets.GridBox(children=[selectImpactHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ), 
            
            widgets.GridBox(children=[self.selectImpact, 
                                      self.selecImpactOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "top top"
                        "bot bot"
                        ''')
                   ),   
            
            
            ###########Select Ground Truth validity#################
            space,
            widgets.GridBox(children=[selectGTHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),
                
             widgets.GridBox(children=[self.gtAssumption, 
                                       self.selecGTOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "top top"
                        "bot bot"
                        ''')
                   ),   
            
            
            
            
            ############Select input and Protected Feature################
            space,
            selectXHTML_h,
            
            widgets.GridBox(children=[selectXHTML,
                                      self.selectXFeatures, 
                                      self.selectProtectedAttributes,
                                      self.selectLabelXOutput],
                        layout=Layout(
                        width='90%',
                        align_content = 'space-evenly',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "bot bot"
                        ''')
                   ),   
            
            
            
            ###########Missing Data#################
            space,
            removeRowsColumnsHTML,
            widgets.GridBox(children=[self.analyze_missing_data_button,
                                     self.analyzeMissingDataOutput,
                                     self.missingDataProcessedOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "top top"
                        "mid mid"
                        "bot bot"
                        ''')
                   ),
            
            

                
            ############Set description fot labels################
            space,
            storeReferenceForFeaturesHTML,
            widgets.GridBox(children=[storeReferenceForFeaturesHTML_b,
                                      self.theSelectedCategoricalFeaturesDropDown,
                                      self.choosenFeatureValues, 
                                      self.descriptionText, 
                                      self.save_description_button,
                                      accordion_about_one,
                                      self.saveDescriptionOut,
                                      storeReferenceForFeaturesHTMLNote
                                      
                                     ],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto auto auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "middle ."
                        "bottom bottom"
                        "acc acc"
                        "five five"
                        "six six"
                        ''')
                   ),

        
              
                
            ############Select Reference Group ################
            space,
            widgets.GridBox(children=[selectReferenceGroupsHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),
            widgets.GridBox(children=[selectReferenceGroupsHTML_b,
                                     self.selectReferenceGroupsOutput,
                                     selectReferenceGroupsHTMLNote],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "top top"
                        "note note"
                        ''')
                   ),   
            
            
            ############View Representation of groups in the data ################
            space,
            widgets.GridBox(children= [viewGroupRepresentationHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),
            widgets.GridBox(children=[viewGroupRepresentationHTML_b,
                                      self.view_representation_button, 
                                      self.viewRepresentationOut,
                                      self.auditRepresentationOut],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "top top"
                        "bottom bottom"
                        "out out"
                        ''')
                   ), 
               
            
            
            ############View Distribution of groups in the output ################
            space,
            widgets.GridBox(children= [viewOutputDistributionHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),
            widgets.GridBox(children=[viewOutputDistributionHTML_b,
                                     self.viewOutputDistributionOut,
                                     self.auditOutputDistributionOut],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "bottom bottom"
                        "out out"
                        ''')
                   ),  
                
            
            
            ###########Profile data using pandas profile#################
            space,
           
             widgets.GridBox(children= [ profileHTML],
                        layout=Layout(
                        width='90%',
                        )
                   ),
            # self.show_correlation_btn,
            widgets.GridBox(children=[profileHTML_b,
                                      self.theSelectedInputFeaturesChoice, 
                                      profileSelectionHTML, 
                                      self.profile_data_button,
                                      self.profileDataOut],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto, auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "middlel middlel"
                        "out out"
                        ''')
                   ),    
            
            
            
            ##########Drop Features##################
            space,
            dropFeaturesHTML,
            widgets.GridBox(children=[self.theSelectedInputFeaturesChoice, 
                                      dropFeaturesHTMLNote, 
                                      self.drop_features_button ],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "topl topr"
                        "bottom bottom"
                        ''')
                   ), 
            self.dropColOut,
            
                
            ############Audit of selected input features ################
            space,
            widgets.GridBox(children=[featureAuditForProxiesHTML ],
                        layout=Layout(
                        width='90%',
                        )
                   ),
            widgets.GridBox(children=[self.selectFeatureAuditOutput],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "top top"
                        ''')
                   ),   
                
      

            ##########Merge Feature values##################
            space,
            mergeFeaturesHTML,
            widgets.GridBox(children=[mergeFeaturesHTML_b,
                                      self.theSelectedCategoricalFeaturesDropDown, 
                                      self.choosenFeatureValues, 
                                      self.newNameForValue, 
                                      self.merge_values_button,
                                      accordion_about_two,
                                      self.mergeOut],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto auto auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "middle ."
                        "bottom bottom"
                        "acc acc"
                        "six six"
                        ''')
                   ),
 
            

            ###########Label Encode#################  
            space,
            selectLEHTML,
            widgets.GridBox(children=[selectLEHTML_b,
                                      self.theSelectedCategoricalFeaturesDropDown, 
                                      self.label_encode_button,
                                      accordion_about_three,
                                      self.LEOut
                                     ],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "acc acc"
                        "four four"
                        ''')
                   ),
            
            
            ###########One-Hot-Encode#################
            space,
            selectHEHTML,
            widgets.GridBox(children=[selectHEHTML_b,
                                      self.theSelectedCategoricalFeaturesDropDown, 
                                      self.one_hot_encode_button,
                                      accordion_about_four,
                                      self.HotEncodeOut],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "acc acc"
                        "three three"
                        ''')
                   ), 
            
            
            ###########Scale/Normalise Features#################
            space,
            selectScaleHTML,
            widgets.GridBox(children=[selectScaleHTML_b,
                                      self.theSelectedNumericFeaturesChoice, 
                                      self.selectScaleType, 
                                      self.scaleNormaliseOut,
                                      self.view_scale_button,
                                      self.apply_scale_button],
                        layout=Layout(
                        width='90%',
                        grid_template_rows='auto',
                        grid_template_columns='50% 50%',
                        border= '1px solid grey',
                        padding = '10px',
                        grid_gap='10px 10px',
                        grid_template_areas='''
                        "html html"
                        "topl topr"
                        "five five"
                        "view view"
                        "middlel middlel"
                        ''')
                   ),   
           
    
        )
        
        display (
            selectSaveHTML,
            self.fcOut)
        if use_demo_data == True:
            self.use_sample_dataset()
        
        


# In[ ]:




