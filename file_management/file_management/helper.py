from requests_toolbelt.multipart.encoder import MultipartEncoder
from mimetypes import MimeTypes
import ast
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def getpath(userid,name):
    try:
        url = "http://0.0.0.0:7003/file/{userid}/{name}".format(userid=userid,name=name)
        response = requests.get(url)
        print(response)
        return response.data['one_file']
    except Exception as e:
        print("getpath")
        print(e)


def callUploaderService(name,userid,file):
    try:
        mime = MimeTypes()
        mime_type = mime.guess_type(name)
        mp_encoder = MultipartEncoder(
                            fields={
                                'name':name, 
                                'user_id':userid,
                                # plain file object, no filename or mime type produces a
                                # Content-Disposition header with just the part name
                                'one_file': (name,file.read(), mime_type[0]),
                            }
                        )
        response = requests.post(
                            'http://0.0.0.0:7003/file/',
                            data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
                            # The MultipartEncoder provides the content-type header with the boundary:
                            headers={'Content-Type': mp_encoder.content_type}
                        
                        )
        print(response)
        return response.status_code
    except Exception as e:
        print("callUploaderService")
        print(e)