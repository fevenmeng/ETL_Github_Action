import pandas as pd
import psycopg2
import os
from get_data import get_article_data

# Add more print/logging to ensure the script is reaching the database update part

df = get_article_data()
print(df)

#Iterate through each column name.
#Convert the column name to lowercase.
#Replace any spaces in the column name with underscores (_).
#Example: "Time Uploaded" becomes "time_uploaded".
#Access the "reading_time" column.
#For each value in the column, remove the string " min read" from the end.
#Ensure that the remaining value in the column is converted to the appropriate datatype, probably an integer.
#Access the "article_content" column.
#For each value in the column, replace all occurrences of the newline character (\n) with an empty string ("").

df.columns=[x.lower() for x in df.columns] # this methodis called list comprehension
df.columns=[x.replace(' ','_') for x in df.columns] 
df['reading_time']=df['reading_time'].str.replace(' min read','')
df['article_content']=df['article_content'].str.replace('\n','')

#df
#After the transformations, ensure that each column has the correct data type (e.g., integer, string, date, etc.).
 #You might need to use Pandas functions like astype() to enforce these data types.
#Determine the appropriate data types for each column based on the data that it contains.

#import pandas as pd
df = df.astype({
    'link': 'string',
    'title': 'string',
    'time_uploaded': 'string',  # Can be converted to datetime later
    'author': 'string',
    'tags': 'string',
    'reading_time': 'int64',
    'article_content': 'string',
    'word_count': 'int64',
    'sentiment': 'string',
    'compound_score': 'float64'
})

df['time_uploaded'] = pd.to_datetime(df['time_uploaded'])
#df

#Open pgAdmin.
#Create a new server connection using the provided credentials:
#In the connected database, create a new table with your name (e.g., yourname).
#Define the columns with appropriate data types:

#The link column must be defined as the primary key.
#Analyze the transformed data to determine the correct data type for each column.
#Examples of datatypes are: text, integer, timestamp, date.
# Database connection parameters
import psycopg2
import pandas as pd

# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "testtech",
    "password": "Your_password",
    "host": "testtech.postgres.database.azure.com",
    "port": "5432"
}


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    # SQL Insert Query
    insert_query = """
    INSERT INTO feven (link, title, time_uploaded, author, tags, reading_time, article_content, word_count, sentiment, compound_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (link) DO NOTHING;  -- Avoids duplicate primary key errors
    """
    
    # Insert DataFrame records one by one
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['link'], row['title'], row['time_uploaded'], row['author'], row['tags'],
            row['reading_time'], row['article_content'], row['word_count'], row['sentiment'], row['compound_score']
        ))

    # Commit and close
    conn.commit()
    print("Data inserted successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if conn:
        cursor.close()
        conn.close()



#"password": os.getenv("DB_PASSWORD")  