import streamlit as st

def run():
    st.title("Energy Assessment Form")
    st.write("Please fill out the form below to help us understand your energy usage.")

    with st.form("energy_form"):
        st.subheader("I. Quantifiable Energy Consumption")
        kwh_consumed = st.number_input("What was the total number of electricity units (e.g., kWh) consumed in your last full billing cycle?", min_value=0, value=0, step=1)
        energy_cost = st.number_input("What was the total cost of your electricity bill for the same billing cycle (in your local currency)?", min_value=0.0, value=0.0, step=0.01)
        billing_cycle_days = st.number_input("Approximately how many days was this billing cycle for?", min_value=1, value=30, step=1)

        st.subheader("II. Household Characteristics")
        num_occupants = st.number_input("How many people currently reside in your household (including yourself)?", min_value=1, value=1, step=1)
        dwelling_type = st.selectbox("What type of dwelling do you primarily live in?", ["Apartment", "House (Single-family)", "Townhouse", "Duplex", "Other"])
        floor_area = st.number_input("Approximately what is the total floor area of your dwelling (in square feet or square meters)?", min_value=100, value=1000, step=100)
        income_range = st.selectbox("What is your approximate annual household income range?", ["Less than ₹3,00,000", "₹3,00,000 - ₹5,00,000", "₹5,00,000 - ₹10,00,000", "₹10,00,000 - ₹20,00,000", "More than ₹20,00,000"])
        city_name = st.text_input("What is your city name?", "Bengaluru")

        st.subheader("III. Major Energy-Consuming Appliances")
        heating_system = st.selectbox("What type of primary heating system do you use?", ["Central forced air (gas/electric)", "Heat pump", "Electric baseboard heaters", "Other", "Not applicable"])
        cooling_system = st.selectbox("What type of primary cooling system do you use?", ["Central air conditioning", "Window AC units", "Ductless mini-split", "Evaporative cooler (swamp cooler)", "Fans only", "Other", "Not applicable"])
        if heating_system != "Not applicable" or cooling_system != "Not applicable":
            thermostat_temperature = st.number_input("On average, what temperature do you typically set your thermostat to during the [relevant season - e.g., summer for cooling, winter for heating]?", value=72, step=1)
        else:
            thermostat_temperature = None
        water_heating_system = st.selectbox("What type of water heating system do you have?", ["Electric storage tank", "Gas storage tank", "Tankless/On-demand", "Solar water heater", "Other"])
        washing_machine_usage = st.number_input("How often do you typically use your washing machine per week (on average)?", min_value=0, value=3, step=1)
        clothes_drying = st.selectbox("Do you primarily use a clothes dryer or do you air dry your clothes?", ["Primarily dryer", "Primarily air dry", "Mix of both"])
        refrigerator_age = st.selectbox("Approximately how old is your refrigerator?", ["Less than 5 years", "5-10 years", "10-15 years", "Older than 15 years", "Not sure"])
        has_dishwasher = st.checkbox("Do you have a dishwasher?")
        dishwasher_usage = st.number_input("If so, how often do you typically use it per week (on average)?", min_value=0, value=3, step=1) if has_dishwasher else 0
        lighting_type = st.selectbox("What type of light bulbs do you primarily use in your home?", ["Primarily LED", "Mix of LED and incandescent/fluorescent", "Primarily incandescent/fluorescent", "Not sure"])

        st.subheader("IV. Energy Usage Habits and Behaviors")
        occupants_at_home = st.selectbox("Are there typically occupants at home during the day on weekdays?", ["Yes", "No", "Sometimes"])
        devices_plugged_in = st.selectbox("Do you often leave electronic devices (like TVs, computers, chargers) plugged in when they are not in use?", ["Yes, Often", "Sometimes", "Rarely", "No"])
        energy_waste_areas = st.text_input("Are you aware of any specific areas in your home where you believe you might be using more energy than necessary? (Optional)")

        st.subheader("V. Existing Energy-Saving Measures and Interests")
        existing_measures = st.text_input("Have you already implemented any energy-saving measures in your home (e.g., smart thermostat, weather stripping, energy-efficient appliances)? (Optional)")
        saving_interests = st.multiselect("Are you interested in learning more about any specific areas of energy saving?", ["Solar panels", "Smart home technologies", "Reducing heating/cooling costs", "Improving insulation", "Energy-efficient appliances"])

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Form submitted successfully!")
            st.session_state.form_data = {
                "kwh_consumed": kwh_consumed,
                "energy_cost": energy_cost,
                "billing_cycle_days": billing_cycle_days,
                "num_occupants": num_occupants,
                "dwelling_type": dwelling_type,
                "floor_area": floor_area,
                "income_range":income_range,
                "city_name": city_name,
                "heating_system": heating_system,
                "cooling_system": cooling_system,
                "thermostat_temperature": thermostat_temperature,
                "water_heating_system": water_heating_system,
                "washing_machine_usage": washing_machine_usage,
                "clothes_drying": clothes_drying,
                "refrigerator_age": refrigerator_age,
                "has_dishwasher": has_dishwasher,
                "dishwasher_usage": dishwasher_usage,
                "lighting_type": lighting_type,
                "occupants_at_home": occupants_at_home,
                "devices_plugged_in": devices_plugged_in,
                "energy_waste_areas": energy_waste_areas,
                "existing_measures": existing_measures,
                "saving_interests": saving_interests,
            }
            st.write("Form data saved to session state. Please proceed to chatpage")