import requests

KAVENEGAR_API_KEY = "56634E63794A4D4B4C465372734C6F2B577046514959622B306B714A316867617931502F335830316252553D"

def send_otp_kavenegar(phone_number, otp_code):
    url = f"https://api.kavenegar.com/v1/{KAVENEGAR_API_KEY}/verify/lookup.json"
    params = {
        "receptor": phone_number,
        "template": "otp_template", 
        "token": otp_code,  
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("return", {}).get("status") == 200:
            print("کد OTP با موفقیت ارسال شد.")
            return True
        else:
            print(f"خطا در ارسال OTP: {data}")
            return False
    except Exception as e:
        print(f"خطا در اتصال به کاوه نگار: {e}")
        return False



phone_number = "09304374247"  
send_otp_kavenegar(phone_number,otp_code=None)