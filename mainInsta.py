import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

AccessToken = '3128064930.f273002.9ca896a2ddb4498d80f8ada523d14a4a'
BASE_URL = 'https://api.instagram.com/v1/'

def check__code(d):
    if d['meta']['code'] == 200:
        return None
    else:
        print 'Status code other than 200 received!'
        exit()

def get_data_from_url(request_url):
    r = requests.get(request_url).json()
    return r

def post_data_request(request_url, payload):
    r = requests.post(request_url, payload).json()
    return r


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        print 'Username: %s' % (d['data']['username'])
        print 'No. of followers: %s' % (d['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (d['data']['counts']['follows'])
        print 'No. of posts: %s' % (d['data']['counts']['media'])
    else:
        print 'User does not exist!'


'''
Function declaration to get the ID of a user by username
'''

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        return d['data'][0]['id']
    else:
        return None


'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        print '\nUsername: %s' % (d['data']['username'])
        print 'No. of followers: %s' % (d['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (d['data']['counts']['follows'])
        print 'No. of posts: %s' % (d['data']['counts']['media'])
    else:
        print 'There is no data for this user!'


'''
Function declaration to get your recent post
'''

def download_image(d):

    image_name = d['data'][0]['id'] + '.jpeg'
    image_url = d['data'][0]['images']['standard_resolution']['url']
    urllib.urlretrieve(image_url, image_name)
    return None

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        download_image(d)
        print '\nYour image has been downloaded!'
    else:
        print 'Post does not exist!'

'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        download_image(d)
        print '\nYour image has been downloaded!'
    else:
        print 'Post does not exist!'


'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_recent_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        return d['data'][0]['id']
    else:
        print 'There is no recent post of the user!'
        exit()


'''
Function to get a list of people who have liked the recent post of a user
'''
def like_list(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        for x in range(0,len(d['data'])):
            print "liked by: " + d['data'][x]['username']
    else:
        "There is no like on this media"


'''
Function declaration to like the recent post of a user
'''

def like_a_post(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": AccessToken}
    print '\nPOST request url : %s' % (request_url)

    d = post_data_request(request_url , payload)
    if d['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


'''
Function to get a list of comments on the recent post of a user
'''

def list_of_comments(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id,AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        for x in range(0,len(d['data'])):
            print "comment:" + d['data'][0]['text']
    else:
        print "No comments to show!"




'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_recent_post_id(insta_username)
    comment_text = raw_input("\nWrite your comment here: ")
    payload = {"access_token": AccessToken, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print '\nPOST request url : %s' % (request_url)

    d = post_data_request(request_url,payload)

    if d['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"



'''
Function declaration to make delete negative comments from the recent post
'''

def delete_negative_comment(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, AccessToken)
    print '\nGET request url : %s' % (request_url)
    d = get_data_from_url(request_url)
    check__code(d)

    if len(d['data']):
        # Here's the implementation of code that how to delete the negative comments
        for x in range(0, len(d['data'])):
            comment_id = d['data'][x]['id']
            comment_text = d['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print 'Negative comment : %s' % (comment_text)
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, AccessToken)
                print 'DELETE request url : %s' % (delete_url)
                delete_info = requests.delete(delete_url).json()

                if delete_info['meta']['code'] == 200:
                    print 'Comment successfully deleted!'
                else:
                    print 'Unable to delete comment!'
            else:
                print 'Positive comment : %s' % (comment_text)
    else:
        print 'There are no existing comments on the post!'



def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to InstaBot!'
        print 'Select from these options:\n'
        print "a. Get your own details\n"
        print "b. Get details of a user by username\n"
        print "c. Get your own recent post\n"
        print "d. Get the recent post of a user by username\n"
        print "e. Get a list of people who have liked the recent post of a user\n"
        print "f. Like the recent post of a user\n"
        print "g. Get a list of comments on the recent post of a user\n"
        print "h. Make a comment on the recent post of a user\n"
        print "i. Delete negative comments from the recent post of a user\n"
        print "j. Exit"

        choice = raw_input("\nEnter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           like_list(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           list_of_comments(insta_username)
        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "j":
            exit()
        else:
            print "wrong choice"

start_bot()