"""
Streamlit application to convert a Real Intent CSV export into a format
compatible with Pipedrive's spreadsheet importer.  Pipedrive expects
specific column names for contacts (people), such as First name, Last
name, Email and Phone, and it allows multiple emails and phone numbers
to be imported by mapping the same field more than once during the
import process.  Address fields can be provided either in a single
column or split into separate columns for street, city, state and
postal code【181921423446661†L139-L170】.  Pipedrive's default person
fields include first name, last name, email address, mobile phone,
address, city, state and postal code【42388033684824†L48-L60】.

Any Real Intent columns that don't correspond to a default field will
remain in the output CSV so that you can map them to custom fields in
Pipedrive.  For example, the Real Intent ``household_income`` column is
renamed to ``Household income``; you'll need to create a custom
"Household income" field in Pipedrive before importing if you wish to
preserve this information.

To run this script locally, execute ``streamlit run real_intent_to_pipedrive.py``
from your terminal.  Upload a CSV with the expected column names and
download the converted file ready for Pipedrive import.
"""

import streamlit as st
import pandas as pd


# Mapping from Real Intent column keys to Pipedrive column headers.  The
# keys represent columns in the uploaded file; the values are the
# corresponding column names expected by Pipedrive.  When importing,
# you can map multiple ``Email`` or ``Phone`` columns to the same
# Pipedrive field to handle secondary contact details【181921423446661†L180-L199】.
COLUMN_MAPPINGS = {
    "first_name": "First name",
    "last_name": "Last name",
    "email_1": "Email",       # primary email
    "email_2": "Email 2",     # secondary email
    "email_3": "Email 3",     # tertiary email
    "phone_1": "Phone",       # primary phone; label it appropriately in Pipedrive
    "phone_2": "Phone 2",     # secondary phone
    "address": "Address",      # street address
    "city": "City",           # city or locality
    "state": "State",         # state or region
    "zip_code": "Postal code", # ZIP/postal code
    "household_income": "Household income",  # custom field
}


def main() -> None:
    """Main entry point for the Streamlit app."""
    st.title("Real Intent to Pipedrive Converter")

    st.info(
        """
        Upload a CSV file exported from Real Intent.  The app will convert your
        file into a format suitable for Pipedrive's CSV import.  Pipedrive
        requires a person name (either a single full name or separate first
        name and last name) as well as other contact details like email and
        phone【156037038803486†L193-L205】.  During the import, you can map
        multiple phone numbers by dragging the Phone field multiple times and
        assigning labels such as Work, Home or Mobile【181921423446661†L180-L199】.
        
        Address information can be split across separate columns (Address,
        City, State, Postal code) as provided here【181921423446661†L139-L170】.
        For fields not present in Pipedrive by default—such as household
        income—you should create a custom field in your Pipedrive account prior
        to importing.
        """
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Determine if any expected columns are missing
        missing_columns = [col for col in COLUMN_MAPPINGS if col not in df.columns]

        if missing_columns:
            st.error(
                f"The uploaded file does not contain the required columns: {', '.join(missing_columns)}."
            )
            return

        # Reorder and rename the DataFrame according to the mapping
        df_converted = df[list(COLUMN_MAPPINGS.keys())].rename(columns=COLUMN_MAPPINGS)

        st.write("Converted DataFrame:")
        st.dataframe(df_converted)

        # Encode the converted DataFrame to CSV for download
        csv_data = df_converted.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download converted CSV",
            data=csv_data,
            file_name="converted_pipedrive_file.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
