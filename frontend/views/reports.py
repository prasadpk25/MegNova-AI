import streamlit as st
import pandas as pd


def reports_page():

    st.title("📄 Medical Reports")

    st.write("Manage and review patient medical reports.")

    st.divider()

    # -----------------------------
    # Upload Section
    # -----------------------------
    uploaded_file = st.file_uploader(
        "📁 Upload Medical Report",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.success(f"✅ Uploaded Successfully: {uploaded_file.name}")

    st.divider()

    # -----------------------------
    # Reports Table
    # -----------------------------
    reports = pd.DataFrame(
        {
            "Patient": [
                "Rahul",
                "Sneha",
                "Arjun",
                "Priya",
                "Vikram"
            ],
            "Report": [
                "Blood Report",
                "MRI Scan",
                "Chest X-Ray",
                "ECG",
                "CT Scan"
            ],
            "Department": [
                "ICU",
                "Neurology",
                "Pulmonology",
                "Cardiology",
                "Radiology"
            ],
            "Status": [
                "Ready",
                "Pending",
                "Ready",
                "Ready",
                "Pending"
            ]
        }
    )

    st.subheader("📋 Uploaded Reports")

    st.dataframe(
        reports,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # Report Selection
    # -----------------------------
    patient = st.selectbox(
        "👤 Select Patient",
        reports["Patient"]
    )

    report = reports[reports["Patient"] == patient].iloc[0]

    st.subheader("📄 Report Details")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Patient",
            report["Patient"]
        )

        st.metric(
            "Department",
            report["Department"]
        )

        st.metric(
            "Report",
            report["Report"]
        )

    with c2:

        if report["Status"] == "Ready":
            st.success("✅ Report Ready")
        else:
            st.warning("⏳ Processing")

        st.metric(
            "Status",
            report["Status"]
        )

    st.divider()

    # -----------------------------
    # AI Summary
    # -----------------------------
    st.subheader("🤖 AI Medical Summary")

    st.info("""
### Clinical Summary

Patient shows mild signs of respiratory infection.

### Risk Level

🟡 Medium

### AI Recommendations

• Complete Blood Count (CBC)

• Chest X-Ray

• Oxygen Monitoring

• Start Antibiotics (Physician Approval)

• Review after 48 Hours
""")

    st.divider()

    # -----------------------------
    # Download Report
    # -----------------------------
    st.download_button(
        "📥 Download Report",
        data=reports.to_csv(index=False),
        file_name="medical_reports.csv",
        mime="text/csv",
    )