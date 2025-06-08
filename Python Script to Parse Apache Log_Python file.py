#!/usr/bin/env python
# coding: utf-8

# #### Data looks like Apache log while i have opened in the notebook. Now i have parse that notebook log file with python and saving it to csv file after creating the data as pandas data frame.

# In[34]:


import re
import pandas as pd
from datetime import datetime

log_file = r"D:\Information Technology\calgary_access_log" # log file path

log_pattern = r'(?P<host>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<resource>\S+) \S+" (?P<status>\d{3}) (?P<bytes>\d+)' # defining a pattern
 
parsed_data = [] # Initialize a list to store parsed lines

with open(log_file, 'r', encoding='utf-8', errors='ignore') as file: #  Read and parse the log file
    for line in file: # implementing for loop here to match the pattern with the regular expression 
        match = re.match(log_pattern, line)
        if match: 
            data = match.groupdict()
            data['timestamp'] = datetime.strptime(data['timestamp'], "%d/%b/%Y:%H:%M:%S %z") # Convert timestamp string to datetime object
            parsed_data.append(data)


# In[36]:


df = pd.DataFrame(parsed_data) # Create DataFrame 

print(df.head()) # Prining the data

df.to_csv("calgary_access_log_parsed.csv", index=False) # Save to CSV, if needed


# In[39]:


df.info() # pringing the info here


# ## 1. Plot Number of Requests Per Minute / Hour / Day

# In[41]:


import matplotlib.pyplot as plt # importing ploting library

# Convert to datetime index
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True) # converting data type into 'datetime' format
df.set_index('timestamp', inplace=True)

# Plot number of requests per minute, hour, and day
requests_per_minute = df.resample('T').size() 
requests_per_hour = df.resample('h').size()
requests_per_day = df.resample('D').size()

# Plot hourly requests
plt.figure(figsize=(12, 5))
requests_per_hour.plot()
plt.title("Number of Requests per Hour")
plt.xlabel("Time")
plt.ylabel("Number of Requests")
plt.grid(True)
plt.tight_layout()
plt.show()


# ## 2. Find Most Requested Resources

# In[46]:


top_resources = df['resource'].value_counts().head(10)

plt.figure(figsize=(10, 5)) # Defining the figure size here for the plot
top_resources.plot(kind='bar', color='skyblue')
plt.title("Top 10 Most Requested Resources")
plt.xlabel("Resource")
plt.ylabel("Number of Requests")
plt.xticks(rotation=45)
plt.tight_layout() 
plt.show()


# #### Most requested resources are the 'index.html' and apart from it we can see few more status of requested resource

# ## 3. Count by Status Codes (e.g., 200, 404)

# In[51]:


status_counts = df['status'].value_counts().sort_index()

plt.figure(figsize=(8, 4))
status_counts.plot(kind='bar', color='orange')
plt.title("HTTP Status Code Distribution")
plt.xlabel("Status Code")
plt.ylabel("Frequency")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# #### http 200 status code represents the 'request successful' and here in the above plot we can see the volume of all the status code 

# ## 4. Analyze Traffic Volume Over Time (Rolling Average)

# In[54]:


# Smooth out spikes using a rolling window average
rolling_traffic = requests_per_hour.rolling(window=3).mean() # calclating average of request in current hour and two more hours right before
# This rolling average calculation is for reducing the noise and can give a better visibility in the plot.
plt.figure(figsize=(12, 5))
plt.plot(requests_per_hour.index, requests_per_hour, label='Hourly Requests', alpha=0.4)
plt.plot(rolling_traffic.index, rolling_traffic, label='3-Hour Rolling Avg', color='red')
plt.title("Traffic Volume Over Time")
plt.xlabel("Time")
plt.ylabel("Requests")
plt.legend()
plt.tight_layout()
plt.show()


# In[61]:


df.columns


# ## 5. Top Hosts (Remote and Local)

# In[71]:


import seaborn as sns
top_hosts = df['host'].value_counts().head(10)
sns.barplot(x=top_hosts.values, y=top_hosts.index)


# #### Looks like local host is more then remote host

# ## 6.  Request Type Analysis

# In[87]:


sns.countplot(data=df, x='method', palette='pastel')


# #### GET methord is absolutely high here

# # I have analyzed what i have thought so far. We can analyze so many other aspects as per the business requirements as well. Thanks for beleving in me and i hope to go to the next step of the interview rounds.
# 
# # Here is my portfolio and the work samples : https://mukut45.github.io/
# 
# 
# # Regards
# ### Mukut May Dutta

# In[ ]:





# In[ ]:




