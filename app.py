import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat Analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # bytes_data = uploaded_file.getvalue()
    # data = bytes_data.decode("utf-8")
    #st.text(data)

    data = uploaded_file.read().decode("utf-8").splitlines()

    df = preprocessor.preprocess(data)

    df.drop(columns=['user_message'] , inplace =True) 


    # st.dataframe(df)


    #fetch unique users

    user_list= df['user'].unique().tolist()
    user_list.remove('group_notif')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    if st.sidebar.button("Show Analysis"):

        #stats area
        num_messages,words,num_media_msg, num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        

        col1, col2 , col3, col4 = st.columns(4)

        with col1:
            st.header("All Messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        
        #monthly_timeline
        st.title('Monthly Activity')
        timeline = helper.monthly_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')

        st.pyplot(fig)


        #daily_timeline
        st.title('Daily activity')
        daily_timeline = helper.daily_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color = 'black')
        plt.xticks(rotation='vertical')

        st.pyplot(fig)


        #activity map
        st.title("Activity map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Bussiest Day")
            busy_day = helper.week_activity_map(selected_user,df)

            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Bussiest Month")
            busy_month = helper.month_activity_map(selected_user,df)

            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            st.pyplot(fig)    

        st.title('Heat map')
        user_heatmap = helper.activiy_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)



        #most active user in group
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
           

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most comon words
        st.title("Word Frequency")
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])

        st.pyplot(fig)

        st.dataframe(most_common_df)



    