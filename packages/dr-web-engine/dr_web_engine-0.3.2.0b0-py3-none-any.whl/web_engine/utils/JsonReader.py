
class JsonReader:

    def __init__(self, json_object, cache=None):
        self.json_object = json_object
        self._cache = cache or []

    # Final method call
    def get(self):
        temp_value = self.json_object
        for item in self._cache:
            if not isinstance(item, int) and item not in temp_value:
                return None
            temp_value = temp_value[item]
        return temp_value

    # Build the cache, and handle special cases
    def _(self, name):
        # Enables method chaining
        return JsonReader(self.json_object, self._cache + [name])

    # Reflection
    def __getattr__(self, name):
        return self._(name)

    # Called with the object is deleted
    def __del__(self):
        self.json_object = None
        self._cache = None

    def __getitem__(self, item):
        return self._(item)

