import requests
import os
import json
import time

blacklist_file = open('viewed.txt', "r+", encoding="utf-8")
blacklist = blacklist_file.read()
daily_limit = False
skip = False


search_finished = False
distances = ["5", "10", "20", "50", "75", "80", "100", "160", "200", "300", "500", "800", "1000", "1600", "2000", "3000", "5000", "10000", "999998"]
print('This is prototype code, you will have to supply the autologin cookie manually.')
print('I will later add code to automate the login process.\n')
autologin_cook = input('Cookie: ')

cookies = {
    'stay': '1',
    'autologin': autologin_cook,
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://adultfriendfinder.com/go/page/new_search.html?',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = ''
session = requests.Session()
initial_response = session.get('https://adultfriendfinder.com/go/page/home_delta.html', params=params, cookies=cookies, headers=headers)
if 'ffadult_tr' in initial_response.cookies:
    ## Search code
    # Log clear
    print("Clearing old logs...")
    temp_var = './'
    temp_var2 = os.listdir(temp_var)

    for temp_var3 in temp_var2:
        if temp_var3.endswith('.json'):
            os.remove(os.path.join(temp_var, temp_var3))
    ##
    print('Enter a search distance from below.')
    for distance_sel in distances:
        print(distance_sel)
    distance = input('Distance: ')
    country_grab = initial_response.cookies['LOCATION_FROM_IP'].split('&')[1]
    city_grab = initial_response.cookies['LOCATION_FROM_IP'].split('&')[5]
    latitude_grab = initial_response.cookies['LOCATION_FROM_IP'].split('&')[6]
    longitude_grab = initial_response.cookies['LOCATION_FROM_IP'].split('&')[8]
    state_grab = initial_response.cookies['LOCATION_FROM_IP'].split('&')[11]
    print(f"Grabbing all accounts within {distance} miles...")
    for increment in range(0, 960000, 96):
        if search_finished is False:
            params = {
                'find_sex': [
                    '2',
                    '5',
                ],
                'looking_for_person': '1',
                'min_age': '18',
                'max_age': '99',
                'max_dist_value': str(distance),
                'lat': latitude_grab,
                'lon': longitude_grab,
                'location_text': f"{city_grab}, {state_grab}, {country_grab}",
                'has_photo': '1',
                # 'join_date': '1_week',
                'sex_orient': [
                    '1',
                    '2',
                    '3',
                ],
                'min_height': '',
                'max_height': '',
                'zodiac': '',
                'chinese_zodiac': '',
                'offset': str(increment),
                'do_relax': '1',
                'limit': '96',
                'order': 'last_login',
                'do_json': '1',
                'search_type': 'online',
                'cb': '1674771482815',
            }
            search_response = session.get('https://adultfriendfinder.com/search_combined', params=params, cookies=cookies, headers=headers)
            time.sleep(1)
            if '"results":[]' in search_response.text:
                print(f"Finished all search results!")
                search_finished = True
            with open(f'temp_{increment}.json', 'w', encoding='utf-8') as f:
                f.write(search_response.text)
                print(f"Wrote temp_{increment}.json")
                f.close()
    for increment in range(0, 960000, 96):
        try:
            if os.path.isfile(f"./temp_{increment}.json"):
                print(f"Reading temp_{increment}.json...")
                with open(f'temp_{increment}.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for result_keys in data['results']:
                        user_id = result_keys['pwsid']
                        if user_id in blacklist:
                            skip = True
                        else:
                            skip = False
                        if skip is False:
                            blacklist_file.write(user_id + "\n")
                            params = {
                                'mid': user_id
                            }
                            view_response = session.get('https://adultfriendfinder.com/p/member.cgi', params=params, cookies=cookies, headers=headers)
                            user_name = view_response.url.rsplit('/', 1)[-1]
                            print(f"Viewed user: {user_name}")
                            time.sleep(2)
                            ## ADD FRIEND CODE HERE
                            if daily_limit is False:
                                data = {
                                    'site_tab': 'social',
                                    '_templatename_': '',
                                    'action': 'send_invites',
                                    'inviter_pwsid': '489972444_11105',
                                    'groupid': '49831970',
                                    'status': '1',
                                    'alt_from_handle': '',
                                    'mid': user_id,
                                    'showmore': '1',
                                    'invitee_handles': f'{user_name}  ',
                                    'brief': '1',
                                    'subject': '6_pt_6_bigbrain wants you to join his Friends Network',
                                    'message': 'Heyy',
                                    'cat_id': '1',
                                    'charcount': '250',
                                    'send': 'Send',
                                }
                                friend_response = session.post('https://adultfriendfinder.com/p/circle/people.cgi', cookies=cookies, headers=headers, data=data)
                                if "Invitation has been sent to" in friend_response.text:
                                    print(f"Friends request sent to {user_name} [{user_id}]")
                                elif "Your daily limit has been reached" in friend_response.text:
                                    print("Daily limit reached for friends requests.")
                                    daily_limit = True
                                else:
                                    print(f"Error adding friend {user_name} [{user_id}]")
                                    daily_limit = True
                                time.sleep(2)
        except Exception:
            pass
