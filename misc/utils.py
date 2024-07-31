class DataUtils:
    @staticmethod
    def values_from_key(data, key):
        values = {row[key] for row in data}
        return values

    def intersection_list(self, data, new_data, key):
        old_values_from_key = self.values_from_key(
            data=data,
            key=key
        )
        result = [row for row in new_data if row[key] in old_values_from_key]
        return result

    def subtract_list(self, data, new_data, key):
        old_values_from_key = self.values_from_key(
            data=data,
            key=key
        )
        result = [row for row in new_data if row[key] not in old_values_from_key]
        return result