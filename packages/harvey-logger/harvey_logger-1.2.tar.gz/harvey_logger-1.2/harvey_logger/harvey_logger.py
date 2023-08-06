from datetime import datetime


class Colours:
  BLACK = '\u001b[30m'
  RED = '\u001b[31m'
  GREEN = '\u001b[32m'
  YELLOW = '\u001b[33m'
  BLUE = '\u001b[34m'
  MAGENTA = '\u001b[35m'
  CYAN = '\u001b[36m'
  WHITE = '\u001b[37m'
  RESET = '\u001b[0m'


class Logger:
  @staticmethod
  def printWithTime(msg):
    print(
        f"{Colours.YELLOW}[ {datetime.now().strftime('%H:%M:%S.%f')[:-3]} ] -> {msg}{Colours.RESET}")

  def log(self, msg):
    self.printWithTime(f"{Colours.YELLOW}{msg}")

  def success(self, msg):
    self.printWithTime(f"{Colours.GREEN}{msg}")

  def error(self, msg):
    self.printWithTime(f"{Colours.RED}{msg}")

  def warn(self, msg):  # * Warn of something that needs an action
    self.printWithTime(f"{Colours.MAGENTA}{msg}")

  def alert(self, msg):  # * Alert of something good/neutral
    self.printWithTime(f"{Colours.BLUE}{msg}")

  def msg(self, msg):  # * Display a message
    self.printWithTime(f"{Colours.CYAN}{msg}")


# logger = Logger()

# logger.log("Hello, this is a log!")
# logger.success("Hello, this is a success message!")
# logger.error("Hello, this is an error!")
# logger.warn("Hello, this is a warning!")
# logger.alert("Hello, this is an alert!")
# logger.msg("Hello, this is cyan!")
