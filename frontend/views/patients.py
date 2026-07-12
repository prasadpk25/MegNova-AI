import streamlit as st
import pandas as pd


def patients_page():

    st.title("👥 Patient Records")

    df = pd.read_csv("../datasets/patients.csv")

    # -----------------------------
    # Search
    # -----------------------------
    search = st.text_input(
        "🔍 Search Patient",
        placeholder="Search by patient name..."
    )

    col1, col2 = st.columns(2)

    with col1:
        department = st.selectbox(
            "🏥 Department",
            ["All"] + sorted(df["department"].unique())
        )

    with col2:
        status = st.selectbox(
            "🚨 Status",
            ["All"] + sorted(df["status"].unique())
        )

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["name"].str.contains(search, case=False)
        ]

    if department != "All":
        filtered = filtered[
            filtered["department"] == department
        ]

    if status != "All":
        filtered = filtered[
            filtered["status"] == status
        ]

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("👥 Patients", len(filtered))
    c2.metric("🚨 Critical", len(filtered[filtered["status"] == "Critical"]))
    c3.metric("❤️ Avg Oxygen", f"{filtered['oxygen_level'].mean():.1f}%")

    st.divider()

    st.subheader("📋 Patient Records")

    st.dataframe(
        filtered[
            [
                "patient_id",
                "name",
                "age",
                "gender",
                "department",
                "status",
                "oxygen_level",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # -----------------------------
    # Patient Details
    # -----------------------------
    patient = st.selectbox(
        "👤 Select Patient",
        filtered["name"]
    )

    row = filtered[filtered["name"] == patient].iloc[0]

    st.subheader("🏥 Patient Details")

    d1, d2 = st.columns(2)

    with d1:

        st.metric("❤️ Heart Rate", row["heart_rate"])

        st.metric("🌡 Temperature", row["temperature"])

        st.metric("🫁 Oxygen", f"{row['oxygen_level']} %")

        st.metric("🛏 Bed", row["bed_no"])

    with d2:

        st.metric("🩸 Blood Pressure", row["blood_pressure"])

        st.write("### Diagnosis")

        st.info(row["diagnosis"])

        st.write("### Status")

        if row["status"] == "Critical":
            st.error("🔴 Critical")
        else:
            st.success("🟢 Stable")

    st.download_button(
        "📥 Download Patient Data",
        filtered.to_csv(index=False),
        "patients.csv",
        "text/csv",
    )