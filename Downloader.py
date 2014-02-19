from Command import *
import Queue
import threading
import time


class Downloader(object):

    run_threads = True

    def __init__(self, runners=1):
        self.q = Queue.Queue()
        self.threads = []
        self.downloaditems = []

        for i in range(runners):
            thread = DownloadThread(i, self.q)
            self.threads.append(thread)
            thread.start()

    def add(self, downloaditem):
        self.q.put(item) 
        self.downloaditems.append(item)

    def stop(self):
        Downloader.run_threads = False
        for thread in self.threads:
            thread.join()


class DownloadThread(threading.Thread):

    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q

    def run(self):
        while Downloader.run_threads:
            self.__download_streams(self)
            time.sleep(0.1)

    def __download_streams(self):
        if not self.q.empty():
            item = self.q.get()
            item.command.run()
       

class DownloadItem(object):

    def __init__(self, stream):
        self.stream = stream
        args = [ "ffmpeg", "-i", self.stream.streamurl ]
        args += self.stream.ffmpegargs
        args.append('/'.join([self.stream.output_dir, self.stream.filename]))
        self.command = Command(args, name=filename)

