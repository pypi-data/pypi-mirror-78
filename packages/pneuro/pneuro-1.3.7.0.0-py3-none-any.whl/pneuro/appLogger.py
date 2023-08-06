from datetime import datetime


class AppLogger:
    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

    def log(self, file_object, log_message):
        """This method will be used for logger all the information to the file."""

        file_object.write(
            str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message + "\n")