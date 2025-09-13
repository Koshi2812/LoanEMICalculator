import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

st.set_page_config(page_title="Loan EMI Calculator", layout="centered")

st.title("🏦 Loan EMI Calculator")

with st.form("loan_form"):
    loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=1000.0, format="%.2f")
    annual_interest = st.number_input("Annual Interest Rate (%)", min_value=0.1, step=0.1, format="%.2f")
    tenure_years = st.slider("Loan Tenure (Years)", 1, 30, 5)
    submitted = st.form_submit_button("Calculate EMI")

if submitted:
    # Convert interest rate and duration
    monthly_rate = annual_interest / (12 * 100)
    tenure_months = tenure_years * 12

    # EMI Formula
    emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    total_payment = emi * tenure_months
    total_interest = total_payment - loan_amount

    # Display Results
    st.subheader("📊 EMI Calculation Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly EMI", f"₹{emi:,.2f}")
    col2.metric("Total Interest", f"₹{total_interest:,.2f}")
    col3.metric("Total Payment", f"₹{total_payment:,.2f}")

    # Pie Chart: Principal vs Interest
    st.subheader("📈 Principal vs Interest Breakdown")
    pie_data = pd.DataFrame({
        "Component": ["Principal", "Interest"],
        "Amount": [loan_amount, total_interest]
    })
    fig_pie = px.pie(pie_data, names='Component', values='Amount',
                     title="Loan Repayment Split", hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Year-wise Loan Balance
    st.subheader("📉 Year-wise Outstanding Balance")

    balance = []
    principal_paid = []
    interest_paid = []
    remaining = loan_amount
    for i in range(1, tenure_months + 1):
        interest = remaining * monthly_rate
        principal = emi - interest
        remaining -= principal
        if i % 12 == 0 or i == tenure_months:
            balance.append(remaining)
            interest_paid.append(interest)
            principal_paid.append(principal)

    year_labels = list(range(1, len(balance) + 1))
    df_balance = pd.DataFrame({
        "Year": year_labels,
        "Outstanding Balance": balance
    })
    fig_line = px.line(df_balance, x="Year", y="Outstanding Balance",
                       markers=True, title="Loan Outstanding Over Time",
                       color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_line, use_container_width=True)

    st.info("EMI calculated using the standard amortization formula.\nAdjust interest rate and tenure to compare plans.")

