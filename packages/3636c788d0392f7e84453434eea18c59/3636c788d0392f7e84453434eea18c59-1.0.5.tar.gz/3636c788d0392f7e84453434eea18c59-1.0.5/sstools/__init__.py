import requests
import json
import pandas as pd
import datetime
from IPython.display import clear_output
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import pymysql
import random
import math

"""# SAFFRONSTAYS


```
sql_query(query,cypher_key)
sql_query_destructive(query,cypher_key)
ss_calendar(listing_ids,check_in,check_out)
ss_fb_catalogue()
```
"""

# SQL query on the SS database (ONLY SELECT) - returns a dataframe
def sql_query(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  if query.split(' ')[0] != 'SELECT':
    print("Error. Please only use non destructive (SELECT) queries.")
    return "Please only use non destructive (SELECT) queries."

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df



# to execute destructive queries 
def sql_query_destructive(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()

# Get the status for all the dates for a list of homes
def ss_calendar(listing_ids,check_in,check_out):

  parsed_listing_ids = str(listing_ids)[1:-1]
  parsed_listing_ids = parsed_listing_ids.replace("'","").replace(" ","")

  url = "https://www.saffronstays.com/calender_node.php"

  params={
      "listingList": parsed_listing_ids,
      "checkIn":check_in,
      "checkOut":check_out
      
  }
  payload = {}
  headers= {}

  response = requests.get(url, headers=headers, data = payload,params=params)
  response = json.loads(response.text.encode('utf8'))
  return response

# SS Facebook catalogue (a list of currently live listings)
def ss_fb_catalogue():
  url = "https://www.saffronstays.com/items_catalogue.php"

  response = requests.get(url)
  response_data = response.text.encode('utf8')

  csv_endpoint = str(response_data).split('`')[1]
  csv_download_url = "https://www.saffronstays.com/"+csv_endpoint

  ss_data = pd.read_csv(csv_download_url)

  return ss_data

"""# Vista
```
# Vista API Wrappers 
# Refining the APIs
# Dataframes
# SQL
```
"""

# Return list of all locations
def vista_locations():
  locations = ["lonavala, maharashtra",
  "goa, goa",
  "alibaug, maharashtra",
  "nainital, uttarakhand",
  "chail, himanchal-pradesh",
  "manali, himachal-pradesh",
  "shimla, himanchal%20pradesh",
  "ooty, tamil%20nadu",
  "coorg, karnataka",
  "dehradun, uttarakhand",
  "jaipur, rajasthan",
  "udaipur, rajasthan",
  "mahabaleshwar, maharashtra",
  "nashik, maharashtra",
  "kerala, kerala",
  "gangtok, sikkim",
  "gurgaon, haryana",
  "vadodara, gujarat",
  "kashmir, jammu"
  ]


  return locations

# Wrapper on the search API
def vista_search_api(search_type='city',location="lonavala,%20maharashtra",checkin="",checkout="",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  payload = {
      
      "city": location,
      "search_type": "city",
      "checkin": checkin,
      "checkout": checkout,
      "total_guests": guests,
      "adults": adults,
      "childs": childs,
      "page": page_no,
      "min_bedrooms": 1,
      "max_bedrooms": 30,
      "amenity": [],
      "facilities": [],
      "price_start": 1000,
      "price_end": 5000000,
      "sort_by_price": ""
        
    }
  headers = {}

  response = requests.post(url, params=param, headers=headers, data=payload)
  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# Wrapper on the listing API
def vista_listing_api(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2),
                         guest=3,adult=3,child=0):
  
  url = "https://v3api.vistarooms.com/api/single-property"

  param={
          'slug': slug,
          'checkin': checkin,
          'checkout': checkout,
          'guest': guest,
          'adult': adult,
          'child': child    
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  property_deets = json.loads(response.text.encode('utf8'))
  return property_deets

# Wrapper on the listing extra details API
def vista_listing_other_details_api(slug='the-boulevard-villa'):

  url = "https://v3api.vistarooms.com/api/single-property-detail"

  param={
          'slug': slug,
      }

  payload = {}
  headers = {
  }
  
  response = requests.get(url, params=param, headers=headers, data = payload)
  property_other_deets = json.loads(response.text.encode('utf8'))
  return property_other_deets

# Wrapper on the price calculator
def vista_price_calculator_api(property_id='710', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0):

  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')


  url = "https://v3api.vistarooms.com/api/price-breakup"
  
  param={
      'property_id': property_id,
      'checkin': checkin,
      'checkout': checkout,
      'guest': guest,
      'adult': adult,
      'child': child,   
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  pricing_deets = json.loads(response.text.encode('utf8'))
  return pricing_deets

# Gives a json response for basic listing data for the list of locations
def vista_search_locations_json(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):

  # Empty list to append (extend) all the data
  properties = []

  if get_all:
    locations = vista_locations()

  # Outer loop - for each location
  for location in locations:

    page_no = 1

    # Inner Loop - for each page in location ( acc to the Vista Search API )
    while True:

      clear_output(wait=True)
      print(f"Page {page_no} for {location.split('%20')[0]} ")

      # Vista API call (search)
      search_data = vista_search_api(location=location,guests=guests,page_no=page_no)

      # Break when you reach the last page for a location
      if not search_data['data']['properties']:
        break
        
      properties.extend(search_data['data']['properties'])
      page_no += 1

      time.sleep(wait_time)


  return properties

# Retruns a DATAFRAME for the above functions & **DROPS DUPLICATES (always use this for analysis)
def vista_search_locations(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):
  villas = vista_search_locations_json(locations=locations, guests=guests,get_all=get_all,wait_time=wait_time)
  villas = pd.DataFrame(villas)
  villas = villas.drop_duplicates('id')

  return villas

# Returns a JSON with the listing details
def vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2)):

  print("Fetching ",slug)
  # Vista API call (listing)
  property_deets = vista_listing_api(slug=slug,guests=guests,checkin=checkin, checkout=checkout)
  
  # Get lat and long (diff API call)
  lat_long = vista_listing_other_details_api(slug)['data']['location']

  # Get pricing for various durations
  weekday_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(1))
  weekend_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(5),checkout=next_weekday(5)+datetime.timedelta(1))
  entire_week_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(7))
  entire_month_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(30))

  # Add the extra fields in response (JSON)
  property_deets['data']['slug'] = slug
  property_deets['data']['lat'] = lat_long['latitude']
  property_deets['data']['lon'] = lat_long['longitude']
  property_deets['data']['checkin_date'] = checkin
  property_deets['data']['checkout_date'] = checkout
  property_deets['data']['weekday_pricing'] = weekday_pricing
  property_deets['data']['weekend_pricing'] = weekend_pricing
  property_deets['data']['entire_week_pricing'] = entire_week_pricing
  property_deets['data']['entire_month_pricing'] = entire_month_pricing
  property_deets['data']['price_per_room'] = property_deets['data']['price']['amount_to_be_paid']/property_deets['data']['property_detail']['number_of_rooms']

  return property_deets['data']

# Calculates the price for a duration (if unavailable, will automatically look for the next available dates) % Recursive function
def vista_price_calculator(property_id, checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0, depth=0):

  date_diff = (checkout-checkin).days

  # Set the exit condition for the recursion depth ( to avoid an endless recursion -> slowing down the scripts )
  if date_diff < 7:
    depth_lim = 15
    next_hop = 7
  elif date_diff >= 7 and date_diff < 29:
    depth_lim = 7
    next_hop = 7
  else:
    depth_lim = 5
    next_hop = date_diff
    
  if depth==depth_lim:
    return f"Villa Probably Inactive, checked till {checkin}"
  
  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')

  # Vista API call (Calculation)
  pricing = vista_price_calculator_api(property_id=property_id, checkin=checkin, checkout=checkout, guest=guest, adult=adult, child=child)

  if 'error' in pricing.keys():

    # Recursion condition (Call self with next dates in case the dates are not available)
    if pricing['error'] == 'Booking Not Available for these dates':

      next_checkin = checkin + datetime.timedelta(next_hop)
      next_chekout = checkout + datetime.timedelta(next_hop)

      next_pricing = vista_price_calculator(property_id,checkin=next_checkin ,checkout=next_chekout,depth=depth+1)
      return next_pricing

    # For other errors (Like invalid listing ID)
    else:
      return pricing['error']
      
    return next_pricing
  else:
    return pricing['data']['price']

# Uses a list of slugs to generate a master DATAFRAME , this contains literally everything, ideal for any analysis on Vista
def vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira'])):
  
  total_slugs = len(slugs)
  temp_progress_counter = 0
  villas_deets = []   

  for slug in slugs:
    villa_deets = vista_listing(slug=slug)
    villas_deets.append(villa_deets)
    villas_df = pd.DataFrame(villas_deets)

    temp_progress_counter += 1
    clear_output(wait=True)
    print("Done ",int((temp_progress_counter/total_slugs)*100),"%")

  prop_detail_df = pd.DataFrame(list(villas_df['property_detail']))
  agent_details_df =  pd.DataFrame(list(villas_df['agent_details']))
  price_df =  pd.DataFrame(list(villas_df['price']))

  literally_all_deets = pd.concat([prop_detail_df,villas_df,price_df,agent_details_df], axis=1)

  literally_all_deets = literally_all_deets.drop(['property_detail','mini_gallery', 'base_url',
       'agent_details', 'house_rule_pdf', 'mini_gallery_text',
       'seo','number_extra_guest', 'additionalcost',
       'days', 'min_occupancy', 'max_occupancy', 'amount_to_be_paid','total_guest',
       'extra_adult', 'extra_child', 'extra_adult_cost', 'extra_child_cost',
       'per_person','price','checkin_date','checkout_date','total_price','agent_short_words'], axis = 1)
  
  literally_all_deets['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in literally_all_deets['amenities']]
  literally_all_deets['weekday_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekday_pricing']]
  literally_all_deets['weekend_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekend_pricing']]
  literally_all_deets['entire_week_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_week_pricing']]
  literally_all_deets['entire_month_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_month_pricing']]
  
  return literally_all_deets

# Takes 2 lists of listings (Old and New) and only responds with the Dataframe of the newly added listings
def added_villas_dataframe(old_slugs,new_slugs):
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  added_villas = []

  if added_slugs:
    added_villas = vista_master_dataframe(added_slugs) 

  return added_villas

# Non Desctructive SQL QUERY - Try "SELECT * FROM VISTA_MASTER"
def vista_sql_query(query,cypher_key):
  # Returns a daframe object of the query response

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = "uat_ss_db"

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df

# DESTRCUTIVE sql query
def vista_sql_destructive(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = "uat_ss_db"

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()

"""Vista Weekly Update Script
Only execute weekly
"""

def vista_weekly_update_script(cypher_key,search_api_wait=10):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  sql_db_url = cipher_suite.decrypt(host_enc).decode("utf-8")
  sql_user = cipher_suite.decrypt(user_enc).decode("utf-8")
  sql_pw = cipher_suite.decrypt(pass_enc).decode("utf-8")
  sql_db = "uat_ss_db"

  # Get the list of all the current villas lited
  vista_search_data = vista_search_locations(get_all=True,wait_time=search_api_wait)

  new_slugs = vista_search_data['slug'].values

  query = "SELECT slug FROM VISTA_MASTER"

  old_slugs = vista_sql_query(query,cypher_key)
  old_slugs = old_slugs['slug'].values

  # Get the list of recently added and removed slugs
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  removed_slugs = list(set(old_slugs).difference(set(new_slugs)))

  # Add the new listings to the Database
  vista_newly_added_df = added_villas_dataframe(old_slugs,new_slugs)

  if len(vista_newly_added_df) > 0:
      vista_newly_added_df['listing_status'] = "LISTED"
      vista_newly_added_df['status_on'] = datetime.datetime.today()

      # changind all the "Object" data types to str (to avoid some weird error in SQL)
      all_object_types = pd.DataFrame(vista_newly_added_df.dtypes)
      all_object_types = all_object_types[all_object_types[0]=='object'].index

      for column in all_object_types:
        vista_newly_added_df[column] = vista_newly_added_df[column].astype('str')

      engine = create_engine(f"mysql+pymysql://{sql_user}:{sql_pw}@{sql_db_url}/{sql_db}")

      for i in range(len(vista_newly_added_df)):
        try:
          vista_newly_added_df.iloc[i:i+1].to_sql(name='VISTA_MASTER',if_exists='append',con = engine,index=False)
        except IntegrityError:
          pass  
          
      engine.dispose()

  # Update Delisted Homes
  update_delisted_query = "UPDATE VISTA_MASTER SET listing_status = 'DELISTED' WHERE slug in " + str(tuple(removed_slugs)) + " AND listing_status = 'LISTED'"
  vista_sql_destructive(update_delisted_query,cypher_key)

  update_delisted_query = "UPDATE VISTA_MASTER SET status_on = '" + str(datetime.datetime.today()) +"' WHERE slug in " + str(tuple(removed_slugs))  + " AND listing_status = 'LISTED'"
  vista_sql_destructive(update_delisted_query,cypher_key)

  # Update the rebirth of listings (That went from delisted to listed)
  rebirth_query1 = "UPDATE VISTA_MASTER SET listing_status = 'LISTED' WHERE slug in " + str(tuple(added_slugs)) + " AND listing_status = 'DELISTED'"
  vista_sql_destructive(rebirth_query1,cypher_key)

  rebirth_query2 = "UPDATE VISTA_MASTER SET status_on = '" + str(datetime.datetime.today()) +"' WHERE slug in " + str(tuple(added_slugs))  + " AND listing_status = 'DELISTED'"
  vista_sql_destructive(rebirth_query2,cypher_key)

  # A Summary of the updates
  final_success_response = {
      "No of Added Villas" : len(added_slugs),
      "No of Removed Villas" : len(removed_slugs),
      "Added Villas" : added_slugs,
      "Removed Villas" : removed_slugs
  }

  return final_success_response

# Breadth first seach algorithm to get the blocked dates

def vista_blocked_dates(property_id,ci,co):

  # check if the listing is 

  if vista_check_if_inactive(property_id) == "Probably Inactive":
    return {
        "blocked_dates" : "Probably Inactive"   
    }

  rg = (datetime.datetime.strptime(co, "%Y-%m-%d") - datetime.datetime.strptime(ci, "%Y-%m-%d")).days    # Range => checkout - checkin (in days)

  api_calls = 0

  DTE = [(ci,co,rg)]                  # This list contains all the date ranges to be checked - there will be additions and subtractions to this list

  blocked = {}                         # we will add the blocekd dates here
  explored = []


  while len(DTE) != 0:

    api_calls += 1                        # To see how many API calls happened (fewer the better)

    dates = DTE.pop()                     # Pick one item (date range) from the DTE list -> to see if it is available

    print(f"Checking : {dates[0]} for {dates[2]} days")

    explored.append(dates)

    checkin = dates[0]
    checkout = dates[1]
    range = dates[2]

    api_response = vista_price_calculator_api(property_id=property_id,checkin=checkin,checkout=checkout)      # Call the vista API to see of this is available

    if "error" not in api_response.keys():                      # If no error -> it is available, start the next iteration of the loop
      print("Not Blocked")
      continue

    else:                                                       # if the range is unavailable  do this
      print("Blocked")
      if range == 1:                                                                 # if the range is 1, mark the date as blocked
        blocked[checkin] = api_response['data']['price']['amount_to_be_paid']
        #blocked.append((checkin,api_response['data']['price']['amount_to_be_paid']))
      else:                                                                           # if the range is not 1, split the range in half and add both these ranges to the DTE list
        checkin_t = datetime.datetime.strptime(checkin, "%Y-%m-%d")
        checkout_t = datetime.datetime.strptime(checkout, "%Y-%m-%d")

        middle_date = checkin_t + datetime.timedelta(math.ceil(range/2))

        first_half = ( str(checkin_t)[:10] , str(middle_date)[:10] , (middle_date - checkin_t).days )
        second_half = ( str(middle_date)[:10] , str(checkout_t)[:10] , (checkout_t - middle_date).days)

        DTE.extend([first_half,second_half])


  response_obj = {
      "blocked_dates" : blocked,
      "meta_data": {
          "total_blocked_dates" : len(blocked),
          "api_calls":api_calls,
          "checked from": ci,
          "checked till":co
          #"date_ranges_checked":explored
      }
  }

  return response_obj

def vista_check_if_inactive(property_id="",slug=""):

  if len(slug)>0:
    try:
      listing = vista_listing_api(slug)
      property_id = listing['data']['property_detail']['id']
    except: 
      print("invalid listing or a delisted property")

  min_nights = 1

  for i in [8,16,32,64,128]:
    price = vista_price_calculator_api(property_id , checkin=datetime.date.today()+datetime.timedelta(i), checkout = datetime.date.today()+datetime.timedelta(i + min_nights))
    
    if "error" not in price.keys():
      return "Active"
    
    elif price['error'] == 'Booking Not Available for these dates':
      pass
    
    elif type(price['error'].split(" ")[4]) == "int":
      min_nights = price['error'].split(" ")[4]

    return "Probably Inactive"

"""# Lohono


```
# Lohono API wrappers
# Refining the APIs
# Master DataFrame
```
"""

# List of all lohono locations 
def lohono_locations():
  locations = ['india-alibaug','india-goa']
  return locations

# lohono Search API wrapper
def lohono_search_api(location_slug="india-goa",page=1):
  url = "https://www.lohono.com/api/property"

  params = {
      'location_slug': location_slug,
      'page': page
  }

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/{ location_slug.split("-")[-1] }',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }


  response = requests.get(url, headers=headers, data = payload, params=params)

  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# lohono listing API wrapper
def lohono_listing_api(slug='prop-villa-magnolia-p5sp'):
  url = f"https://www.lohono.com/api/property/{slug}"

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent':  mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.lohono.com/villas/india/goa/prop-fonteira-vaddo-a-C6Cn',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  listing_data = json.loads(response.text.encode('utf8'))
  return listing_data['response']

# lohono Pricing API wrapper
def lohono_pricing_api(slug,checkin,checkout,adult=2,child=0):

  url = f"https://www.lohono.com/api/property/{slug}/price"

  payload = "{\"property_slug\":\""+slug+"\",\"checkin_date\":\""+str(checkin)+"\",\"checkout_date\":\""+str(checkout)+"\",\"adult_count\":"+str(adult)+",\"child_count\":"+str(child)+",\"coupon_code\":\"\",\"price_package\":\"\",\"isEH\":false}"

  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'content-type': 'application/json',
    'origin': 'https://www.lohono.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/goa/{slug}?checkout_date={checkout}&adult_count={adult}&checkin_date={checkin}',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  response = requests.post(url, headers=headers, data = payload)
  pricing_data = json.loads(response.text.encode('utf8'))

  return pricing_data

# Basic details from the search API
def lohono_search(location_slugs=lohono_locations()):
  page = 1
  all_properties = []

  for location_slug in location_slugs:
    while True:
      print(f"page{ page } for {location_slug}")
      search_response = lohono_search_api(location_slug,page)
      all_properties.extend(search_response['response']['properties'])
      if search_response['paginate']['total_pages'] == page:
        break
      page += 1

  return pd.DataFrame(all_properties)

# All details for all the listings
def lohono_master_dataframe():
  search_data = lohono_search()

  slugs = search_data['property_slug'].values

  all_properties = []

  for slug in slugs:
    print(f"getting {slug}")
    listing_raw = lohono_listing_api(slug)
    all_properties.append(listing_raw)

  all_properties = pd.DataFrame(all_properties)

  all_properties['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in all_properties['amenities']]
  all_properties['price'] = search_data['rate']
  all_properties['search_name'] = search_data['name']


  return all_properties

"""# Helper Functions


```
next_weekday()
mock_user_agent()
mock_proxy()
```
"""

# Get the next weekday ( 0=monday , 1 = tuesday ... )
def next_weekday(weekday=0, d=datetime.date.today()):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# default - next monday

# gives a random user-agent to use in the API call
def mock_user_agent():
  users = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
  "Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00",
  "Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"]

  return users[random.randint(0,7)]

# Gives a 'proxies' object for a 'requests' call
def mock_proxy():

  proxies_list = ["45.72.30.159:80",
  "45.130.255.156:80",
  "193.8.127.117:80",
  "45.130.255.147:80",
  "193.8.215.243:80",
  "45.130.125.157:80",
  "45.130.255.140:80",
  "45.130.255.198:80",
  "185.164.56.221:80",
  "45.136.231.226:80"]

  proxy = proxies_list[random.randint(0,9)]

  proxies = {
  "http": proxy,
  "https": proxy
  }

  return proxies

"""# TEST"""

def final_test():
  ss_latest()
  vista_latest()
  vista_locations()
  vista_search_locations_json(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_search_locations(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2))
  vista_listing_other_details_api(slug='the-boulevard-villa')
  vista_price_calculator(property_id='310', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0)
  next_weekday(weekday=0, d=datetime.date.today())
  vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira']))
  vista_map_all()
  ss_map_all()
  ss_vs_vista()

  return "All Good :)"