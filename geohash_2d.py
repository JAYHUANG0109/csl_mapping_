def convert_to_binary(value, span, precision):
    binary_str = ""
    for i in range(precision):
        mid = (span[0] + span[1]) / 2
        if value >= mid:
            binary_str += "1"
            span[0] = mid
        else:
            binary_str += "0"
            span[1] = mid
    # print(binary_str)
    return binary_str

def interweave(str1, str2):
    interwoven = ""
    for i in range(len(str1)):
        interwoven += str1[i] + str2[i]
    return interwoven

def binary_to_base32(binary_str):
    base32_alphabet = "0123456789bcdefghjkmnpqrstuvwxyz"
    base32_str = ""
    # print(binary_str)
    for i in range(0, len(binary_str), 5):
        chunk = binary_str[i:i+5]
        decimal_val = int(chunk, 2)
        base32_str += base32_alphabet[decimal_val]
    return base32_str[0:-1]

def encode_geohash(latitude, longitude, precision):
    lat_bin = convert_to_binary(latitude, [-90, 90], 18)
    lon_bin = convert_to_binary(longitude, [-180, 180], 18)
    
    interwoven_bin = interweave(lon_bin, lat_bin)
    
    geohash = binary_to_base32(interwoven_bin)
    
    return geohash[:precision]


# 25.042920559576547, 121.51768370394866
# print(encode_geohash(25.042920559576547, 121.51768370394866, 15))

# import geohash

# geohash_code = geohash.encode(25.042920559576547, 121.51768370394866, precision=7)
# print(geohash_code)


