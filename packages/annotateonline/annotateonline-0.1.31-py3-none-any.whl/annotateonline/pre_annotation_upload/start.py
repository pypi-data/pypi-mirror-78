import json
import boto3
import traceback
import threading
from queue import Queue
from threading import Thread
import os
from .coco_convert import get_jsons_dict
from .pixel_convert import convert
from io import BytesIO

class AppWorkerUpload(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            key,body,content_type,args,logger = self.queue.get()
            try:
                logger.info('runing {}'.format(key))
                upload(key,body,content_type,args,logger)
            finally:
                self.queue.task_done()


def upload(key,body,content_type,args,logger):
    try:
        logger.info('start---'+key+'----')
        bucket = args.bucket
        session = boto3.Session(aws_access_key_id=args.aws_access_key_id,aws_secret_access_key=args.aws_secret_access_key,aws_session_token=args.aws_session_token)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(args.bucket)
        put_data = my_bucket.put_object(Body=body, Bucket=bucket, Key=key , ContentType=content_type)
        logger.info('done---'+key+'----')
    except Exception as e:
        logger.error(traceback.format_exc())

def start(args,logger):
    queue = Queue()   
    destination = args.destination
 
    for x in range(8):
        worker = AppWorkerUpload(queue)
        worker.daemon = True
        worker.start()

    if(args.ao_jsons):
        if int(args.project_type) == 1 :
            pwd = args.ao_jsons
            files = os.listdir(pwd)
            if pwd[-1] != '/':
                pwd += '/'
            for f in files:
                if not '___objects.json' in f:
                    continue
                file_path = pwd + f
                logger.info('Queueing {}'.format(file_path))
                key = destination + '/' + f
                with open(file_path, 'rb') as f:
                    buf = BytesIO(f.read())
                body = buf
                content_type = "application/json"
                queue.put((key,body,content_type,args,logger))     

        if int(args.project_type) == 2 :    
            pwd = args.ao_jsons
            files = os.listdir(pwd)
            if pwd[-1] != '/':
                pwd += '/'
            for f in files:
                if not '___save.png' in f:
                    continue
                file_path = pwd + f
                logger.info('Queueing {}'.format(file_path))
                
                # Put save png
                key = destination + '/' + f
                with open(file_path, 'rb') as png_file:
                    buf = BytesIO(png_file.read())
                body = buf
                content_type = "image/png"
                queue.put((key,body,content_type,args,logger))     

                # Put pixel json
                name = f.split('___')[0]
                json_name = str(name) + '___pixel.json'
                file_path = pwd + json_name
                key = destination + '/' + json_name
                with open(file_path, 'rb') as json_file:
                    buf = BytesIO(json_file.read())
                body = buf
                content_type = "application/json"
                queue.put((key,body,content_type,args,logger))  
        
        queue.join()

    if(args.coco_json):   
        coco_json_path = args.coco_json
        
        if int(args.project_type) == 1 :
            ao_jsons = get_jsons_dict(coco_json_path)
            for image_name in ao_jsons:
                logger.info('Queueing {}'.format(image_name))
                key = destination + '/' + image_name + '___objects.json'
                body = json.dumps(ao_jsons[image_name])
                content_type = "application/json"
                queue.put((key,body,content_type,args,logger))
        
        if int(args.project_type) == 2 : 
            ao_jsons_pngs = convert(coco_json_path)
            for image_png in ao_jsons_pngs:
                logger.info('Queueing {}'.format(image_png['image_name']))
                
                # Put png
                key = destination + '/' + image_png['image_name']
                content_type = "image/png"
                data_to_put = BytesIO()
                img = image_png['image']
                img.convert('RGBA').save(data_to_put,'PNG')
                queue.put((key,data_to_put.getvalue(),content_type,args,logger))
                
                # Put json
                key = destination + '/' + image_png['json_name']
                content_type = "application/json"
                queue.put((key,json.dumps(image_png['json']),content_type,args,logger))

        queue.join()

