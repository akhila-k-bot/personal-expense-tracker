import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"

st.set_page_config(page_title="Personal Expense Tracker", layout="centered")

st.title("💰 Personal Expense Tracker")
st.write("Add, view, edit, or delete your daily expenses with visualization.")

# -------------------------------
# Load or create CSV file
# -------------------------------
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# -------------------------------
# Add New Expense
# -------------------------------
st.header("➕ Add Expense")

with st.form("add_expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    description = st.text_input("Description (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = pd.DataFrame([[date, category, amount, description]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ Expense added successfully!")

# -------------------------------
# Display Expenses
# -------------------------------
st.header("📋 All Expenses")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No expenses yet. Add some above.")

# -------------------------------
# Edit or Delete Expense
# -------------------------------
st.header("✏️ Edit or 🗑️ Delete Expense")

if not df.empty:
    index = st.number_input("Select expense index to modify", min_value=0, max_value=len(df)-1, step=1)

    selected_row = df.loc[index]
    st.write("### Selected Entry:")
    st.write(selected_row)

    # --- Edit Section ---
    st.subheader("Edit Expense")
    new_date = st.date_input("New Date", value=pd.to_datetime(selected_row["Date"]))
    new_category = st.selectbox("New Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"], index=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"].index(selected_row["Category"]) if selected_row["Category"] in ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"] else 0)
    new_amount = st.number_input("New Amount (₹)", min_value=0.0, value=float(selected_row["Amount"]), format="%.2f")
    new_description = st.text_input("New Description", value=selected_row["Description"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Changes"):
            df.loc[index] = [new_date, new_category, new_amount, new_description]
            df.to_csv(CSV_FILE, index=False)
            st.success("✅ Entry updated successfully!")
    with col2:
        if st.button("🗑️ Delete Entry"):
            df = df.drop(index).reset_index(drop=True)
            df.to_csv(CSV_FILE, index=False)
            st.warning("🗑️ Entry deleted successfully!")

# -------------------------------
# Visualization
# -------------------------------
st.header("📊 Spending Overview")

if not df.empty:
    df["Amount"] = df["Amount"].astype(float)
    category_total = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    category_total.plot(kind="bar", ax=ax)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Spent (₹)")
    st.pyplot(fig)
else:
    st.info("Add some expenses to see charts.")
