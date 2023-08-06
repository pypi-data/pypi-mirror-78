class UtilList(list):
    @classmethod
    def read_from_file(cls, file_name):
        data = []
        with open(file_name, "rt") as fd:
           for line in fd:
               data.append(line.strip())

        return cls(data)

    def as_dict(self):
        return {k: v for v, k in enumerate(self)}
