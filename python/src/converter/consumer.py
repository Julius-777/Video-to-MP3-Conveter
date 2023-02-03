import sys, os, time
from pymongo import MongoClient
from botocore.exceptions import ClientError
import gridfs
import channel
from convert import to_mp3
mp3_queue = channel.get_queue("MP3Queue")
vid_queue = channel.get_queue("VideoMP3Queue")


def main():
  # MongoDB is hosted locally
  client = MongoClient("host.minikube.internal", 27017)
  db_videos = client.videos
  db_mp3s = client.mp3s
  # gridfs
  fs_videos = gridfs.GridFS(db_videos)
  fs_mp3s = gridfs.GridFS(db_mp3s)

  # Polling VideoQueue for messages every 5s
  while True:
    if message := channel.receive_message(vid_queue):
      err = to_mp3.start(mp3_queue, message[0].body, fs_videos, fs_mp3s)
      if not err:
        # vid processed succesfully, remove message from VideoMP3Queue
        channel.delete_message(message)

    print("Waiting for messages. To exit press CTRL+C")
    
if __name__ == "__main__":
  try:
     main()
  except KeyboardInterrupt:
    print("Interrupted")
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)