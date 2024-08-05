# validate.py
import json
from datetime import datetime

from extract_idcard import extract_info
from validate_addr import is_valid_address


json_data_path = './json/json_sample.json'

def extract_ocr_data(json_data_path):
    with open(json_data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    ocr_data = {
        'id_ocr': data['data'][0]['id'],
        'doe_ocr': data['data'][0]['doe'],
        'dob_ocr': data['data'][0]['dob'],
        'sex_ocr': data['data'][0]['sex'],
        'issuse_ocr': data['data'][0]['issue_date'],
        'home_ocr' : data['data'][0]['home'],
        'address_entities' : data['data'][0]['address_entities']
    }
    
    return ocr_data

ocr_data = extract_ocr_data(json_data_path)

def doubleCheck_idCrad_infor(ocr_data):
    
    id_ocr = ocr_data['id_ocr']
    doe_ocr = ocr_data['doe_ocr']
    issuse_ocr = ocr_data['issuse_ocr']
    dob_ocr = ocr_data['dob_ocr']
    sex_ocr = ocr_data['sex_ocr']
    home_ocr = ocr_data['home_ocr']
    address_entities = ocr_data['address_entities']


    year_ocr = int(dob_ocr.split('/')[-1])
    yoe_ocr = int(doe_ocr.split('/')[-1])
    yoi_ocr = int(issuse_ocr.split('/')[-1])

    # Split the home field into province, district, and ward
    ward_home, district_home, province_home = [part.strip() for part in home_ocr.split(',')]

    # Extract the address entities
    province_Add_ocr = address_entities['province']
    district_Add_ocr = address_entities['district']
    ward_Add_ocr = address_entities['ward']

    idCard_extract = extract_info(id_ocr)

    #Kiểm tra ngày hợp lê:  CCCD hết hạn, Chưa đủ 18 tuổi, Ngày hết hạn không hợp lệ,....
    dates_to_validate = [
        (dob_ocr, 412, "DOB không hợp lệ"),
        (doe_ocr, 413, "DOE không hợp lệ"),
        (issuse_ocr, 414, "DOI không hợp lệ")
    ]
    result = validate_dates(dates_to_validate)
    if result:
        return result
    

    check_datetime = check_vali_datetime(year_ocr, yoe_ocr, yoi_ocr)
    if check_datetime[0] != 400:
        return check_datetime[0], check_datetime[1]


    check_home_address = is_valid_address(province_home, district_home , ward_home)
    home_code_status = check_home_address[0]
    if home_code_status != 100:
        return 320, f"- ID Card: {id_ocr} - {check_home_address[1]}"
    

    check_valid_address = is_valid_address(province_Add_ocr, district_Add_ocr, ward_Add_ocr)
    addr1_code_status = check_valid_address[0]
    if addr1_code_status != 100:
        return addr1_code_status, f"- ID Card: {id_ocr} - {check_valid_address[1]}"
    

    extract_code_status, province, gender, yob = idCard_extract
    if not (province == province_Add_ocr and gender == sex_ocr and yob == year_ocr):
        return 310, f"ID Card: {id_ocr} Thông tin trích xuất từ ID card không trùng với OCR (Tỉnh, Giới tính, Năm Sinh)"
    
    extract_code_status = idCard_extract[0]
    if extract_code_status!=200:
        return extract_code_status, f"ID Card: {id_ocr} is invalid"
    

    return 300,  f"Addr Match profile"

current_year = int(datetime.now().year)

def is_valid_date(date_string):
    try:
        # Định dạng ngày tháng năm là dd/mm/yyyy
        datetime.strptime(date_string, "%d/%m/%Y")
        return 410, f"Ngày hợp lệ"
    except ValueError:
        return 411, f"Ngày không hợp lệ"
    
def is_valid_date(date_string):
    try:
        # Định dạng ngày tháng năm là dd/mm/yyyy
        datetime.strptime(date_string, "%d/%m/%Y")
        return 410, f"Ngày hợp lệ"
    except ValueError:
        return 411, f"Ngày không hợp lệ"

def validate_dates(dates):
    for date, error_code, error_message in dates:
        check = is_valid_date(date)
        if check[0] != 410:
            return error_code, error_message
    return None

def check_vali_datetime(yob, doe, yoi):
    if(yoi - yob < 14):
        return 415, f"Ngày cấp nhỏ hơn 13 tuổi"
    if(yob > current_year or yoi > current_year):
       return 401, f"Year of birth or Issue date is invalid"
    else:
        if( doe < current_year ):
            return 402, f"Date of expiry is invalid"
        else:
            if(current_year - yob <18):
                return 403, f"Chưa đủ 18 tuổi"
            else:
                age_at_issue = yoi - yob
                expected_doe = None
                
                if 14 <= age_at_issue < 23:
                    expected_doe = yob + 25
                elif 23 <= age_at_issue < 38:
                    expected_doe = yob + 40
                elif 38 <= age_at_issue < 58:
                    expected_doe = yob + 60
                elif age_at_issue >= 58:
                    if doe is None:  # Không có ngày hết hạn
                        return 400, "Date valid."
                    else:
                        return 405, "Căn cước công dân không có ngày hết hạn sau 58 tuổi."
                if expected_doe == doe:
                    return 400, "Date valid"
                else:
                    return 405, "Ngày hết hạn không hợp lệ."



# test, message = check_vali_datetime(yob, doe, yoi)
# print(test, message)
test, message = doubleCheck_idCrad_infor(ocr_data)
if test:
    print(test, message)
else:
    print(message)