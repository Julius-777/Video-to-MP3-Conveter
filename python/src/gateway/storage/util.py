import json
from botocore.exceptions import ClientError

def upload(channel, queue, f, fs, access):
    """
    The following function needs to upload file to MongoDB via GridFS
    then send a message via the queue notifying  videoconveter service 
    its ready for processing
    """
    try:
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500

    message = {
            "video_fid": str(fid),
            "mp3_fid": None,
            "username": access["username"],
    }
    try:
       response = channel.send_message(queue, message)
    except Exception as err:
        #message not sent successfully, delete video from dB
        fs.delete(fid)
        return err

