from bs4 import BeautifulSoup
import requests
import pandas as pd

dict = {"Name": [],
        "City": [],
        "Rating": [],
        "Price": [],
        "Amenities": [],
        "Description": [],
        "Reviews": []}

MAIN_URL = "https://www.booking.com"
URL = 'https://www.booking.com/city/in/new-delhi.html'
html_text = requests.get(URL)

soup = BeautifulSoup(html_text.content, 'lxml')
names = soup.find_all('div', class_="sr__card js-sr-card")
for idx, name in enumerate(names):
    hotel_name = name.find('span', class_="bui-card__title").text.replace('\n', '')
    hotel_location = ' '.join(name.find('p', class_="bui-card__subtitle").span.text.replace('\n', '').split()[2:])
    hotel_rating = name.find('div', class_="bui-review-score__badge").text.replace('\n','')
    hotel_price = name.find('div', class_="bui-price-display__value bui-f-color-constructive").text.replace('\n','')
    hotel_desc = name.find('div', class_="hotel-card__text bui-spacer--medium").p.text.replace('\n','')
    hotel_link = MAIN_URL + name.find('div', class_="sr__card_main").a['href']

    hotel_html_text = requests.get(hotel_link)
    hotel_soup = BeautifulSoup(hotel_html_text.content, 'lxml')

    hotel_facilities = hotel_soup.find_all('div', class_="important_facility")
    facilities = []
    for facility in hotel_facilities:
        facilities.append(facility.text.replace('\n', ''))
    facilities = '\n'.join(facilities)


    author_names = hotel_soup.find_all('div', class_="bui-avatar-block__text")[:2]
    author_reviews = hotel_soup.find_all('p', class_="c-review__inner c-review__inner--ltr")[:2]
    reviews = []
    for (author_name, author_review) in zip(author_names, author_reviews):
        name = author_name.span.text.replace("\n", '')
        review = author_review.span.text.replace("\n", '')
        rev = f"{name}: {review}"
        reviews.append(rev)
    reviews = '\n'.join(reviews)
    
    dict['Name'].append(hotel_name)
    dict['City'].append(hotel_location)
    dict['Rating'].append(hotel_rating)
    dict['Price'].append(hotel_price)
    dict['Amenities'].append(facilities)
    dict['Description'].append(hotel_desc)
    dict['Reviews'].append(reviews)

    print(f"Hotel {idx}: Done")

 
df = pd.DataFrame(dict)
df.to_csv('hotels.csv')
