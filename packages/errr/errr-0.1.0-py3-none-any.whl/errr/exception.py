def _details_iter(labels, values):
    i = 1
    next(values, None)
    while True:
        label = next(labels, None)
        try:
            value = next(values)
            actual_values = True
        except StopIteration:
            value = None
            actual_values = False
        if label:
            yield (label, value)
        elif actual_values:
            yield (i, value)
        else:
            break
        i += 1

class DetailedMeta(type):
    def __repr__(self):
        return "<class '{}'>".format(self.__module__ + "." + self.__name__)

class DetailedException(Exception, metaclass=DetailedMeta):
    def __init__(self, *args):
        super().__init__(*args)
        self.__dict__["details"] = dict(_details_iter(iter(self.get_detail_labels()), iter(args)))

    def get_detail_labels(self):
        try:
            return super().get_detail_labels() + self.__class__._detail_labels
        except AttributeError:
            return self.__class__._detail_labels

    def __getattr__(self, attr):
        if attr in self.__class__._detail_labels:
            return self.details[attr]

    def __setattr__(self, attr, value):
        if attr in self.details:
            self.details[attr] = value
            return
        super().__setattr__(attr, value)

    def __str__(self):
        return "{}\n\nDetails:\n{}".format(self._get_msg(), self._get_details_msg())

    def _get_msg(self):
        return self.interpolate(str(self.args[0] if len(self.args) > 1 else ""))

    def interpolate(self, msg):
        print(msg)
        for key, value in self.details.items():
            msg = msg.replace("%{}%".format(key), str(value))
        print(msg)
        return msg

    def _get_details_msg(self):
        return "\n".join(map(_err_line, self.details.items()))

    def __init_subclass__(cls, details=[], **kwargs):
        super().__init_subclass__(**kwargs)
        cls._detail_labels = details

def _err_line(kv):
    return " {}{}: {}".format(chr(746), kv[0], kv[1])
