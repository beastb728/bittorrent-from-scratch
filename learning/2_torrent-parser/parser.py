INFO_START = None
INFO_END = None

def parse_string(data, index):
    colon_index = data.index(b':', index)

    length = int(data[index:colon_index])

    start = colon_index + 1
    end = start + length

    value = data[start:end]

	# value = value.decode()

    return value, end


def parse_integer(data, index):
    end_index = data.index(b'e', index)

    number_bytes = data[index + 1:end_index]

    value = int(number_bytes)

    return value, end_index + 1


def parse_list(data, index):
    result = []

    index += 1  # skip 'l'

    while data[index:index + 1] != b'e':
        value, index = decode(data, index)
        result.append(value)

    return result, index + 1


def parse_dictionary(data, index):
    global INFO_START, INFO_END

    result = {}

    index += 1  # skip 'd'

    while data[index:index + 1] != b'e':

        key, index = decode(data, index)

        if key == b'info':
            INFO_START = index

            value, index = decode(data, index)

            INFO_END = index
        else:
            value, index = decode(data, index)

        result[key] = value

    return result, index + 1


def decode(data, index=0):
    current = data[index:index + 1]

    if current.isdigit():
        return parse_string(data, index)

    elif current == b'i':
        return parse_integer(data, index)

    elif current == b'l':
        return parse_list(data, index)

    elif current == b'd':
        return parse_dictionary(data, index)

    else:
        raise ValueError(f"Invalid bencode at index {index}")
