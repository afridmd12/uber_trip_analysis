# 🚖 Uber Trips Data Dashboard  
An interactive web dashboard built with **Flask**, **Plotly**, and **Pandas** to explore Uber trips data. Deployed seamlessly on **Render**.  

🌐 Live Demo: [Uber Trips Dashboard](https://uber-trip-analysis-os6n.onrender.com)  

## ✨ Features  
- 📊 Dynamic Filtering by: Dispatching Base Number, Date Range, Day of Week, Month  
- 📈 Interactive Visualizations (Plotly): Trips per Day (line chart), Trips by Day of Week (bar chart), Trips by Month (bar chart)  
- 📃 Summary Cards showing: Total Trips, Active Vehicles, Average Trips per Vehicle  
- 🖼️ Clean UI with smooth animations and central alignment  

## 🗂️ Project Structure  
├── templates/  
│   ├── index.html        # Homepage with filters  
│   ├── results.html      # Results page with charts  
│   └── dashboard.html    # (Optional, extra view if needed)  
├── uber_data.csv         # Input dataset  
├── app.py                # Flask backend  
├── requirements.txt      # Python dependencies  
├── Procfile              # Render deployment entry  
└── README.md             # Project documentation  

## ⚙️ Installation & Local Setup  
1. Clone this repository  
   git clone https://github.com/afridmd12/uber_trip_analysis.git  
   cd uber-trips-dashboard  

2. Create virtual environment & activate  
   python -m venv venv  
   source venv/bin/activate     # On Mac/Linux  
   venv\Scripts\activate        # On Windows  

3. Install dependencies  
   pip install -r requirements.txt  

4. Run locally  
   python app.py  
   Open your browser at 👉 http://127.0.0.1:5000/  

## 🚀 Deployment on Render  
1. Push code to GitHub  
2. On Render: Create new Web Service, Connect your repo  
3. Set build & start commands:  
   Build Command: pip install -r requirements.txt  
   Start Command: gunicorn app:app  
4. Deploy → Your app will be live 🎉  

## 📦 Requirements  
Flask  
pandas  
plotly  
gunicorn  

## 📊 Dataset Notes  
The app expects the CSV to have these columns:  
- dispatching_base_number  
- date  
- active_vehicles  
- trips  
- trips_per_vehicle  
- day_of_week  
- month  
Dates should be in YYYY-MM-DD format.  

## 🛠️ Tech Stack  
Backend: Flask  
Frontend: HTML + Jinja + Plotly.js  
Data Handling: Pandas  
Deployment: Render  

## 🙌 Acknowledgements  
This project is for educational and analytical purposes to visualize Uber trips dataset using Flask and Plotly, deployed on Render.  
