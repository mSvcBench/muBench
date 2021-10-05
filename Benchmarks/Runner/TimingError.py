class TimingError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "All Pool Threads are busy. It's impossible to respect the requests timing! " \
                   ":( - Event_time: {0} ".format(self.message)
        else:
            return "All Pool Threads are busy. It's impossible to respect the requests timing! :("
