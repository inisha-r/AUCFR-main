import pandas as pd
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from geopy.distance import geodesic
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection details
username = 'inishasallove19'
password = 'pro123'
cluster_address = "aucfr.30wmt.mongodb.net"
database_name = "AUCFR"

# Construct the MongoDB connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster_address}/{database_name}?retryWrites=true&w=majority"
mongo_client = MongoClient(connection_string)
db = mongo_client[database_name]
suppliers_collection = db['suppliers']

print("Connected to MongoDB successfully!")

# Predefined city coordinates
city_coords = {
    'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
        'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
        'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
        'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
        'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
        'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
        'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
        'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
        'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
        'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
        'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
        'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
        'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
        'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
        'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
        'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
        'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
        'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
        'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
        'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
        'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
        'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
        'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
}

# Function to calculate distance to Gurgaon
def calculate_distance_to_gurgaon(city):
    gurgaon_coords = city_coords.get('Gurgaon', (28.4595, 77.0266))
    return geodesic(gurgaon_coords, city_coords.get(city, gurgaon_coords)).kilometers

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input data
        data = request.json
        user_city = data.get('city', '').strip()

        # Calculate user city distance
        user_distance = calculate_distance_to_gurgaon(user_city) if user_city in city_coords else 100

        # Fetch supplier data from MongoDB
        suppliers_data = list(suppliers_collection.find())
        if not suppliers_data:
            return jsonify({"error": "No supplier data found"}), 400

        # Transform MongoDB data into a DataFrame
        suppliers_df = pd.DataFrame([
            {
                "FACADE VENDOR": supplier.get("name"),
                "Turn Over": supplier.get("turnover", 0),
                "Engineering Staff/Capacity": supplier.get("engineering_capacity", 0),
                "Past Similar projects": supplier.get("similar_projects", 0),
                "Production Capacity": supplier.get("production_capacity", 0),
                "ISO Certified": supplier.get("isocertified", 0),
                "HSE Policy": supplier.get("hse_policy", 0),
                "QA/ QC Policy": supplier.get("qa_qc_policy", 0),
                "Installation Capacity": supplier.get("installation_capacity", 0),
                "Annual Turnover - In Cr": supplier.get("annual_turnover", 0),
                "Unit Per Day Capacity": supplier.get("unit_per_day_capacity", 0),
                "Panel Prod. Capacity Per day": supplier.get("panel_capacity", 0),
                "Distance of Factory from Gurgaon (Kms)": supplier.get("distancefromgurgaon", user_distance),
            }
            for supplier in suppliers_data
        ])

        # Define features and target
        features = [
            "Turn Over", "Engineering Staff/Capacity", "Past Similar projects",
            "Production Capacity", "ISO Certified", "HSE Policy", "QA/ QC Policy",
            "Installation Capacity", "Annual Turnover - In Cr", "Unit Per Day Capacity",
            "Panel Prod. Capacity Per day", "Distance of Factory from Gurgaon (Kms)"
        ]
        target = "Average Rating"  # Replace with the actual target variable

        # Check if target exists in data
        if target not in suppliers_df.columns:
            suppliers_df[target] = 0  # Placeholder, replace with actual data

        # Split data into train and test
        X = suppliers_df[features]
        y = suppliers_df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train XGBoost Regressor
        model = XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                             max_depth=5, alpha=10, n_estimators=10)
        model.fit(X_train, y_train)

        # Predict and rank vendors
        suppliers_df["Predicted Ranking Score"] = model.predict(X)
        suppliers_df["Rank"] = suppliers_df["Predicted Ranking Score"].rank(ascending=False)

        # Prepare ranked vendors
        ranked_vendors = suppliers_df[["FACADE VENDOR", "Rank", "Predicted Ranking Score"]].sort_values(by="Rank")

        # Return JSON response
        return jsonify(ranked_vendors.to_dict(orient="records"))

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)















# # app.py
# import pandas as pd

# from flask import Flask, request, jsonify
# from sklearn.preprocessing import LabelEncoder
# from xgboost import XGBClassifier
# from geopy.distance import geodesic
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# # Load and prepare your model (you might want to save and load your trained model using joblib)
# city_coordinates = {
#     'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
#     'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
#     'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
#     'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
#     'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
#     'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
#     'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
#     'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
#     'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
#     'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
#     'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
#     'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
#     'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
#     'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
#     'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
#     'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
#     'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
#     'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
#     'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
#     'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
#     'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
#     'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
#     'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
#     'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
# }
# # Initialize the model
# xgb_model = XGBClassifier()

# # Function to calculate distance
# def calculate_distance_to_gurgaon(user_place):
#     gurgaon_coords = city_coordinates['Gurgaon']
#     if user_place in city_coordinates:
#         user_place_coords = city_coordinates[user_place]
#         return geodesic(gurgaon_coords, user_place_coords).kilometers
#     else:
#         return None

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     user_place = data.get('city')
    
#     # Calculate distance to Gurgaon
#     distance = calculate_distance_to_gurgaon(user_place)
#     if distance is None:
#         return jsonify({"error": "Invalid location"}), 400
    
#     # Load and preprocess your vendor data
#     vendordata = pd.read_csv('C:\\Users\\ADMIN\\Desktop\\Sample-main (4)\\Sample-main\\src\\vendor_data.csv')
#     technicalrating = pd.read_csv('C:\\Users\\ADMIN\\Desktop\\Sample-main (4)\\Sample-main\\src\\tech_rating.csv')

#     vendordata.columns = vendordata.columns.str.strip()
#     technicalrating.columns = technicalrating.columns.str.strip()

#     merged_data = pd.merge(vendordata, technicalrating, on='FACADE VENDOR')
#     merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

#     # Update distance in the dataframe
#     merged_data['Distance of Factory from Gurgaon (Kms)'] = distance
    
#     # Process categorical columns
#     le = LabelEncoder()
#     for column in merged_data.select_dtypes(include=['object']).columns:
#         merged_data[column] = le.fit_transform(merged_data[column])

#     merged_data['Recommended'] = merged_data['Recommended'].apply(lambda x: 1 if x == 'YES' else 0)

#     # Define features and target
#     X = merged_data.drop(columns=['FACADE VENDOR', 'Recommended'])
#     y = merged_data['Recommended']

#     # Load your pre-trained model (if using joblib to save/load)
#     xgb_model = joblib.load('C:\\Users\\ADMIN\\Desktop\\Sample-main (4)\\Sample-main\\src\\vendor_selection_model.joblib')

#     # Predict using the model
#     xgb_model.fit(X, y)  # Train the model again or use the previously trained model
#     predictions = xgb_model.predict(X)

#     # Ranking logic can be applied here if needed

#     # Return predictions and rankings
#     return jsonify({
#         "predictions": predictions.tolist(),
#         "distance": distance
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

# import pandas as pd
# import joblib
# from flask import Flask, request, jsonify
# from sklearn.preprocessing import LabelEncoder
# from xgboost import XGBClassifier
# from geopy.distance import geodesic
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load your model once when the app startsC:\Users\PRIYA\Downloads\FE\Sample-main\src\vendor_selection_model.joblib
# xgb_model = joblib.load('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\vendor_selection_model.joblib')

# city_coordinates = {
#     'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
#     'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
#     'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
#     'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
#     'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
#     'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
#     'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
#     'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
#     'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
#     'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
#     'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
#     'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
#     'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
#     'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
#     'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
#     'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
#     'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
#     'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
#     'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
#     'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
#     'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
#     'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
#     'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
#     'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
# }

# # Function to calculate distance
# def calculate_distance_to_gurgaon(user_place):
#     gurgaon_coords = city_coordinates.get('Gurgaon')
#     if user_place in city_coordinates:
#         user_place_coords = city_coordinates[user_place]
#         return geodesic(gurgaon_coords, user_place_coords).kilometers
#     return None

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     user_place = data.get('city')

#     # Calculate distance to Gurgaon
#     distance = calculate_distance_to_gurgaon(user_place)
#     if distance is None:
#         return jsonify({"error": "Invalid location"}), 400
    
#     # Load and preprocess vendor data
#     vendordata = pd.read_csv('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\vendor_data.csv')
#     technicalrating = pd.read_csv('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\tech_rating.csv')

#     vendordata.columns = vendordata.columns.str.strip()
#     technicalrating.columns = technicalrating.columns.str.strip()

#     merged_data = pd.merge(vendordata, technicalrating, on='FACADE VENDOR')
#     merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

#     # Update distance in the dataframe
#     merged_data['Distance of Factory from Gurgaon (Kms)'] = distance

#     # Process categorical columns
#     le = LabelEncoder()
#     for column in merged_data.select_dtypes(include=['object']).columns:
#         merged_data[column] = le.fit_transform(merged_data[column])

#     merged_data['Recommended'] = merged_data['Recommended'].apply(lambda x: 1 if x == 'YES' else 0)

#     # Define features and target
#     X = merged_data.drop(columns=['FACADE VENDOR', 'Recommended'])
#     y = merged_data['Recommended']

#     # Predict using the pre-trained model
#     predictions = xgb_model.predict(X)

#     # Add predictions to the dataframe for further analysis if needed
#     merged_data['Predictions'] = predictions

#     # Return predictions and distance
#     return jsonify({
#         "predictions": predictions.tolist(),
#         "distance": distance,
#         "ranked_data": merged_data[['FACADE VENDOR', 'Predictions', 'Distance of Factory from Gurgaon (Kms)']].to_dict(orient='records')
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)










# import pandas as pd
# import joblib
# from flask import Flask, request, jsonify
# from sklearn.preprocessing import LabelEncoder
# from xgboost import XGBClassifier
# from geopy.distance import geodesic
# from flask_cors import CORS
# from pymongo import MongoClient

# app = Flask(__name__)
# CORS(app)

# # Load your model once when the app starts
# xgb_model = joblib.load('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\vendor_selection_model.joblib')
# from urllib.parse import quote_plus
# from pymongo import MongoClient
# from urllib.parse import quote_plus

# username = 'inishasallove19'  # Replace with your actual username
# password = 'pro123'  # Properly escape special characters
# cluster_address = "aucfr.30wmt.mongodb.net"
# database_name = "AUCFR"  # Specify your database name

# # Construct the connection string
# connection_string = f"mongodb+srv://{username}:{password}@{cluster_address}/{database_name}?retryWrites=true&w=majority"

# # Initialize the client and access the database
# mongo_client = MongoClient(connection_string)
# db = mongo_client[database_name]
# suppliers_collection = db['suppliers']

# print("Connected to MongoDB successfully!")


# city_coordinates = {
    # 'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
    # 'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
    # 'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
    # 'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
    # 'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
    # 'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
    # 'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
    # 'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
    # 'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
    # 'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
    # 'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
    # 'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
    # 'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
    # 'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
    # 'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
    # 'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
    # 'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
    # 'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
    # 'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
    # 'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
    # 'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
    # 'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
    # 'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
    # 'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
# }

# # Function to calculate distance
# def calculate_distance_to_gurgaon(user_place):
#     gurgaon_coords = city_coordinates.get('Gurgaon')
#     if user_place in city_coordinates:
#         user_place_coords = city_coordinates[user_place]
#         return geodesic(gurgaon_coords, user_place_coords).kilometers
#     return None

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     user_place = data.get('city')

#     # Calculate distance to Gurgaon
#     distance = calculate_distance_to_gurgaon(user_place)
#     if distance is None:
#         return jsonify({"error": "Invalid location"}), 400

#     # Fetch supplier data from MongoDB
#     suppliers_data = list(suppliers_collection.find())
#     if not suppliers_data:
#         return jsonify({"error": "No supplier data found"}), 400

#     # Transform MongoDB data to a DataFrame
#     suppliers_df = []
#     for supplier in suppliers_data:
#         row = {
#             "name": supplier.get("name"),
#             "factorylocation": next((param["value"] for param in supplier["parameters"] if param["name"] == "factorylocation"), None),
#             "distancefromgurgaon": next((param["value"] for param in supplier["parameters"] if param["name"] == "distancefromgurgaon"), None),
#             "annualturnover": next((param["value"] for param in supplier["parameters"] if param["name"] == "annualturnover"), None),
#             "inhousedesigncapability": next((param["value"] for param in supplier["parameters"] if param["name"] == "inhousedesigncapability"), None),
#             "isocertified": next((param["value"] for param in supplier["parameters"] if param["name"] == "isocertified"), None),
#             "recommended": next((param["value"] for param in supplier["parameters"] if param["name"] == "recommended"), None),
#         }
#         suppliers_df.append(row)
    
#     suppliers_df = pd.DataFrame(suppliers_df)

#     # Handle missing distance if any
#     suppliers_df['Distance of Factory from Gurgaon (Kms)'] = suppliers_df['distancefromgurgaon'].fillna(distance)

#     # Process categorical columns
#     le = LabelEncoder()
#     for column in suppliers_df.select_dtypes(include=['object']).columns:
#         suppliers_df[column] = le.fit_transform(suppliers_df[column])

#     # Convert recommended column to binary
#     suppliers_df['recommended'] = suppliers_df['recommended'].apply(lambda x: 1 if x else 0)

#     # Define features and target
#     X = suppliers_df.drop(columns=['name', 'recommended'])
#     y = suppliers_df['recommended']

#     # Predict using the pre-trained model
#     predictions = xgb_model.predict(X)

#     # Add predictions to the dataframe for further analysis if needed
#     suppliers_df['Predictions'] = predictions
#     print({
#         "predictions": predictions.tolist(),
#         "distance": distance,
#         "ranked_data": suppliers_df[['name', 'Predictions', 'Distance of Factory from Gurgaon (Kms)']].to_dict(orient='records')
#     }
#     )
#     # Return predictions and distance
#     return jsonify({
#         "predictions": predictions.tolist(),
#         "distance": distance,
#         "ranked_data": suppliers_df[['name', 'Predictions', 'Distance of Factory from Gurgaon (Kms)']].to_dict(orient='records')
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# import pandas as pd
# import joblib
# from flask import Flask, request, jsonify
# from sklearn.preprocessing import LabelEncoder
# from xgboost import XGBClassifier
# from geopy.distance import geodesic
# from flask_cors import CORS
# from pymongo import MongoClient

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Load the pre-trained XGBoost model
# xgb_model = joblib.load('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\vendor_selection_model.joblib')

# # MongoDB connection details
# username = 'inishasallove19'
# password = 'pro123'
# cluster_address = "aucfr.30wmt.mongodb.net"
# database_name = "AUCFR"

# # Construct the MongoDB connection string
# connection_string = f"mongodb+srv://{username}:{password}@{cluster_address}/{database_name}?retryWrites=true&w=majority"

# # Initialize the MongoDB client
# mongo_client = MongoClient(connection_string)
# db = mongo_client[database_name]
# suppliers_collection = db['suppliers']

# print("Connected to MongoDB successfully!")

# # Predefined city coordinates
# city_coordinates = {
#     'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
#     'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
#     'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
#     'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
#     'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
#     'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
#     'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
#     'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
#     'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
#     'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
#     'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
#     'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
#     'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
#     'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
#     'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
#     'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
#     'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
#     'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
#     'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
#     'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
#     'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
#     'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
#     'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
#     'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)

# }

# # Function to calculate distance to Gurgaon
# def calculate_distance_to_gurgaon(user_place):
#     gurgaon_coords = city_coordinates.get('Gurgaon')
#     if user_place in city_coordinates:
#         user_place_coords = city_coordinates[user_place]
#         return geodesic(gurgaon_coords, user_place_coords).kilometers
#     return None

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     user_place = data.get('city')

#     # Calculate distance to Gurgaon
#     distance = calculate_distance_to_gurgaon(user_place)
#     if distance is None:
#         return jsonify({"error": "Invalid location"}), 400

#     # Fetch supplier data from MongoDB
#     suppliers_data = list(suppliers_collection.find())
#     if not suppliers_data:
#         return jsonify({"error": "No supplier data found"}), 400

#     # Transform MongoDB data to a DataFrame
#     suppliers_df = []
#     for supplier in suppliers_data:
#         row = {
#             "name": supplier.get("name"),
#             "factorylocation": next((param["value"] for param in supplier["parameters"] if param["name"] == "factorylocation"), None),
#             "distancefromgurgaon": next((param["value"] for param in supplier["parameters"] if param["name"] == "distancefromgurgaon"), None),
#             "annualturnover": next((param["value"] for param in supplier["parameters"] if param["name"] == "annualturnover"), None),
#             "inhousedesigncapability": next((param["value"] for param in supplier["parameters"] if param["name"] == "inhousedesigncapability"), None),
#             "isocertified": next((param["value"] for param in supplier["parameters"] if param["name"] == "isocertified"), None),
#             "recommended": next((param["value"] for param in supplier["parameters"] if param["name"] == "recommended"), None),
#         }
#         suppliers_df.append(row)

#     suppliers_df = pd.DataFrame(suppliers_df)

#     # Handle missing distance if any
#     suppliers_df['Distance of Factory from Gurgaon (Kms)'] = suppliers_df['distancefromgurgaon'].fillna(distance)

#     # Rename columns to match model's expected feature names
#     column_mapping = {
#         "factorylocation": "Factory Location",
#         "distancefromgurgaon": "Distance of Factory from Gurgaon (Kms)",
#         "annualturnover": "Annual Turnover - In Cr",
#         "inhousedesigncapability": "In-house Design Capability",
#         "isocertified": "ISO Certified",
#     }
#     suppliers_df.rename(columns=column_mapping, inplace=True)

#     # Define the list of features expected by the model
#     expected_features = [
#         "Factory Location",
#         "Distance of Factory from Gurgaon (Kms)",
#         "Annual Turnover - In Cr",
#         "In-house Design Capability",
#         "ISO Certified"
#     ]

#     # Ensure the DataFrame has all the required features
#     missing_features = [col for col in expected_features if col not in suppliers_df.columns]
#     if missing_features:
#         return jsonify({"error": f"Missing features in input data: {missing_features}"}), 400

#     # Process categorical and boolean columns
#     le = LabelEncoder()
#     for column in suppliers_df.columns:
#         if suppliers_df[column].dtype == 'object':
#             suppliers_df[column] = suppliers_df[column].fillna("").astype(str)
#             suppliers_df[column] = le.fit_transform(suppliers_df[column])
#         elif pd.api.types.is_bool_dtype(suppliers_df[column]):
#             suppliers_df[column] = suppliers_df[column].fillna(False).astype(int)
#         elif pd.api.types.is_numeric_dtype(suppliers_df[column]):
#             suppliers_df[column] = suppliers_df[column].fillna(0)

#     # Prepare the features DataFrame
#     X = suppliers_df[expected_features]

#     # Predict using the pre-trained model
#     try:
#         predictions = xgb_model.predict(X)
#     except Exception as e:
#         return jsonify({"error": f"Model prediction failed: {str(e)}"}), 500

#     # Add predictions to the dataframe for further analysis if needed
#     suppliers_df['Predictions'] = predictions

#     # Return predictions and distance
#     return jsonify({
#         "predictions": predictions.tolist(),
#         "distance": distance,
#         "ranked_data": suppliers_df[['name', 'Predictions', 'Distance of Factory from Gurgaon (Kms)']].to_dict(orient='records')
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# import pandas as pd
# import joblib
# from flask import Flask, request, jsonify
# from sklearn.preprocessing import LabelEncoder
# from xgboost import XGBClassifier
# from geopy.distance import geodesic
# from flask_cors import CORS
# from pymongo import MongoClient

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Load the pre-trained XGBoost model
# xgb_model = joblib.load('C:\\Users\\PRIYA\\Downloads\\FE\\Sample-main\\src\\vendor_selection_model.joblib')

# # MongoDB connection details
# username = 'inishasallove19'
# password = 'pro123'
# cluster_address = "aucfr.30wmt.mongodb.net"
# database_name = "AUCFR"

# # Construct the MongoDB connection string
# connection_string = f"mongodb+srv://{username}:{password}@{cluster_address}/{database_name}?retryWrites=true&w=majority"

# # Initialize the MongoDB client
# mongo_client = MongoClient(connection_string)
# db = mongo_client[database_name]
# suppliers_collection = db['suppliers']

# print("Connected to MongoDB successfully!")

# # Predefined city coordinates
# city_coordinates = {
#     'Gurgaon': (28.4595, 77.0266),
#     'Delhi': (28.7041, 77.1025),
#     'Mumbai': (19.0760, 72.8777),
#     'Chennai': (13.0827, 80.2707),
#     'Kolkata': (22.5726, 88.3639),
#     'Bangalore': (12.9716, 77.5946),
#     'Hyderabad': (17.3850, 78.4867),
#     'Pune': (18.5204, 73.8567)
# }

# # Function to calculate distance to Gurgaon
# def calculate_distance_to_gurgaon(user_place):
#     gurgaon_coords = city_coordinates.get('Gurgaon')
#     if user_place in city_coordinates:
#         user_place_coords = city_coordinates[user_place]
#         return geodesic(gurgaon_coords, user_place_coords).kilometers
#     return None

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Parse input data
#         data = request.json
#         user_place = data.get('city')

#         # Calculate distance to Gurgaon
#         distance = calculate_distance_to_gurgaon(user_place)
#         if distance is None:
#             return jsonify({"error": "Invalid location"}), 400

#         # Fetch supplier data from MongoDB
#         suppliers_data = list(suppliers_collection.find())
#         if not suppliers_data:
#             return jsonify({"error": "No supplier data found"}), 400

#         # Transform MongoDB data to a DataFrame
#         suppliers_df = []
#         for supplier in suppliers_data:
#             row = {
#                 "name": supplier.get("name"),
#                 "factorylocation": next((param["value"] for param in supplier["parameters"] if param["name"] == "factorylocation"), None),
#                 "distancefromgurgaon": next((param["value"] for param in supplier["parameters"] if param["name"] == "distancefromgurgaon"), None),
#                 "annualturnover": next((param["value"] for param in supplier["parameters"] if param["name"] == "turnover"), None),
#                 "inhousedesigncapability": next((param["value"] for param in supplier["parameters"] if param["name"] == "inhousedesigncapability"), None),
#                 "isocertified": next((param["value"] for param in supplier["parameters"] if param["name"] == "isocertified"), None),
#                 "recommended": next((param["value"] for param in supplier["parameters"] if param["name"] == "recommended"), None),
#             }
#             suppliers_df.append(row)

#         suppliers_df = pd.DataFrame(suppliers_df)

#         # Rename columns to match model's expected feature names
#         column_mapping = {
#             "factorylocation": "Factory Location",
#             "distancefromgurgaon": "Distance of Factory from Gurgaon (Kms)",
#             "annualturnover": "Annual Turnover - In Cr",
#             "inhousedesigncapability": "In-house Design Capability",
#             "isocertified": "ISO Certified",
#         }
#         suppliers_df.rename(columns=column_mapping, inplace=True)

#         # Preserve non-feature columns for output
#         non_feature_columns = ["name", "Distance of Factory from Gurgaon (Kms)"]

#         # Fetch model's expected features
#         model_features = xgb_model.get_booster().feature_names

#         # Add missing features with default values
#         for feature in model_features:
#             if feature not in suppliers_df.columns:
#                 suppliers_df[feature] = 0  # Default value, modify as per feature type

#         # Keep only necessary columns (features + non-feature columns)
#         suppliers_df = suppliers_df[model_features + non_feature_columns]

#         # Debug output for column data
#         for column in suppliers_df.columns:
#             print(f"Column '{column}' sample data: {suppliers_df[column].head(5).to_list()}")

#         # Process categorical and boolean columns
#         le = LabelEncoder()
#         for column in model_features:
#             try:
#                 if suppliers_df[column].dtype == 'object':
#                     suppliers_df[column] = suppliers_df[column].fillna("Unknown").astype(str)
#                     suppliers_df[column] = le.fit_transform(suppliers_df[column])
#                 elif pd.api.types.is_bool_dtype(suppliers_df[column]):
#                     suppliers_df[column] = suppliers_df[column].fillna(False).astype(int)
#                 elif pd.api.types.is_numeric_dtype(suppliers_df[column]):
#                     suppliers_df[column] = pd.to_numeric(suppliers_df[column], errors='coerce').fillna(0)
#             except Exception as e:
#                 print(f"Error processing column '{column}': {e}")

#         # Prepare the features DataFrame
#         X = suppliers_df[model_features]

#         # Predict using the pre-trained model
#         predictions = xgb_model.predict(X)

#         # Add predictions to the dataframe for further analysis if needed
#         suppliers_df['Predictions'] = predictions

#         # Return predictions and distance
#         return jsonify({
#             "predictions": predictions.tolist(),
#             "distance": distance,
#             "ranked_data": suppliers_df[["name", "Predictions", "Distance of Factory from Gurgaon (Kms)"]].to_dict(orient='records')
#         })

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
# # import pandas as pd
# # import numpy as np
# # import geopy.distance
# # import xgboost as xgb
# # from sklearn.model_selection import train_test_split
# # from sklearn.metrics import mean_squared_error
# # vendor_data_1 = pd.DataFrame({
# #     'FACADE VENDOR': ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20'],
# #     'Turn Over': [20, 20, 20, 15, 20, 15, 10, 20, 20, 10, 12, 8, 15, 10, 12, 10, 12, 8, 7, 5],
# #     'Engineering Staff/Capacity': [20, 15, 20, 20, 20, 20, 15, 15, 20, 10, 12, 8, 10, 8, 10, 5, 7, 4, 6, 3],
# #     'Past Similar projects': [15, 15, 10, 15, 12, 12, 12, 10, 12, 5, 8, 3, 7, 5, 6, 300, 250, 200, 150, 100],
# #     'Production Capacity': [20, 20, 18, 20, 15, 10, 10, 12, 18, 5, 6, 4, 6, 4, 7, 300, 250, 200, 150, 100],
# #     'ISO Certified': [5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 3, 1, 2, 3, 4, 1, 1, 0, 1, 0],
# #     'HSE Policy': [5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 3, 1, 2, 3, 4, 2, 2, 2, 1, 0],
# #     'QA/ QC Policy': [5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 3, 1, 2, 3, 4, 1, 1, 2, 1, 0],
# #     'Installation Capacity': [8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 6, 3, 5, 6, 5, 5, 4, 3, 4, 2],
# #     'Average Rating': [98, 93, 91, 93, 90, 80, 70, 80, 93, 55, 65, 50, 60, 55, 70, 60, 58, 55, 52, 50],
# #     'Recommended': [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# # })
# # vendor_data_2 = pd.DataFrame({
# #     'FACADE VENDOR': ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9'],
# #     'Annual Turnover - In Cr': [494, 390, 242, 265, 89, 142, 115, 88, 120],
# #     'Control Location (HO/ Branch)': ['Bangalore', 'Mumbai', 'Mumbai', 'Chennai', 'Mumbai', 'Hyderabad', 'Mumbai', 'Mumbai', 'Gurgaon'],
# #     'In-house Design Capability': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
# #     'Factory Location': ['Bangalore', 'Hyderabad', 'Mumbai', 'Chennai', 'Bangalore/Mumbai', 'Hyderabad', 'Mumbai', 'Hyderabad & Mumbai', 'Delhi'],
# #     'Distance of Factory from Gurgaon (Kms)': [230, 120, 210, 350, np.nan, np.nan, np.nan, np.nan, np.nan],
# #     'Unit Per Day Capacity': [1120, 400, 750, 388, 1200, 1000, 750, 250, 1500],
# #     'Panel Prod. Capacity Per day': [230, 82, 154, 80, 246, 205, 154, 51, 308],
# #     'In-house MS Fabrication': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No-Outsource - J.V.'],
# #     'In House Powder Coating Capability': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes']
# # })
# # vendor_data = pd.merge(vendor_data_1, vendor_data_2, on='FACADE VENDOR', how='outer')
# # vendor_data.fillna({
# #     'Turn Over': -1,
# #     'Engineering Staff/Capacity': -1,
# #     'Past Similar projects': -1,
# #     'Production Capacity': -1,
# #     'ISO Certified': -1,
# #     'HSE Policy': -1,
# #     'QA/ QC Policy': -1,
# #     'Installation Capacity': -1,
# #     'Average Rating': -1,
# #     'Recommended': -1,
# #     'Annual Turnover - In Cr': -1,
# #     'Control Location (HO/ Branch)': -1,
# #     'In-house Design Capability': -1,
# #     'Factory Location': -1,
# #     'Distance of Factory from Gurgaon (Kms)': -1,
# #     'Unit Per Day Capacity': -1,
# #     'Panel Prod. Capacity Per day': -1,
# #     'In-house MS Fabrication': -1,
# #     'In House Powder Coating Capability': -1
# # }, inplace=True)
# # city_coords = {
        # 'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
        # 'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
        # 'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
        # 'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
        # 'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
        # 'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
        # 'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
        # 'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
        # 'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
        # 'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
        # 'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
        # 'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
        # 'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
        # 'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
        # 'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
        # 'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
        # 'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
        # 'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
        # 'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
        # 'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
        # 'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
        # 'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
        # 'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
        # 'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
# #     }
# # def calculate_distance_to_gurgaon(city):
# #     gurgaon_coords = (28.4595, 77.0266) 
# #     return geopy.distance.distance(gurgaon_coords, city_coords.get(city, (28.4595, 77.0266))).km if city in city_coords else 100
# # user_city = input("Enter the city to calculate the distance from Gurgaon: ").strip()
# # if user_city in city_coords:
# #     user_distance = calculate_distance_to_gurgaon(user_city)
# # else:
# #     print("City not found. Using default distance of 100 km.")
# #     user_distance = 100
# # vendor_data['User City Distance from Gurgaon (Kms)'] = user_distance
# # X = vendor_data[['Turn Over', 'Engineering Staff/Capacity', 'Past Similar projects', 'Production Capacity', 'ISO Certified', 
# #                  'HSE Policy', 'QA/ QC Policy', 'Installation Capacity', 'Average Rating', 'Annual Turnover - In Cr', 
# #                  'Unit Per Day Capacity', 'Panel Prod. Capacity Per day', 'Distance of Factory from Gurgaon (Kms)', 
# #                  'User City Distance from Gurgaon (Kms)']]
# # y = vendor_data['Average Rating'] 
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# # model = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
# #                          max_depth=5, alpha=10, n_estimators=10)
# # model.fit(X_train, y_train)
# # y_pred = model.predict(X_test)
# # vendor_data['Predicted Ranking Score'] = model.predict(X)
# # vendor_data['Rank'] = vendor_data['Predicted Ranking Score'].rank(ascending=False)
# # ranked_vendors = vendor_data[['FACADE VENDOR', 'Rank', 'Predicted Ranking Score']]
# # ranked_vendors = ranked_vendors.sort_values(by='Rank')
# # print(ranked_vendors[['FACADE VENDOR', 'Rank', 'Predicted Ranking Score']])



