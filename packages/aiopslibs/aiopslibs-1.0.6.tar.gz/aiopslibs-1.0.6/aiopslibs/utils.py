import csv
import pickle
import os
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.datastore import Datastore
from msrest.exceptions import HttpOperationError
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import ntpath
from azureml.pipeline.core import Schedule
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig, Model
from azureml.pipeline.core import PipelineEndpoint
from azureml.exceptions import WebserviceException
import requests
import json
import torch
from azure.storage.blob import BlobClient
import asyncio
import urllib, json
import urllib.request
from urllib.error import URLError, HTTPError
from os import listdir
from os.path import isfile, join
import shutil
import yaml
import sys
import time
import numpy as np
import joblib
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import uuid
import string
import random
import xml.etree.ElementTree as ET
sns.set(color_codes=True)

class JoblibUtilities:
    @staticmethod
    def load_file_from_txt(file_content):
        temp = "./temp"
        FolderUtilities.make_dir(temp)
        
        temp_file = os.path.join(temp, str(uuid.uuid4()))

        joblib.dump(file_content, temp_file)
        result = joblib.load(file_content)
        shutil.rmtree(temp_file, ignore_errors=True)
        return result
        
class CsvUtilities:

    @staticmethod
    def load_data(filepath,already_labeled = {}, skip_already_labeled=False):
        # csv format: [ID, TEXT, LABEL, SAMPLING_STRATEGY, CONFIDENCE]
        if  not filepath:
            raise Exception("filepath param mus be provided")

        with open(filepath, 'r') as csvfile:
            data = []
            reader = csv.reader(csvfile)
            for row in reader:
                
                if len(row) == 0:
                    continue

                # Create the five columns for the observations that are not already
                # labeled. Because those labeled, already contain the 5 columns
                if skip_already_labeled and row[0] in already_labeled:
                    continue
                    
                if len(row) < 3:
                    row.append("") # add empty col for LABEL to add later
                if len(row) < 4:
                    row.append("") # add empty col for SAMPLING_STRATEGY to add later        
                if len(row) < 5:
                    row.append(0) # add empty col for CONFIDENCE to add later         
                data.append(row)

                # Add to the list already labeled those observations already labeled
                # when loading the script.
                # For saving logs.
                label = str(row[2])
                if row[2] != "":
                    textid = row[0]
                    already_labeled[textid] = label

        csvfile.close()
        return data
    
    # allows add data to csv file
    @staticmethod
    def append_data(filepath, data):
        with open(filepath, 'a', errors='replace') as csvfile:
            for list in data:
                csvfile.write(str(list).replace("['","").replace("', '",",").replace("', ",",").replace("']","").replace("]","")+"\n")
                    
            #writer = csv.writer(csvfile)
            #writer.writerows(data)
        csvfile.close()
    
    # Used to write a csv when it has not yet been initialized?
    @staticmethod
    def write_data(filepath, data):
        with open(filepath, 'w', errors='replace') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        csvfile.close()

    @staticmethod
    def transform_to_local_format(data):

        temp_name = "temp_file_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

        if isinstance(data, pd.DataFrame):
            data.to_csv(temp_name, header=False)
        else:
            FileUtilities.create_file_with_content(temp_name, data)

        #load data in local format
        result = CsvUtilities.load_data(temp_name)

        #delete temp file
        os.remove(temp_name)
        
        return result

class PickleUtilities:

    @staticmethod
    def load_file(path_file):
        """allows to load a file recorded by the pickle library

        Arguments:
            path_file {str} -- recorded pickle file path

        Returns:
            [type] -- pickle object
        """

        file = open(path_file,'rb')
        object_file = pickle.load(file)
        file.close()
        return object_file
    
    @staticmethod
    def write_file(path_file, data):
        """Allows to write data to new pickle file.

        Arguments:
            path_file {str} -- pickle path file  
            data {array} -- data content
        """
        print("write_file.path_file : ", path_file)
        os.makedirs(os.path.dirname(os.path.abspath(path_file)), exist_ok=True)
        
        with open(path_file, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

class FileUtilities:
    @staticmethod
    def create_file_with_content(file_name, content):
        """creates a file and manages closing connection even in case of an exception

        Arguments:
            file_name {str} -- file path
            content {str} -- file content

        Raises:
            Exception: [description]
        """
        try:
            file = open(file_name, "w")
            file.write(content)
        except Exception as e:
            raise Exception('an error occured during writing file operation : {}'.format(e))
        finally:
            #delete temp directory
            file.close() 
    
    @staticmethod
    def list_recursive_files(path):
        for dirpath, dirs, files in os.walk(path):
            for filename in files:
                fname = os.path.join(dirpath,filename)
                print(fname)
    
    @staticmethod
    def direct_download_file(url, download_path):
        donloaded = False
        try:
            r = requests.get(url, allow_redirects=True)
            open(download_path, 'wb').write(r.content)
            print("utils.direct_download_file.url : ", url)
            print("utils.direct_download_file.download_path : ", download_path)
            #if os.path.isfile(download_path):
            #    print("utils.direct_download_file le fichier est là : ")
            #    file = open(download_path,'r')
            #    print(file.read())
            #    file.close()
                #print()
            donloaded = True
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        except Exception as e:
            # do something
            print('Reason: ', e)
        return donloaded
        
class FolderUtilities:
    @staticmethod
    def make_missing_dir_from_file(file_path):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    @staticmethod 
    def make_dir(folder_path):
        os.makedirs(folder_path, exist_ok=True)

class FileNameProvider:

    @staticmethod
    def get_features_index_file(model_path):
        return os.path.join(model_path,"features_index.pickle")
    
    @staticmethod
    def get_model_candidate_name(model_path):
        return os.path.join(model_path, "outputs/model_candidate.mdl")
    
    @staticmethod
    def get_model_to_publish_name(model_path):
        return os.path.join(model_path, "outputs/model_to_publish.mdl")

    @staticmethod
    def get_model_to_be_validated_name(model_path):
        return os.path.join(model_path, "outputs/model_to_be_validated.mdl")
    
    @staticmethod
    def get_validated_model_name(model_path):
        return os.path.join(model_path, "outputs/validated_model.mdl")

    @staticmethod
    def get_outputs_folder(model_path):
        return os.path.join(model_path, "outputs")

class ComputeTargetConfig:
    @staticmethod
    def config(ws,cluster_name, vm_type, min_nodes, max_nodes,idle_seconds ):
        #Create or Attach existing compute resource
        # choose a name for your cluster
        compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", cluster_name)
        compute_min_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MIN_NODES", min_nodes)
        compute_max_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MAX_NODES", max_nodes)

        # This example uses CPU VM. For using GPU VM, set SKU to STANDARD_NC6
        vm_size = os.environ.get("AML_COMPUTE_CLUSTER_SKU", vm_type)

        print("#### vm_type : ", vm_type)
        if compute_name in ws.compute_targets:
            compute_target = ws.compute_targets[compute_name]
            if compute_target and type(compute_target) is AmlCompute:
                print("found compute target: " + compute_name)
        else:
            print("creating new compute target...")
            provisioning_config = AmlCompute.provisioning_configuration(vm_size = vm_size,
                                                                        min_nodes = compute_min_nodes, 
                                                                        max_nodes = compute_max_nodes,
                                                                        idle_seconds_before_scaledown = idle_seconds)
            # create the cluster
            compute_target = ComputeTarget.create(ws, compute_name.strip(), provisioning_config)
            
            # can poll for a minimum number of nodes and for a specific timeout. 
            # if no min node count is provided it will use the scale settings for the cluster
            compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
            
            # For a more detailed view of current AmlCompute status, use get_status()
            print(compute_target.get_status().serialize())
        
        return compute_target

class DataStoreConfig:
    @staticmethod
    def config(ws, blob_datastore_name,account_name,container_name,account_key):
        
        try:
            blob_datastore = Datastore.get(ws, blob_datastore_name)
            print("Found Blob Datastore with name: %s" % blob_datastore_name)
        except HttpOperationError:
            blob_datastore = Datastore.register_azure_blob_container(
                workspace=ws,
                datastore_name=blob_datastore_name,
                account_name=account_name, # Storage account name
                container_name=container_name, # Name of Azure blob container
                account_key=account_key) # Storage account key
            print("Registered blob datastore with name: %s" % blob_datastore_name)
        
        return blob_datastore

class RunConfigurationProvider:
    @staticmethod
    def get_run_config(ws,compute_target, packages):
        huml_env = Environment("huml-pipeline-env")
        huml_env.python.user_managed_dependencies = False # Let Azure ML manage dependencies
        huml_env.docker.enabled = True # Use a docker container

        # Add the dependencies to the environment
        huml_env.python.conda_dependencies = packages

        # Register the environment (just in case you want to use it again)
        huml_env.register(workspace=ws)
        registered_env = Environment.get(ws, 'huml-pipeline-env')

        # Create a new runconfig object for the pipeline
        pipeline_run_config = RunConfiguration()
        #run_config_user_managed.environment.python.user_managed_dependencies = True

        # Use the compute you created above. 
        pipeline_run_config.target = compute_target

        # Assign the environment to the run configuration
        pipeline_run_config.environment = registered_env

        return pipeline_run_config

class Helper:
    @staticmethod
    def generate(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class BlobStorageAPIUtilities:
    def __init__(self, base_url = "https://humlstorage.blob.core.windows.net"):
        self.base_url = base_url
    
    def is_file(self, blob_container, blob_name):

        temp = os.path.join(os.getcwd(), "blob_api_temp_555")
        FolderUtilities.make_dir(temp)
        data_downloaded_file = os.path.join(temp, blob_name)
        
        remote_file = "{0}/{1}/{2}".format(self.base_url, blob_container, blob_name)
        
        is_data_file_downloaded =  FileUtilities.direct_download_file(remote_file,data_downloaded_file)
        
        if is_data_file_downloaded == False:
            return False
        
        xx = self._is_blob_not_found(data_downloaded_file)
        
        result = not self._is_blob_not_found(data_downloaded_file)
        
        shutil.rmtree(temp, ignore_errors=True)

        return result


    def download_file(self, blob_container, blob_name, data_downloaded_file):
        #Helper
        #temp = os.path.join(os.getcwd(), Helper.id_generator())
        FolderUtilities.make_dir(os.path.dirname(data_downloaded_file))
        #local_data_downloaded_file = os.path.join(temp, blob_name)
        remote_file = "{0}/{1}/{2}".format(self.base_url, blob_container, blob_name)
        is_data_file_downloaded =  FileUtilities.direct_download_file(remote_file,data_downloaded_file)
        return is_data_file_downloaded


    def _is_blob_not_found(self, file_path):
        file = open(file_path,'r')
        root = None
        try:
            root = ET.fromstring(file.read())
        except Exception as e:
            print("Impossible to parse XML fle.", e)
        finally:
            file.close()
        
        if not root:
            return False
        
        if root[0].text == "BlobNotFound":
            return True
        return False

class BlobStorageManager:
    def __init__(self, connection_string):
        
        self.connection_string = connection_string
        # Create the BlobServiceClient object which will be used to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload(self,blob_container,  file_path, overwrite_v = False):
        """Upload the file to the Blob Storage 

        Arguments:
            blob_container {str} -- container (or folder) in blob storage 
            file_path {str} -- local file path

        Keyword Arguments:
            overwrite_v {bool} -- whether or not to overwrite the existing file on the blob storage (default: {False})
        """

        file_name = ntpath.basename(file_path)
                
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=overwrite_v)
        
    def delete(self,blob_container,  file_path):
        """deletes the file from the blob storage

        Arguments:
            blob_container {str} -- container (or folder) in blob storage 
            file_path {str} -- [description]
        """

        if os.path.isabs(file_path):
            file_name = ntpath.basename(file_path)
        else:
            file_name = file_path
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=file_name)

        print("\Deleting from Azure Storage:\n\t" + file_name)

        # Upload the created file
        blob_client.delete_blob()
    
    def download_text_by_url(self, file_path):
        """download the file from the http link

        Arguments:
            file_path {str} -- http link

        Returns:
            str -- downloaded file content
        """
        data = None
        try:
            response = urllib.request.urlopen(file_path)
            data = response.read().decode('utf-8')
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        except Exception as e:
            # do something
            print('Reason: ', e)

        return data

    def download_json_by_url(self, file_path):
        data = {}
        try:
            response = urllib.request.urlopen(file_path)
            data = json.loads(response.read())
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)

        return data

    def download_blob2(self, blob_container, blob_name, dest_file):
        blob = BlobClient.from_connection_string(conn_str=self.connection_string, 
                                                    container_name=blob_container, 
                                                    blob_name=blob_name)
        with open(dest_file, "wb") as my_blob:
            blob_data = blob.download_blob()
            print(blob_data)
            #my_blob.writelines(blob_data.content_as_bytes())
            blob_data.readinto(my_blob)

        #dest_content = None
        
        return  my_blob

    

    """
    def download_blob4(self):
        block_blob_service = BlockBlobService(account_name="", account_key="")
        return block_blob_service
    """

class PipelinePublisher:
    def __init__(self, ws):
        self.ws = ws
    
    def publish(self, experiment_name,pipeline_name):
        """Publish an experiment from name and the last Run that has just performed

        Arguments:
            experiment_name {str} -- The name of the experiment in the workspace...
            pipeline_name {str} --The name of the published pipeline

        Returns:
            str --pipeline id published, str --endpoint : http address through which the pipeline can be called
        """
        
        pipeline_experiment = self.ws.experiments.get(experiment_name)
        run = list(pipeline_experiment.get_runs())[0]
       
        published_pipeline = run.publish_pipeline(name = pipeline_name, description='pipelines', version="2.1")

        #return published_pipeline.id, published_pipeline.endpoint
        return published_pipeline

class EndpointPipelinePublisher:
    def __init__(self, ws):
        self.ws = ws
    
    def publish(self, experiment_name,pipeline, pipeline_name,pipeline_endpoint_name):
        pipeline_endpoint = None
        try:
            pipeline_endpoint = PipelineEndpoint.get(workspace=self.ws, name=pipeline_endpoint_name)
        except Exception as e:
            s = str(e)
            if not "BadRequest" in s:
                raise Exception(e)

        if not pipeline_endpoint:
            pipeline_endpoint = PipelineEndpoint.publish(workspace=self.ws,
                                                        name=pipeline_endpoint_name,
                                                        pipeline=pipeline,
                                                        description="New Pipeline Endpoint for {0}".format(pipeline_endpoint_name))
            published_endpoint = pipeline_endpoint.endpoint
            
        else:
            publisher = PipelinePublisher(self.ws)
            published_pipeline = publisher.publish(experiment_name, pipeline_name)
            
            pipeline_endpoint.add(published_pipeline)
            published_endpoint = published_pipeline.endpoint
            
        return published_endpoint
        
class WebServiceDeployer:
    def __init__(self, ws):
        self.ws = ws
        self.aciconfig = AciWebservice.deploy_configuration(cpu_cores=1, 
                                                    memory_gb=1, 
                                                    tags={"data": "Disaster-data",  "method" : "torch"}, 
                                                    description='Predict Disaster with torch')
        myenv = Environment.from_conda_specification(name="myenv", file_path="myenv.yml")
        self.inference_config = InferenceConfig(entry_script="score.py", environment=myenv)

    def deploy(self):
        myenv = CondaDependencies()                                                        
        myenv.add_pip_package("azureml-sdk")
        myenv.add_pip_package("torch")
        #myenv.add_pip_package("torch")
        myenv.add_pip_package("torchvision")
        myenv.add_pip_package("azureml-dataprep[pandas,fuse]>=1.1.14")

        with open("myenv.yml","w") as f:
            f.write(myenv.serialize_to_string())

        #Create a deployment configuration file and specify the number of CPUs and gigabyte 
        # of RAM needed for ACI container.
        #aciconfig = AciWebservice.deploy_configuration(cpu_cores=1, 
        #                                            memory_gb=1, 
        #                                            tags={"data": "Disaster-data",  "method" : "torch"}, 
        #                                            description='Predict Disaster with torch')


        #myenv = Environment.from_conda_specification(name="myenv", file_path="myenv.yml")
        #inference_config = InferenceConfig(entry_script="score.py", environment=myenv)

        try:
            AciWebservice(self.ws, AllConstants.SERVICE_NAME).delete()
        except WebserviceException:
            pass

        model = self.ws.models[AllConstants.MODEL_NAME]
        

        service = Model.deploy(workspace=self.ws, 
                            name=AllConstants.SERVICE_NAME, 
                            models=[model], 
                            inference_config=self.inference_config, 
                            deployment_config=self.aciconfig)
        
        service.wait_for_deployment(show_output=True)
        
    
    def test(self):
        service = AciWebservice(self.ws, AllConstants.SERVICE_NAME)
        #print(type(service))
        #scoring_uri = service.scoring_uri
        #headers = {'Content-Type':'application/json'}
        print(service.get_logs())
        test_data = json.dumps({'data': 'Today is a great day!'})

        # Call the web service, passing the input data (the web service will also accept the data in binary format)
        predictions = service.run(input_data = test_data)

        # Get the predicted class - it'll be the first (and only) one.
        predicted_classes = json.loads(predictions)
        print(predicted_classes[0])

        #response = requests.post(scoring_uri, data=test_data, headers=headers)
        #print(response.status_code)
        #print(response.elapsed)
        #print(response.json())
class AllConstants:
    BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=humlstorage;AccountKey=InGUfK++98C0tANJqmP3AbV5tTMpDj+5XikesQpjYWSH1MYxAspw5sbmfMcmMPgBGpYHVGuGtuEuGAICu3zFlw==;EndpointSuffix=core.windows.net"
    EXPERIMENT_NAME = "huml_experiment"
    MODEL_NAME = "huml_model"
    #PIPELINE_NAME = "huml_pipeline"
    PIPELINE_NAME = "huml_pipeline"
    SERVICE_NAME = "huml-svc"
    EXPERIMENT_SAMPLING_NAME = "huml-sampling-experiment"
    PIPELINE_SAMPLING = "huml_sampling_pipeline"
    SCHEDULER_CURRENT_ANNOTATED_DATA = "scheduler_current_annotated_data"
    CURRENT_ANNOTATED_DATA_PATH = "annotated_data/current"

class LogicAppPipelineConfigManager:
    def __init__(self, config):
        """Initializing class with the config object.
            
        Arguments:
            config {object} -- Object containing all the information in the yaml configuration file
        """

        # BlobStorageManager object is created from the connectionstring coming from config object.
        self.blobManager = BlobStorageManager(config.BLOB_STORAGE_CONNECTION_STRING)
        # declaration of file name that will contain the endpoint that has just been published.
        self.REMOTE_FILE_NAME = "published_pipeline.json"
        # declaration of container (or folder) which will contain the json file
        self.BLOB_CONTAINER = "{0}/configs".format(config.CONTAINER_NAME)
        #http link where the json file will be deposited
        self.file_url = "https://humlstorage.blob.core.windows.net/{0}/{1}".format(self.BLOB_CONTAINER,self.REMOTE_FILE_NAME)
    
    def update(self, pipelineid, pipeline_endpoint):
        """ Create or update json file of the pipeline in the blob storage

        Arguments:
            pipelineid {str} -- pipeline id published
            pipeline_endpoint {str} --endpoint : http address through which the pipeline can be called
        """
            
        data = self.blobManager.download_json_by_url(self.file_url)

        data["pipelineid"] = pipelineid
        data["published_pipeline_endpoint"] = pipeline_endpoint

        temp = "./temp"
        FolderUtilities.make_dir(temp)

        temp_file = os.path.join(temp, self.REMOTE_FILE_NAME)

        with open(temp_file, 'w') as outfile:
            json.dump(data, outfile)

        print("update remote file")
        self.blobManager.upload(self.BLOB_CONTAINER, temp_file, overwrite_v = True)

        shutil.rmtree(temp_file, ignore_errors=True)

class FilesProviders:
    @staticmethod
    def get_path_files(root, exclude_files=[]):
        """[summary]

        Arguments:
            root {[type]} -- [description]

        Keyword Arguments:
            exclude_files {list} -- [description] (default: {[]})

        Returns:
            [type] -- [description]
        """
        result = []
        for root, _, files in os.walk(root):
            for filename in files:
                filepath = join(root, filename)
                dirname = os.path.basename(filepath)
                if dirname in exclude_files:
                    continue
                if filename in exclude_files:
                    continue
                result.append(filepath)

        return result

class WorkspaceProvider:
    def __init__(self, config):
        """Initializing WorkspaceProvider's class from config object

        Arguments:
            config {object} -- Object containing all the invalidations of the yaml config file
        """
        self.config = config
    
    def get_ws(self):
        """Creates the Workspace (ws) using information from config object.

        Returns:
            Workspace -- Defines an Azure Machine Learning resource for managing training and deployment artifacts.
        """
        print("tenant_id:", self.config.SPA_TENANTID)
        print("service_principal_id:", self.config.SPA_APPLICATIONID)
        print("service_principal_password:", self.config.SPA_PASSWORD)
        print("subscription_id:", self.config.SPA_TENANTID)
        print("service_principal_id:", self.config.SPA_APPLICATIONID)
        print("service_principal_password:", self.config.SPA_PASSWORD)
        svc_pr = ServicePrincipalAuthentication(
                            tenant_id=self.config.SPA_TENANTID,
                            service_principal_id=self.config.SPA_APPLICATIONID,
                            service_principal_password=self.config.SPA_PASSWORD)

        
        ws = Workspace(subscription_id=self.config.SUBSCRIPTION_VALUE,
                            resource_group=self.config.RESOURCEGROUP,
                            workspace_name=self.config.WORKSPACENAME,
                            auth=svc_pr
                )
        return ws, svc_pr

class DataTransformer:
    @staticmethod
    def arr_to_dataframe(array, cols, index_col):
        """Transformation of an array to a dataframe

        Arguments:
            array {array} -- array containing the data to be transformed
            cols {array} -- names of the columns that must be in the dataframe
            index_col {str} -- column that will represent the dataframe index

        Returns:
            DataFrame -- pandas's dataframe contain data
        """
        arr = np.array(array)
        
        df = pd.DataFrame(data=arr, columns=cols)
        df = df.set_index(index_col)
        return df

class PlotUtilities:
    @staticmethod
    def plot_distributed_data(df, col):
        """Plot distribution of data from a column having discrete data

        Arguments:
            df {dataframe} -- dataframe having the data
            col {str} -- column with discrete values used

        Returns:
            plot -- plot fig
        """
        plt.clf()
        dist = df.groupby([col]).size()
        dist = dist / dist.sum()
        fig, _ = plt.subplots(figsize=(12,8))
        sns.barplot(dist.keys(), dist.values)
        return fig
    
    @staticmethod
    def _get_confusion_matrix_plot(cm):
        """plot confusion matrix

        Arguments:
            cm {array} -- array that contains the data of confusion matrix

        Returns:
            plot -- plot fig
        """
        plt.clf()
        plt.imshow(cm, interpolation='nearest', cmap = plt.cm.Wistia) # pylint: disable=no-member
        classNames = ['Positive', 'Negative']
        plt.title('Confusion Matrix')
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        tick_marks = np.arange(len(classNames))
        plt.xticks(tick_marks, classNames, rotation=45)
        plt.yticks(tick_marks, classNames)

        plt.text(0, 0, 'TP' + " = " + str(cm[0][0]))
        plt.text(1, 0, 'FP' + " = " + str(cm[0][1]))
        plt.text(0, 1, 'FN' + " = " + str(cm[1][0]))
        plt.text(1, 1, 'TN' + " = " + str(cm[1][1]))

        return plt

class AzureMLLogsProvider:
    def __init__(self, run):
        self.run = run
    
    def get_log_from_brother_run(self, script_name, log_name):
        if not self.run.parent :
            raise Exception("this run has not parent")
        
        log_value = None
        
        for brother_run in self.run.parent.get_children():
            if brother_run.get_details()["runDefinition"]["script"] != script_name:
                continue
            run_metrics = brother_run.get_metrics()
            
            if log_name in run_metrics:
                log_value = run_metrics[log_name]
                print("log_value :", log_value)

        return  log_value
    
    def get_tag_from_brother_run(self, script_name, tag_name):
        if not self.run.parent :
            raise Exception("this run has not parent")

        tag_value = None
        for brother_run in self.run.parent.get_children():
            if brother_run.get_details()["runDefinition"]["script"] != script_name:
                continue
            run_tags = brother_run.get_tags()
            
            if tag_name in run_tags:
                tag_value = run_tags[tag_name]
                print("tag_value :", tag_value)

        #check if bool
        if (tag_value == "True"):
            tag_value = True
        elif (tag_value == "False"):
            tag_value = False

        return  tag_value

class FeaturesHandler:
    """
    FeaturesHandler's role is to create a large dictionary containing 
    the words and their number of occurrences (Bag-of-words). 
    It is this dictionary that we will use as features. 
    """
    def create_features(self,unlabeled_data, minword = 3):
        """This method allows to create the Bag-of-words which will be used as Features
        
            Arguments:
                unlabeled_data {str} -- variable that contains unlabeled data
                minword {int} -- minimum number of occurrences per word of bag-of-words
            
            returns:
                feature_index {int} -- variable that contains Bag-of-words for all data (unlabeled + traning)
        """
        feature_index = {}

        if (unlabeled_data is None) | (unlabeled_data is "") :
            raise Exception("unlabeled data cannot be empty") 

        total_training_words = {}
        for item in unlabeled_data:
            text = item[1]
            for word in text.split():
                if word not in total_training_words:
                    total_training_words[word] = 1
                else:
                    total_training_words[word] += 1

        for item in unlabeled_data:
            text = item[1]
            for word in text.split():
                if word not in feature_index and total_training_words[word] >= minword:
                    feature_index[word] = len(feature_index)

        return feature_index
    
    def make_feature_vector(self, features, feature_index):
        """[summary]
            This method allows to create one-hot vector from list of words
        
            Arguments:
                features {str} -- list of words 
                feature_index {str} -- bag-of-words from all data (unlabeled + traning)
            
            returns:
                 {pytorch.view} -- one-hot vector
        """
        vec = torch.zeros(len(feature_index)) # pylint: disable=no-member 
        for feature in features:
            if feature in feature_index:
                vec[feature_index[feature]] += 1
        return vec.view(1, -1)

class DataCorresponder:
    def __init__(self, all_data_vec):
        self.all_data_vec = all_data_vec

    def get_vec_correspondence(self, data_text):
        if not data_text :
            raise Exception("data_text cannot be empty")
        
        X_all_data, _, id_all_data = self.all_data_vec
        X_data = []
        y_data = []
        id_data = []
        for item in data_text:
            id = int(item[0])
            if len(item) > 2:
                item[2] = item[2].replace(" '","")
                label = item[2]
            for feature_vec, x_id in zip(X_all_data,id_all_data):
                if id == x_id:
                    X_data.append(feature_vec)
                    y_data.append(label)
                    id_data.append(int(id))
                    break
        
        return X_data, y_data, id_data

class DataAdapter:
    def __init__(self):
        self.featuresHandler = FeaturesHandler()

    def adapt(self, data, features_index):
        if not data:
            raise Exception("data cannot be empty")

        if not features_index:
            raise Exception("features_index cannot be empty")

        X = [] #initialize X
        y = [] #initialize y (target)
        ids = [] #initialize id for identification

        for item in data:
            id = item[0]
            features = item[1].split()
            label = "_"
            if len(item) > 2:
                item[2] = item[2].replace(" '","")
                label = item[2]
            
            feature_vec = self.featuresHandler.make_feature_vector(features,features_index)
            X.append(feature_vec)
            y.append(label)
            ids.append(int(id))

        return X, y, ids

class ConfigProvider:
    def __init__(self, config_path):
        self.config_path = config_path

    def _load_data(self):
        with open(self.config_path) as stream:
            data = yaml.safe_load(stream)
        return data
    
    def load(self):
        data = self._load_data()

        self.AML_COMPUTE_CLUSTER_NAME = data["Azure"]["AmlCompute"]["ClusterName"]
        self.AML_COMPUTE_CLUSTER_MIN_NODES = data["Azure"]["AmlCompute"]["ClusterMinNode"]
        self.AML_COMPUTE_CLUSTER_MAX_NODES = data["Azure"]["AmlCompute"]["ClusterMaxNode"]
        self.AML_COMPUTE_CLUSTER_VM_TYPE = data["Azure"]["AmlCompute"]["ClusterType"]
        self.IDLE_SECONDS_BEFORE_SCALEDOWN = data["Azure"]["AmlCompute"]["IdleSecondes_Before_Scaledown"]

        #StorageAccount
        self.BLOB_DATASTORE_NAME = data["Azure"]["StorageAccount"]["BlobDatastoreName"]
        self.ACCOUNT_NAME = data["Azure"]["StorageAccount"]["AccountName"]
        self.CONTAINER_NAME = data["Azure"]["StorageAccount"]["ContainerName"]
        self.ACCOUNT_KEY = data["Azure"]["StorageAccount"]["AccountKey"]
        self.BLOB_STORAGE_CONNECTION_STRING = data["Azure"]["StorageAccount"]["BlobStorageConnectionString"]
        #Azureml
        self.LOCATION = data["Azure"]["Azureml"]["Location"]
        self.RESOURCEGROUP = data["Azure"]["Azureml"]["ResourceGroup"]
        self.WORKSPACENAME = data["Azure"]["Azureml"]["WorkspaceName"]


        #ExperimentName
        #self.EXPERIMENT_NAME = data["Azure"]["Azureml"]["Experiment"]["Name"]
        
        self.EXPERIMENT_DS_NAME = data["Azure"]["Azureml"]["Experiments"]["DataScience"]["Name"]
        self.EXPERIMENT_SAMPLING_NAME = data["Azure"]["Azureml"]["Experiments"]["Sampling"]["Name"]
        
        #self.PIPELINE_NAME = data["Azure"]["Azureml"]["Pipeline"]["Name"]

        self.PIPELINE_DS_NAME = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["Name"]
        self.PIPELINE_DS_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["EndPoint"]
        self.PIPELINE_SAMPLING_NAME = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["Name"]
        self.PIPELINE_SAMPLING_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["EndPoint"]
        #Model
        self.MODEL_NAME = data["Azure"]["Azureml"]["Model"]["Name"]

        #ServicePrincipalAuthentication
        self.SPA_TENANTID = data["Azure"]["ServicePrincipalAuthentication"]["TenantId"]
        self.SPA_APPLICATIONID = data["Azure"]["ServicePrincipalAuthentication"]["ApplicationId"]
        self.SPA_PASSWORD = data["Azure"]["ServicePrincipalAuthentication"]["Password"]

        #Subscriptions
        self.SUBSCRIPTION_VALUE = data["Azure"]["Subscriptions"]["Value"]
        #self.SUBSCRIPTION_ENTERPRISE = data["Azure"]["Subscriptions"]["Enterprise"]
        #self.SUBSCRIPTION_PROFESSIONAL = data["Azure"]["Subscriptions"]["Professional"]

class ConfigGenerator:
    def __init__(self, config_template_file):
        """initializing class with path to the template of config file

        Arguments:
            config_template_file {str} -- path that points to template of the config file
        """
        self.config_template_file = config_template_file

    def by_file(self, config_value_file, confile_fle):
        """[summary]

        Arguments:
            config_value_file {str} -- path that contains file where there are values to replace in the template
            confile_fle {str} -- new config file to be created
        """
        config_template = open(self.config_template_file, "rt").read()
        with open(config_value_file) as fp:
            for line in fp:
                arr = line.split(":")
                config_template = config_template.replace(arr[0].strip(),arr[1].strip())

        with open(confile_fle,'w') as f:
            f.write(config_template)        

    def _keys_from_template(self):
        """returns keys found in the template file ex: azure.amlcompute.clustername

        Returns:
            array -- list of retrieved keys
        """
        keys = []
        with open(self.config_template_file) as fp:
            for line in fp:
                if ":" not in line:
                    continue
                if "{{" in line:
                    arr = line.split(":")
                    key = arr[1].strip()
                    key = key.replace("{{","").replace("}}", "").replace(".", "_")
                    keys.append(key)
        
        return keys

    def _create_config_values(self,args):
        """creation of dictionary containing keys and values for conf file

        Arguments:
            args {array} -- which contains arguments passed in parameters

        Returns:
            {dict} -- contains information that will be in yaml config file.
        """
        config_values = {}
        last_value = 0
        for index, value in enumerate(args):
            if index == 0:
                continue
            if index % 2 != 0:
                last_value = value
            else:
                if value.isnumeric():
                    config_values[last_value] = value
                else:
                    config_values[last_value] = '"' + value + '"'
        
        return config_values

    def _valide_config_values(self,args):
        """ validate information format for new config file

        Arguments:
            args {dict} -- contains information that will be in yaml config file

        Raises:
            TypeError: [description]
            Exception: [description]
            Exception: [description]
        """

        for key in args.keys():

            if "-" not in key:
                raise TypeError("{0} argname must be preceded by '-'".format(key))
        
        key_templates = self._keys_from_template()

        if len(key_templates) != len(args.keys()):
            raise Exception("number of arguments are not sufficient ({0}). {1} are needed. Refer to the config.template.yaml file".format(len(args.keys()), len(key_templates)))
    
        for key in args.keys():
            key = key.replace("-","")
            if key not in key_templates:
                raise Exception("{0} is not a supported key. Refer to the config.template.yaml file".format(key))

    def by_args(self, args, confile_fle):
        """ Generates config file by the arguments passed in parameters 

        Arguments:
            args {array} -- arguments passed in parameters 
            confile_fle {[type]} -- new config file to be created
        """

        config_values = self._create_config_values(args)

        self._valide_config_values(config_values)

        config_template = open(self.config_template_file, "rt").read()

        for key,value in config_values.items():
            key = key.replace("_", ".").replace("-","")
            config_template = config_template.replace("{{" + key + "}}",  value)

        with open(confile_fle,'w') as f:
            f.write(config_template)

class ConfigHandler:
    def get_file(self,config_path):
        """Loading config object to be used in the entire program

        Arguments:
            config_path {str} -- generated config file path

        Returns:
            ConfigProvider -- Object containing all the information in the config file
        """
        config = ConfigProvider(config_path)
        config.load()
        return config

    def generate(self, config_template, config_path):
        configGen = ConfigGenerator(config_template)

        # If it run locally, then we're going to use the config.values.txt 
        # file containing all the necessary information
        if len(sys.argv) == 1:
            configGen.by_file("../../config.values.txt",config_path)
        # If it's launched via DevOps, then the values will be pass as params
        else:
            configGen.by_args(sys.argv, config_path)