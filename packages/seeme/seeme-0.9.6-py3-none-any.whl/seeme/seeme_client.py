import os
import json
import requests
import http
import zipfile
from requests_toolbelt.multipart.encoder import MultipartEncoder

REGISTER_ENDPOINT = 'register'
LOGIN_ENDPOINT = 'login'
MODELS_ENDPOINT = 'models'
TRAINING_REQUESTS_ENDPOINT = 'trainingrequests'
INFERENCE_ENDPOINT = 'inferences'
DETECTION_ENDPOINT = 'detections'
DATASETS_ENDPOINT = 'datasets'
DATASET_VERSIONS_ENDPOINT = 'versions'
LABELS_ENDPOINT = 'labels'
NLP_CLASSIFICATION_ENDPOINT = 'nlpclassification'
APPLICATIONS_ENDPOINT = 'applications'

ID = "id"

class Client():
  def __init__(self, username:str=None, apikey:str=None, backend:str="https://api.seeme.ai/api/v1/"):
    self.backend = backend
    self.headers = {}
    self.update_auth_header(username, apikey)
    self.endpoints = {
      REGISTER_ENDPOINT: self.crud_endpoint(REGISTER_ENDPOINT),
      LOGIN_ENDPOINT: self.crud_endpoint(LOGIN_ENDPOINT),
      MODELS_ENDPOINT: self.crud_endpoint(MODELS_ENDPOINT),
      TRAINING_REQUESTS_ENDPOINT: self.crud_endpoint(TRAINING_REQUESTS_ENDPOINT),
      INFERENCE_ENDPOINT: self.crud_endpoint(INFERENCE_ENDPOINT),
      DETECTION_ENDPOINT: self.crud_endpoint(DETECTION_ENDPOINT),
      NLP_CLASSIFICATION_ENDPOINT: self.crud_endpoint(NLP_CLASSIFICATION_ENDPOINT),
      DATASETS_ENDPOINT: self.crud_endpoint(DATASETS_ENDPOINT),
      APPLICATIONS_ENDPOINT: self.crud_endpoint(APPLICATIONS_ENDPOINT)
    }
    self.applications = []

  # -- Login / Registration --

  def register(self, username:str, email:str, password:str, firstname:str, name:str):
    register_api = self.endpoints[REGISTER_ENDPOINT]
    register_data = {
      'username': username,
      'email': email,
      'password': password,
      'firstname': firstname,
      'name': name,
    }

    r = requests.post(register_api, data=json.dumps(register_data), headers=self.headers)

    registered_user = r.json()

    if "message" in registered_user:
      raise ValueError(registered_user["message"])
    
    return registered_user

  def login(self, username:str, password:str):
    login_api = self.endpoints[LOGIN_ENDPOINT]
    login_data = {
      'username': username,
      'password': password
    }
    
    logged_in = self.api_post(login_api, login_data)

    self.update_auth_header(logged_in["username"], logged_in["apikey"])

    applications_api = self.endpoints[APPLICATIONS_ENDPOINT]
    self.applications =  self.api_get(applications_api)

    return logged_in
      
  def logout(self):
    self.update_auth_header("", "")
    
  # -- CRUD models --

  def get_models(self):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT]

    return self.api_get(model_api)

  def create_model(self, model):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT]

    return self.api_post(model_api, model)

  # obsolete
  def create_full_model(self, model):
    return self.create_model(model)
    
  def get_application_id(self, base_framework="pytorch", framework="fastai", base_framework_version="1.6.0", framework_version="2.0.9", application="image_classification"):
    if self.applications == []:
      self.applications = self.get_applications()

    for f in self.applications:
      if f["base_framework"] == base_framework \
        and f["framework"] == framework \
        and f["base_framework_version"] == base_framework_version \
        and f["framework_version"] == framework_version \
        and f["application"] == application:
          return f["id"]
    
    for f in self.applications:
      if f["base_framework"] == base_framework \
        and f["framework"] == framework \
        and f["base_framework_version"] in base_framework_version \
        and f["framework_version"] == framework_version \
        and f["application"] == application:
          return f["id"]
      
    raise NotImplementedError()

  def get_model(self, model_id:str):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id

    return self.api_get(model_api)

  def update_model(self, model):
    self.requires_login()

    assert model
    assert model[ID]
    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model[ID]
    return self.api_put(model_api, model)

  def delete_model(self, id:str):
    self.requires_login()
    delete_api = self.endpoints[MODELS_ENDPOINT] + "/" + id

    return self.api_delete(delete_api)

  def upload_model(self, model_id:str, folder:str="data", filename:str="export.pkl"):
    return self.upload(model_id, folder, filename, 'application/octet-stream')
  
  def upload_logo(self, model_id:str, folder:str="data", filename:str="logo.jpg"):
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"

    return self.upload(model_id, folder, filename,  content_type)
  
  def get_logo(self, model):
    logo_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model["id"] + "/download/logo"
    return self.api_download(logo_endpoint, model["logo"])

  def get_mlmodel(self, model):
    mlmodel_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model["id"] + "/download/mlmodel"
    return self.api_download(mlmodel_endpoint, model["id"]+".mlmodel")

  def upload(self, model_id:str, folder:str, filename:str, content_type:str):
    self.requires_login()

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    data = MultipartEncoder(
                fields={
                    'file': (filename, open(folder + "/" + filename, 'rb'), content_type)}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(model_upload_api, data=data, headers=content_headers)

  def upload_detection_model(self, model_id:str, folder:str="data", filename:str="export.pkl"):
    self.requires_login()

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    data = MultipartEncoder(
                fields={
                    'file': ('filename', open(folder + "/" + filename, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(model_upload_api, data=data, headers=content_headers)

  # -- CRUD requests --

  def get_training_requests(self):
    self.requires_login()

    training_requests_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT]

    return self.api_get(training_requests_api)
  
  def create_training_request(self, version):
    self.requires_login()

    req_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT]
    req_data = {
      'dataset_id': version["dataset_id"],
      'dataset_version_id': version["id"]
    }

    return self.api_post(req_api, req_data)

  def update_training_request(self, training_request):
    self.requires_login()

    assert training_request
    assert training_request[ID]
    training_request_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT] + "/" + training_request[ID]
    return self.api_put(training_request_api, training_request)

  def delete_training_request(self, id:str):
    self.requires_login()
    delete_api = self.endpoints[TRAINING_REQUESTS_ENDPOINT] + "/" + id

    return self.api_delete(delete_api)

  # -- CRUD Inference --

  def inference(self, model_id:str, file:str):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + model_id

    data = MultipartEncoder(
                fields={
                    'file': ('filename', open(file, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(inference_api, data=data, headers=content_headers)
  
  def update_inference(self, inference):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + inference["id"]

    return self.api_put(inference_api, inference)

  # -- CRUD Detection --

  def detect(self, model_id:str, file:str):
    self.requires_login()

    detection_api = self.endpoints[DETECTION_ENDPOINT] + "/" + model_id

    data = MultipartEncoder(
                fields={
                    'file': (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(detection_api, data=data, headers=content_headers)

  # -- CRUD Nlp Classification

  def nlpclassification(self, model_id:str, input_text:str):
    self.requires_login()

    nlp_api = self.endpoints[NLP_CLASSIFICATION_ENDPOINT] + "/" + model_id

    req_data = {
      'input_text': input_text
    }

    return self.api_post(nlp_api, req_data)

  # -- CRUD applicationS --
  def get_applications(self):
    self.requires_login()

    application_api = self.endpoints[APPLICATIONS_ENDPOINT]

    return self.api_get(application_api)
  
  def create_application(self, application):
    self.requires_login()

    application_api = self.endpoints[APPLICATIONS_ENDPOINT]

    return self.api_post(application_api, application)

  # -- CRUD DATASETS --

  def get_datasets(self):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]

    return self.api_get(dataset_api)

  def create_dataset(self, dataset):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]

    return self.api_post(dataset_api, dataset)

  def get_dataset(self, dataset_id:str):
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset_id

    return self.api_get(dataset_api)

  def update_dataset(self, dataset):
    self.requires_login()

    assert dataset
    assert dataset[ID]
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset[ID]
    return self.api_put(dataset_api, dataset)

  def delete_dataset(self, id:str):
    self.requires_login()
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + id

    return self.api_delete(dataset_api)

  def create_dataset_version(self, dataset_id, dataset_version):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}"

    return self.api_post(dataset_version_api, dataset_version)

  def get_dataset_versions(self, dataset_id):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}"

    return self.api_get(dataset_version_api)
  
  def get_dataset_version(self, dataset_id, version_id):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}"

    return self.api_get(dataset_version_api)

  def update_dataset_version(self, dataset_id, dataset_version):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{dataset_version['id']}"

    return self.api_put(dataset_version_api, dataset_version)

  def delete_dataset_version(self, dataset_id, dataset_version):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{dataset_version['id']}"

    return self.api_delete(dataset_version_api)
  
  def create_label(self, dataset_id, version_id, label):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/labels"

    return self.api_post(labels_api, label)

  def get_labels(self, dataset_id, version_id):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/labels"

    return self.api_get(labels_api)
  
  def get_label(self, dataset_id, version_id, label_id):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/labels/{label_id}"

    return self.api_get(labels_api)

  def update_label(self,  dataset_id, version_id, label):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/labels/{label['id']}"

    return self.api_put(labels_api, label)

  def delete_label(self, dataset_id, version_id, label):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/labels/{label['id']}"

    return self.api_delete(labels_api)
  
  def create_split(self, dataset_id, version_id, split):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/splits"

    return self.api_post(splits_api, split)

  def get_splits(self, dataset_id, version_id):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/splits"

    return self.api_get(splits_api)
  
  def get_split(self, dataset_id, version_id, split_id):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/splits/{split_id}"

    return self.api_get(splits_api)

  def update_split(self,  dataset_id, version_id, split):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/splits/{split['id']}"

    return self.api_put(splits_api, split)

  def delete_split(self, dataset_id, version_id, split):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/splits/{split['id']}"

    return self.api_delete(splits_api)

  def create_item(self, dataset_id, version_id, item):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items"

    return self.api_post(items_api, item)

  def get_items(self, dataset_id, version_id, params=None):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items"

    return self.api_get(items_api, params=params)
  
  def get_item(self, dataset_id, version_id, item_id):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items/{item_id}"

    return self.api_get(items_api)

  def update_item(self,  dataset_id, version_id, item):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items/{item['id']}"

    return self.api_put(items_api, item)

  def delete_item(self, dataset_id, version_id, item):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items/{item['id']}"

    return self.api_delete(items_api)

  def upload_item_image(self, dataset_id, version_id, item_id, folder, filename):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items/{item_id}/upload"
    
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"
    else:
      print("Image type not supported")
      return

    data = MultipartEncoder(
                fields={
                    'file': (filename, open(folder + "/" + filename, 'rb'), content_type)}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(items_api, data=data, headers=content_headers)

  def download_item_image(self, dataset_id, version_id, item_id, download_location):
    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/items/{item_id}/download"
  
    return self.api_download(items_api, download_location)
  
  def download_dataset(self, dataset_id, version_id, extract_to_dir="data", download_file="dataset.zip", remove_download_file= True):
    dataset_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{DATASET_VERSIONS_ENDPOINT}/{version_id}/download"

    self.api_download(dataset_api, download_file)

    with zipfile.ZipFile(download_file, 'r') as zip_ref:
      zip_ref.extractall(extract_to_dir)
    
    if remove_download_file:
      os.remove(download_file)

  # Convenience methods

  def get_apikey(self):
    return self.apikey

  # Helpers

  def requires_login(self):
    if not self.is_logged_in():
      raise Exception("You need to be logged in for this.")

  def update_auth_header(self, username:str=None, apikey:str=None):
    if username == None or apikey == None:
      return

    self.apikey = apikey
    
    self.headers = {
      "Authorization": f"{username}:{apikey}"
    }
  
  def is_logged_in(self):
    if "Authorization" in self.headers:
      return True

    return False

  def crud_endpoint(self, endpoint:str):
    return f"{self.backend}{endpoint}"

  ## CRUD API methods

  def api_get(self, api:str, params=None):
    r = requests.get(api, headers=self.headers, params=params)

    return r.json()

  def api_post(self, api:str, data):
    data = json.dumps(data)

    r = requests.post(api, data=data, headers=self.headers)
    
    return r.json()
  
  def api_upload(self, api:str, data, headers):
    r = requests.post(api, data=data, headers=headers)
    
    return r.json()
  
  def api_put(self, api:str, data):
    data = json.dumps(data)

    r = requests.put(api, data=data, headers=self.headers)

    return r.json()
  
  def api_delete(self, api:str):
    r = requests.delete(api, headers=self.headers)

    return r.json()

  def api_download(self, api:str, filename:str):
    r = requests.get(api, allow_redirects=True, headers=self.headers)

    open(filename, "wb").write(r.content)