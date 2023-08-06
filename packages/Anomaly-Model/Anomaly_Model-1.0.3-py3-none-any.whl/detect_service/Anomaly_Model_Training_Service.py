# -*- coding: utf-8 -*-
"""
Created on Sept 1 20:11:03 2020

@author: Wilson
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime
import time
import copy
import matplotlib.pyplot as plt
import ibm_boto3
from botocore.client import Config

#-----------------------------
def Read_Problem_data(model_id,icos_client,bucketName,feature_data_original,feature_data_normal):
    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    weld_id = int(weldId_with_toolID.split('_')[0])

    # Read Problem dta
    DR_file_name = 'Production_Anomaly_data/Formet_FR4_STA60_MIG_Weld_DR_Defects.csv'
    print(DR_file_name)
    body = icos_client.get_object(Bucket=bucketName,Key=DR_file_name)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    DR_file_df = pd.read_csv(body)
    DR_file_df = DR_file_df.drop_duplicates(subset =['PSN','WeldID'],keep='first',inplace=False)

    DR_PSN_red_list   = DR_file_df['PSN'].loc[(DR_file_df.WeldID == weld_id) & (DR_file_df.deviceId == deviceId) & (DR_file_df.Level == 'red')].tolist()
    DR_PSN_green_list = DR_file_df['PSN'].loc[(DR_file_df.WeldID == weld_id) & (DR_file_df.deviceId == deviceId) & (DR_file_df.Level != 'red')].tolist()
    #get validation data 
    validate_df = feature_data_original.loc[lambda x: (x.LPSN.isin(DR_PSN_red_list)) & (x.weld_id == weld_id),:]   
    validate_df['label'] = 1
    Data_PSN_for_red_list = validate_df['LPSN'].tolist()
    Data_WRI_for_red_list = validate_df['weld_record_index'].apply(lambda y: int(y)).tolist()

    validate_green_df = feature_data_original.loc[lambda x: (x.LPSN.isin(DR_PSN_green_list)) & (x.weld_id == weld_id),:]   
    validate_green_df['label'] = 0
    Data_PSN_for_green_list = list()
    Data_PSN_for_green_list = validate_green_df['LPSN'].tolist()
    Data_WRI_for_green_list = validate_green_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    
    validate_df = pd.concat([validate_df, validate_green_df])

    Data_PSN_for_all_list = validate_df['LPSN'].tolist()
    Data_WRI_for_all_list = validate_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    PSN_WRI_dict = {}
    for i in range(len(Data_PSN_for_all_list)):
        PSN_WRI_dict[Data_WRI_for_all_list[i]] = Data_PSN_for_all_list[i]
    #print(PSN_WRI_dict)
    print('Data_PSN_for_all_list:',len(Data_PSN_for_all_list))
    print('Problem point (weld_record_index) list = ',len(Data_WRI_for_all_list))
    dftemp= DR_file_df.loc[lambda x: (x.PSN.isin(Data_PSN_for_all_list)) & (x.WeldID == weld_id),:]
    print(dftemp)
    #
    # remove the defect that belongs to normal data
    #
    # get defect from normal data
    #get validation data 
    validate_normal_df = feature_data_normal.loc[lambda x: (x.LPSN.isin(DR_PSN_red_list)) & (x.weld_id == weld_id),:]

    Data_PSN_for_normal_list = validate_normal_df['LPSN'].tolist()
    Data_WRI_for_normal_list = validate_normal_df['weld_record_index'].apply(lambda y: int(y)).tolist()

    Data_PSN_removeNormal_list = list(set(Data_PSN_for_all_list) - set(Data_PSN_for_normal_list))
    Data_WRI_removeNormal_list = list(set(Data_WRI_for_all_list) - set(Data_WRI_for_normal_list))
    print('Data_PSN_removeNormal_list=',len(Data_PSN_removeNormal_list))
    print('Data_WRI_removeNormal_list=',len(Data_WRI_removeNormal_list))

    validation_wo_normal_df = validate_df.loc[lambda x: (x.LPSN.isin(Data_PSN_removeNormal_list)),:]
    #print(validation_wo_normal_df)
    
    Problem_object = {
                    'DR_file_df':DR_file_df,
                    'DR_PSN_red_list':DR_PSN_red_list,
                    'DR_PSN_green_list':DR_PSN_green_list,
                    'PSN_WRI_dict':PSN_WRI_dict,
                    'Data_WRI_for_red_list':Data_WRI_for_red_list,
                    'Data_PSN_for_red_list':Data_PSN_for_red_list,
                    'Data_WRI_for_green_list':Data_WRI_for_green_list,
                    'Data_PSN_for_green_list':Data_PSN_for_green_list,
                    'Data_WRI_for_all_list':Data_WRI_for_all_list,
                    'Data_PSN_for_all_list':Data_PSN_for_all_list,
                    'validate_df':validate_df,
                    'validation_wo_normal_df':validation_wo_normal_df
                   }
    return Problem_object


def read_feature_data(model_id,feature_file_base_list,icos_client,bucketName):
    #
    # read all feature data set from the file list
    #
    feature_data_original = pd.DataFrame()
    feature_data_normal = pd.DataFrame()

    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    toolID =  'tool'+model_id.split('_tool')[1]
    
    for feature_file_base in feature_file_base_list:
        try:
            feature_file_name = feature_file_base.replace('toolX',toolID)
            inputFile_date = feature_file_base.split('_LincolnFANUC_')[1].split('_welding_')[0]
            print(feature_file_name)
            body = icos_client.get_object(Bucket=bucketName,Key=feature_file_name)['Body']
            # add missing __iter__ method, so pandas accepts body as file-like object
            if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
            feature_data = pd.read_csv(body)
            feature_data_original = pd.concat([feature_data_original, feature_data])
            # Read normal data
            normal_file_name = feature_file_name[:-4] + '_normal.csv'
            print(normal_file_name)
            body = icos_client.get_object(Bucket=bucketName,Key=normal_file_name)['Body']
            # add missing __iter__ method, so pandas accepts body as file-like object
            if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
            normal_data = pd.read_csv(body)
            feature_data_normal = pd.concat([feature_data_normal, normal_data])

        except Exception as e:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            print('###### Exception, feature_data file might not exist in COS:' + feature_file_name)
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    feature_data_original   = feature_data_original.reset_index(drop = True)
    feature_data_normal = feature_data_normal.reset_index(drop = True)

    print('feature_data_original=',feature_data_original.shape)
    print('feature_data_normal=',feature_data_normal.shape)
    return feature_data_original,feature_data_normal


def export_training_validation_to_COS(model_id,icos_client,bucketName_model,feature_data_original,feature_data_normal,validate_df,validation_wo_normal_df,dateRange='',localPath='./Production_Anomaly_data/'):
    # Note: using model_id for file name in COS
    # Train
    fileName = 'Train_'+model_id+dateRange+'.csv'
            
    localfileName=localPath+fileName
    feature_data_normal.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # original feature data
    fileName = 'Original_feature_data_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    feature_data_original.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # validation
    fileName = 'validation_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    validate_df.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # validation_without_normal
    fileName = 'validation_wo_normal_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    validation_wo_normal_df.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)
    return

def read_training_validation_from_COS(model_id,icos_client,bucketName,bucketName_model,testData_date,dateRange=''):
    #
    #############################################################################################    
    # Training data
    csv_fileName=model_id+'/Train_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    feature_data_normal = pd.read_csv(body)
    print('feature_data_normal = ',feature_data_normal.shape)
    
    # Raw data
    csv_fileName=model_id+'/Original_feature_data_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    feature_data_original = pd.read_csv(body)
    print('feature_data_original = ',feature_data_original.shape)   
    
    #############################################################################################    
    # validation data
    csv_fileName=model_id+'/validation_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    validate_df = pd.read_csv(body)
    print ('Validation Data=',validate_df.shape)
    #############################################################################################
    # validation_wo_normal data
    csv_fileName=model_id+'/validation_wo_normal_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    validation_wo_normal_df = pd.read_csv(body)
    print ('Validation_without_normal Data=',validation_wo_normal_df.shape)

    ##############################################################################################
    #
    # === testDate date
    #
    #testData_date = '2020-08-24'
    # 
    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    feature_file_name = 'Production_Lincoln_features_data/'+deviceId+'_LincolnFANUC_'+testData_date+'_welding_stable_data_weldid_'+weldId_with_toolID+'_feature.csv'
    body = icos_client.get_object(Bucket=bucketName,Key=feature_file_name)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    testData1 = pd.read_csv(body)

    testData1 = pd.concat([testData1,validate_df.loc[validate_df.label == 1]]).reset_index(drop=True)
    testData1 = testData1.drop(['label'],axis = 1)
    testData = testData1.drop_duplicates(subset ="weld_record_index",keep='first',inplace=False)
    testData = testData.sort_values(['weld_record_index'],inplace=False)
    testData = testData.reset_index(drop=True)
    print ('test Data=',testData.shape)
    return feature_data_original,feature_data_normal,validate_df,validation_wo_normal_df,testData
#----------------------------------------------------------------

def print_and_plot_anomaly_score(model_name,df_join_TF,Problem_object,anomaly_threshold,anomaly_score,df_anomaly_score,plot_anomaly_score='YES'):
    # get from problem report:
    DR_file_df = Problem_object['DR_file_df']
    DR_PSN_red_list = Problem_object['DR_PSN_red_list']
    DR_PSN_green_list = Problem_object['DR_PSN_green_list']
    PSN_WRI_dict = Problem_object['PSN_WRI_dict']
    Data_WRI_for_red_list = Problem_object['Data_WRI_for_red_list']
    Data_WRI_for_green_list = Problem_object['Data_WRI_for_green_list']
    Data_WRI_for_all_list = Problem_object['Data_WRI_for_all_list']
   
    # calculate 99% quanytile
    percentile_point_95 = df_anomaly_score.apply(lambda y: np.percentile(y, 95))[0]
    print('percentile_point_95 : ',percentile_point_95)
    outlier95_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score >= percentile_point_95), 'weld_record_index']))
    anomaly_above_threshold_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score >= anomaly_threshold), 'weld_record_index']))
    #print('outlier95_list: ', outlier90_list)
    num_anomaly_95 = len( set(outlier95_list) & set(Data_WRI_for_red_list) )
    anomaly_above_threshold_join_defects =  list(set(anomaly_above_threshold_list) & set(Data_WRI_for_red_list))
    # normal
    normal_below_threshold_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score < anomaly_threshold), 'weld_record_index']))
    normal_green_list = list(set(normal_below_threshold_list) & set(Data_WRI_for_green_list))
    num_normal_below_threshold = len(normal_below_threshold_list)
    num_normal_green_list = len(normal_green_list)
    
    # plot anomaly score
    if (plot_anomaly_score == 'YES'):
        plt.figure(figsize=(20,4))
        plt.plot(anomaly_score)
        plt.title('Anomaly Score of each Weld based on Model ' + model_name)
        plt.xlabel('Observation')
        plt.ylabel('Anomaly Score')
        plt.axhline(y=percentile_point_95, ls="--", c="red")
        plt.axhline(y=anomaly_threshold, ls="--", c="yellow")
        # bad welds:
        Y = df_join_TF.loc[df_join_TF.weld_record_index.isin(Data_WRI_for_red_list),'anomaly_score']
        X = df_join_TF.loc[df_join_TF.weld_record_index.isin(Data_WRI_for_red_list)].index.tolist()
        plt.scatter(X, Y, s= 30, c = 'red') 
        # normal welds"
        Y = df_join_TF.loc[df_join_TF.weld_record_index.isin(Data_WRI_for_green_list),'anomaly_score']
        X = df_join_TF.loc[df_join_TF.weld_record_index.isin(Data_WRI_for_green_list)].index.tolist()
        plt.scatter(X, Y, s= 30, c = 'green') 
        
        plt.show()
    
    
    # print

    num_anomaly_list_PSN = [PSN_WRI_dict[x] for x in anomaly_above_threshold_join_defects]
    num_anomaly_df = DR_file_df.loc[lambda x: (x.PSN.isin(num_anomaly_list_PSN)),:]
    df_join_PSN_TF = df_join_TF.rename(columns={"LPSN": "PSN"})
    num_anomaly_df = num_anomaly_df.merge(df_join_PSN_TF[['PSN','anomaly_score']],on = ['PSN'], how = 'left')
    num_anomaly_df = num_anomaly_df.drop_duplicates(subset ="PSN",keep='first',inplace=False)
    num_anomaly_threshold = num_anomaly_df.shape[0]
    #
    print('=========number of anomaly =============== \n percentile_95:',num_anomaly_95,', bad validation num above threshold:',num_anomaly_threshold)
    print('---------number of normal ---------------- \n num_normal_green_list:',num_normal_green_list,', total num_normal_below_threshold:',num_normal_below_threshold)
    print(num_anomaly_df)
    return num_anomaly_95,num_anomaly_threshold