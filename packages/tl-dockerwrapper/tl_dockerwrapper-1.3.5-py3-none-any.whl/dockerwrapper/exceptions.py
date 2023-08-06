class ImageError(Exception):
    def __init__(self, msg, original_exception):
        super(ImageError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class ContainerError(Exception):
    def __init__(self, msg, original_exception):
        super(ContainerError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class ConfigError(Exception):
    def __init__(self, msg, original_exception):
        super(ConfigError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class VolumeError(Exception):
    def __init__(self, msg, original_exception):
        super(VolumeError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception


class NetworkError(Exception):
    def __init__(self, msg, original_exception):
        super(NetworkError, self).__init__("{} : {}".format(msg, original_exception))
        self.original_exception = original_exception
