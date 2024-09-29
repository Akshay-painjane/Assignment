class Transformer:
    def transform(self, input_data, template):
        try:
            # Create a mapping dictionary from the template for faster lookup
            mappings = {mapping.source_field.name: mapping.destination_field.name for mapping in template.mappings.all()}

            # Perform transformation on the entire input data
            return self.replace_fields(input_data, mappings)
        except Exception as e:
            raise ValueError(f"Error during transformation: {str(e)}")

    def replace_fields(self, data, mappings):
        """
        Recursively traverses the JSON object (data) and replaces the field names based on the mappings.
        """
        if isinstance(data, dict):
            transformed_dict = {}
            for key, value in data.items():
                # Replace the key if it's in the mappings, otherwise keep it as is
                new_key = mappings.get(key, key)
                # Recursively replace fields for nested dictionaries or lists
                transformed_dict[new_key] = self.replace_fields(value, mappings)
            return transformed_dict
        elif isinstance(data, list):
            return [self.replace_fields(item, mappings) for item in data]
        else:
            # Base case: if it's not a dict or list, just return the value (leaf node)
            return data
