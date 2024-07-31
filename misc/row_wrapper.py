class RowWrapper:
    def __init__(self, data):
        self.data = data
        self.keys = list(data[0].keys())

    def create_tuple(self, row):
        _tuple = tuple()
        for i in range(len(self.keys)):
            _tuple += (row[self.keys[i]],)
        return _tuple

    def create_matrix(self):
        matrix = [
            self.create_tuple(
                row=row
            ) for row in self.data
        ]
        return matrix


class RowWrapperFromKeys:
    def __init__(self, data, keys):
        self.data = data
        self.keys = keys

    def create_tuple(self, row):
        _tuple = tuple()
        for i in range(len(self.keys)):
            _tuple += (row[self.keys[i]],)
        return _tuple

    def create_matrix(self):
        matrix = [
            self.create_tuple(
                row=row
            ) for row in self.data
        ]
        return matrix


class InsertValues:
    def __init__(self, db_row_data):
        self.data = db_row_data[0]
        self.keys = list(self.data.keys())[1:]

    def create_values_tuple(self):
        _tuple = tuple()
        for i in range(len(self.keys)):
            _tuple += (self.data[self.keys[i]],)
        return _tuple


class ValuesFromKeys:
    def __init__(self, data):
        self.data = data

    def extract_values(self, key):
        values = tuple()
        for i in range(len(self.data)):
            values += (self.data[i][key],)
        return values