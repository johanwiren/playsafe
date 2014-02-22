import distutils.spawn
import os.path
import signal
import subprocess


class Command(object):

    jobcount = 0;

    def __init__(self, args, name=None):

        self.jobId = Command.jobcount
        Command.jobcount += 1
        self.status = "Queued"
        self.stdout = ''
        if not os.path.isabs(args[0]):
            abspath = distutils.spawn.find_executable(args[0])
            args[0] = abspath
        self.name = name
        self.args = args
        self.process = None

    def pause(self):
        self.process.send_signal(signal.SIGSTOP)

    def resume(self):
        self.process.send_signal(signal.SIGCONT)

    def terminate(self):
        self.process.terminate()

    def kill(self):
        self.process.kill()

    def wait(self):
        self.process.wait()

    def run(self):
        print "Starting command %s" % self.args
        self.status = "Running"
        try:
            self.process = subprocess.Popen(
                self.args,
                bufsize=1,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        except:
            self.status = "Failed"
            return

        for line in iter(self.process.stdout.readline, ""):
            self.stdout += line

        self.process.wait()
        if self.process.returncode == 0:
            self.status = "Completed"
        else:
            self.status = "Failed"
        print "Job %s status: %s" % (self.args, self.status)

    def simple_dict(self):
        ''' Returns plain dict representation of the object '''
        result = dict()
        for k,v in self.__dict__.iteritems():
            if k != 'process':
                result[k] = v
        return result

