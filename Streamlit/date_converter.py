#pip install nepali_date_utils

#converter.bs_to_ad(date) #BS to AD conversion
#converter.ad_to_bs(date) #AD to BS conversion

# logic:
# 1. Get the date from the user -> date
# 2. Get the conversion type from the user -> conversion_type --> using radio
# 3. If conversion_type is 'bs_to_ad', convert the date from BS to AD
# 4. If conversion_type is 'ad_to_bs', convert the date from AD to BS

import nepali_date_utils
from nepali_date_utils import converter
import streamlit as st

st.title("Nepali Date Converter")
st.subheader("Convert between Nepali (BS) and Gregorian (AD) dates")

date = st.text_input("Select a date in XXXX/XX/XX")
conversion_type = st.radio("Select conversion type", ("BS to AD", "AD to BS"))


if st.button("Convert"):
    if conversion_type == "BS to AD":
        converted_date = converter.bs_to_ad(date)
        st.success(f"Converted date (AD): {converted_date}")
    else:
        converted_date = converter.ad_to_bs(date)
        st.success(f"Converted date (BS): {converted_date}")