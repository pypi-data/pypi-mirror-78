import json
import datetime

class TokenizedStringIterator:
    def __init__(self, separator):
        self.separator = separator

    def getTokens(self, value):
        if isinstance(value, str):
            if len(self.separator) == 0:
                tokens = value
            else:    
                tokens = value.split(self.separator)

            for token in tokens:
                yield token
        else:
            return

class TokenizedJsonIterator:
    def __init__(self, property_name):
        self.property_name = property_name

    def getTokens(self, value):
        if isinstance(value, str):
            if not value or len(value) == 0:
                return
                
            data_objects = json.loads(value.replace('\'', '"'))
            for data_object in data_objects:
                yield data_object[self.property_name]
        else:
            return

class FeatureGenerationUtils:
    def get_document_property(self, document, property_path, transform_properties=None):
        path_tokens = property_path.split('.')

        fragment = document
        for property in path_tokens:
            if not fragment:
                return None

            property = self.safe_parse_int(property)
            if isinstance(property, int):
                fragment = fragment[property]
            else:
                fragment = fragment.get(property)

        if not transform_properties:
            return self.safe_parse_float(fragment) if fragment is not None else fragment
        else:
            values = []
            if not fragment:
                return fragment

            for property_object in fragment:
                values.append(property_object[transform_properties['property_name']])

            return transform_properties['transform_separator'].join([str(x) for x in values if x is not None])

    def safe_parse_int(self, token):
        try:
            return int(token)
        except:
            return token

    def safe_parse_float(self, token):
        try:
            return float(token)
        except:
            return token

    def edit_distance(self, str1, str2, len_str1=None, len_str2=None):
        if len_str1 == None:
            len_str1 = len(str1)

        if len_str2 == None:
            len_str2 = len(str2)
            
        if len_str1 == 0:
            return len_str2

        if len_str2 == 0:
            return len_str1

        if str1[len_str1 -1] == str2[len_str2 - 1]:
            return self.edit_distance(str1, str2, len_str1-1, len_str2-1)

        return 1 + min(
            self.edit_distance(str1, str2, len_str1=len_str1-1, len_str2=len_str2-1),
            self.edit_distance(str1, str2, len_str1=len_str1, len_str2=len_str2-1),
            self.edit_distance(str1, str2, len_str1=len_str1-1, len_str2=len_str2),
        )

    def get_days_delta(self, start_date_str, end_date_str):
        if isinstance(start_date_str, str) & isinstance(end_date_str, str):
            try:
                if start_date_str.startswith('-1'):
                    return -1

                if end_date_str.startswith('-1'):
                    return -1

                end_date = datetime.datetime.strptime(end_date_str[0:8], '%Y%m%d')
                start_date = datetime.datetime.strptime(start_date_str[0:8], '%Y%m%d')

                return (end_date - start_date).days

            except:
                return -1

        else:
            return -1

    def vectorize_feature(self, row, feature, tokenizer):
        categorical_vector = []
        value = row[feature]
        if isinstance(value, str):
            for feature_value in tokenizer.getTokens(value):
                if len(feature_value) > 0:
                    encoded_feature_name = feature + '_' + feature_value.lower()
                    categorical_vector.append(encoded_feature_name)
        
        return categorical_vector