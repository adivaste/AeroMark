import urllib.parse

def encode_query_parameter(input_string):
    return urllib.parse.quote(input_string)

# # Example usage
# incoming_string = "example string with spaces and special characters!"
# encoded_string = encode_query_parameter(incoming_string)
# print(encoded_string)
