import re

province_codes = {
    '001': 'Hà Nội',
    '002': 'Hà Giang',
    '004': 'Cao Bằng',
    '006': 'Bắc Kạn',
    '008': 'Tuyên Quang',
    '010': 'Lào Cai',
    '011': 'Điện Biên',
    '012': 'Lai Châu',
    '014': 'Sơn La',
    '015': 'Yên Bái',
    '017': 'Hòa Bình',
    '019': 'Thái Nguyên',
    '020': 'Lạng Sơn',
    '022': 'Quảng Ninh',
    '024': 'Bắc Giang',
    '025': 'Phú Thọ',
    '026': 'Vĩnh Phúc',
    '027': 'Bắc Ninh',
    '030': 'Hải Dương',
    '031': 'Hải Phòng',
    '033': 'Hưng Yên',
    '034': 'Thái Bình',
    '035': 'Hà Nam',
    '036': 'Nam Định',
    '037': 'Ninh Bình',
    '038': 'Thanh Hóa',
    '040': 'Nghệ An',
    '042': 'Hà Tĩnh',
    '044': 'Quảng Bình',
    '045': 'Quảng Trị',
    '046': 'Thừa Thiên Huế',
    '048': 'Đà Nẵng',
    '049': 'Quảng Nam',
    '051': 'Quảng Ngãi',
    '052': 'Bình Định',
    '054': 'Phú Yên',
    '056': 'Khánh Hòa',
    '058': 'Ninh Thuận',
    '060': 'Bình Thuận',
    '062': 'Kon Tum',
    '064': 'Gia Lai',
    '066': 'Đắk Lắk',
    '067': 'Đắk Nông',
    '068': 'Lâm Đồng',
    '070': 'Bình Phước',
    '072': 'Tây Ninh',
    '074': 'Bình Dương',
    '075': 'Đồng Nai',
    '077': 'Bà Rịa - Vũng Tàu',
    '079': 'Hồ Chí Minh',
    '080': 'Long An',
    '082': 'Tiền Giang',
    '083': 'Bến Tre',
    '084': 'Trà Vinh',
    '086': 'Vĩnh Long',
    '087': 'Đồng Tháp',
    '089': 'An Giang',
    '091': 'Kiên Giang',
    '092': 'Cần Thơ',
    '093': 'Hậu Giang',
    '094': 'Sóc Trăng',
    '095': 'Bạc Liêu',
    '096': 'Cà Mau'
}

def check_id_card(id_card):
    # Định nghĩa regex theo quy tắc đã nêu
    regex = re.compile(r'^0([0-9]{2})([0-9])([0-9]{2})([0-9]{6})$')
    
    if regex.match(id_card):
        return 210  # Status code for valid ID format
    else:
        return 211  # Status code for invalid ID format

def extract_info(id_card):
    status_code = check_id_card(id_card)
    if status_code == 210:
        province_code = id_card[1:3]
        gender_code = id_card[3]
        yob_code = id_card[4:6]

        # Extract province
        province_extract = province_codes.get('0' + province_code)
        if not province_extract:
            return 212, None, None, None  # Status code for invalid province code
        
        # Extract gender
        if int(gender_code) % 2 == 0:
            gender_extract = 'Nam'
        else:
            gender_extract = 'Nữ'

        # Extract year of birth
        if gender_code in {'0', '1'}:
            yob_extract = '19' + yob_code
        elif gender_code in {'2', '3'}:
            yob_extract = '20' + yob_code
        elif gender_code in {'4', '5'}:
            yob_extract = '21' + yob_code
        elif gender_code in {'6', '7'}:
            yob_extract = '22' + yob_code
        elif gender_code in {'8', '9'}:
            yob_extract = '23' + yob_code

        return 200, province_extract, gender_extract, int(yob_extract)
    else:
        return status_code, None, None, None

# # Ví dụ kiểm tra
# id_cards = [
#     "087084000999",  # Đúng
#     "001000000001",  # Đúng
#     "099215000999",  # Sai
#     "010300123456",  # Đúng
#     "123456789012",  # Sai, không bắt đầu bằng '0'
#     "0123456"        # Sai, không đủ 12 ký tự
# ]

# for id_card in id_cards:
#     status, province, gender, yob = extract_info(id_card)
#     if status == 200:
#         print(f'status code: {status} - Province: {province}, Gender: {gender}, Year of Birth: {yob}')
#     else:
#         print(f'status code: {status} - ID card {id_card} is invalid')