import time
import codecs
import json
import base64
import requests
# from .logger import Logger


class API:
    _host = ""
    _access_token = ""
    _api_version = "1.0"
    _authenticated = False
    _logger = None

    def __init__(self, host: str = "https//api.antcde.io/"):
        self._host = host

    def login(self, client_id: str, client_secret: str, username: str, password: str) -> bool:
        """ Login into ANT"""
        self._authenticated = False
        response = self._make_request('/oauth/token', 'POST', {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret
        })
        parsed_response = response.json()
        if 'access_token' not in parsed_response:
            raise SystemError("Please check credentials")
        self._access_token = parsed_response['access_token']
        self._authenticated = True
        return True

    def _make_api_request(self, path: str, method: str,
                          parameters: dict = None, delete_data: dict = None) -> dict:
        parameters = {} if parameters is None else parameters
        if not self._authenticated:
            raise SystemError("You are not authenticated, please use login first.")

        data = parameters if method in ['GET', 'DELETE'] else json.dumps(
            parameters)
        url = 'api/{}/{}'.format(self._api_version, path)
        response = self._make_request(
            url,
            method,
            data,
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(
                    self._access_token)
            }, 
            delete_data)
            
        # print(response.text)

        if response.text == '':
            print("response was empty")
            return ''
        # print(response.text)
        parsed_response = response.json()
        if 'message' in parsed_response:
            if parsed_response['message'] == 'Unauthenticated.':
                raise PermissionError('Unauthenticated')
            if parsed_response['message'] == "Too Many Attempts.":
                raise ProcessLookupError("Too many requests attempted")
        return parsed_response

    def _make_request(self, path: str, method: str, parameters: dict = None,
                      headers: dict = None, data: dict = None) -> requests.Response:
        parameters = {} if parameters is None else parameters
        headers = {} if headers is None else headers
        url = '{}{}'.format(self._host, path)
        if method == 'GET':
            return requests.get(
                url, params=parameters, headers=headers, verify=True)
        if method == 'PUT':
            return requests.put(
                url, data=parameters, headers=headers, verify=True)
        if method == 'DELETE':
            return requests.delete(
                url, data=data, params=parameters, headers=headers, verify=True)
        if method == 'POST':
            return requests.post(
                url, data=parameters, headers=headers, verify=True)
        raise NotImplementedError("http method not implemented")

    def projects_read(self) -> [dict]:
        """ List all your projects"""
        path = 'projects'
        return self._make_api_request(path, 'GET')

    def project_create(self,licenseid: str, name: str, number:str = '', description:str = '', imageName:str = '', imageExtension:str = '', imageData:str = '') -> dict:
        """ Create a new project """
        path = 'project'
        if(imageExtension == ''):
            project = {
                "name": name,
                "number": number,
                "description": description,
                "license": licenseid,
            }
        else:
            project = {
            "name": name,
            "number": number,
            "description": description,
            "license": licenseid,
            "image": {
                "name": imageName,
                "extension": imageExtension,
                "data": imageData
            }
        }
        return self._make_api_request(path, 'POST', project)

    def project_read(self, project_id: str) -> dict:
        """ Get project details """
        path = 'project/{}'.format(project_id)
        return self._make_api_request(path, 'GET')

    def project_Update(self, project_id: str, name: str) -> dict:
        """ Get project update """
        path = 'project/{}'.format(project_id)
        return self._make_api_request(path, 'PUT', {
            "name": name
        })

    def project_delete(self, project_id: str) -> dict:
        """ Get project delete """
        path = 'project/{}'.format(project_id)
        return self._make_api_request(path, 'DELETE')

    def tables_read(self, project_id: str) -> [dict]:
        """ Get tables in a project """
        path = 'tables'
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id
        })

    def table_create(self, project_id: str, name: str) -> dict:
        """ Create a table in a project """
        path = 'table'
        return self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "name": name
        })

    def table_read(self, project_id: str, table_id: str) -> dict:
        """ Get details of a table in a project """
        path = 'table/{}'.format(table_id)
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id
        })

    def table_update(self, project_id: str, table_id: str, name: str) -> dict:
        """ Update a table in a project """
        path = 'table/{}'.format(table_id)
        return self._make_api_request(path, 'PUT', {
            "project": {"id": project_id},
            "name": name
        })

    def table_delete(self, project_id: str, table_id: str) -> dict:
        """ Delete a table in a project """
        path = 'table/{}'.format(table_id)
        return self._make_api_request(path, 'DELETE', {
            "project[id]": project_id
        })

    def columns_read(self, project_id: str, table_id: str) -> [dict]:
        """ Get all columns in a table """
        path = 'columns'
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def column_create(self, project_id: str, table_id: str, name: str,
                      fieldType: str, defaultValue: str = "",
                      options: list = None, required: bool = True, ordinal: int = "") -> dict:
        """ Create a column in a table """
        options = [] if options is None else options
        path = 'column'
        return self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "name": name,
            "type": fieldType,
            "options": options,
            "default": defaultValue,
            "required": required,
            "ordinal": ordinal
        })

    def column_read(self, project_id: str, table_id: str, column_id):
        """ Get details for a specific column in a table """
        path = 'column/{}'.format(column_id)
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def column_update(self, project_id: str, table_id: str, column_id: str,
                      name: str, defaultValue: str = "",
                      options: list = None, required: bool = True, ordinal: int = 0) -> dict:
        """ Update details for a specific column in a table """
        path = 'column/{}'.format(column_id)
        return self._make_api_request(path, 'PUT', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "name": name,
            "required": required,
            "options": options,
            "default": defaultValue,
            "ordinal": ordinal
        })

    def column_delete(self,
                      project_id: str, table_id: str, column_id: str) -> dict:
        path = 'column/{}'.format(column_id)
        """ Delete column in a table """
        return self._make_api_request(path, 'DELETE', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def records_create_csv(self, project_id: str, table_id: str,
                       records_csv: str) -> [dict]:
        """ Import a csv file into a table """
        path = 'records/import'
        with codecs.open(records_csv, mode="r", encoding='utf-8') as csv_file:
            encoded_csv = base64.b64encode(str.encode(csv_file.read()))
        result = self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "records": encoded_csv.decode("utf-8")
        })
        return result

    def records_create(self, project_id: str, table_id: str,
                       records: list) -> [dict]:
        """ Create multiple records into a table """
        path = 'records/import'
        encoded_csv = base64.b64encode(self.create_virtual_csv(records).encode("utf-8"))
        result = self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "records": encoded_csv.decode("utf-8")
        })
        return result

    def records_read(self, project_id: str, table_id: str, limit: int = 0, offset: int = 0) -> dict:
        """ Get reords of table """
        path = 'records'
        record_data = self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id,
            "filter[limit]": limit,
            "filter[offset]":offset,
        })
        return record_data["records"]

    def records_delete(self, project_id: str, table_id: str,
                       records_ids: [str]) -> dict:
        """ Delete records in table """
        path = 'records'
        data = {
            "project":{
                "id": project_id
            },
            "table": {
                "id": table_id
            },
            "records": records_ids
        }
        return self._make_api_request(path, 'DELETE', data)

    def records_verify_csv(self, project_id: str, table_id: str, records_csv: str) -> dict:
        """ Verify structure of CSV file against a table """
        path = 'records/verify'
        with codecs.open(records_csv, mode="r", encoding='utf-8') as csv_file:
            encoded_csv = base64.b64encode(str.encode(csv_file.read()))
        result = self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "records": encoded_csv.decode("utf-8")
        })
        return result

    def records_verify(self, project_id: str, table_id: str, records: list) -> dict:
        """ Verify structure of records against a table """
        path = 'records/verify'
        encoded_csv = base64.b64encode(self.create_virtual_csv(records).encode("utf-8"))
        result = self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "records": encoded_csv.decode("utf-8")
        })
        return result

    def record_create(self, project_id: str, table_id: str,
                      record_values: dict) -> dict:
        """ Create a single record into a table """           
        path = 'record'
        return self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": record_values
        })

    def record_read(self, project_id: str, table_id: str,
                    record_id: str) -> dict:
        """ Read a specific record of a table """
        path = 'record/{}'.format(record_id)
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def record_update(self, project_id: str, table_id: str, record_id: str,
                      updated_record_values: dict) -> dict:
        """ Update a specific record of a table """
        path = 'record/{}'.format(record_id)
        return self._make_api_request(path, 'PUT', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": updated_record_values
        })

    def record_delete(self, project_id: str, table_id: str,
                      record_id: str) -> dict:
        """ Delete a specific record of a table """
        path = 'record/{}'.format(record_id)
        return self._make_api_request(path, 'DELETE', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def record_history(self, project_id: str, table_id: str,
                       record_id: str) -> dict:
        """ Get change record history a specific record of a table """
        path = 'record/{}'.format(record_id)
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def revisions_read(self, project_id: str, table_id: str) -> dict:
        """ Get all revisions of a table """
        path = 'revisions'
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def revision_create(self, project_id: str, table_id: str,
                        name: str) -> dict:
        """ Create a new revisions for a table """
        path = 'revision'
        return self._make_api_request(path, 'POST', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "name": name,
            "timestamp": time.time()
        })

    def revision_read(self, project_id  : str, table_id: str,
                      revision_id: str) -> dict:
        """ Get details of a revisions for a table """
        path = 'revision/{}'.format(revision_id)
        return self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            
            "table[id]": table_id
        })

    def revision_update(self, project_id: str, table_id: str,
                        revision_id: str, name: str) -> dict:
        """ Update a revision for a table """
        path = 'revision/{}'.format(revision_id)
        return self._make_api_request(path, 'PUT', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "name": name,
            "timestamp": time.time()
        })

    def revision_delete(self: str, project_id: str, table_id: str,
                        revision_id: str) -> dict:
        """ Delete a revision for a table """
        path = 'revision/{}'.format(revision_id)
        return self._make_api_request(path, 'DELETE', {
            "project[id]": project_id,
            "table[id]": table_id
        })

    def upload_document(self, project_id: str, table_id: str, column_name: str, document_location, document_title: str = None):
        """ Upload a document to a table. Creates a new record """
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_title.split(".")[-1]
        path = 'record'
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        dataset = {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": {
                column_name: {
                    "name": document_title,
                    "extension": ext,
                    "data": encoded_file.decode("utf-8")
                }
            }
        }
        res = self._make_api_request(path, 'POST', dataset)
        if 'id' in res:
            return res
        else:
            return "Error"

    def attach_document(self, project_id: str, table_id: str, column_name: str, record_id: str, document_location, document_title: str = None):
        """ Upload a document to an existing record. """
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_location.split(".")[-1]
        # print(document_title)
        path = 'record/{}'.format(record_id)
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        dataset = {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": {
                column_name: {
                    "name": document_title,
                    "extension": ext,
                    "data": encoded_file.decode("utf-8")
                }
            }
        }
        # print(dataset)
        res = self._make_api_request(path, 'PUT', dataset)
        if 'id' in res:
            return res
        elif 'message' in res:
            return res['message']
        else:
            return "Error"

    def download_document(self, project_id: str, table_id: str, document_id: str, file_location: str, file_name: str = None):
        """ Download a document. Specify save location and filename """
        path = 'record/document/{}'.format(document_id)
        response = self._make_api_request(path, 'GET', {
            "project[id]": project_id,
            "table[id]": table_id
        },'')
        if 'file' in response[0]:
            if file_name is None:
                file_name = '{}.{}'.format(response[0]['name'], response[0]['extension'])
            content = base64.b64decode(response[0]['file'])
            try:
                file = open('{}/{}'.format(file_location, file_name), 'wb+')
                file.write(content)
                file.close()
            except Exception as ex:
                print('Error saving file: {}'.format(ex))
        

    # def record_create_withdocument(self, project_id: str, table_id: str, record: str,):
    #     if document_title is None:
    #         document_title = document_location.split("/")[-1]
    #     ext = document_location.split(".")[-1]
    #     path = 'record'
    #     with open(document_location, "rb") as image_file:
    #         encoded_file = base64.b64encode(image_file.read())
    #     record[document_column_name] = {
    #                 "name": document_title,
    #                 "extension": ext,
    #                 "data": encoded_file.decode("utf-8")
    #             }
    #     dataset = {
    #         "project": {"id": project_id},
    #         "table": {"id": table_id},
    #         "record": record
    #     }
    #     res = self._make_api_request(path, 'POST', dataset)
    #     if 'id' in res:
    #         return res
    #     elif 'message' in res:
    #         return res['message']
    #     else:
    #         return "Error"

    def record_update_withdocument(self, project_id: str, table_id: str, record_id: str, updated_record_values: dict, document_column_name: str, document_location, document_title: str = None) -> dict:
        """ Update record with a document """
        path = 'record/{}'.format(record_id)
        if document_title is None:
            document_title = document_location.split("/")[-1]
        ext = document_location.split(".")[-1]
        with open(document_location, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        updated_record_values[document_column_name]: {
            "name": document_title,
            "extension": ext,
            "data": encoded_file.decode("utf-8")
        }
        return self._make_api_request(path, 'PUT', {
            "project": {"id": project_id},
            "table": {"id": table_id},
            "record": updated_record_values
        })

    def create_virtual_csv(self, records: list):
        """ Not for use. Create a virtual CSV of records """
        encoded_csv = ",".join(records[0].keys())+"\n"
        for record in records:
            recs = []
            for key in record.keys():
                recs.append(record[key])
            encoded_csv += ",".join(recs)+"\n"
        return encoded_csv  

    def parse_document(self, documentLocation, documentTitle:str = None):
        if documentTitle is None:
            documentTitle = documentLocation.split("/")[-1]
        ext = documentTitle.split(".")[-1]
        with open(documentLocation, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())
        document = {
            "name": documentTitle,
            "extension": ext,
            "data": encoded_file.decode('utf-8')
        }
        return document