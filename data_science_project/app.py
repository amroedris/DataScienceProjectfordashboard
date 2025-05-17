# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

#choose the data set

st.set_page_config(layout="wide")
st.sidebar.title("📂 Dataset Selection")
dataset_option = st.sidebar.selectbox("Choose a dataset:", ["Dataset 1: master-5.csv", "Dataset 2: addiction.csv"])


if dataset_option == "Dataset 1: master-5.csv":
    # Load data
    data = pd.read_csv("master-5 2.csv")
    dataset_name = "master-5.csv"
    dataset_type = "structured survey with mental health + behavioral indicators"
    show_dataset = "Dataset 1"
else:
    data = pd.read_csv("mobile_addiction.csv")
    dataset_name = "addiction.csv"
    dataset_type = "addiction-focused behavioral data"
    show_dataset = "Dataset 2"


st.markdown(f"### 📊 Visualizing {show_dataset}")
st.markdown(f"**Source**: `{dataset_name}`  ")
st.markdown(f"**Description**: {dataset_type}")

st.sidebar.title("📊 Visualization Mode")
viz_mode = st.sidebar.radio("Select visualization type:", ["Static Visualizations", "Interactive Dashboard"])


st.title("📱 Social Media & Smartphone Addiction Dashboard")
if show_dataset == "Dataset 1":

    if viz_mode == "Static Visualizations":
        st.markdown("#### Static Plots for Dataset 1")


        # Static plots for Dataset 1
        st.markdown("### 📈 Addiction Score Distribution")
        fig0 = px.histogram(
            data,
            x="Self Reported Addiction Score",
            nbins=10
        )


        st.plotly_chart(fig0, use_container_width=True, key="staticd1f0")

        st.info(
            "💡 Most participants think they are addicted to their smartphones.")


        st.markdown("### 📈 Avg Addiction Score vs Age ")


        fig1 = px.histogram(
            data,
            x="Age",
            y="Self Reported Addiction Score",
            histfunc="avg",
            nbins=10
        )


        st.plotly_chart(fig1, use_container_width=True, key="staticd1f1")
        st.info(
            "💡 Most ages have high average addiction scores circling around 8.3 to 8.6.")



        st.markdown("### 📈 Addiction Score vs Avg Sleep Quality ")

        avg_sleep_quality = data.groupby("Self Reported Addiction Score")["Sleep Quality"].mean().reset_index()

        fig2 = px.scatter(
            avg_sleep_quality,
            x="Self Reported Addiction Score",
            y="Sleep Quality"
        )


        st.plotly_chart(fig2, use_container_width=True, key="staticd1f2")
        st.info(
            "💡 Average Sleep quality decreased as addiction score increase, then stabilizes")


        st.markdown("### 📈 Addiction Score vs Avg Anxiety Score ")

        avg_anx_quality = data.groupby("Self Reported Addiction Score")["Anxiety Score"].mean().reset_index()

        fig3 = px.line(
            avg_anx_quality,
            x="Self Reported Addiction Score",
            y="Anxiety Score"
        )


        st.plotly_chart(fig3, use_container_width=True, key="staticd1f3")
        st.info(
            "💡 As the addiction score rises, the anxiety score rises. Positive correlation")


        st.markdown("### 📈 Addiction Score vs Avg Self-Esteem Score ")

        avg_selfesteem_quality = data.groupby("Self Reported Addiction Score")["Self Esteem Score"].mean().reset_index()

        fig4 = px.line(
            avg_selfesteem_quality,
            x="Self Reported Addiction Score",
            y="Self Esteem Score"
        )

        st.plotly_chart(fig4, use_container_width=True, key="staticd1f4")
        st.info(
            "💡 As the addiction score increases, the anxiety score decreases. Negative correlation")



        st.markdown("### 📈Avg Addiction Score vs  Mental Health Status ")

        avg_add_mental_health = data.groupby("Mental Health Status")["Self Reported Addiction Score"].mean().reset_index()

        fig5 = px.bar(
            avg_add_mental_health,
            x="Mental Health Status",
            y="Self Reported Addiction Score",
            category_orders=["Poor", "Fair", "Good", "Excellent"]
        )

        st.plotly_chart(fig5, use_container_width=True, key="staticd1f5")
        st.info(
            "💡 People will high addiction scores tend to have poor mental health status. ")



        st.markdown("### 📈 Daily Usage vs Avg Addiction Score ")

        avg_addiction_by_usage = data.groupby("Daily Social Media Usage(hours)")["Self Reported Addiction Score"].mean().reset_index()

        fig6 = px.line(
            avg_addiction_by_usage,
            x="Daily Social Media Usage(hours)",
            y="Self Reported Addiction Score"
        )

        st.plotly_chart(fig6, use_container_width=True, key="staticd1f6")
        st.info(
            "💡 The higher the daily usage, the more prone a participant becomes to smartphone addiction. ")





        st.markdown("### 📈 Platforms vs Daily Usage")



        fig7 = px.histogram(
            data,
            x="Number of Social Media Platforms",
            y="Daily Social Media Usage(hours)",
            histfunc="avg"
        )

        fig7.update_traces(marker_line_color="black", marker_line_width=1)


        st.plotly_chart(fig7, use_container_width=True, key="staticd1f7")
        st.info(
            "💡 Regardless of the number of social media platforms, the average daily usage remains around 5 hours.")





        st.markdown("### 📈 Frequency of Posts vs Daily Usage")
        avg_usage_by_posts = data.groupby("Frequency of Posts")["Daily Social Media Usage(hours)"].mean().reset_index()

        fig8 = px.bar(
            avg_usage_by_posts,
            x="Frequency of Posts",
            y="Daily Social Media Usage(hours)",
            category_orders={
                "Frequency of Posts": ["Never", "Rarely", "Sometimes", "Often", "Always"]
            }
        )
        st.plotly_chart(fig8, use_container_width=True, key="staticd1f8")

        st.info(
            "💡 Frequency of posts doesn't have a significant affect on daily usage. ")

        st.markdown("### 📈 Notification Frequency vs Daily Usage")

        avg_usage_by_notif = data.groupby("Frequency of Checking Notifications")["Daily Social Media Usage(hours)"].mean().reset_index()

        fig9 = px.bar(
            avg_usage_by_notif,
            x="Frequency of Checking Notifications",
            y="Daily Social Media Usage(hours)",

            category_orders={
                "Frequency of Checking Notifications": ["Rarely", "Occasionally", "Frequently"]
            }
        )


        st.plotly_chart(fig9, use_container_width=True, key="staticd1f9")
        st.info(
            "💡 Frequency of checking notifications also doesn't have a huge affect on daily usage. ")









    elif viz_mode == "Interactive Dashboard":
        st.markdown("#### Interactive Dashboard for Dataset 1")
        # Displays the dashboard title at the top.


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

        Addiction_Range = st.sidebar.slider(
            "Select Addiction Score Range",
            int(data["Self Reported Addiction Score"].min()),
            int(data["Self Reported Addiction Score"].max()),
            (int(data["Self Reported Addiction Score"].min()),
             int(data["Self Reported Addiction Score"].max()))
        )

        # Creates a slider in the sidebar to let the user select an age range.
        age_range = st.sidebar.slider(
            "Select Age Range",
            int(data["Age"].min()),
            int(data["Age"].max()),
            (int(data["Age"].min()), int(data["Age"].max()))
        )


        mh_options = data["Mental Health Status"].dropna().unique().tolist()

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
        data["Cyberbullying Experience"] = data["Cyberbullying Experience"].replace({0:"No", 1:"Yes"})
        cyber_options = data["Cyberbullying Experience"].dropna().unique().tolist()

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
            (data["Cyberbullying Experience"].isin(cyber_selection)) &
            (data["Self Reported Addiction Score"] >= Addiction_Range[0]) &
            (data["Self Reported Addiction Score"] <= Addiction_Range[1])
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
        st.info(
            "💡 The dataset includes a fairly balanced number of male and female participants, with a small number identifying as 'Others'.")

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

        notif_dist = filtered_data.groupby(["Gender", "Frequency of Checking Notifications"]).size().reset_index(
            name="Count")

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

        # Figure 3: Self Esteem Score Distribution
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

        # Figure 4: Average daily usage
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
        st.info("💡 Daily social media usage is fairly consistent across genders, with no significant differences observed.")


        # Figure 5: Anxiety Score by Gender
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

        # Figure 6: Daily Usage vs. Addiction Score
        st.markdown("### 🔁 Daily Usage vs. Addiction Score")

        scatter_data = filtered_data.dropna(subset=["Anxiety Score"])

        fig6 = px.scatter(
            scatter_data,
            x="Daily Social Media Usage(hours)",
            y="Self Reported Addiction Score",
            color="Gender",
            size="Anxiety Score",
            hover_data=["Gender","Self Esteem Score", "Sleep Quality"]
        )

        fig6.update_layout(
            xaxis_title="Daily Social Media Usage(hours)",
            yaxis_title="Self Reported Addiction Score",
            height=600
        )

        st.plotly_chart(fig6, use_container_width=True, key="usage_vs_addiction")
        st.info(
            "💡 There’s a clear positive correlation between daily social media usage and self-reported addiction score.")

        # Figure 7: Mental Health Status Count
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

        st.info(
            "💡 Most participants report poor mental health status, with fewer reporting excellent mental health.")

        # Figure 8: Daily Usage vs. Average Anxiety Score
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

        st.info(
            "💡 Anxiety scores tend to increase with higher daily social media usage, suggesting a positive correlation.")

        # Figure 9: Impact of Cyberbullying on Self Esteem and Anxiety
        st.markdown("### 🔁 Impact of Cyberbullying on Self Esteem and Anxiety")

        grouped = filtered_data.groupby("Cyberbullying Experience")[
            ["Self Esteem Score", "Anxiety Score"]].mean().reset_index()
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

        # Figure 10: Age vs Self Esteem and Anxiety
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

        st.info("💡 Anxiety peaks around age 30, while self-esteem is at its lowest point. This suggests that early adulthood may be a more mentally stressful period.")

        # Figure 11: Avg Social Media Fatigue by Usage Hours
        st.markdown("### 📈 Average Social Media Fatigue by Usage Hours")
        avg_fatigue = filtered_data.groupby("Daily Social Media Usage(hours)")[
            "Social Media Fatigue Score"].mean().reset_index()

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

        # Figure 12: Sleep Quality vs. Addiction Score
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

        st.info(
            "💡 This suggests that higher self-reported addiction is associated with poorer sleep, especially after crossing a certain threshold")

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

        avg_social_media_fatigue = filtered_data.groupby("Self Reported Addiction Score")[
            "Social Media Fatigue Score"].mean().reset_index()

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


elif show_dataset == "Dataset 2":
    if viz_mode == "Static Visualizations":
        st.markdown("#### Static Plots for Dataset 2")
        # Static plots for Dataset 2

        st.markdown("### 📈 Addiction Distribution")

        addicted_dist = data["addicted"].value_counts().reset_index()
        fig0 = px.pie(
            addicted_dist,
            names="addicted",
            values="count"
        )
        st.plotly_chart(fig0, use_container_width=True, key="staticd2f0")
        st.info(
            "💡 Around 50.4% of people are addicted to social media")



        st.markdown("### 📈 Addiction Status by Daily Usage")

        fig1 = px.box(
            data,
            x="addicted",
            y="daily_screen_time",
            color="addicted",
            color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
            labels={"daily_screen_time": "Daily Screen Time (hours)", "addicted": "Addiction Status"}
        )
        st.plotly_chart(fig1, use_container_width=True, key="staticd2f1")
        st.info(
            "💡 Addicted people tend to use the phone more often")



        st.markdown("### 📈 Avg Daily Usage by Age")

        fig2 = px.histogram(data, x = "age", y = "daily_screen_time", nbins= 10, histfunc= "avg")
        st.plotly_chart(fig2, use_container_width=True, key="staticd2f2")

        st.info(
            "💡 Teenagers have the most screen time averaging at around 4.5 hours per day")

        st.markdown("### 📈 Addiction Status by Night Usage")

        fig3 = px.box(
            data,
            x="addicted",
            y="night_usage",
            color="addicted",
            color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
            labels={"night_usage": "Night Usage (hours)", "addicted": "Addiction Status"}
        )
        st.plotly_chart(fig3, use_container_width=True, key="staticd2f3")
        st.info(
            "💡 Users classified as addicted tend to spend more time on their phones after bedtime."
        )

        st.markdown("### 📈 Addiction Status by App Sessions")

        fig4 = px.box(
            data,
            x="addicted",
            y="app_sessions",
            color="addicted",
            color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
            labels={"app_sessions": "App Sessions", "addicted": "Addiction Status"}
        )
        st.plotly_chart(fig4, use_container_width=True, key="staticd2f4")
        st.info(
            "💡 Addicted users typically open apps more frequently throughout the day."
        )

        st.markdown("### 📈 Work/Study Hours by Addiction Status")

        fig5 = px.box(
            data,
            x="addicted",
            y="work_study_hours",
            color="addicted",
            color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
            labels={"work_study_hours": "Work/Study Hours", "addicted": "Addiction Status"}
        )
        st.plotly_chart(fig5, use_container_width=True, key="staticd2f5")
        st.info(
            "💡 Addicted individuals tend to spend slightly fewer hours on work or study tasks compared to non-addicted individuals."
        )




    elif viz_mode == "Interactive Dashboard":
        st.markdown("#### Interactive Dashboard for Dataset 2")
        # Displays the dashboard title at the top.

        # Adds a sidebar section titled “Filter Data” where you’ll place all user input widgets.
        st.sidebar.header("🔎 Filter Data")


        # Creates a slider in the sidebar to let the user select a screen time range.
        daily_range2 = st.sidebar.slider(
            "Select Daily Social Media Usage Range (hours)",
            int(data["daily_screen_time"].min()),
            int(data["daily_screen_time"].max()),
            (int(data["daily_screen_time"].min()),
             int(data["daily_screen_time"].max()))
        )

        # Creates a slider in the sidebar to let the user select an age range.
        age_range2 = st.sidebar.slider(
            "Select Age Range",
            int(data["age"].min()),
            int(data["age"].max()),
            (int(data["age"].min()), int(data["age"].max()))
        )




        # Get the unique values in the "addicted" column
        addiction_options2 = data["addicted"].dropna().unique().tolist()

        addiction_filter2 = st.sidebar.multiselect(
            "Addiction Status",
            options=["All"] + addiction_options2,
            default=["All"]
        )

        if "All" in addiction_filter2 and len(addiction_filter2) > 1:
            addiction_filter2.remove("All")

        if "All" in addiction_filter2 or not addiction_filter2:
            addiction_selection2 = addiction_options2
        else:
            addiction_selection2 = addiction_filter2

        # Apply filters
        filtered_data = data[
            (data["age"] >= age_range2[0]) &
            (data["age"] <= age_range2[1]) &
            (data["daily_screen_time"] >= daily_range2[0]) &
            (data["daily_screen_time"] <= daily_range2[1]) &
            (data["addicted"].isin(addiction_selection2))
            ]

        # Figure 0: Addiction Status Distribution
        st.markdown("### 👥 Addiction Status Distribution")

        addicted_dist = filtered_data["addicted"].value_counts().reset_index()

        fig0 = px.pie(
            addicted_dist,
            names="addicted",
            values="count",
            color="addicted",
            color_discrete_map={
                "Yes": "#AED6F1",
                "No": "#1f77b4"
            }
        )

        fig0.update_layout(
            height=600
        )

        st.plotly_chart(fig0, use_container_width=True, key="addicted_dist_pie")
        st.info(
            "💡 Just over half of the participants (50.4%) are classified as addicted, highlighting how widespread smartphone dependency has become.")

        st.markdown("### 📊 Avg Screen Time by Addiction")

        avg_screen = data.groupby("addicted")["daily_screen_time"].mean().reset_index()
        fig1 = px.bar(avg_screen, x="addicted", y="daily_screen_time",
                      color="addicted",
                      color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                      labels={"daily_screen_time": "Average Screen Time (hrs)", "addicted": "Addiction Status"},
                      text_auto=".2f")
        st.plotly_chart(fig1, use_container_width=True)

        st.info(
            "💡 Average screen time is drastically more for addicted individuals (4.5 hours) compared to non-addicted individuals (3 hours).")

        st.markdown("### 🌙 Avg Stress Level vs Night Usage")

        avg_sleep = data.groupby("night_usage")["stress_level"].mean().reset_index()
        fig2 = px.scatter(avg_sleep, x="night_usage", y="stress_level",
                          color="stress_level", opacity=0.7,
                          color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                          labels={"night_usage": "Night Usage (hrs)", "stress_level": "Stress Level"})
        st.plotly_chart(fig2, use_container_width=True)

        st.info(
            "💡 Clear positive correlation: when night usage increases, stress level increases.")

        st.markdown("### 🎮 Gaming Time by Addiction Status")

        fig3 = px.bar(data.groupby("addicted")["gaming_time"].mean().reset_index(),
                      x="addicted", y="gaming_time",
                      color="addicted",
                      color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                      labels={"gaming_time": "Avg Gaming Time (hrs)", "addicted": "Addiction Status"},
                      text_auto=".2f")
        st.plotly_chart(fig3, use_container_width=True)

        st.info(
            "💡 Addicted individuals tend to game more than non-addicted individuals.")

        st.markdown("### 🔔 Notifications vs Avg Stress Level")

        avg_noti = data.groupby("notifications")["stress_level"].mean().reset_index()
        fig4 = px.scatter(avg_noti, x="notifications", y="stress_level",
                          color="stress_level", opacity=0.7,
                          color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                          labels={"notifications": "Notifications (per day)", "stress_level": "Stress Level"})
        st.plotly_chart(fig4, use_container_width=True)

        st.info(
            "💡 Stress level elevates with the increase of notifications (per day)")



        st.markdown("### 👤 Age vs Daily Screen Time")

        avg_screen_age = data.groupby("age")["daily_screen_time"].mean().reset_index()
        fig5 = px.line(avg_screen_age, x="age", y="daily_screen_time",
                       labels={"daily_screen_time": "Avg Screen Time (hrs)", "age": "Age"})
        st.plotly_chart(fig5, use_container_width=True)

        st.info(
            "💡 As people get older, they tend to use their phones less. ")


        st.markdown("### 📚 Work/Study Hours by Addiction Status")

        fig6 = px.box(data, x="addicted", y="work_study_hours", color="addicted",
                      color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                      labels={"work_study_hours": "Work/Study Hours", "addicted": "Addiction Status"})
        st.plotly_chart(fig6, use_container_width=True)

        st.info(
            "💡 Non-addicted individuals tend to spend more time on work/study tasks compared to addicted individuals.")

        st.markdown("### 📱 Avg Stress Level vs App Sessions")
        avg_app_sess = data.groupby("app_sessions")["stress_level"].mean().reset_index()
        fig7 = px.scatter(data, x="app_sessions", y="stress_level",
                          color="stress_level", opacity=0.7,
                          color_discrete_map={"Yes": "#1f77b4", "No": "#AED6F1"},
                          labels={"app_sessions": "App Sessions", "stress_level": "Stress Level"})
        st.plotly_chart(fig7, use_container_width=True)

        st.info(
            "💡 More app sessions lead to higher stress levels. ")



