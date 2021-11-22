
#import config
import requests
import time
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw

########################################################################################
a = 230
b = 140
c = 250
d = 155
dict_coordinate = {
    'WTI Crude': {'price': (355, 90), 'percentage': (a+20, 139), 'rate_up_down': (a+120, 139), 'symbol': {'%': (a, 139), 'arrow_left': (a+70, 139), '$': (a+100, 139), 'arrow_right': (a+170, 139)}},
    'Brent Crude': {'price': (280, 210), 'percentage': (b+20, 260), 'rate_up_down': (b+120, 260), 'symbol': {'%': (b, 260), 'arrow_left': (b+70, 260), '$': (b+100, 260), 'arrow_right': (b+170, 260)}},
    'Natural Gas': {'price': (410, 460), 'percentage': (c+20, 510), 'rate_up_down': (c+120, 510),'symbol': {'%': (c, 510), 'arrow_left': (c+70, 510), '$': (c+100, 510), 'arrow_right': (c+170, 510)}},
    'Gasoline': {'price': (280, 335), 'percentage': (d+20, 385), 'rate_up_down': (d+120, 385), 'symbol': {'%': (d, 385), 'arrow_left': (d+70, 385), '$': (d+100, 385), 'arrow_right': (d+170, 385)}}
}
####################################################################################

def scrape():
    website = 'https://oilprice.com/oil-price-charts'
    r = requests.request('GET', website)
    # r = requests.get(website, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    result = ''
    all_rows = soup.find_all("tr")
    lst_oil_prices = []
    for row in all_rows:
        span = row.find("span", {"class": "blend_name_span"})
        if span:
            if (span.text == 'WTI Crude') | (span.text == 'Brent Crude') | (span.text == 'Natural Gas') | (span.text == 'Gasoline'):
                price = row.find("td", {"class": "last_price"})
                oil_prices = {'oil_name': '', 'price': '', 'increase_by': '', 'decrease_by': '', 'percentage': ''}
                oil_prices['oil_name'] = span.text
                oil_prices['price'] = price.text
                change_up = row.find("td", {"class": "change_up"})
                if change_up:
                    change_up_percentage = row.find("td", {"class": "change_up_percent"})
                    # print(change_up_percentage)
                    span_text_percentage = change_up_percentage.find("span", {"class": "blend_update_text"}).text
                    change_up_percentage_text = change_up_percentage.text
                    if span_text_percentage:
                        change_up_percentage_text = change_up_percentage_text.replace(span_text_percentage, "")
                    oil_prices['increase_by'] = change_up.text
                    oil_prices['percentage'] = change_up_percentage_text
                change_down = row.find("td", {"class": "change_down"})
                if change_down:
                    change_down_percentage = row.find("td", {"class": "change_down_percent"})
                    change_down_percentage_text = change_down_percentage.text
                    span_text_percentage = change_down_percentage.find("span", {"class": "blend_update_text"}).text
                    if span_text_percentage:
                        change_down_percentage_text = change_down_percentage_text.replace(span_text_percentage, "")
                    oil_prices['decrease_by'] = change_down.text
                    oil_prices['percentage'] = change_down_percentage_text
                lst_oil_prices.append(oil_prices)
    return lst_oil_prices

############################################################################################

def post(lst_oil_prices):
    my_image = Image.open("images/template.jpg")
    fontSize = 44
    title_font = ImageFont.truetype('fonts/ge-ss-two-medium.ttf', fontSize)
    price_font = ImageFont.truetype('fonts/ge-ss-two-medium.ttf', fontSize - 20)
    symbol_percentage_font = ImageFont.truetype('arial.ttf', fontSize - 20)
    symbol_arrow_font = ImageFont.truetype('fonts/esri_business_regular.ttf', fontSize - 20)
    image_editable = ImageDraw.Draw(my_image)

    for item_oil in lst_oil_prices:
        oil_name = item_oil['oil_name']
        oil_price = item_oil['price']
        oil_percentage = item_oil['percentage'].replace("%", "").replace("-", "").replace("+", "")
        increase_by = item_oil['increase_by'].replace("-", "").replace("+", "")
        decrease_by = item_oil['decrease_by'].replace("-", "").replace("+", "")

        grey = (102, 102, 102)
        red = (255, 0, 0)
        green = (0, 255, 0)

        if oil_name in dict_coordinate:
            image_editable.text(dict_coordinate[oil_name]['price'], oil_price, grey, font=title_font)
            if increase_by:
                if oil_percentage == '0.00':
                    #image_editable.text(dict_coordinate[oil_name]['price'], oil_price, grey, font=title_font)
                    image_editable.text(dict_coordinate[oil_name]['percentage'], oil_percentage, grey,
                                        font=price_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['%'], '%', grey,
                                        font=symbol_percentage_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_left'], 'b', grey,
                                        font=symbol_arrow_font)
                    image_editable.text(dict_coordinate[oil_name]['rate_up_down'], increase_by, grey,
                                        font=price_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_right'], 'b', grey,
                                        font=symbol_arrow_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['$'], '$', grey, font=price_font)
                else:
                    #image_editable.text(dict_coordinate[oil_name]['price'], oil_price, green, font=title_font)
                    image_editable.text(dict_coordinate[oil_name]['percentage'], oil_percentage, green,
                                    font=price_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['%'], '%', green,
                                    font=symbol_percentage_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_left'], 'e', green,
                                    font=symbol_arrow_font)
                    image_editable.text(dict_coordinate[oil_name]['rate_up_down'], increase_by, green,
                                    font=price_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_right'], 'e', green,
                                    font=symbol_arrow_font)
                    image_editable.text(dict_coordinate[oil_name]['symbol']['$'], '$', green, font=price_font)
            elif decrease_by:
                #image_editable.text(dict_coordinate[oil_name]['price'], oil_price, red, font=title_font)
                image_editable.text(dict_coordinate[oil_name]['percentage'], oil_percentage, red,
                                    font=price_font)
                image_editable.text(dict_coordinate[oil_name]['symbol']['%'], '%', red,
                                    font=symbol_percentage_font)
                image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_left'], 'c', red,
                                    font=symbol_arrow_font)
                image_editable.text(dict_coordinate[oil_name]['rate_up_down'], decrease_by, red,
                                    font=price_font)
                image_editable.text(dict_coordinate[oil_name]['symbol']['arrow_right'], 'c', red,
                                    font=symbol_arrow_font)
                image_editable.text(dict_coordinate[oil_name]['symbol']['$'], '$', red, font=price_font)


    my_image.save("images/result.jpg")
    page_id_1 = '385114094931345'
    facebook_access_token_1 = 'EAARnlhMWujcBACLzGOKZCkFZCUnM3iwB39G8ZBTZA7F3yGkCNRXsUNm9iZAlY49DVAGCTpPUh4TZBHCa6xjo2vfNRBY22YlqrbK28BBpHzBZCgpsAxmoyav7eZBHlFHJVrFRHjIRRl4tGSyowHe4fkX7yI8siEcepD7ZAcoCif144nX4SfQZAwDl1X'
    image_url = 'https://graph.facebook.com/{}/photos'.format(page_id_1)
    img_payload = {
        'access_token': facebook_access_token_1
    }
    files = {
        'file': open('images/result.jpg', 'rb')
    }
    r = requests.post(image_url, data=img_payload, files=files)
##############################################################################################

if __name__ == '__main__':
    while(true):
        my_post = scrape()
        print('Done scraping')
        post(my_post)
        print('Done posting')
        time.sleep(60*60*24)
