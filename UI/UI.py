import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import joblib as jl
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA, TruncatedSVD

df = pd.read_csv("DataVersion3.csv")


def main():    

    html_temp="""
    <div style = "background-color: #a1d8ff; padding: 16px;">
    <h2 style="color: #4790f6; text-align:center;"> Simple Car Price Prediction App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.write("")
    st.write("""            
    ##### Do you need a help with predicting your wanted car's price?
    ##### We will help you!
    ##### Answer our questions and the result will be showed to you!
            """)
    st.write("")
    
    input_feature = user_input_feature()
    processed_feature = processing(input_feature)
    model = jl.load("best_model.joblib")
    

    
    try:
        if st.button("Predict"):
            price_predict = float(model.predict(processed_feature))
            price_predict_in_vnd = transform_to_vnd(price_predict)
            if price_predict > 0:
                st.balloons()
                st.success(f"You can sell/buy that car for {price_predict_in_vnd}")
            else:
                st.warning("You are not able to sell/buy that car!!!")
    except Exception as e:
        st.warning(e)

def user_input_feature():
    origin = st.selectbox("Which is your wanted car's origin?",("Domestic assembly","Imported"))
    st.write("")

    car_model = st.selectbox("Which is your wanted car's model?",('Truck', 'SUV', 'Crossover', 'Van/Minivan', 'Pickup', 'Sedan',
       'Hatchback', 'Wagon', 'Coupe', 'Convertible/Cabriolet'))
    st.write("")
    car_name = st.selectbox("What is your wanted car's name?",(df['car_name'].unique().tolist()))
    st.write("")
    year_of_manufacture = int(st.number_input("Which year is that car produced?"))
    st.write("")
    mileage = st.number_input("How much mileage your wanted car had gone?")
    st.write("")
    exterior_color = st.selectbox("Which exterior color does that car have?", (df['exterior_color'].unique().tolist()))
    st.write("")
    interior_color = st.selectbox("Which interior color does that car have?",(df['interior_color'].unique().tolist()))
    st.write("")
    num_of_doors = st.number_input("How many doors does that car have?")
    st.write("")
    seating_capacity = st.number_input("How many seats does that car have?")
    st.write("")
    engine = st.selectbox("Which engine does that car use?", (df['engine'].unique().tolist()))
    st.write("")
    engine_capacity = st.number_input("How much capacity of that engine?")
    st.write("")
    fuel_consumption = st.number_input("How much fuel consumption does that car have?")
    st.write("")
    transmission = st.selectbox("Which type of transmission of that car?",(df['transmission'].unique().tolist()))
    st.write("")
    drive_type = st.selectbox("Which type of drive that car use?",(df["drive_type"].unique().tolist()))
    
    data = {
        'origin': origin,
        'car_model': car_model,
        'exterior_color': exterior_color,
        'interior_color': interior_color,
        'engine': engine,
        'transmission': transmission,
        'drive_type': drive_type,
        'car_name': car_name,
        'num_of_doors':num_of_doors,
        'seating_capacity': seating_capacity,
        'engine_capacity': engine_capacity,
        'fuel_consumption': fuel_consumption,
        'mileage': mileage,
        'year_of_manufacture': year_of_manufacture
    }
    features = pd.DataFrame(data, index=[0])
    return features    
    
def processing(data):
    process_model = jl.load("stacking_processing.pkl")
    processed_data = process_model.transform(data)
    return processed_data

def transform_to_vnd(price_in_billion):
    price_in_vnd = price_in_billion * 10 ** 9
    return f"{price_in_vnd:,.0f} VND"
if __name__ == "__main__":
    main()