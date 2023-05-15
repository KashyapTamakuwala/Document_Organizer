from requests_toolbelt.multipart.encoder import MultipartEncoder
from mimetypes import MimeTypes
import ast
import requests



def callUploaderService(name,userid,file):
    try:
        mime = MimeTypes()
        mime_type = mime.guess_type(name)
        mp_encoder = MultipartEncoder(
                            fields={
                                'user_id':userid,
                                # plain file object, no filename or mime type produces a
                                # Content-Disposition header with just the part name
                                'one_file': (name,file.read(), mime_type[0]),
                            }
                        )
        response = requests.post(
                            'http://fileuploader:7003/file/',
                            data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
                            # The MultipartEncoder provides the content-type header with the boundary:
                            headers={'Content-Type': mp_encoder.content_type}
                        
                        )
        print(response)
        return response
    except Exception as e:
        print("callUploaderService")
        print(e)