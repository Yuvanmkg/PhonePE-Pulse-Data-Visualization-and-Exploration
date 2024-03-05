import streamlit as st
import sys
sys.path.insert(1, "C:/Users/GANAPATHI.S/Desktop/guviproject1/phonepe.py/streamlit_option_menu")
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests 
import json

#Dataframe Creation
#sql connection
mydb= psycopg2.connect(host= "localhost",
                       user="postgres",
                       port= "5432",
                       database="phonepe_data",
                       password= "1234")

cursor=mydb.cursor()


#aggregated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#aggregated_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))



#aggregated_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))



#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))



#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))

def transaction_amount_count_Y(df,year):
    

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace = True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:


        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount",title=f"{year}TRANSACTION AMOUNT",           color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount,height= 650,width= 600)


    tacy=Aggre_insurance[Aggre_insurance["Years"] == 2021]
    tacy.reset_index(drop = True, inplace = True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_count",title=f"{year}   TRANSACTION COUNT",           color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650, width= 600)
        st.plotly_chart(fig_count)

   

    col1,col2 = st.columns(2)
    with col1:
            
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1=json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States",  featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION_AMOUNT", fitbounds= "locations", 
                                height= 650,width= 600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1) 

    with col2:    
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations= "States",  featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION_COUNT", fitbounds= "locations", 
                                height= 650,width= 600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


def transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace = True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION_AMOUNT",           color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        
        st.plotly_chart(fig_amount)

    with col2:
        tacy=Aggre_insurance[Aggre_insurance["Years"] == 2021]
        tacy.reset_index(drop = True, inplace = True)

        tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
        tacyg.reset_index(inplace= True)

        fig_count=px.bar(tacyg, x="States", y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION_COUNT",           color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1=json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States",  featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION_AMOUNT", fitbounds= "locations", 
                                height= 650,width= 600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1) 

    with col2:
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations= "States",  featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION_COUNT", fitbounds= "locations", 
                                height= 650,width= 600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy



def Aggre_tran_transaction_type(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    
    with col1:
        fig_pie_1=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount", 
                    width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count", 
                width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
    st.plotly_chart(fig_pie_2) 


#Aggregated_User_Analysis_1
def Aggre_user_plot_1(df, year):
        aguy= df[df["Years"]== year]
        aguy.reset_index(drop= True, inplace= True)

        aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
        aguyg.reset_index(inplace= True)

        fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f" {year} BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")

        st.plotly_chart(fig_bar_1)

        return aguy

#Aggre_user_Analysis_2

def Aggre_user_plot_2(df, quarter):
        aguyq= df[df["Quarter"]== quarter]
        aguyq.reset_index(drop= True, inplace= True)

        aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
        aguyqg.reset_index(inplace= True)

        fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")

        st.plotly_chart(fig_bar_1)

        return aguyq


#Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y = "Transaction_count", hover_data= "Percentage", 
                    title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)    


#Map_Insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)
    
    tacyg= tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
   
    fig_bar_1=px.bar(data_frame= tacyg, x="Transaction_amount", y="District", orientation= "h",
                    title= f"{state} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
    st.plotly_chart(fig_bar_1)


    fig_bar_1=px.bar(data_frame= tacyg, x="Transaction_count", y="District", orientation= "h",
                    title= f"{state} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_bar_2)



# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)
    muyg

    fig_line_1= px.line(muyg, x= "States", y = ["RegisteredUser", "AppOpens"], 
                    title= f"{year} REGISTERED USER APPOPENS",width= 1000, height= 800, markers= True)
    fig_line_1.show() 

    return muy


# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)
    

    fig_line_1= px.line(muyqg, x= "States", y = ["RegisteredUser", "AppOpens"], 
                    title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True, 
                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
    fig_line_1.show() 

    return muyq


#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)
    
    col1,col2= st.columns(2)
    with col1:  
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District",   orientation= "h",
                                title=f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District",   orientation= "h",
                                title=f"{states.upper()}APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

 


#top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= Top_insur_tac_Y[Top_insur_tac_Y["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    tiyg= tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace= True)
    tiyg

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y = "Transaction_amount", hover_data= "Pincodes",
                    title= "TRANSACTION AMOUNT", width= 650, height= 600, 
                    color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plolty_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y = "Transaction_count", hover_data= "Pincodes",
                    title= "TRANSACTION COUNT", width=600 , height= 600, 
                    color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df, year):
        tuy= df[df["Years"]== year]
        tuy.reset_index(drop= True, inplace= True)

        tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
        tuyg.reset_index(inplace= True)
       

        fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                            color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                            title= f"{year} REGISTERED USERS")
        st.plotly_chart(fig_top_plot_1)

        return tuy

#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= Top_user_Y[Top_user_Y["Years"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x="Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)



#Streamlit Part 

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select= option_menu("Main Menu", ["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    pass

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])

    with tab1:
        
        method = st.radio("Select The Method",["Insurance Analysis","Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            
          col1,col2= st.columns(2)
          with col1:
       

             years= st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
          tac_Y= transaction_amount_count_Y(Aggre_insurance, years)

          col1,col2= st.columns(2)
          with col1:


              quarters= st.slider("Select The Quarter",Aggre_insurance["Quarter"].min(), tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
          tac_Y= transaction_amount_count_Y(Aggre_insurance, years)

          transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method == "Transaction Analysis":
                    
          col1,col2= st.columns(2)
          with col1:
       

             years= st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
          Aggre_tran_tac_Y= transaction_amount_count_Y(Aggre_transaction, years)

          col1,col2=st.columns(2)
          with col1:
              states= st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
              
          Aggre_tran_transaction_type(Aggre_tran_tac_Y, states)

          col1,col2= st.columns(2)
          with col1:

              quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
          tac_Y= transaction_amount_count_Y(Aggre_insurance, years)

          Aggre_tran_tac_Y_Q= transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

          col1,col2=st.columns(2)
          with col1:
              states= st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())
              
          Aggre_tran_transaction_type(Aggre_tran_tac_Y_Q, states)

        elif method == "User Analysis":
          
          col1,col2=st.columns(2)
          with col1:

                years= st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
                Aggre_user_Y=  Aggre_user_plot_1(Aggre_user, years)
 
            
          col1,col2= st.columns(2)
          with col1:

              quarters= st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
          tac_Y= transaction_amount_count_Y(Aggre_insurance, years)

          Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y,quarters)
           

          col1,col2=st.columns(2)
          with col1:
              states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())
              
          Aggre_user_plot_3(Aggre_user_Y_Q, states)
                
            
        with tab2:

            method_2 = st.radio("Select The Method",["Map Insurance","Map Transaction", "Map User"])

            if method_2 == "Map Insurance":

                col1,col2=st.columns(2)
                with col1:

                    years= st.slider("Select The Year_mi", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min())
                map_insur_tac_Y= transaction_amount_count_Y(map_insurance, years)

                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_mi",  map_insur_tac_Y["States"].unique())
                
                Map_insur_District(map_insur_tac_Y, states)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter_mi",map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            
                map_insur_tac_Y_Q= transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["States"].unique())
                    
                Map_insur_District(map_insur_tac_Y_Q, states)


                

            elif method_2 == "Map Transaction":
                col1,col2=st.columns(2)
                with col1:

                    years= st.slider("Select The Year", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min())
                map_tran_tac_Y= transaction_amount_count_Y(map_transaction, years)

                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_mi",  map_tran_tac_Y["States"].unique())
                
                Map_insur_District(map_tran_tac_Y, states)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter_mt",  map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            
                map_tran_tac_Y_Q= transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_Ty",  map_tran_tac_Y_Q["States"].unique())
                    
                Map_insur_District(map_insur_tac_Y_Q, states)



            elif method_2 == "Map User":
                col1,col2=st.columns(2)
                with col1:

                    years= st.slider("Select The Year_mu", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
                map_user_Y= map_user_plot_1(map_user, years)

    
                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter_mu",  map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            
                map_user_Y_Q= map_user_plot_2(map_user_Y,quarters)


                
                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_mu",  map_user_Y_Q["States"].unique())
                    
                map_user_plot_3(map_user_Y_Q, states)



    
    with tab3:

        method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction", "Top User"])

        if method_3 == "Top Insurance":

             col1,col2=st.columns(2)
             with col1:

                years= st.slider("Select The Year_ti", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min())
                top_insur_tac_Y= transaction_amount_count_Y(top_insurance, years)

               
               
                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_ti",   top_insur_tac_Y["States"].unique())
                    


                Top_insurance_plot_1(top_insur_tac_Y, states)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter_mu", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            
                top_insur_tac_Y_Q= transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)




        elif method_3 == "Top Transaction":
             col1,col2=st.columns(2)
             with col1:

                years= st.slider("Select The Year_tt", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min())
                top_tran_tac_Y= transaction_amount_count_Y(top_transaction, years)

               
               
                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_tt", 
                    top_tran_tac_Y["States"].unique())
                    


                Top_insurance_plot_1(top_tran_tac_Y, states)

                col1,col2= st.columns(2)
                with col1:

                    quarters= st.slider("Select The Quarter_tt", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            
                top_tran_tac_Y_Q= transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)


        elif method_3 == "Top User":
            col1,col2=st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
                top_user_Y= top_user_plot_1(top_user, years)

                col1,col2=st.columns(2)
                with col1:
                    states= st.selectbox("Select The State_tu", 
                    top_user_Y["States"].unique())
                    


                top_user_plot_2(top_user_Y, states)


 
elif select == "TOP CHARTS":
    pass
       
