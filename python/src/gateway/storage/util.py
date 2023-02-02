import channel, json
from botocore.exceptions import ClientError

"""
    The following function needs to upload file to MongoDB via GridFS
    then send a message via the queue notifying  videoconveter service 
    its ready for processing
"""
def upload(f, fs, queue, access):
    #upload file to MongoDB
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500

    message = {
            "video_fid": str(fid),
            "mp3_fid": None,
            "username": access["username"],
    }

    # If there is no message sent for the file delete from dB
    try:
         queue.send_message(
            queue=queue,
            message_attributes={
                "Processed" : {
                    'StringValue': "No",
                    'DataType': 'string'
                }
            },
            message_body=json.dumps(message)
        )
    except ClientError as error:
        fs.delete(fid)
        return "internal server error", 500

