import backoff
import requests
import re
from bs4 import BeautifulSoup as bs

class ForbiddenError(Exception):
    pass

@backoff.on_exception(backoff.expo, ForbiddenError, max_tries=20)
def returnQuery(username, name, regno, year, dept, section, domain, mail, phone):
    url = 'https://leetcode.com/graphql'


    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'cookies' : 'asdfads',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

    }
    
    query = '''
        query combinedQueries($username: String!) {
            matchedUser(username: $username) {
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
            userContestRanking(username: $username) {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
                badge {
                    name
                }
            }
        }
    '''

    variables = {
        "username": f"{username}"
    }

    payload = {
        'query': query,
        'variables': variables
    }

    response = requests.post(url, json=payload, headers=headers)


    if response.status_code == 200:
        json_dict = response.json()

        if not json_dict:
            return None

        matchedUser = json_dict['data']['matchedUser']

        contestCount,rating,globalRank,topPercent = 0,0,0,0
        easy, medium, hard, total = 0, 0, 0, 0

        if  matchedUser:
            problems_solved = matchedUser['submitStatsGlobal']['acSubmissionNum']

            for pair in problems_solved:
                if pair['difficulty'] == 'All':
                    total = pair['count']
                elif pair['difficulty'] == 'Easy':
                    easy = pair['count']
                elif pair['difficulty'] == 'Medium':
                    medium = pair['count']
                elif pair['difficulty'] == 'Hard':
                    hard = pair['count']

            score = easy + medium * 2 + hard * 3

        else:
            return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False


        contest = json_dict['data']['userContestRanking']

        if  contest:

            for key, value in contest.items():
                if key == 'attendedContestsCount':
                    contestCount = value
                elif key == 'rating':
                    rating = value
                elif key == 'globalRanking':
                    globalRank = value
                elif key == 'topPercentage':
                    topPercent = value

        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username,'Easy' : easy, 'Medium' : medium, 'Hard' : hard, 'Total' : total, 'Score' : score,'Total Contests Count' : contestCount, 'Contest Rating' : rating, 'Global Rank' : globalRank, 'Top%' : topPercent, 'Mail ID' : mail, 'Mobile Number' : phone}, True

    
    elif response == 404:
       
        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False
        
    else :
        print(username)

        raise ForbiddenError("Received a 403 Forbidden response")
    
def codechef(username):

    r = requests.get(f"https://www.codechef.com/users/{username}")

   

    soup = bs(r.content,"html.parser")
    div_number = soup.find("div", {"class":"rating-header text-center"})

    rankings = soup.find("div", {"class":"rating-ranks"})

    if div_number and rankings:

        ul_element = rankings.find('ul')

        contestcount = soup.find("div", {"class":"contest-participated-count"})

        # for global ranking
        if ul_element:
            globalrank = ul_element.find('li').text.split()[0]
        else:
            globalrank = "NA"

    # for country ranking
        if ul_element:
            countryrank = ul_element.find_all('li')[1].text.split()[0]
        else:
            countryrank = "NA"

        div_number1 = div_number.find_all("div")

        highestRating = div_number.find('small').text.strip(')').split()[-1]
        L = []

        for tag in div_number1:
            L.append(tag.get_text())

        count = contestcount.find('b').text

        problemscount = []
        prob = soup.find("section", {"class":"rating-data-section problems-solved"})
        a = prob.find_all("h3")
        
        ans1 = a[0].text.strip()
        ans1 = ans1.strip('):')
        ans1 = ans1[19:]

        ans2 = a[1].text.strip()
        ans2 = ans2.strip('):')
        ans2 = ans2[10:]

        ans3 = a[2].text.strip()
        ans3 = ans3.strip('):')
        ans3 = ans3[16:]

        
        ans4 = a[3].text.strip()
        ans4 = ans4.strip('):')
        ans4 = ans4[16:]

        number1 = int(ans1)
        number2 = int(ans2)
        number3 = int(ans3)
        number4 = int(ans4)

        rating = L[0]
        rating = rating.strip()
        rating = rating[:4].strip('\n')
        rating = rating.strip('?i')
        div = L[1]
        star = L[2]



        return ({
        "Current Rating" : int(rating) , 
        "Highest Rating" : int(highestRating),
        "Division" : int(div[-2]),
        "Star Rating" : star,
        "Global Ranking" :globalrank,
        "Country Ranking":countryrank,
        "No. of Contests Participated" :int(count),
        "practiceProblems" : int(ans1),
        "contestProblems" : int(ans2),
        "learningProblems" : int(ans3),
        "practicePaths" : int(ans4),
        "Total Problems Solved" : int(ans1) + int(ans2) + int(ans3) + int(ans4)
        } , True)
    else:
        return ({},False)


def codeForces(username):
    
    infoUrl = f'https://codeforces.com/api/user.info?handles={username}'
    submissionsUrl = f'https://codeforces.com/api/user.status?handle={username}'
    contestUrl = f'https://codeforces.com/api/user.rating?handle={username}'

    infoResponse = requests.get(infoUrl)
    submissionsResponse = requests.get(submissionsUrl)
    contestResponse = requests.get(contestUrl)

    found,current_rating ,current_rank ,max_rating ,max_rank ,problems_count,contestAttended = True,0,0,0,0,0,0

    if infoResponse.status_code == 200:

        infoResponse = infoResponse.json()

        if infoResponse['status'] == 'OK':

            infoResponse = infoResponse['result'][0]

            if 'rating' in infoResponse:
                current_rating = infoResponse['rating']
                current_rank = infoResponse['rank']
                max_rating = infoResponse['maxRating']
                max_rank = infoResponse['maxRank']

    elif infoResponse.status_code == 400:
        return ({'found' : False},False)
    else:
        print('Try again after sometime')

    if submissionsResponse.status_code == 200:

        submissionsResponse = submissionsResponse.json()

        if submissionsResponse['status'] == 'OK':
            submissionsResponse = submissionsResponse['result']
            
            if submissionsResponse:
                submissionSet = set()

                for submission in submissionsResponse:
                    if submission['verdict'] == 'OK':
                        submissionSet.add(submission['id'])

                problems_count = len(submissionSet)

            
        else:
            print('Try again after sometime')


    if contestResponse.status_code == 200:

        contestResponse = contestResponse.json()

        if contestResponse['status'] == 'OK':
            contestResponse = contestResponse['result']

            contestAttended = len(contestResponse)



    return ({ 'current_rating' : current_rating  ,'current_rank' : current_rank ,'max_rating' : max_rating ,'max_rank' :max_rank ,'problems_count':problems_count ,'contestAttended' : contestAttended},True)

def codechef_contest(username, contest_name):
    url = f"https://www.codechef.com/users/{username}"
    r = requests.get(url)

    if r.status_code != 200:
        print(f"Failed to retrieve the user's profile. Status Code: {r.status_code}")
        return {'message' : r.status_code} , False

    soup = bs(r.content, "html.parser")
    result = {'rank' : 0 , 'rating' : 0,'change' : 0 , 'div' : 0 , 'number' : 0 }

    # Get the number of problems solved
    contest_section = soup.find("section", {"class": "rating-data-section problems-solved"})
 
    if contest_section:
        contest_names = [h5.get_text(strip=True) for h5 in reversed(contest_section.find_all('h5'))]
        matching_contests = [name for name in contest_names if contest_name.lower() in name.lower()]

        if matching_contests:
            matching_contest_name = matching_contests[0]
            matching_h5 = next((h5 for h5 in contest_section.find_all('h5') if matching_contest_name.lower() in h5.get_text(strip=True).lower()), None)

            if matching_h5:
                problems_div = matching_h5.find_parents('div', class_='content')[0]

                if problems_div:
                    span_tag = problems_div.find('p').find('span')

                    if span_tag:
                        a_tags = span_tag.find_all('a')
                        num_a_tags = len(a_tags)
                        # print(f"Number of problems solved for {contest_name}: {num_a_tags}")
                        result['number'] = num_a_tags
        else:
            return result , False
    else:
        return result , False
    
  
    rating_box_all = soup.find("div", {"id": "rating-box-all"})
    if rating_box_all:
        global_rank_container = rating_box_all.find('div', {'id': 'global-rank-all'})

        if global_rank_container:
            global_rank_element = global_rank_container.find('strong', {'class': 'global-rank'})

            if global_rank_element:
                global_rank = global_rank_element.get_text(strip=True)
                result['rank'] = int(global_rank)
            else:
                print("No global rank information found.")
        else:
            print("Global Rank information not available.")
    else:
        print("Rating box information not found on the user's profile page.")

    # Get user rating and division
    rating_container = soup.find("div", {"class": "rating-container"})
    if rating_container:
        rating_element = rating_container.find('a', {'class': 'rating'})

        if rating_element:
            rating_text = rating_element.get_text(strip=True)

            # Extract rating and division from the rating string
            rating_parts = rating_text.split()
            if len(rating_parts) == 2:
                rating = rating_parts[0]
                division_part = rating_parts[1]

                # Check if the division is in the expected format
                if '(' in division_part and ')' in division_part:
                    division = division_part.strip('()')

                    # Extract division from the contest name in rating-box-all div
                    contest_name_division = soup.find("div", {"id": "rating-box-all"}).find("div", {"class": "contest-name"})
                    if contest_name_division:
                        contest_division = contest_name_division.find("a").text.strip().replace(contest_name, '').strip()
                       
                        rating = rating.strip()
                        rating = rating[:4].strip('\n')
                        rating = rating.strip('?i')
                        result['rating'] = int(rating)

                        result['change'] = division
                        contest_division = contest_division.strip('(Rated)')
                        contest_division = contest_division.strip('(Unrated)')
                        contest_division = contest_division.strip()
                        contest_division = contest_division[-1]

                        result['div'] = int(contest_division)
                        
                        return result , True
                    else:
                        print("Division information not found.")
                else:
                    print("Invalid division format.")
            else:
                print("Invalid rating format.")
        else:
            print("No rating information found.")
    else:
        print("Rating container not found on the user's profile page.")

    return result , True