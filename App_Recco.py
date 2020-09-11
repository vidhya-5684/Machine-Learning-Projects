#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# ## Introduction
# Our aim in this project is to find mobile app profiles that are profitable for the App Store and Google Play markets. We're working as data analysts for a company that builds Android and iOS mobile apps, and our job is to enable our team of developers to make data-driven decisions with respect to the kind of apps they build.
# 
# At our company, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means that our revenue for any given app is mostly influenced by the number of users that use our app. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.
# 
# 
# 
# 
# 

# ## Data Exploration
# 
# To find out the type of apps are likely to attract more users on Google Play and the App Store. To do this, we'll need to collect and analyze data about mobile apps available on Google Play and the App Store.
# 
# As of September 2018, there were approximately 2 million iOS apps available on the App Store, and 2.1 million Android apps on Google Play.Collecting data for over 4 million apps requires a significant amount of time and money, so we'll try to analyze a sample of the data instead. 
# 
# We will start by opening and exploring two data sets that are suitable for our goals. The two data sets named as "AppleStore.csv" containing datas about Applestore apps and "googleplaystore.csv" file containing details about googleplay apps. 

# In[1]:


from csv import reader
def data_start(file):
    o_file =open(file)
    r_file = reader(o_file)
    data = list(r_file)
    return data
 

apple_data = data_start("AppleStore.csv")  
android_data = data_start("googleplaystore.csv")   
print(apple_data[1:3])
    
    


# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

explore_data(apple_data,1,2)  
explore_data(android_data,1,2)
print(apple_data[0])
#print(android_data[0])


# ## Data Cleaning
# 
# The Google Paly data set has a dedicated discussion section where it has been pointed out that error for row 10472. Let's print this row and compare it against the header and another row that is correct.

# In[4]:



print(android_data[0]) 
print('\n')
print(android_data[10473])


# The rating column of row number 10473 shows a rating of 10473 which explicitly wrong since ratings range from 1-5. So we nned to delete this row from the data set.

# In[5]:


del android_data[10473]
print(android_data[10473])


# ### Deleting duplicate data
# 
# It has been noticed from exploring the Google play data set is that there are some apps which have duplicate entries.
# 
# 
# For instance, Instagram has four entries:
# 

# In[6]:


names = "Instagram"
for app in android_data:
    if app[0] == names:
        print (app)


# In[7]:


duplicate = []
u_names = []

for apps in android_data:
    name=apps[0]
    
    if name in u_names:
        duplicate.append(name)
        
    else:
        u_names.append(name)
        
print("count of duplicate is :", (len(duplicate)))


# In total there are 1181 cases where an app occurs more than once.
# 
# The difference in duplicated rows is in fourth column whcih contains number of reviews for each app. So instead of deleting duplicted rows randomly we will only keep the row with the highest number of reviews and remove the other entries for any given app.

# In[8]:


reviews_max = {}

for app in android_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[9]:


android_clean = []
already_added = []

for app in android_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name) 
        
        


# In[10]:


explore_data(android_clean, 0, 3, True)


# ### Removing non English apps
# 
# We develop only English apps at our company and we would like to analyze only the apps that are directed toward an English-speaking audience. However, if we explore the data long enough, we'll find that both data sets have apps with names that suggest they are not directed toward an English-speaking audience.

# In[13]:


print(apple_data[814][1])
print(apple_data[6732][1])
print('\n')
print(android_clean[4412][0])
print(android_clean[7940][0])


# We're not interested in keeping these apps, so we'll remove them. One way to go about this is to remove each app with a name containing a symbol that is not commonly used in English text.
# 
# All these characters that are specific to English texts are encoded using the ASCII standard. Each ASCII character has a corresponding number between 0 and 127 associated with it, and we can take advantage of that to build a function that checks an app name and tells us whether it contains non-ASCII characters.
# We built this function below, and we use the built-in ord() function to find out the corresponding encoding number of each character.

# In[16]:


def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
    
    return True

print(is_english("instagram"))
print(is_english("爱奇艺PPS -《欢乐颂2》电视剧热播"))
print(is_english("Docs To Go™ Free Office Suite"))
print(is_english("Instachat 😜"))

      


# Previous function could not detect correctly identify certain English app names like 'Docs To Go™ Free Office Suite' and 'Instachat 😜'. This is because emojis and characters like ™ fall outside the ASCII range and have corresponding numbers over 127.
# 
# So we modified the function such a way that it will only remove an app if its name has more than three characters with corresponding numbers falling outside the ASCII range. This means all English apps with up to three emoji or other special characters will still be labeled as English

# In[17]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True
    
    


# Filtering non English apps using new function.

# In[20]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in apple_data:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# ### Selecting free app
# 
# As mentined earlier we only aims to build apps that are free to download and install. So we need to isolate free apps for isolation.

# In[21]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# # Most common apps
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 
# 1.
# Build a minimal Android version of the app, and add it to Google Play.
# 
# 2.
# If the app has a good response from users, we then develop it further.
# 
# 3.
# If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# 
# Let's begin the analysis by getting a sense of the most common genres for each market.For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.

# We'll build two functions we can use to analyze the frequency tables:
# One function to generate frequency tables that show percentages
# Another function that we can use to display the percentages in a descending order

# In[25]:


def freq_table(dataset,index):
    freq_dict = {}
    total = 0
    for apps in dataset:
        total +=1
        entry = apps[index]
        if entry in freq_dict:
            freq_dict[entry] +=1
        else:
            freq_dict[entry] = 1
            
    perct_dict = {}        
    for key in freq_dict:
        perct_dict[key] = (freq_dict[key]/total)*100
        
    return perct_dict

        
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        



# In[29]:


display_table(ios_final,11)     
  


# We can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# 
# The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.
# 
# Lets contunue by examining Catgory column of Google play apps.

# In[32]:


display_table(android_final,1) #Catagory of googleplay


# The scenarion is quite different in Google play, here are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.

# In[ ]:





# In[33]:


display_table(android_final,-4)


# Eventhough the difference between Catagory and Genre column in not that clear, the Genre column has much more catagories.
# 
# We will continue the analysis with Catagory column.

# ### Most common Apps by Genre on Apple Store
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Below, we calculate the average number of user ratings per app genre on the App Store:
# 

# In[19]:


uni = freq_table(ios_final,11)

for genre in uni:
   
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        
        if genre_app == genre:
           
            ratings = float(app[5])
            total += ratings
            len_genre +=1
    avrg_rating = total / len_genre
    print(genre,avrg_rating)
   
 


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:
# 

# In[34]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.
# 
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[35]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# 
# Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# 
# Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# 
# Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# Now let's analyze the Google Play market a bit.

# ### Most Common app in Google Play by Genre
# 
# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity.One problem with this data is that is not precise. For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to get an idea which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# To perform computations, however, we'll need to convert each install number to float — this means that we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error. We'll do this directly in the loop below, where we also compute the average number of installs for each genre (category).
# 

# In[36]:


Cat_table = freq_table(android_final,1)

for category in Cat_table:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            no_installs = app[5]
            no_installs = no_installs.replace('+','')
            no_installs = no_installs.replace(',','')
            
            total += float(no_installs)
            len_category +=1
            
    avrg_inst = total / len_category
    
    print(category,avrg_inst)


# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[37]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])
        


# Since these Genre is dominated by giants it is hard to compete with.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[38]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# In[40]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# In[41]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 

# ## Conclusion
# 
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
