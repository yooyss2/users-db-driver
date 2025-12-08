class ExecutionError(Exception):
  def __init__(self, msg, errno):
    self.msg = msg
    self.errno = errno
    super().__init__(self.msg, self.errno)
