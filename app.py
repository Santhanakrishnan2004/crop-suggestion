# # import streamlit as st
# # import pickle
# # import numpy as np
# # from firebase_admin import credentials, initialize_app, db
# # import firebase_admin

# # # Firebase Configuration
# # FIREBASE_CREDENTIALS = "sdk.json"
# # DATABASE_URL = "https://crop-select-default-rtdb.asia-southeast1.firebasedatabase.app/"

# # # Initialize Firebase Admin SDK only if not already initialized
# # if not firebase_admin._apps:
# #     cred = credentials.Certificate(FIREBASE_CREDENTIALS)
# #     initialize_app(
# #         cred,
# #         {
# #             "databaseURL": DATABASE_URL,
# #         },
# #     )

# # # Load the trained models
# # CROP_MODEL_PATH = "modelcrop.pkl"
# # YIELD_MODEL_PATH = "yieldpreddtr.pkl"
# # with open(CROP_MODEL_PATH, "rb") as crop_model_file:
# #     crop_model = pickle.load(crop_model_file)
# # with open(YIELD_MODEL_PATH, "rb") as yield_model_file:
# #     yield_model = pickle.load(yield_model_file)

# # # Define crop names and demand
# # CROPS_AND_DEMAND = {
# #     1: {"name": "rice", "demand": "Moderate Demand"},
# #     2: {"name": "maize", "demand": "Moderate Demand"},
# #     3: {"name": "jute", "demand": "Low Demand"},
# #     4: {"name": "cotton", "demand": "Moderate Demand"},
# #     5: {"name": "coconut", "demand": "High Demand"},
# #     6: {"name": "papaya", "demand": "High Demand"},
# #     7: {"name": "orange", "demand": "High Demand"},
# #     8: {"name": "apple", "demand": "Low Demand"},
# #     9: {"name": "muskmelon", "demand": "Moderate Demand"},
# #     10: {"name": "watermelon", "demand": "High Demand"},
# #     11: {"name": "grapes", "demand": "High Demand"},
# #     12: {"name": "mango", "demand": "High Demand"},
# #     13: {"name": "banana", "demand": "High Demand"},
# #     14: {"name": "pomegranate", "demand": "Moderate Demand"},
# #     15: {"name": "lentil", "demand": "Moderate Demand"},
# #     16: {"name": "blackgram", "demand": "Moderate Demand"},
# #     17: {"name": "mungbean", "demand": "High Demand"},
# #     18: {"name": "mothbeans", "demand": "Low Demand"},
# #     19: {"name": "pigeonpeas", "demand": "Moderate Demand"},
# #     20: {"name": "kidneybeans", "demand": "Moderate Demand"},
# #     21: {"name": "chickpea", "demand": "Moderate Demand"},
# #     22: {"name": "coffee", "demand": "High Demand"},
# # }

# # # Add baseline yields for each crop (example values in tons per hectare)
# # BASELINE_YIELDS = {
# #     "rice": 2.5,
# #     "maize": 2.0,
# #     "jute": 1.8,
# #     "cotton": 1.6,
# #     "coconut": 3.0,
# #     "papaya": 5.0,
# #     "orange": 7.0,
# #     "apple": 3.5,
# #     "muskmelon": 3.0,
# #     "watermelon": 4.0,
# #     "grapes": 5.0,
# #     "mango": 6.0,
# #     "banana": 7.0,
# #     "pomegranate": 4.5,
# #     "lentil": 1.2,
# #     "blackgram": 1.5,
# #     "mungbean": 1.8,
# #     "mothbeans": 1.0,
# #     "pigeonpeas": 1.2,
# #     "kidneybeans": 1.8,
# #     "chickpea": 1.3,
# #     "coffee": 0.5,
# # }


# # # Fetch sensor data from Firebase
# # def get_sensor_data():
# #     sensors_ref = db.reference("sensors")
# #     all_data = sensors_ref.get()

# #     if not all_data:
# #         raise ValueError("No sensor data found in Firebase.")

# #     # Get the latest data by timestamp
# #     latest_timestamp = max(all_data.keys(), key=lambda t: t)
# #     return all_data[latest_timestamp]


# # # Map sensor data to model input for crop suggestion
# # def map_to_crop_model_input(sensor_data):
# #     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
# #     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
# #     ambient_temp = sensor_data.get("Ambient_Temperature_C", 0)
# #     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
# #     soil_pH = sensor_data.get("Soil_pH", 0)
# #     rainfall = sensor_data.get("Solar_Radiance_W_m2", 0) / 100  # Approximate rainfall

# #     # Split NPK into individual components (example ratios used here)
# #     N, P, K = npk_level * 0.4, npk_level * 0.3, npk_level * 0.3

# #     # Temperature and humidity
# #     temperature = (ambient_temp + soil_temp) / 2  # Average temperature
# #     humidity = soil_moisture  # Approximate humidity

# #     return [N, P, K, temperature, humidity, soil_pH, rainfall]


# # # Map sensor data to model input for yield prediction
# # def map_to_yield_model_input(sensor_data):
# #     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
# #     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
# #     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
# #     soil_pH = sensor_data.get("Soil_pH", 0)
# #     area = 1  # Encoded area for India
# #     year = 2024
# #     avg_rainfall = 924
# #     avg_temp = (soil_temp + sensor_data.get("Ambient_Temperature_C", 0)) / 2

# #     return [
# #         npk_level,
# #         soil_temp,
# #         soil_moisture,
# #         soil_pH,
# #         avg_rainfall,
# #         avg_temp,
# #         area,
# #         year,
# #         0,  # Placeholder for additional model-required features
# #         0,  # Placeholder
# #     ]


# # # Predict the top crops based on crop model
# # def predict_top_crops(input_features, top_n=3):
# #     input_array = np.array([input_features])  # Reshape input for prediction
# #     probabilities = crop_model.predict_proba(input_array)[0]

# #     top_indices = np.argsort(probabilities)[-top_n:][::-1]
# #     top_crops = [
# #         {
# #             "name": CROPS_AND_DEMAND.get(index, {"name": "Unknown"}).get(
# #                 "name", "Unknown"
# #             ),
# #             "demand": CROPS_AND_DEMAND.get(index, {"demand": "Unknown"}).get(
# #                 "demand", "Unknown"
# #             ),
# #             "probability": probabilities[index],
# #         }
# #         for index in top_indices
# #     ]
# #     return top_crops


# # # Predict yield for a given crop using yield model
# # def predict_yield(input_features, crop_name):
# #     input_array = np.array([input_features])
# #     predicted_yield = yield_model.predict(input_array)[0]

# #     # Calculate yield percentage based on baseline
# #     baseline_yield = BASELINE_YIELDS.get(crop_name.lower(), 1)  # Default baseline
# #     yield_percentage = (predicted_yield / baseline_yield) * 100

# #     return predicted_yield, yield_percentage


# # # Streamlit App
# # def main():
# #     st.title("Crop and Yield Suggestion System")
# #     st.write(
# #         "This tool uses sensor data and trained AI models to suggest suitable crops and predict their yield."
# #     )

# #     try:
# #         # Fetch and display sensor data
# #         sensor_data = get_sensor_data()

# #         st.subheader("Latest Sensor Data")
# #         st.json(sensor_data, expanded=False)

# #         # Map sensor data to model input for crop suggestion
# #         crop_input = map_to_crop_model_input(sensor_data)
# #         top_crops = predict_top_crops(crop_input)

# #         st.subheader("Suggested Crops")
# #         for crop in top_crops:
# #             st.write(
# #                 f"**{crop['name'].capitalize()}**: {crop['demand']} (Probability: {crop['probability']:.2f})"
# #             )

# #         # Select a crop to predict yield
# #         selected_crop = st.selectbox(
# #             "Select a crop to predict its yield:",
# #             [crop["name"] for crop in top_crops],
# #         )

# #         # Map sensor data to model input for yield prediction
# #         yield_input = map_to_yield_model_input(sensor_data)
# #         predicted_yield, yield_percentage = predict_yield(yield_input, selected_crop)

# #         st.subheader("Predicted Yield")
# #         st.write(
# #             f"The predicted yield for {selected_crop} is {predicted_yield:.2f} tons per hectare."
# #         )
# #         st.write(
# #             f"This is {yield_percentage:.2f}% of the baseline yield for {selected_crop}."
# #         )

# #     except ValueError as e:
# #         st.error(f"Error: {e}")
# #     except Exception as e:
# #         st.error(f"Unexpected error: {e}")


# # if __name__ == "__main__":
# #     main()
# import streamlit as st
# import pickle
# import numpy as np
# from firebase_admin import credentials, initialize_app, db
# import firebase_admin

# # Firebase Configuration
# FIREBASE_CREDENTIALS = "sdk.json"
# DATABASE_URL = "https://crop-select-default-rtdb.asia-southeast1.firebasedatabase.app/"

# # Initialize Firebase Admin SDK only if not already initialized
# if not firebase_admin._apps:
#     cred = credentials.Certificate(FIREBASE_CREDENTIALS)
#     initialize_app(
#         cred,
#         {
#             "databaseURL": DATABASE_URL,
#         },
#     )

# # Load the trained models
# CROP_MODEL_PATH = "modelcrop.pkl"
# YIELD_MODEL_PATH = "yieldpreddtr.pkl"
# with open(CROP_MODEL_PATH, "rb") as crop_model_file:
#     crop_model = pickle.load(crop_model_file)
# with open(YIELD_MODEL_PATH, "rb") as yield_model_file:
#     yield_model = pickle.load(yield_model_file)

# # Define crop names and demand
# CROPS_AND_DEMAND = {
#     1: {"name": "rice", "demand": "Moderate Demand"},
#     2: {"name": "maize", "demand": "Moderate Demand"},
#     3: {"name": "jute", "demand": "Low Demand"},
#     4: {"name": "cotton", "demand": "Moderate Demand"},
#     5: {"name": "coconut", "demand": "High Demand"},
#     6: {"name": "papaya", "demand": "High Demand"},
#     7: {"name": "orange", "demand": "High Demand"},
#     8: {"name": "apple", "demand": "Low Demand"},
#     9: {"name": "muskmelon", "demand": "Moderate Demand"},
#     10: {"name": "watermelon", "demand": "High Demand"},
#     11: {"name": "grapes", "demand": "High Demand"},
#     12: {"name": "mango", "demand": "High Demand"},
#     13: {"name": "banana", "demand": "High Demand"},
#     14: {"name": "pomegranate", "demand": "Moderate Demand"},
#     15: {"name": "lentil", "demand": "Moderate Demand"},
#     16: {"name": "blackgram", "demand": "Moderate Demand"},
#     17: {"name": "mungbean", "demand": "High Demand"},
#     18: {"name": "mothbeans", "demand": "Low Demand"},
#     19: {"name": "pigeonpeas", "demand": "Moderate Demand"},
#     20: {"name": "kidneybeans", "demand": "Moderate Demand"},
#     21: {"name": "chickpea", "demand": "Moderate Demand"},
#     22: {"name": "coffee", "demand": "High Demand"},
# }

# # Add baseline yields for each crop (example values in tons per hectare)
# BASELINE_YIELDS = {
#     "rice": 250000,
#     "maize": 20000,
#     "jute": 18000,
#     "cotton": 16000,
#     "coconut": 30000,
#     "papaya": 5.0,
#     "orange": 7.0,
#     "apple": 3.5,
#     "muskmelon": 3.0,
#     "watermelon": 4.0,
#     "grapes": 5.0,
#     "mango": 6.0,
#     "banana": 7.0,
#     "pomegranate": 4.5,
#     "lentil": 1.2,
#     "blackgram": 1.5,
#     "mungbean": 1.8,
#     "mothbeans": 1.0,
#     "pigeonpeas": 1.2,
#     "kidneybeans": 1.8,
#     "chickpea": 1.3,
#     "coffee": 0.5,
# }


# # Fetch sensor data from Firebase
# def get_sensor_data():
#     sensors_ref = db.reference("sensors")
#     all_data = sensors_ref.get()

#     if not all_data:
#         raise ValueError("No sensor data found in Firebase.")

#     # Get the latest data by timestamp
#     latest_timestamp = max(all_data.keys(), key=lambda t: t)
#     return all_data[latest_timestamp]


# # Map sensor data to model input for crop suggestion
# def map_to_crop_model_input(sensor_data):
#     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
#     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
#     ambient_temp = sensor_data.get("Ambient_Temperature_C", 0)
#     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
#     soil_pH = sensor_data.get("Soil_pH", 0)
#     rainfall = sensor_data.get("Solar_Radiance_W_m2", 0) / 100  # Approximate rainfall

#     # Split NPK into individual components (example ratios used here)
#     N, P, K = npk_level * 0.4, npk_level * 0.3, npk_level * 0.3

#     # Temperature and humidity
#     temperature = (ambient_temp + soil_temp) / 2  # Average temperature
#     humidity = soil_moisture  # Approximate humidity

#     return [N, P, K, temperature, humidity, soil_pH, rainfall]


# # Map sensor data to model input for yield prediction
# def map_to_yield_model_input(sensor_data):
#     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
#     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
#     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
#     soil_pH = sensor_data.get("Soil_pH", 0)
#     area = 1  # Encoded area for India
#     year = 2024
#     avg_rainfall = 924
#     avg_temp = (soil_temp + sensor_data.get("Ambient_Temperature_C", 0)) / 2

#     return [
#         npk_level,
#         soil_temp,
#         soil_moisture,
#         soil_pH,
#         avg_rainfall,
#         avg_temp,
#         area,
#         year,
#         0,  # Placeholder for additional model-required features
#         0,  # Placeholder
#     ]


# # Predict the top crops based on crop model
# def predict_top_crops(input_features, top_n=3):
#     input_array = np.array([input_features])  # Reshape input for prediction
#     probabilities = crop_model.predict_proba(input_array)[0]

#     top_indices = np.argsort(probabilities)[-top_n:][::-1]
#     top_crops = [
#         {
#             "name": CROPS_AND_DEMAND.get(index, {"name": "Unknown"}).get(
#                 "name", "Unknown"
#             ),
#             "demand": CROPS_AND_DEMAND.get(index, {"demand": "Unknown"}).get(
#                 "demand", "Unknown"
#             ),
#             "probability": probabilities[index],
#         }
#         for index in top_indices
#     ]
#     return top_crops


# # Predict yield for a given crop using yield model
# def predict_yield(input_features, crop_name):
#     input_array = np.array([input_features])
#     predicted_yield = yield_model.predict(input_array)[0]

#     # Calculate yield percentage based on baseline
#     baseline_yield = BASELINE_YIELDS.get(crop_name.lower(), 1)  # Default baseline
#     yield_percentage = (predicted_yield / baseline_yield) * 100

#     # Format the yield percentage to one decimal place
#     yield_percentage = round(yield_percentage, 1)

#     # Classify the demand based on yield percentage
#     if yield_percentage > 80:
#         demand_class = "High Demand"
#     elif 40 <= yield_percentage <= 80:
#         demand_class = "Moderate Demand"
#     else:
#         demand_class = "Low Demand"

#     return predicted_yield, yield_percentage, demand_class


# # Streamlit App
# def main():
#     st.title("Crop and Yield Suggestion System")
#     st.write(
#         "This tool uses sensor data and trained AI models to suggest suitable crops and predict their yield."
#     )

#     try:
#         # Fetch and display sensor data
#         sensor_data = get_sensor_data()

#         st.subheader("Latest Sensor Data")
#         st.json(sensor_data, expanded=False)

#         # Map sensor data to model input for crop suggestion
#         crop_input = map_to_crop_model_input(sensor_data)
#         top_crops = predict_top_crops(crop_input)

#         st.subheader("Suggested Crops")
#         for crop in top_crops:
#             st.write(
#                 f"**{crop['name'].capitalize()}**: {crop['demand']} (Probability: {crop['probability']:.2f})"
#             )

#         # Select a crop to predict yield
#         selected_crop = st.selectbox(
#             "Select a crop to predict its yield:",
#             [crop["name"] for crop in top_crops],
#         )

#         # Map sensor data to model input for yield prediction
#         yield_input = map_to_yield_model_input(sensor_data)
#         predicted_yield, yield_percentage, demand_class = predict_yield(
#             yield_input, selected_crop
#         )

#         st.subheader("Predicted Yield")
#         st.write(
#             f"The predicted yield for {selected_crop} is {predicted_yield:.2f} tons per hectare."
#         )
#         st.write(
#             f"This is {yield_percentage} % of the baseline yield for {selected_crop}."
#         )
#         st.write(f"Demand classification based on yield: {demand_class}")

#     except ValueError as e:
#         st.error(f"Error: {e}")
#     except Exception as e:
#         st.error(f"Unexpected error: {e}")


# if __name__ == "__main__":
#     main()
# import streamlit as st
# import pickle
# import numpy as np
# from firebase_admin import credentials, initialize_app, db
# import firebase_admin

# # Firebase Configuration
# FIREBASE_CREDENTIALS = "sdk.json"
# DATABASE_URL = "https://crop-select-default-rtdb.asia-southeast1.firebasedatabase.app/"

# # Initialize Firebase Admin SDK only if not already initialized
# if not firebase_admin._apps:
#     cred = credentials.Certificate(FIREBASE_CREDENTIALS)
#     initialize_app(
#         cred,
#         {
#             "databaseURL": DATABASE_URL,
#         },
#     )

# # Load the trained models
# CROP_MODEL_PATH = "modelcrop.pkl"
# YIELD_MODEL_PATH = "yieldpreddtr.pkl"
# with open(CROP_MODEL_PATH, "rb") as crop_model_file:
#     crop_model = pickle.load(crop_model_file)
# with open(YIELD_MODEL_PATH, "rb") as yield_model_file:
#     yield_model = pickle.load(yield_model_file)

# # Define crop names and demand
# CROPS_AND_DEMAND = {
#     1: {"name": "rice", "demand": "Moderate Demand"},
#     2: {"name": "maize", "demand": "Moderate Demand"},
#     3: {"name": "jute", "demand": "Low Demand"},
#     4: {"name": "cotton", "demand": "Moderate Demand"},
#     5: {"name": "coconut", "demand": "High Demand"},
#     6: {"name": "papaya", "demand": "High Demand"},
#     7: {"name": "orange", "demand": "High Demand"},
#     8: {"name": "apple", "demand": "Low Demand"},
#     9: {"name": "muskmelon", "demand": "Moderate Demand"},
#     10: {"name": "watermelon", "demand": "High Demand"},
#     11: {"name": "grapes", "demand": "High Demand"},
#     12: {"name": "mango", "demand": "High Demand"},
#     13: {"name": "banana", "demand": "High Demand"},
#     14: {"name": "pomegranate", "demand": "Moderate Demand"},
#     15: {"name": "lentil", "demand": "Moderate Demand"},
#     16: {"name": "blackgram", "demand": "Moderate Demand"},
#     17: {"name": "mungbean", "demand": "High Demand"},
#     18: {"name": "mothbeans", "demand": "Low Demand"},
#     19: {"name": "pigeonpeas", "demand": "Moderate Demand"},
#     20: {"name": "kidneybeans", "demand": "Moderate Demand"},
#     21: {"name": "chickpea", "demand": "Moderate Demand"},
#     22: {"name": "coffee", "demand": "High Demand"},
# }

# # Add baseline yields for each crop (updated values in tons per hectare)
# BASELINE_YIELDS = {
#     "rice": 2500,
#     "maize": 2000,
#     "jute": 1800,
#     "cotton": 1600,
#     "coconut": 3000,
#     "papaya": 5.0,
#     "orange": 7.0,
#     "apple": 3.5,
#     "muskmelon": 3.0,
#     "watermelon": 4.0,
#     "grapes": 5.0,
#     "mango": 6.0,
#     "banana": 7.0,
#     "pomegranate": 4.5,
#     "lentil": 1.2,
#     "blackgram": 1.5,
#     "mungbean": 1.8,
#     "mothbeans": 1.0,
#     "pigeonpeas": 1.2,
#     "kidneybeans": 1.8,
#     "chickpea": 1.3,
#     "coffee": 0.5,
# }


# # Fetch sensor data from Firebase
# def get_sensor_data():
#     sensors_ref = db.reference("sensors")
#     all_data = sensors_ref.get()

#     if not all_data:
#         raise ValueError("No sensor data found in Firebase.")

#     # Get the latest data by timestamp
#     latest_timestamp = max(all_data.keys(), key=lambda t: t)
#     return all_data[latest_timestamp]


# # Map sensor data to model input for crop suggestion
# def map_to_crop_model_input(sensor_data):
#     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
#     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
#     ambient_temp = sensor_data.get("Ambient_Temperature_C", 0)
#     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
#     soil_pH = sensor_data.get("Soil_pH", 0)
#     rainfall = sensor_data.get("Solar_Radiance_W_m2", 0) / 100  # Approximate rainfall

#     # Split NPK into individual components (example ratios used here)
#     N, P, K = npk_level * 0.4, npk_level * 0.3, npk_level * 0.3

#     # Temperature and humidity
#     temperature = (ambient_temp + soil_temp) / 2  # Average temperature
#     humidity = soil_moisture  # Approximate humidity

#     return [N, P, K, temperature, humidity, soil_pH, rainfall]


# # Map sensor data to model input for yield prediction
# def map_to_yield_model_input(sensor_data):
#     npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
#     soil_temp = sensor_data.get("Soil_Temperature_C", 0)
#     soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
#     soil_pH = sensor_data.get("Soil_pH", 0)
#     area = 1  # Encoded area for India
#     year = 2024
#     avg_rainfall = 924
#     avg_temp = (soil_temp + sensor_data.get("Ambient_Temperature_C", 0)) / 2

#     return [
#         npk_level,
#         soil_temp,
#         soil_moisture,
#         soil_pH,
#         avg_rainfall,
#         avg_temp,
#         area,
#         year,
#         0,  # Placeholder for additional model-required features
#         0,  # Placeholder
#     ]


# # Predict the top crops based on crop model
# def predict_top_crops(input_features, top_n=3):
#     input_array = np.array([input_features])  # Reshape input for prediction
#     probabilities = crop_model.predict_proba(input_array)[0]

#     top_indices = np.argsort(probabilities)[-top_n:][::-1]
#     top_crops = [
#         {
#             "name": CROPS_AND_DEMAND.get(index, {"name": "Unknown"}).get(
#                 "name", "Unknown"
#             ),
#             "demand": CROPS_AND_DEMAND.get(index, {"demand": "Unknown"}).get(
#                 "demand", "Unknown"
#             ),
#             "probability": probabilities[index],
#         }
#         for index in top_indices
#     ]
#     return top_crops


# # Predict yield for a given crop using yield model
# def predict_yield(input_features, crop_name):
#     input_array = np.array([input_features])
#     predicted_yield = yield_model.predict(input_array)[0]

#     # Calculate yield percentage based on baseline
#     baseline_yield = BASELINE_YIELDS.get(crop_name.lower(), 1)  # Default baseline
#     yield_percentage = (predicted_yield / baseline_yield) * 100

#     return predicted_yield, yield_percentage


# # Streamlit App
# def main():
#     st.title("Crop and Yield Suggestion System")
#     st.write(
#         "This tool uses sensor data and trained AI models to suggest suitable crops and predict their yield."
#     )

#     try:
#         # Fetch and display sensor data
#         sensor_data = get_sensor_data()

#         st.subheader("Latest Sensor Data")
#         st.json(sensor_data, expanded=False)

#         # Map sensor data to model input for crop suggestion
#         crop_input = map_to_crop_model_input(sensor_data)
#         top_crops = predict_top_crops(crop_input)

#         st.subheader("Suggested Crops")
#         for crop in top_crops:
#             st.write(
#                 f"**{crop['name'].capitalize()}**: {crop['demand']} (Probability: {crop['probability']:.2f})"
#             )

#         # Select a crop to predict yield
#         selected_crop = st.selectbox(
#             "Select a crop to predict its yield:",
#             [crop["name"] for crop in top_crops],
#         )

#         # Map sensor data to model input for yield prediction
#         yield_input = map_to_yield_model_input(sensor_data)
#         predicted_yield, yield_percentage = predict_yield(yield_input, selected_crop)

#         st.subheader("Predicted Yield")
#         st.write(
#             f"The predicted yield for {selected_crop} is {predicted_yield:.2f} tons per hectare."
#         )
#         st.write(
#             f"This is {yield_percentage:.2f}% of the baseline yield for {selected_crop}."
#         )

#     except ValueError as e:
#         st.error(f"Error: {e}")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}")


# if __name__ == "__main__":
#     main()
import streamlit as st
import pickle
import numpy as np
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# Firebase Configuration
FIREBASE_CREDENTIALS = "sdk.json"
DATABASE_URL = "https://crop-select-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Initialize Firebase Admin SDK only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    initialize_app(
        cred,
        {
            "databaseURL": DATABASE_URL,
        },
    )

# Load the trained models
CROP_MODEL_PATH = "modelcrop.pkl"
YIELD_MODEL_PATH = "yieldpreddtr.pkl"
with open(CROP_MODEL_PATH, "rb") as crop_model_file:
    crop_model = pickle.load(crop_model_file)
with open(YIELD_MODEL_PATH, "rb") as yield_model_file:
    yield_model = pickle.load(yield_model_file)

# Define crop names and demand
CROPS_AND_DEMAND = {
    1: {"name": "rice", "demand": "Moderate Demand"},
    2: {"name": "maize", "demand": "Moderate Demand"},
    3: {"name": "jute", "demand": "Low Demand"},
    4: {"name": "cotton", "demand": "Moderate Demand"},
    5: {"name": "coconut", "demand": "High Demand"},
    6: {"name": "papaya", "demand": "High Demand"},
    7: {"name": "orange", "demand": "High Demand"},
    8: {"name": "apple", "demand": "Low Demand"},
    9: {"name": "muskmelon", "demand": "Moderate Demand"},
    10: {"name": "watermelon", "demand": "High Demand"},
    11: {"name": "grapes", "demand": "High Demand"},
    12: {"name": "mango", "demand": "High Demand"},
    13: {"name": "banana", "demand": "High Demand"},
    14: {"name": "pomegranate", "demand": "Moderate Demand"},
    15: {"name": "lentil", "demand": "Moderate Demand"},
    16: {"name": "blackgram", "demand": "Moderate Demand"},
    17: {"name": "mungbean", "demand": "High Demand"},
    18: {"name": "mothbeans", "demand": "Low Demand"},
    19: {"name": "pigeonpeas", "demand": "Moderate Demand"},
    20: {"name": "kidneybeans", "demand": "Moderate Demand"},
    21: {"name": "chickpea", "demand": "Moderate Demand"},
    22: {"name": "coffee", "demand": "High Demand"},
}

# Add baseline yields for each crop (updated values in tons per hectare)
BASELINE_YIELDS = {
    "rice": 2500,
    "maize": 2000,
    "jute": 1800,
    "cotton": 1600,
    "coconut": 3000,
    "papaya": 5.0,
    "orange": 7.0,
    "apple": 3.5,
    "muskmelon": 3.0,
    "watermelon": 4.0,
    "grapes": 5.0,
    "mango": 6.0,
    "banana": 7.0,
    "pomegranate": 4.5,
    "lentil": 1.2,
    "blackgram": 1.5,
    "mungbean": 1.8,
    "mothbeans": 1.0,
    "pigeonpeas": 1.2,
    "kidneybeans": 1.8,
    "chickpea": 1.3,
    "coffee": 0.5,
}


# Fetch sensor data from Firebase
def get_sensor_data():
    sensors_ref = db.reference("sensors")
    all_data = sensors_ref.get()

    if not all_data:
        raise ValueError("No sensor data found in Firebase.")

    # Get the latest data by timestamp
    latest_timestamp = max(all_data.keys(), key=lambda t: t)
    return all_data[latest_timestamp]


# Map sensor data to model input for crop suggestion
def map_to_crop_model_input(sensor_data):
    npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
    soil_temp = sensor_data.get("Soil_Temperature_C", 0)
    ambient_temp = sensor_data.get("Ambient_Temperature_C", 0)
    soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
    soil_pH = sensor_data.get("Soil_pH", 0)
    rainfall = sensor_data.get("Solar_Radiance_W_m2", 0) / 100  # Approximate rainfall

    # Split NPK into individual components (example ratios used here)
    N, P, K = npk_level * 0.4, npk_level * 0.3, npk_level * 0.3

    # Temperature and humidity
    temperature = (ambient_temp + soil_temp) / 2  # Average temperature
    humidity = soil_moisture  # Approximate humidity

    return [N, P, K, temperature, humidity, soil_pH, rainfall]


# Map sensor data to model input for yield prediction
def map_to_yield_model_input(sensor_data):
    npk_level = sensor_data.get("NPK_Level_mg_kg", 0)
    soil_temp = sensor_data.get("Soil_Temperature_C", 0)
    soil_moisture = sensor_data.get("Soil_Moisture_Percentage", 0)
    soil_pH = sensor_data.get("Soil_pH", 0)
    area = 1  # Encoded area for India
    year = 2024
    avg_rainfall = 924
    avg_temp = (soil_temp + sensor_data.get("Ambient_Temperature_C", 0)) / 2

    return [
        npk_level,
        soil_temp,
        soil_moisture,
        soil_pH,
        avg_rainfall,
        avg_temp,
        area,
        year,
        0,  # Placeholder for additional model-required features
        0,  # Placeholder
    ]


# Predict the top crops based on crop model
def predict_top_crops(input_features, top_n=3):
    input_array = np.array([input_features])  # Reshape input for prediction
    probabilities = crop_model.predict_proba(input_array)[0]

    top_indices = np.argsort(probabilities)[-top_n:][::-1]
    top_crops = [
        {
            "name": CROPS_AND_DEMAND.get(index, {"name": "Unknown"}).get(
                "name", "Unknown"
            ),
            "demand": CROPS_AND_DEMAND.get(index, {"demand": "Unknown"}).get(
                "demand", "Unknown"
            ),
            "probability": probabilities[index],
        }
        for index in top_indices
    ]
    return top_crops


# Predict yield for a given crop using yield model
def predict_yield(input_features, crop_name):
    input_array = np.array([input_features])
    predicted_yield = yield_model.predict(input_array)[0]

    # Calculate yield percentage based on baseline
    baseline_yield = BASELINE_YIELDS.get(crop_name.lower(), 1)  # Default baseline
    yield_percentage = (predicted_yield / baseline_yield) * 100

    # Scale down the yield percentage for display (to avoid overly large numbers)
    scaled_yield_percentage = round(yield_percentage / 100, 1)

    return predicted_yield, scaled_yield_percentage


# Streamlit App
def main():
    st.title("Crop and Yield Suggestion System")
    st.write(
        "This tool uses sensor data and trained AI models to suggest suitable crops and predict their yield."
    )

    try:
        # Fetch and display sensor data
        sensor_data = get_sensor_data()

        st.subheader("Latest Sensor Data")
        st.json(sensor_data, expanded=False)

        # Map sensor data to model input for crop suggestion
        crop_input = map_to_crop_model_input(sensor_data)
        top_crops = predict_top_crops(crop_input)
        st.header("Based on the current paramters :")
        st.subheader("Suggested Crops")
        for crop in top_crops:
            # Classify demand based on the probability
            demand_value = crop["probability"] * 100  # Scaled demand value
            # If the probability is greater than 75%, set demand to "High Demand"
            if demand_value >= 75:
                demand = "High Demand"
            else:
                demand = CROPS_AND_DEMAND.get(top_crops.index(crop) + 1, {}).get(
                    "demand", "Unknown"
                )

            st.write(
                f"**{crop['name'].capitalize()}**: {demand} (Sucess rate: {crop['probability'] * 100:.1f}%)"
            )

        # Select a crop to predict yield
        selected_crop = st.selectbox(
            "Select a crop to predict its yield:",
            [crop["name"] for crop in top_crops],
        )

        # Map sensor data to model input for yield prediction
        yield_input = map_to_yield_model_input(sensor_data)
        predicted_yield, yield_percentage = predict_yield(yield_input, selected_crop)

        st.subheader("Predicted Yield")
        st.write(
            f"The predicted yield for {selected_crop} is {predicted_yield:.2f} hg/ha."
        )
        st.write(
            f"This is {yield_percentage:.2f}% of the baseline yield for {selected_crop}."
        )

    except ValueError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
