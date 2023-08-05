import yaml

experiment_conf = {
    'workspace_slug': str,
    'project_slug': str,
    'image_id': int,
    'resource_spec_id': int,
    'start_command': str,
}


class YmlLoader:
    def __init__(self, filename, conf):
        self.filename = filename
        self.conf = conf
        self.data = self._load()

        if not self.validate():
            raise Exception('Yml load validation error')

    def _load(self):
        try:
            with open(self.filename) as f:
                documents = yaml.full_load(f)
                if not documents:
                    raise Exception('Nothing in config file')
                data_dict = dict()
                for item, doc in documents.items():
                    data_dict[item] = doc
                return data_dict
        except EnvironmentError:
            print('Error: Config file not found')

    def _validate_helper(self, struct, conf):
        if isinstance(struct, dict) and isinstance(conf, dict):
            # struct is a dict of types or other dicts
            return all(k in conf and self._validate_helper(struct[k], conf[k]) for k in struct)
        if isinstance(struct, list) and isinstance(conf, list):
            # struct is list in the form [type or dict]
            return all(self._validate_helper(struct[0], c) for c in conf)
        elif isinstance(conf, type):
            # struct is the type of conf
            return isinstance(struct, conf)
        else:
            # struct is neither a dict, nor list, not type
            return False

    def validate(self):
        return self._validate_helper(self.data, self.conf)

    def pop_val_by_key(self, key):
        return self.data.pop(key, None)



