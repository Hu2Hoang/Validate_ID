# validate.py
import json
from datetime import datetime

from extract_idcard import extract_info
from validate_addr import is_valid_address


json_data_path = './json/json_sample.json'

def doubleCheck_idCrad_infor(json_data_path):
    # Read the JSON data from a file
    with open(json_data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Extract the "id" value
    id_ocr = data['data'][0]['id']
    dob_ocr = data['data'][0]['dob']
    year_ocr = int(dob_ocr.split('/')[-1])

    doe_ocr = data['data'][0]['doe']
    yoe_ocr = int(doe_ocr.split('/')[-1])

    issuse_ocr = data['data'][0]['issue_date']
    yoi_ocr = int(issuse_ocr.split('/')[-1])

    sex_ocr = data['data'][0]['sex']

    home_ocr = data['data'][0]['home']

    # Split the home field into province, district, and ward
    ward_home, district_home, province_home = [part.strip() for part in home_ocr.split(',')]


    # Extract the address entities
    address_entities = data['data'][0]['address_entities']
    province_Add_ocr = address_entities['province']
    district_Add_ocr = address_entities['district']
    ward_Add_ocr = address_entities['ward']

    idCard_extract = extract_info(id_ocr)

    #Kiểm tra ngày hợp lê:  CCCD hết hạn, Chưa đủ 18 tuổi, Ngày hết hạn không hợp lệ,....
    check_yob =is_valid_date(dob_ocr)
    if check_yob[0]==410:
        pass
    else:
        return 412, f"YOB không hợp lệ"
    
    check_doe =is_valid_date(doe_ocr)
    if check_doe[0]==410:
        pass
    else:
        return 413, f"DOE không hợp lệ"
    
    check_yoi =is_valid_date(issuse_ocr)
    if check_yoi[0]==410:
        pass
    else:
        return 414, f"YOI không hợp lệ"
    

    check_datetime = check_vali_datetime(year_ocr, yoe_ocr, yoi_ocr)
    if check_datetime[0] == 400:
        pass
    else:
        return check_datetime[0], check_datetime[1]

    extract_code_status = idCard_extract[0]
    if extract_code_status==200:
        extract_code_status, province, gender, yob = idCard_extract
        if province == province_Add_ocr and gender == sex_ocr and yob == year_ocr:
            check_valid_address = is_valid_address(province_Add_ocr, district_Add_ocr, ward_Add_ocr)
            addr1_code_status = check_valid_address[0]
            if addr1_code_status == 100:
                check_home_address = is_valid_address(province_home, district_home , ward_home)
                home_code_status = check_home_address[0]
                if home_code_status == 100:
                    return 300,  f"Addr Match profile"
                else:
                    return 320, f"- ID Card: {id_ocr} - {check_home_address[1]}"
            else:
                return addr1_code_status, f"- ID Card: {id_ocr} - {check_valid_address[1]}"
            # return True, f"Match profile - Province: {province}, Gender: {gender}, Year of Birth: {yob}"
        else:
            return 310, f"ID Card: {id_ocr} Thông tin trích xuất từ ID card không trùng với OCR (Tỉnh, Giới tính, Năm Sinh)"
    else:
        return extract_code_status, f"ID Card: {id_ocr} is invalid"
    
yob=2003
doe=2028
issue_date=2021

current_year = int(datetime.now().year)

def is_valid_date(date_string):
    try:
        # Định dạng ngày tháng năm là dd/mm/yyyy
        datetime.strptime(date_string, "%d/%m/%Y")
        return 410, f"Ngày hợp lệ"
    except ValueError:
        return 411, f"Ngày không hợp lệ"
    
def check_vali_datetime(yob, doe, issue_date):
    if(yob > current_year or issue_date > current_year):
       return 401, f"Year of birth or Issue date is invalid"
    else:
        if( doe < current_year ):
            return 402, f"Date of expiry is invalid"
        else:
            if(current_year - yob <18):
                return 403, f"Chưa đủ 18 tuổi"
            else:
                age_at_issue = issue_date - yob
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



# test, message = check_vali_datetime(yob, doe, issue_date)
# print(test, message)
test, message = doubleCheck_idCrad_infor(json_data_path)
if test:
    print(test, message)
else:
    print(message)