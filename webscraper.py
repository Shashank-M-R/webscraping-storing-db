import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from tqdm import tqdm
def extract_article_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_element = soup.find("h1", class_="native_story_title")
        title = title_element.text.strip() if title_element else None
        url_element = soup.find("input", class_="native_story_url")
        url = url_element["value"] if url_element else None
        author_element = soup.find("a", class_="bulletProj")
        author = author_element.text.strip() if author_element else None
        date_time_element = soup.find("span", itemprop="dateModified")
        date_time = date_time_element.text.strip() if date_time_element else None
        content_element = soup.find('div', id='pcl-full-content', class_='story_details')
        extracted_content = ""
        paragraphs = content_element.find_all('p')
        for p in paragraphs:
            extracted_content += p.get_text(separator='\n') + '\n\n'  # Separate paragraphs with two newlines

        data_dict = {
            "URL":url,
            "Title":title,
            "Author":author,
            "Publication Date and Time":date_time,
            "Content":extracted_content

        }
        return data_dict
    except:
        return {}
def main(main_url):
    page = requests.get(main_url)
    bSoup = BeautifulSoup(page.content, 'html.parser')
    links_list = bSoup.find_all('a')
    print(links_list[0])

    article_links_all = [
        l.get('href') for l  in links_list 
        if 'href' in l.attrs and 'article/' in l.attrs['href']]
    article_links = list(set(article_links_all))
    list_of_dicts = []
    for link in tqdm(article_links):
        resp = extract_article_info(link)
        if resp:
            list_of_dicts.append(resp)

    df = pd.DataFrame(list_of_dicts)

    conn = sqlite3.connect('articles.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    publication_date TEXT,
                    content TEXT
                )''')

    for idx, row in df.iterrows():
        title = row['Title']
        author = row['Author']
        publication_date = row['Publication Date and Time']
        content = row['Content']
    
    
        cur.execute('''INSERT INTO articles (title, author, publication_date, content)
                        VALUES (?, ?, ?, ?)''', (title, author, publication_date, content))


    conn.commit()

## print all rows from database to check.
    query = 'SELECT * FROM articles'
    df = pd.read_sql_query(query, conn)
    print(df)

    cur.close()
    conn.close()
    return "success"
#main_url="https://indianexpress.com/section/technology/"
#main(main_url)

