import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')

   

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   #streamlit.text(fruityvice_response.json())
   # write your own comment -what does the next line do? 
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   streamlit.write('The user entered ', fruit_choice)
   if not fruit_choice:
      streamlit.error('Please select a fruit to get information.')
   else:
      back_from_function=get_fruityvice_data(fruit_choice)
      # write your own comment - what does this do?
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()
      

#stop here
#streamlit.stop();

streamlit.header("View Our Fruit List- Add Your Favorites!!")
#define a function to laod the fruits list from snowflake
def get_fruits_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()
      
#add a button to load the fruits
if streamlit.button('Get Fruits Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_row=get_fruits_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_row)



def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+ new_fruit +"')")
      return "Thanks for adding "+ new_fruit

fruit_choice = streamlit.text_input('What fruit would you like add?','Jackfruit')
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
insert_row_snowflake(fruit_choice)
my_cnx.close()
   
