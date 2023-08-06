import json

class CDFDataset:
    def __init__(self, id, crs, survey_id, custom_metadata):
        self.id = id
        self.crs = crs
        self.survey_id = survey_id
        self.custom_metadata = custom_metadata

    def __str__(self):
        raw = {
            'id': self.id,
            'crs': self.crs,
            'survey_id': self.survey_id,
            'custom_metadata': self.custom_metadata
        }

        return json.dumps(raw, indent=2)


class GCSDataset:
    def __init__(self, name, url, size, custom_metadata):
        self.name = name
        self.url = url
        self.size = size
        self.custom_metadata = custom_metadata

    def __str__(self):
        raw = {
            'name': self.name,
            'url': self.url,
            'size': self.size,
            'custom_metadata': self.custom_metadata
        }

        return json.dumps(raw, indent=2)
