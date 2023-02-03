import json, tempfile, os
from bson.objectid import ObjectId
import channel
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import moviepy.editor

def start(queue, body, fs_videos, fs_mp3s):
  """
  Convert video to mp3 and in MongoDB then send message to MP3Queue 
  for notification service to alert user
  
  :param body:
  :param fs_videos:
  :param fs_mp3s:
  return: Error if failed to send message to queue 
  """
  message = json.loads(body)

  # empty temp file
  tf = tempfile.NamedTemporaryFile()
  # video contents
  out = fs_videos.get(ObjectId(message["video_fid"]))
  # add video to temp file
  tf.write(out.read())
  # create audio from temp video file
  audio = moviepy.editor.VideoFileClip(tf.name).audio
  tf.close()

  #write audio to file
  tf_path = f"{tempfile.getttempdir()}/{message['video_fd']}.pm3"
  audio.write_audiofile(tf_path)
  #store audio file in MongoDB
  with open(tf_path, "rb") as f:
    data = f.read()
    fid = fs_mp3s.put(data)
  os.remove(tf_path)

  message["mp3_fid"] = str(fid) 
  try:
       response = channel.send_message(queue, message)
  except Exception as err:
      #message not sent successfully, delete mp3 from dB
      fs_mp3s.delete(fid)
      return "failed to publish message"