import streamlit as st
import preprocessor, helper
from datetime import datetime
from matplotlib import pyplot as plt
import seaborn as sns


st.set_page_config(layout="wide")

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    #fetch unique user
    user_list = df['users'].unique().tolist()

    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

    
    #KPIs
    if st.sidebar.button("Show Analysis"):
        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.text("Total Messages")
            st.title(num_messages)
        with col2:
            st.text("Total Words")
            st.title(words)
        with col3:
            st.text("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.text("Links Shared")
            st.title(links)

        # Monthly Timeline
        st.title("Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color = 'purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        #Activity Map
        st.title('Activity Map')

        col1, col2 = st.columns(2)

        with col1:
            st.header("Busiest Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            bars = ax.bar(busy_day.index, busy_day.values, color = "red")
            ax.bar_label(bars, labels=busy_day.values, padding=3)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        with col2:
            st.header("Busiest Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            bars = ax.bar(busy_month.index, busy_month.values, color = "green")
            ax.bar_label(bars, labels=busy_month.values, padding=3)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

       
       #Activity Heatmap

        # Ensure proper day and period order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        period_order = [
            '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10','10-11','11-12','12-13',
            '13-14','14-15','15-16','16-17','17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
        ]

        # Your function should return a DataFrame (user_heatmap) with index=dayname, columns=period
        user_heatmap = helper.activity_heatmap(selected_user, df)

        # Reorder the DataFrame
        user_heatmap = user_heatmap.reindex(index=day_order)
        user_heatmap = user_heatmap[[p for p in period_order if p in user_heatmap.columns]]

        # Plot
        st.title("Weekly Activity Heatmap")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(user_heatmap, ax=ax, cmap="YlOrRd", linewidths=0.3, linecolor='gray')  # light to dark
        st.pyplot(fig)




        #Busiest User
        if selected_user == "Overall":
            st.title("Busiest Users")

            x, new_df = helper.fetch_busiest_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                bars = ax.bar(x.index,x.values)
                ax.bar_label(bars, labels=x.values, padding=3)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordcount
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        bars = plt.barh(most_common_df[0],most_common_df[1], color = 'orange')
        ax.bar_label(bars, labels=most_common_df[1], padding=3)
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        #emoji
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_df = emoji_df.head(10)
            plt.rcParams['font.family'] = 'Segoe UI Emoji' 
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct="%0.2f%%")
            st.pyplot(fig)