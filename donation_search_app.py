import streamlit as st
import pandas as pd

st.set_page_config(page_title="Donation System")
st.title("Donation System")

# -------- LOAD DATA --------
@st.cache_data
def load_data():
    df = pd.read_excel("members.xlsx")

    # Remove empty mobile numbers
    df = df.dropna(subset=["Mobile_No"])

    # Convert mobile number properly (remove .0 issue)
    df["Mobile_No"] = df["Mobile_No"].astype(str).str.replace(".0", "", regex=False)

    return df

df = load_data()

mobile_input = st.text_input("Enter Mobile Number")

if st.button("Submit"):

    if mobile_input.strip() == "":
        st.warning("Please enter mobile number")
    else:
        search_number = mobile_input.strip()

        person_df = df[df["Mobile_No"] == search_number]

        if person_df.empty:
            st.error("Mobile number not found ❌")
        else:
            st.success("Record Found")

            person = person_df.iloc[0]

            # -------- PERSON DETAILS --------
            st.write("### Person Details")
            st.write("Name:", person["Name"])
            st.write("Location:", person["Location"])

            # -------- MONTH LOGIC --------
            month_order = [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ]

            month_dict = {}
            total = 0

            # Month columns start from index 6
            # Skip receipt column (every alternate column)
            month_columns = df.columns[6:-1:2]

            for i, col in enumerate(month_columns):
                amount = person[col]

                if pd.notna(amount) and amount != 0:
                    amount = int(amount)
                    total += amount
                else:
                    amount = "-"   # show dash if no donation

                month_dict[month_order[i]] = amount

            # -------- CREATE TABLE --------
            table_data = []

            for m in month_order:
                table_data.append([m, month_dict[m]])

            table_data.append(["Total", total])

            donation_table = pd.DataFrame(
                table_data,
                columns=["Months", "Donation"]
            )

            # 🔥 IMPORTANT FIX FOR ARROW ERROR
            donation_table["Donation"] = donation_table["Donation"].astype(str)

            st.write("### Monthly Donation Details")
            st.table(donation_table)

            