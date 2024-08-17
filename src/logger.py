import logging

class Logger:
    def __init__(self):
        self.log = []

    def log(self, message):
        self.log.append(message)

    def print_log(self):
        for message in self.log:
            print(message)