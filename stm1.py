import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import japanize_matplotlib
#ros.chdir('C:\Users\kasei\新しいフォルダー\st')
#from streamlit-pandas_profiling import stProfile

st.title('欠品チェック app')

data_file = st.file_uploader('Upload data',type=['xlsx','csv'])

#st.beta_set_page_config(layout='wide')

if data_file is not None :
    df = pd.read_excel(data_file,sheet_name='欠品データ')


#df = pd.read_excel(r'C:\Users\kasei\Downloads\欠品チェック.xlsx',sheet_name='欠品データ')
    
    #sidebar
    col1 = st.sidebar
    col1.header('店舗名と日付を選択して下さい')


    #sort 店舗名
    data1 = df['店舗名'].unique()
    df1 = df.set_index('店舗名')
    option1 = col1.selectbox("店舗名",data1)
    df2_1 = df1.loc[option1]

    #sort 貼付日

    date2 = df2_1['貼付日'].unique()
    df2 = df2_1.set_index('貼付日')
    option2 = col1.selectbox("貼付日",date2)
    df2_2 = df2_1[df2_1['貼付日'] == option2 ]


    #sort 週発注回数

    #data4 = df['週発注回数'].unique()
    #df4 = st.sidebar.multiselect("週発注回数",data4)
    #df_select1 = df[df["週発注回数"] == df4]

#  
    
    #sort 中分類名
    data3 = df['中分類名'].unique()
    #df3 = st.multiselect("中分類",data3)
    #df_select = df2_2[(df2_2['中分類名'].isin(df3))]

    #図
    df1_1 = df2_2.groupby('中分類名').count()
    df1_2 = df1_1['中分類']

    #図2

    def pie(df1_2):
        df1_2 = df1_2.sort_values(ascending=False)
        df1_2 = df1_2[0:10]
        label = df1_2.index
        #labe2 = df1['中分類名']
        #explode=[0.5,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0]
        plt.pie(df1_2,labels=label,radius=1.5,startangle=90,autopct='%1.1f%%',counterclock=False,pctdistance=0.8)
        #plt.legend(label,bbox_to_anchor=(1.5,1),loc = 'upper left')
        #plt.pie(x = labe2,labels=date1,startangle=90,counterclock=False,
        #      radius = 0.8,labeldistance = 0.6)
        #plt.pie([70],colors='white',radius=0.5)
        plt.title(df2_2['店舗コード'][0],y = -0.3)
        plt.show()

    #図3小分類
    def small(option3):
        df_sum = df2_2.groupby(['中分類名','小分類名']).count()
        df3_1 = df_sum['中分類'].loc[option3].sort_values(ascending=False)
        index = df3_1.index
        plt.pie(df3_1,labels= index,radius=1.5,startangle=90,
               autopct='%1.1f%%',counterclock=False,pctdistance=0.8)
        #plt.figure(figsize=(3,6))
        plt.pie([2],colors='white',radius=1)
        plt.show()
        st.table(df3_1)

    #def select_store(store):

    ######################################################
    st.dataframe(df2_2.loc[option1].head(100))
    st.write('総欠品数:',len(df2_2['中分類']))


    #report = ProfileReport(df)
    st.bar_chart(df1_2.sort_values(ascending=False))

    st.subheader('中分類円グラフ')
    st.pyplot(pie(df1_2))

    
    if st.checkbox('中分類分析:'):
        st.subheader('中分類分析')
        df3 = st.multiselect("中分類",data3)
        df_select = df2_2[(df2_2['中分類名'].isin(df3))]
        st.markdown('中分類項目:')
        st.dataframe(df_select)
        st.write('中分類欠品数:',len(df_select['中分類']))

    
    if st.checkbox('小分類分析:'):
        st.subheader('小分類分析')
        option3 = st.selectbox('小分類円グラフ',data3)
        st.markdown('小分類欠品割合:')
        st.pyplot(small(option3))

    
    if st.checkbox('週発注欠品:'):
        week = df['週発注回数'].unique()
        week_select = st.selectbox('週発注回数:',week)
        df_week = df2_2.set_index('週発注回数')
        df5_1 = df_week.loc[week_select].head(100)
        st.dataframe(df5_1)
        st.write('欠品数:',len(df5_1['中分類名']))


    if st.checkbox('欠品数割合比較:'):
        row1, row2 = st.beta_columns(2)
        with row1:
            option3 = st.selectbox("貼付日1",date2)
            df2_3 = df2_1[df2_1['貼付日'] == option3]
            df4_1 = df2_3.groupby('中分類名').count()
            df4_2 = df4_1['中分類'].sort_values(ascending=False)
            st.title(str(option3))
            st.pyplot(pie(df4_2))
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.write('総欠品数:',len(df2_3['中分類']))
            st.write(df4_2)
            
        with row2:
            option4 = st.selectbox("貼付日2",date2)
            df2_4 = df2_1[df2_1['貼付日'] == option4 ]
            df4_2 = df2_4.groupby('中分類名').count()
            df4_3 = df4_2['中分類'].sort_values(ascending=False)
            st.title(str(option4))
            st.pyplot(pie(df4_3))
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.write('総欠品数:',len(df2_4['中分類']))
            st.write(df4_3)