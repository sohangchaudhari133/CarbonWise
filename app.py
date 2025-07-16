import streamlit as st

st.title("🌍 CarbonWise - Local Chatbot for Carbon Footprint Estimation")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.km_per_day = None
    st.session_state.flights_per_year = None
    st.session_state.electricity_monthly = None
    st.session_state.diet_type = None
    st.session_state.waste_per_week = None

if 'messages' not in st.session_state:
    st.session_state.messages = []
    intro = "Hello! I'm CarbonWise 🌍. Let's calculate your carbon footprint.\n\nHow many kilometers do you drive daily by car or bike?"
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Your answer...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    step = st.session_state.step
    bot_reply = ""

    if step == 1:
        try:
            st.session_state.km_per_day = float(user_input)
            bot_reply = "✈️ How many short flights do you take per year?"
            st.session_state.step += 1
        except ValueError:
            bot_reply = "⚠️ Please enter a valid number for kilometers driven daily."

    elif step == 2:
        try:
            st.session_state.flights_per_year = int(user_input)
            bot_reply = "⚡ What is your monthly electricity usage (in kWh)?"
            st.session_state.step += 1
        except ValueError:
            bot_reply = "⚠️ Please enter a valid whole number for flights per year."

    elif step == 3:
        try:
            st.session_state.electricity_monthly = float(user_input)
            bot_reply = "🥗 What is your diet type? (Reply with: Meat Daily / Occasional Meat / Vegetarian)"
            st.session_state.step += 1
        except ValueError:
            bot_reply = "⚠️ Please enter a valid number for electricity usage."

    elif step == 4:
        diet_input = user_input.strip().lower()
        if "meat" in diet_input:
            if "daily" in diet_input:
                st.session_state.diet_type = "Meat Daily"
            elif "occasional" in diet_input:
                st.session_state.diet_type = "Occasional Meat"
            else:
                st.session_state.diet_type = "Meat Daily"
        elif "vegetarian" in diet_input:
            st.session_state.diet_type = "Vegetarian"
        else:
            st.session_state.diet_type = "Vegetarian"

        bot_reply = "🗑️ How much waste do you produce weekly? (in kg)?"
        st.session_state.step += 1

    elif step == 5:
        try:
            st.session_state.waste_per_week = float(user_input)

            # Calculate emissions
            car_emission = st.session_state.km_per_day * 365 * 0.271
            flight_emission = st.session_state.flights_per_year * 150
            electricity_emission = st.session_state.electricity_monthly * 12 * 0.5
            waste_emission = st.session_state.waste_per_week * 52 * 1

            diet = st.session_state.diet_type
            if diet == "Meat Daily":
                diet_emission = 2000
            elif diet == "Occasional Meat":
                diet_emission = 1500
            else:
                diet_emission = 1200

            total_emission = car_emission + flight_emission + electricity_emission + waste_emission + diet_emission

            # Overall footprint level
            if total_emission < 4000:
                level = "Low 🌱"
                comparison = "Equivalent to **driving a small car for 7,000 km per year** or **charging 450 smartphones daily for a year**."
            elif total_emission < 8000:
                level = "Medium 🚶‍♂️"
                comparison = "Similar to **taking 5 short domestic flights** or **powering 2 average homes for a year**."
            elif total_emission < 12000:
                level = "High 🚗✈️"
                comparison = "Comparable to **driving an SUV for 15,000 km** or needing **10 mature trees to absorb your emissions** each year."
            else:
                level = "Very High 🔥"
                comparison = "Similar to **two people's average annual emissions combined** or **multiple international flights**."

            # Individual category tips
            individual_tips = ""

            # Transport
            annual_km = st.session_state.km_per_day * 365
            if annual_km < 3000:
                individual_tips += "🚲 **Transport:** Low usage. Keep it up by walking, cycling, or using public transport!\n\n"
            elif annual_km < 8000:
                individual_tips += "🚗 **Transport:** Moderate use. Try to carpool or combine trips to reduce driving.\n\n"
            elif annual_km < 15000:
                individual_tips += "🚙 **Transport:** High driving distance. Consider using an electric vehicle or cutting down unnecessary trips.\n\n"
            else:
                individual_tips += "🚙 **Transport:** Very high travel distance! Shift to eco-friendly transport or reduce personal vehicle use.\n\n"

            # Flights
            flights = st.session_state.flights_per_year
            if flights == 0:
                individual_tips += "✈️ **Flights:** No flights taken—excellent for the environment!\n\n"
            elif flights <= 2:
                individual_tips += "✈️ **Flights:** Low flight usage. Try to prefer trains or virtual meetings when possible.\n\n"
            elif flights <= 5:
                individual_tips += "✈️ **Flights:** Frequent short flights. Consider offsetting carbon emissions or reducing air travel.\n\n"
            else:
                individual_tips += "✈️ **Flights:** Very frequent flying. Reduce flights and opt for sustainable travel methods.\n\n"

            # Electricity
            electricity = st.session_state.electricity_monthly
            if electricity < 100:
                individual_tips += "⚡ **Electricity:** Great! Your energy use is low.\n\n"
            elif electricity < 300:
                individual_tips += "⚡ **Electricity:** Moderate usage. Upgrade to LED bulbs and energy-efficient appliances.\n\n"
            elif electricity < 500:
                individual_tips += "⚡ **Electricity:** High energy use. Consider switching to renewable energy sources.\n\n"
            else:
                individual_tips += "⚡ **Electricity:** Very high consumption. Conduct a home energy audit to reduce usage.\n\n"

            # Diet
            diet = st.session_state.diet_type
            if diet == "Vegetarian":
                individual_tips += "🥗 **Diet:** Vegetarian diet—great for reducing emissions!\n\n"
            elif diet == "Occasional Meat":
                individual_tips += "🥗 **Diet:** Occasional meat eater. Try to reduce meat meals further to lower your footprint.\n\n"
            else:
                individual_tips += "🥩 **Diet:** Daily meat consumption increases emissions. Try adding more plant-based meals.\n\n"

            # Waste
            waste = st.session_state.waste_per_week
            if waste < 2:
                individual_tips += "♻️ **Waste:** Low waste generation. Keep composting and recycling!\n\n"
            elif waste < 5:
                individual_tips += "♻️ **Waste:** Moderate waste. Focus on composting and reducing single-use plastics.\n\n"
            elif waste < 8:
                individual_tips += "♻️ **Waste:** High waste levels. Reduce packaging and reuse items where possible.\n\n"
            else:
                individual_tips += "♻️ **Waste:** Very high waste output. Conduct a waste audit to find ways to cut down.\n\n"

            # Final bot reply
            bot_reply = f"""
🌍 **Your estimated annual carbon footprint is:** **{total_emission:.2f} kg CO₂**

**Overall Level:** {level}  

{comparison}

---

### **Personalized Tips Based on Your Inputs:**

{individual_tips}
"""
            st.session_state.step += 1

        except ValueError:
            bot_reply = "⚠️ Please enter a valid number for waste in kg."

    else:
        bot_reply = "✅ Thank you! If you'd like to calculate again, please refresh the app."

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
