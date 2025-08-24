from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# ---- Load & prep data -------------------------------------------------------
# Expecting columns:
# dispatching_base_number, date, active_vehicles, trips, trips_per_vehicle, day_of_week, month
df = pd.read_csv("uber_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Optional: enforce title-case for DoW/Month if needed
if df["day_of_week"].dtype == object:
    df["day_of_week"] = df["day_of_week"].str.strip().str.title()
if df["month"].dtype == object:
    df["month"] = df["month"].str.strip().str.title()


# ---- Routes -----------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    base_numbers = sorted(df["dispatching_base_number"].dropna().unique())
    # Infer min/max dates for date inputs
    min_date = df["date"].min().strftime("%Y-%m-%d")
    max_date = df["date"].max().strftime("%Y-%m-%d")
    days = ["All","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    months = ["All","January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    return render_template(
        "index.html",
        base_numbers=base_numbers,
        min_date=min_date,
        max_date=max_date,
        days=days,
        months=months
    )


@app.route("/results", methods=["POST"])
def results():
    base_number = request.form.get("base_number")
    start_date  = request.form.get("start_date")
    end_date    = request.form.get("end_date")
    day_of_week = request.form.get("day_of_week", "All")
    month       = request.form.get("month", "All")

    # ---- Filter --------------------------------------------------------------
    q = df[df["dispatching_base_number"] == base_number].copy()
    if start_date:
        q = q[q["date"] >= pd.to_datetime(start_date)]
    if end_date:
        q = q[q["date"] <= pd.to_datetime(end_date)]
    if day_of_week and day_of_week != "All":
        q = q[q["day_of_week"] == day_of_week]
    if month and month != "All":
        q = q[q["month"] == month]

    # Handle empty result gracefully
    if q.empty:
        return render_template(
            "results.html",
            base_number=base_number,
            empty=True
        )

    # ---- Summary cards -------------------------------------------------------
    total_trips = int(q["trips"].sum())
    total_vehicles = int(q["active_vehicles"].sum())
    avg_tpv = round(q["trips_per_vehicle"].mean(), 2) if "trips_per_vehicle" in q else 0.0

    # ---- Charts --------------------------------------------------------------
    fig1 = px.line(
        q.sort_values("date"),
        x="date", y="trips",
        title="Trips per Day",
        markers=True
    )
    fig1.update_layout(margin=dict(l=20,r=20,t=60,b=20), height=420)

    dow = q.groupby("day_of_week", as_index=False)["trips"].sum()
    # Order days
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow["day_of_week"] = pd.Categorical(dow["day_of_week"], dow_order, ordered=True)
    dow = dow.sort_values("day_of_week")
    fig2 = px.bar(dow, x="day_of_week", y="trips", title="Trips by Day of Week")
    fig2.update_layout(margin=dict(l=20,r=20,t=60,b=20), height=380)

    mo = q.groupby("month", as_index=False)["trips"].sum()
    mo_order = ["January","February","March","April","May","June",
                "July","August","September","October","November","December"]
    mo["month"] = pd.Categorical(mo["month"], mo_order, ordered=True)
    mo = mo.sort_values("month")
    fig3 = px.bar(mo, x="month", y="trips", title="Trips by Month")
    fig3.update_layout(margin=dict(l=20,r=20,t=60,b=20), height=380)

    graph1 = pio.to_html(fig1, full_html=False, include_plotlyjs="cdn")
    graph2 = pio.to_html(fig2, full_html=False, include_plotlyjs=False)
    graph3 = pio.to_html(fig3, full_html=False, include_plotlyjs=False)

    return render_template(
        "results.html",
        base_number=base_number,
        start_date=start_date, end_date=end_date,
        day_of_week=day_of_week, month=month,
        total_trips=total_trips, total_vehicles=total_vehicles, avg_tpv=avg_tpv,
        graph1=graph1, graph2=graph2, graph3=graph3, empty=False
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---- Run locally ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
