# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.express import density_heatmap

# Load data
data = pd.read_csv("data_morad_elshorbagy.csv")


# Sets the page layout to use the full browser width.
# Displays the dashboard title at the top.
st.set_page_config(layout="wide")
st.title("📱 Social Media & Smartphone Addiction Dashboard")


# Adds a sidebar section titled “Filter Data” where you’ll place all user input widgets.
st.sidebar.header("🔎 Filter Data")

# Retrieves all unique, non-null gender values from the dataset and stores them as a list.
gender_options = data["Gender"].dropna().unique().tolist()

# Creates a multi-select dropdown in the sidebar to let the user pick genders.
# Adds "All" to the list and sets it as the default.
gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=["All"] + gender_options,
    default=["All"]
)

# If "All" is selected w something else, remove it from the filter list.
if "All" in gender_filter and len(gender_filter) > 1:
    gender_filter.remove("All")


# If "All" is selected, use all genders, if nothing is selected also show all.
if "All" in gender_filter or not gender_filter:
    gender_selection = gender_options
else:
    gender_selection = gender_filter



# Creates a slider in the sidebar to let the user select an age range.
Daily_range = st.sidebar.slider(
    "Select Daily Social Media Usage Range (hours)",
    int(data["Daily Social Media Usage(hours)"].min()),
    int(data["Daily Social Media Usage(hours)"].max()),
    (int(data["Daily Social Media Usage(hours)"].min()),
    int(data["Daily Social Media Usage(hours)"].max()))
)





# Creates a slider in the sidebar to let the user select an age range.
age_range = st.sidebar.slider(
    "Select Age Range",
    int(data["Age"].min()),
    int(data["Age"].max()),
    (int(data["Age"].min()), int(data["Age"].max()))
)


# Map mental health status
mental_health_map = {
    0: "Poor",
    1: "Fair",
    2: "Good",
    3: "Excellent"
}
data["Mental Health Status"] = data["Mental Health Status"].map(mental_health_map)


# Map frequency of posts
post_freq_map = {
    0: "Never",
    1: "Rarely",
    2: "Sometimes",
    3: "Often",
    4: "Always"
}

data["Frequency of Posts"] = data["Frequency of Posts"].map(post_freq_map)

# Map frequency of checking notifications
notif_freq_map = {
    0: "Rarely",
    1: "Occasionally",
    2: "Frequently"
}


data["Frequency of Checking Notifications"] = data["Frequency of Checking Notifications"].map(notif_freq_map)

# Cyberbullying filter: 0 = No, 1 = Yes
cyberbully_map = {0: "No", 1: "Yes"}
# Map the values in the "Cyberbullying Experience" column to their corresponding labels
data["Cyberbullying Experience"] = data["Cyberbullying Experience"].map(cyberbully_map)



# Creates a multi-select dropdown in the sidebar to let the user pick mental health statuses.


mh_options = list(mental_health_map.values())

mh_filter = st.sidebar.multiselect(
    "Mental Health Status",
    options=["All"] + mh_options,
    default=["All"]
)

if "All" in mh_filter and len(mh_filter) > 1:
    mh_filter.remove("All")

if "All" in mh_filter or not mh_filter:
    mh_selection = mh_options
else:
    mh_selection = mh_filter



# Get the unique values in the "Cyberbullying Experience" column
cyber_options = list(cyberbully_map.values())

cyber_filter = st.sidebar.multiselect(
    "Cyberbullying Experience",
    options=["All"] + cyber_options,
    default=["All"]
)

if "All" in cyber_filter and len(cyber_filter) > 1:
    cyber_filter.remove("All")

if "All" in cyber_filter or not cyber_filter:
    cyber_selection = cyber_options
else:
    cyber_selection = cyber_filter



# Apply filters
filtered_data = data[
    (data["Gender"].isin(gender_selection)) &
    (data["Age"] >= age_range[0]) &
    (data["Age"] <= age_range[1]) &
    (data["Daily Social Media Usage(hours)"] >= Daily_range[0]) &
    (data["Daily Social Media Usage(hours)"] <= Daily_range[1]) &
    (data["Mental Health Status"].isin(mh_selection)) &
    (data["Cyberbullying Experience"].isin(cyber_selection))
]





# Figure 0: Gender Distribution
st.markdown("### 👥 Gender Distribution")

gender_dist = filtered_data["Gender"].value_counts().reset_index()
gender_dist.columns = ["Gender", "Count"]

fig0 = px.pie(
    gender_dist,
    names="Gender",
    values="Count"
)

fig0.update_layout(
    height=600
)

st.plotly_chart(fig0, use_container_width=True, key="gender_dist_pie")
st.info("💡 The dataset includes a fairly balanced number of male and female participants, with a small number identifying as 'Others'.")


# Figure 1: Frequency of Posts by Gender
st.markdown("### 🗨️ Frequency of Posts by Gender")

fig1 = px.histogram(
    filtered_data,
    x="Frequency of Posts",
    color="Gender",
    barmode="group",
    category_orders={"Frequency of Posts": ["Never", "Rarely", "Sometimes", "Often", "Always"]}
)

fig1.update_layout(
    yaxis_title="Frequency of Posts",
    xaxis_title="Gender",
    height=600
)

st.plotly_chart(fig1, use_container_width=True, key="post_freq_box")
st.info("💡 Most people only post occasionally, with a few posting frequently. ")




# Figure 2: Frequency of Checking Notifications by Gender
st.markdown("### 🔔 Frequency of Checking Notifications by Gender")

notif_dist = filtered_data.groupby(["Gender", "Frequency of Checking Notifications"]).size().reset_index(name="Count")

fig2 = px.bar(
    notif_dist,
    x="Frequency of Checking Notifications",
    y="Count",
    color="Gender",
    barmode="group"
)

fig2.update_layout(
    yaxis_title="Number of Participants",
    xaxis_title="Notification Checking Frequency",
    height=600
)

st.plotly_chart(fig2, use_container_width=True, key="notif_freq_by_gender")



#Figure 3: Self Esteem Score Distribution
st.markdown("### 📈 Self Esteem Score Distribution")
fig3 = px.histogram(
    filtered_data,
    x="Self Esteem Score",
    color="Gender",
    nbins=10,
    barmode="group",
    hover_data=["Age", "Daily Social Media Usage(hours)"]
)
fig3.update_layout(
    xaxis_title="Self Esteem Score",
    yaxis_title="Number of Participants",
    height=600
)

st.plotly_chart(fig3, use_container_width=True, key="self_esteem_hist")
st.info("💡 Lots of men and woman suffer from low self-esteem.")


#Figure 4: Average daily usage
avg_usage_gender = filtered_data.groupby("Gender")["Daily Social Media Usage(hours)"].mean().reset_index()

st.markdown("### 📈 Average daily usage")

fig4 = px.bar(
    avg_usage_gender,
    x="Gender",
    y="Daily Social Media Usage(hours)",
    color="Gender",
)

fig4.update_traces(width=0.4)

fig4.update_layout(
    yaxis_title="Average Daily Usage (hours)",
    xaxis_title="Gender",
    height=600
)

st.plotly_chart(fig4, use_container_width=True, key="avg_daily_usage_bar")
st.info("💡 On average, females report slightly higher daily social media usage compared to males and others.")


#Figure 5: Anxiety Score by Gender
st.markdown("### 📦 Anxiety Score by Gender")
fig5 = px.box(
    filtered_data,
    x="Gender",
    y="Anxiety Score",
    color="Gender"
)

fig5.update_layout(
    xaxis_title="Gender",
    yaxis_title="Anxiety Score",
    height=600
)

st.plotly_chart(fig5, use_container_width=True, key="anxiety_box_gender")

st.info("💡 The median anxiety score across genders is around 5, with some variation in spread and outliers.")

#Figure 6: Daily Usage vs. Addiction Score
st.markdown("### 🔁 Daily Usage vs. Addiction Score")
fig6 = px.scatter(
    filtered_data,
    x="Daily Social Media Usage(hours)",
    y="Self Reported Addiction Score",
    color="Gender",
    size="Anxiety Score",
    size_max=20,
    hover_data=["Self Esteem Score", "Sleep Quality"]
)

fig6.update_layout(
    xaxis_title="Daily Social Media Usage(hours)",
    yaxis_title="Self Reported Addiction Score",
    height=600
)

st.plotly_chart(fig6, use_container_width=True, key="usage_vs_addiction")
st.info("💡 There’s a clear positive correlation between daily social media usage and self-reported addiction score.")


#Figure 7: Mental Health Status Count
st.markdown("### Mental Health Status Count")

mh_counts = filtered_data["Mental Health Status"].value_counts().reset_index()
mh_counts.columns = ["Mental Health Status", "Count"]


fig7 = px.bar(
    mh_counts,
    x="Mental Health Status",
    y="Count",
    category_orders={"Mental Health Status": ["Poor", "Fair", "Good", "Excellent"]},
    text_auto=True
)

fig7.update_layout(
    yaxis_title="Number of Participants",
    xaxis_title="Mental Health Status",
    height=600
)

st.plotly_chart(fig7, use_container_width=True, key="mental_health_bar")

st.info("💡 Most participants report either poor or fair mental health status, with fewer reporting good or excellent mental health.")

#Figure 8: Daily Usage vs. Average Anxiety Score
st.markdown("### 🔁 Daily Usage vs. Average Anxiety Score")

avg_anxscore = filtered_data.groupby("Daily Social Media Usage(hours)")["Anxiety Score"].mean().reset_index()

fig8 = px.line(
    avg_anxscore,
    x="Daily Social Media Usage(hours)",
    y="Anxiety Score",
    markers=True
)

fig8.update_layout(
    xaxis_title="Daily Social Media Usage (hours)",
    yaxis_title="Average Anxiety Score",
    height=600
)

st.plotly_chart(fig8, use_container_width=True, key="usage_vs_anxiety_line")

st.info("💡 Anxiety scores tend to increase with higher daily social media usage, suggesting a positive correlation.")



#Figure 9: Impact of Cyberbullying on Self Esteem and Anxiety
st.markdown("### 🔁 Impact of Cyberbullying on Self Esteem and Anxiety")

grouped = filtered_data.groupby("Cyberbullying Experience")[["Self Esteem Score", "Anxiety Score"]].mean().reset_index()
melted = grouped.melt(id_vars="Cyberbullying Experience", var_name="Metric", value_name="Average")


fig9 = px.bar(
    melted,
    x="Cyberbullying Experience",
    y="Average",
    color="Metric",
    barmode="group",
    text_auto=".2f"
)

fig9.update_layout(
    xaxis_title="Cyberbullying Experience",
    yaxis_title="Average Self-Esteem and Anxiety Score",
    height=600
)


st.plotly_chart(fig9, use_container_width=True, key="cyberbullying_impact_bar")

st.info("💡 Cyberbullying appears to have little impact on self-esteem and anxiety scores. "
        "This may be due to a small number of 'Yes' responses, limiting the ability to detect clear differences.")


#Figure 10: Age vs Self Esteem and Anxiety
st.markdown("### 🔁 Age vs Average Self Esteem and Anxiety")


age_group = filtered_data.groupby("Age")[["Self Esteem Score", "Anxiety Score"]].mean().reset_index()

fig10 = px.line(
    age_group,
    x="Age",
    y=["Self Esteem Score", "Anxiety Score"]
)

fig10.update_layout(
    xaxis_title="Age",
    yaxis_title="Average Self-Esteem and Anxiety Score",
    height=600
)

st.plotly_chart(fig10, use_container_width=True, key="age_selfesteem_anxiety_line")

st.info("💡 Negative Correlation: The lower the anxiety score, the higher the self-esteem score.")

#Figure 11: Avg Social Media Fatigue by Usage Hours
st.markdown("### 📈 Average Social Media Fatigue by Usage Hours")
avg_fatigue = filtered_data.groupby("Daily Social Media Usage(hours)")["Social Media Fatigue Score"].mean().reset_index()


fig11 = px.line(
    avg_fatigue,
    x="Daily Social Media Usage(hours)",
    y="Social Media Fatigue Score",
    markers=True
)

fig11.update_layout(
    xaxis_title="Daily Social Media Usage(hours)",
    yaxis_title="Average Social Media Fatigue Score",
    height=600
)


st.plotly_chart(fig11, use_container_width=True, key="fatigue_by_usage_line")

st.info("💡 There’s a rising trend in social media fatigue scores as daily usage increases.")



#Figure 12: Sleep Quality vs. Addiction Score
st.markdown("### 😴 Average Sleep Quality by Addiction Score")
avg_sleep = filtered_data.groupby("Self Reported Addiction Score")["Sleep Quality"].mean().reset_index()


fig12 = px.line(
    avg_sleep,
    x="Self Reported Addiction Score",
    y="Sleep Quality",
    markers=True
)

fig12.update_layout(
    xaxis_title="Self Reported Addiction Score",
    yaxis_title="Average Sleep Quality",
    height=600
)


st.plotly_chart(fig12, use_container_width=True, key="sleep_by_addiction_line")

st.info("💡 This suggests that higher self-reported addiction is associated with poorer sleep, especially after crossing a certain threshold")




# Figure 13: Mental Health vs. Addiction Score
st.markdown("### 🧠 Average Sleep Quality by Mental Health Status")

avg_sleep_mentalhealth = filtered_data.groupby("Mental Health Status")["Sleep Quality"].mean().reset_index()


fig13 = px.bar(
    avg_sleep_mentalhealth,
    x="Mental Health Status",
    y="Sleep Quality",
    text_auto=".2f",
    category_orders={"Mental Health Status": ["Poor", "Fair", "Good", "Excellent"]},
    color="Mental Health Status"
)

fig13.update_layout(
    xaxis_title="Mental Health Status",
    yaxis_title="Average Sleep Quality",
    height=600
)


st.plotly_chart(fig13, use_container_width=True, key="sleep_by_Mental_Health Status")

st.info("💡 Improved mental health is associated with better sleep quality. ")


# Figure 14: Addiction Score vs. Social Media Fatigue
st.markdown("### 💥 Average Social Media Fatigue by Addiction Score")

avg_social_media_fatigue = filtered_data.groupby("Self Reported Addiction Score")["Social Media Fatigue Score"].mean().reset_index()

fig14 = px.line(
    avg_social_media_fatigue,
    x="Self Reported Addiction Score",
    y="Social Media Fatigue Score",
    markers=True
)

fig14.update_layout(
    xaxis_title="Addiction Score",
    yaxis_title="Average Social Media Fatigue Score",
    height=600
)

st.plotly_chart(fig14, use_container_width=True, key="addict_vs_fatigue")
st.info("💡 Positive correlation: Higher addiction scores are associated with increased social media fatigue.")
