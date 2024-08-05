import json

json_file_path = './json/vn_only_simplified_json_generated_data_vn_units.json'

def load_valid_addresses(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

valid_addresses = load_valid_addresses(json_file_path)

def find_city(city_name):
    for city in valid_addresses:
        if city['FullName'] == city_name:
            return city
    return None

def find_district(city, district_name):
    for district in city['District']:
        if district['FullName'] == district_name:
            return district
    return None

def find_ward(district, ward_name):
    for ward in district['Ward']:
        if ward['FullName'] == ward_name:
            return ward
    return None

def is_valid_address(city_name, district_name, ward_name):
    city = find_city(city_name)
    if city:
        district = find_district(city, district_name)
        if district:
            ward = find_ward(district, ward_name)
            if ward:
                return 100, f"Địa chỉ hợp lệ: {ward_name}, {district_name}, {city_name}"
            else:
                return 101, f"'{ward_name}' không tồn tại trong quận '{district_name}' của thành phố '{city_name}'"
        else:
            return 102, f"Quận '{district_name}' không tồn tại trong thành phố '{city_name}'"
    else:
        return 103, f"Thành phố '{city_name}' không tồn tại"


# city_name = "Ninh Bình"
# district_name = "Yên Khánh"
# ward_name = "Khánh An"
# street_name = "Phố A"

# code_status, message = is_valid_address(city_name, district_name, ward_name)
# if code_status == 100:
#     print("Địa chỉ hợp lệ.")
# else:
#     print(f"Lỗi {code_status}: {message}")
