import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import re

def analyze_phone_number(phone_number, country_code='IN'):
    """
    Analyze a phone number using OSINT techniques to extract carrier, region, and other information.

    Args:
        phone_number (str): Phone number to analyze (with or without country code)
        country_code (str): Default country code if not provided in phone number

    Returns:
        dict: Dictionary containing analysis results
    """
    try:
        # Clean the phone number
        phone_number = re.sub(r'[^\d+\-\s\(\)]', '', phone_number.strip())

        # Parse the phone number
        try:
            parsed_number = phonenumbers.parse(phone_number, country_code)
        except phonenumbers.NumberParseException as e:
            return {
                'valid': False,
                'error': f"Invalid phone number format: {str(e)}",
                'input': phone_number
            }

        # Basic validation
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)

        result = {
            'input': phone_number,
            'formatted_number': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'valid': is_valid,
            'possible': is_possible,
            'country_code': parsed_number.country_code,
            'national_number': parsed_number.national_number
        }

        if not is_valid:
            result['error'] = "Phone number is not valid"
            return result

        # Get carrier information
        try:
            carrier_name = carrier.name_for_number(parsed_number, "en")
            result['carrier'] = carrier_name if carrier_name else "Unknown"
        except:
            result['carrier'] = "Could not determine"

        # Get region/location information
        try:
            region = geocoder.description_for_number(parsed_number, "en")
            result['region'] = region if region else "Unknown"
        except:
            result['region'] = "Could not determine"

        # Get timezone information
        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            result['timezone'] = list(timezones) if timezones else []
        except:
            result['timezone'] = []

        # Determine line type
        if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE:
            result['line_type'] = "Mobile"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.FIXED_LINE:
            result['line_type'] = "Fixed Line"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
            result['line_type'] = "Fixed Line or Mobile"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.TOLL_FREE:
            result['line_type'] = "Toll Free"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.PREMIUM_RATE:
            result['line_type'] = "Premium Rate"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.SHARED_COST:
            result['line_type'] = "Shared Cost"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.VOIP:
            result['line_type'] = "VoIP"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.PERSONAL_NUMBER:
            result['line_type'] = "Personal Number"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.PAGER:
            result['line_type'] = "Pager"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.UAN:
            result['line_type'] = "UAN"
        elif phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.VOICEMAIL:
            result['line_type'] = "Voicemail"
        else:
            result['line_type'] = "Unknown"

        return result

    except Exception as e:
        return {
            'valid': False,
            'error': f"Analysis failed: {str(e)}",
            'input': phone_number
        }