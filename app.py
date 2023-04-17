import streamlit as st
import requests
from service.main import ScrapTool, Data, predict
from Data.database import create_database, add_customer, delete_predict, view_customers, search_customer


def main():

    st.title('WEB CLASSIFICATION')
    message = st.text_input("Ingrese la URL para la predicción")

    create_database()

    if st.button('Predict'):

        res = predict(message)
        st.write(res)
        #st.write(res["prediction"])
        add_customer(res["Name"], res["Url"], res["prediction"])

        # payload = {
        #     "url": message
        # }
        # res = requests.post(f'http://service:8000/predict/',json=payload)
        # with st.spinner('Classifying, please wait....'):
        #     st.write(res.json())
        # st.write(res)
        # titulo = ScrapTool().get_website_name(url1)
        # url = url1
        # add_customer(titulo, url, pred)

    st.sidebar.header("Configuración")
    try:  
        if st.sidebar.button("Delete"):
            b1 = st.sidebar.text_input("Ingrese el titulo")
            b2 = st.sidebar.text_input("Ingrese el id")
            customers = delete_predict(b1, b2)
            st.table(customers)
        elif st.sidebar.button("Search"):
            b1=st.sidebar.text_input("Ingrese el titulo")
            b2=st.sidebar.text_input("Ingrese el id")
            customers = search_customer(b1, b2)
            st.header("predicciones File")
            st.table(customers)   
        elif st.sidebar.button("View"):
            customers = view_customers()
            st.header("predicciones File")
            st.table(customers)
    except:
     st.write("Por favor ingresa una URL")  

if __name__ == '__main__':
    main()