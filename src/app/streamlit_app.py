import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

API_URL = "http://api:8000"
TIMEOUT = 5

st.title("Housing Price Estimator with Batch Visualization")

# -----------------------
# SINGLE PREDICTION
# -----------------------
st.header("Single Prediction")

size = st.slider("Size (m²)", 20, 200, 50)
n_rooms = st.slider("Number of rooms", 1, 5, 2)
quality = st.selectbox("Quality", ["Low", "Medium", "High"])

if st.button("Predict"):
    try:
        with st.spinner("Calculating prediction..."):
            response = requests.get(
                f"{API_URL}/predict",
                params={"size": size, "n_rooms": n_rooms, "quality": quality},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            st.success(f"Predicted price: {round(response.json()['predicted_price'], 2)}")
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")

# -----------------------
# BATCH PREDICTION
# -----------------------
st.divider()
st.header("Batch Prediction from CSV")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error("Invalid CSV file!")
        st.stop()

    required_cols = {"size", "n_rooms", "quality"}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain the columns: size, n_rooms, quality")
        st.stop()

    # Store dataframe in session_state to preserve across reruns
    # session state = memory store for the app
    st.session_state["df_uploaded"] = df

    st.subheader("Uploaded Data Preview")
    st.dataframe(df.head())

if "df_uploaded" in st.session_state:
    if st.button("Run Batch Prediction"):
        try:
            payload = st.session_state["df_uploaded"].to_dict(orient="records")
            with st.spinner("Running batch prediction..."):
                response = requests.post(
                    f"{API_URL}/batch_predict",
                    json=payload,
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                preds = response.json()["predictions"]

            st.session_state["df_predicted"] = st.session_state["df_uploaded"].copy()
            st.session_state["df_predicted"]["predicted_price"] = preds

            st.success("Batch prediction completed!")
            st.dataframe(st.session_state["df_predicted"])

        except requests.exceptions.RequestException as e:
            st.error(f"API error during batch prediction: {e}")
        except KeyError:
            st.error("Invalid API response format!")

if "df_predicted" in st.session_state and st.button("Generate charts"):
    df = st.session_state["df_predicted"].copy()
    df["predicted_price"] = pd.to_numeric(df["predicted_price"])

    st.divider()
    st.header("Prediction Visualization")

    # Layout in 2 columns
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Scatter plot: size vs predicted price
    with col1:
        st.subheader("Size vs Predicted Price")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x="size", y="predicted_price", hue="quality", palette="coolwarm", ax=ax)
        plt.xlabel("Size (m2)")
        plt.ylabel("Predicted Price")
        st.pyplot(fig)

    # Histogram of predicted prices
    with col2:
        st.subheader("Predicted Price Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(df["predicted_price"], bins=40, kde=True, color="skyblue", ax=ax2)
        plt.xlabel("Predicted Price")
        plt.ylabel("Frequency")
        st.pyplot(fig2)

    # Boxplot: predicted price vs number of rooms
    with col3:
        st.subheader("Predicted Price vs Rooms")
        fig3, ax3 = plt.subplots()
        sns.boxplot(data=df, x="n_rooms", y="predicted_price", palette="Set2", ax=ax3)
        plt.xlabel("Number of Rooms")
        plt.ylabel("Predicted Price")
        st.pyplot(fig3)

    # Correlation map
    with col4:
        st.subheader("Correlation Heatmap")
        corr = df[["size", "n_rooms", "quality", "predicted_price"]].corr()
        fig4, ax4 = plt.subplots()
        cax = ax4.matshow(corr, cmap="coolwarm")
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.colorbar(cax)
        st.pyplot(fig4)
