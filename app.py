import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

from helper import most_common_words, daily_timeline

st.sidebar.title("Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")


    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        #stats area
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top statistic")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='darkgreen')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        # Create a wider figure with adjusted height (without changing the color)
        fig, ax = plt.subplots(figsize=(20, 8))  # Increase width (20) and height (8)
        ax = sns.heatmap(user_heatmap, ax=ax, cbar_kws={'shrink': 0.5})  # Keep the existing color scheme

        # Set aspect ratio for uniform cells
        ax.set_aspect('auto')

        # Rotate the x and y axis labels for better readability
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)

        # Display the heatmap
        st.pyplot(fig)


        #finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')

            # Assuming the helper function `most_busy_users` returns two values: `x` for user counts and `new_df` for user data
            x, new_df = helper.most_busy_users(df)

            # Create the figure for the bar plot
            fig, ax = plt.subplots()

            # Define two columns to show both the plot and the dataframe
            col1, col2 = st.columns(2)

            # Display the bar chart in the first column
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')  # Rotate the x-axis labels for better readability
                st.pyplot(fig)

            # Display the dataframe in the second column
            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        # Streamlit code
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.bar(emoji_df['emoji'], emoji_df['count'])
            ax.set_xlabel("Emojis")
            ax.set_ylabel("Count")
            st.pyplot(fig)








