from termcolor import colored                          # change the color of the text
from colored import fg, attr
import requests, urllib                                        # Install requests library to make network requests and urllib to download images.
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer         # analyze the sentiments of the comment



'''
>> Access token generated from instagram.com/developer.
>> Global variable for the instagram API access token and  base url of all the requests.
'''
AccessToken = '3128064930.f273002.9ca896a2ddb4498d80f8ada523d14a4a'
BASE_URL = 'https://api.instagram.com/v1/'


'''
>> Function declaration to check whether code is correct or not
'''
def check__code(d):
    if d['meta']['code'] == 200:
        return None
    else:
        print (colored('Status code other than 200 received!','red'))
        exit()

'''
>> Function declaration to make a get call to fetch data
'''
def get_data_from_url(request_url):                  # get call function
    r = requests.get(request_url).json()
    return r

'''
>> Function declaration to post a request
'''
def post_data_request(request_url, payload):
    r = requests.post(request_url, payload).json()
    return r

'''
>> Function declaration to fetch your own info
>> It will not accept any input parameter.
>> The function will make a get call to fetch your details and print the same on the console.
>> If the user will not found then the function prints a meaningful message whereas for the successful search, the function return the user's id.
'''
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
>> Function declaration to get the ID of a user by username
>> It can accept his/her username as an input parameter.
>> The function will make a get call to search user with his username.
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
>>  Function declaration to get the info of a user by username.
>>  make use of the above created function to fetch the user's Id using the username.
>>  make use of above created get call function to fetch user details.
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print (colored('\nUser does not exist!' , 'red'))
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, AccessToken)
        d = get_data_from_url(request_url)
        check__code(d)
        if len(d['data']):
            print '\nUsername: %s' % (d['data']['username'])
            print  ('Bio: %s') % (d['data']['bio'])
            print 'No. of followers: %s' % (d['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (d['data']['counts']['follows'])
            print 'No. of posts: %s' % (d['data']['counts']['media'])
        else:
            print 'There is no data for this user!'


'''
  Function declaration to download the most recent post.
'''

def download_image(d):
    image_name = d['data'][0]['id'] + '.jpeg'
    image_url = d['data'][0]['images']['standard_resolution']['url']
    urllib.urlretrieve(image_url, image_name)
    return None


'''
  Function declaration to get your recent post and It will not accept any input parameter.
'''
def get_own_recent_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        download_image(d)
        print '\nYour image has been downloaded!'
    else:
        print (colored('Post does not exist!' , 'red'))


'''
>> Function declaration to get the recent post of a user by username ant it can accept any input parameter.
>> The function will make use of the above created function to fetch the user's Id using the username.
'''

def get_user_recent_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print (colored('User does not exist!','red'))
    else:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AccessToken)
        d = get_data_from_url(request_url)
        check__code(d)
        if len(d['data']):
            download_image(d)
            print (colored('\nYour image has been downloaded!','green'))
        else:
            print (colored('Post does not exist!', 'red'))



'''
   Function declaration to fetch any post of the user by its number
'''

def get_any_post_of_user(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print (colored('User does not exist!','red'))
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        image_number = raw_input("Enter the image number, you want to fetch: ")
        image_number = int(image_number)
        x = image_number - 1
        if x < len(d['data']):
            image_name = d['data'][x]['id'] + ".jpeg"
            image_url = d['data'][x]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print (colored('\nYour image has been downloaded!','green'))
        else:
            print colored("Image does not exist", 'red')
    else:
        print (colored('Post does not exist!' , 'red'))




'''
  Function declaration to get the ID of the recent post of a user by username
'''

def get_recent_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print (colored('User does not exist!','red'))
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
  Function to get a list of people who have liked the recent post of a user.
'''
def like_list(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        liked_by = 1
        print (colored("Liked by: ", 'blue'))
        for x in range(0,len(d['data'])):
            print str(liked_by) + ". " + d['data'][x]['username']

            liked_by = liked_by +1
    else:
         print (colored("There is no like on this media",'cyan'))


'''
>> Function declaration to like the recent post of a user and it will accept the user's username as input parameter.
>> The function will make use of the above created function to fetch the post's Id using the username.
>> The function will make a POST call to like a post.
'''

def like_a_post(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": AccessToken}
    print '\nPOST request url : %s' % (request_url)

    d = post_data_request(request_url , payload)
    if d['meta']['code'] == 200:
        print (colored('Like was successful!','green'))                                        # print a meaningful message upon successfully liking a post.
    else:
        print (colored('Your like was unsuccessful. Try again!' , 'red'))   # print a meaningful message upon any error in liking a post.


'''
  Function to fetch recent media liked by self
'''
def get_recently_liked_media():
    request_url = BASE_URL +"users/self/media/liked?access_token=%s" %(AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        image_name = d['data'][0]['id'] + ".jpeg"
        image_url = d['data'][0]['images']['standard_resolution']['url']
        urllib.urlretrieve(image_url, image_name)
        print (colored("Your image has been downloaded!!",'green'))
    else:
        print (colored("Media does not exist!!",'red'))


'''
  Function to get a list of comments on the recent post of a user. It will accept the user's username for whose post you want to fetch the list.
  The function should make use of the above created function to fetch the post's id using the username.
'''

def list_of_comments(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id,AccessToken)
    d = get_data_from_url(request_url)
    check__code(d)
    if len(d['data']):
        comment_no =1
        print (colored('\nList of comments:', 'blue'))                  # print a meaningful message upon successfully getting the list of comments on the post.
        for x in range(0,len(d['data'])):
            print str(comment_no) + "." + d['data'][x]['text']
            comment_no = comment_no + 1
    else:
        print (colored("No comments to show!" , 'cyan'))                # print a meaningful message upon any error in getting the list of comments on the post.



'''
  Function declaration to make a comment on the recent post of the user.It will accept the user's username for whose post you want to comment on.
  The function will make use of the above created function to fetch the post's id using the username.
  The function will make a POST call to comment on the post
'''

def post_a_comment(insta_username):
    media_id = get_recent_post_id(insta_username)
    comment_text = raw_input("\nWrite your comment here: ")
    payload = {"access_token": AccessToken, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print '\nPOST request url : %s' % (request_url)

    d = post_data_request(request_url,payload)

    if d['meta']['code'] == 200:
        print (colored("Successfully added a new comment!",'green'))                             # print a meaningful message upon successfully commenting.

    else:
        print (colored("Unable to add comment. Try again!" , 'red'))          # print a meaningful message if function fails to comment.


'''
  Function declaration to make delete negative comments from the recent post.
'''

def delete_negative_comment(insta_username):
    media_id = get_recent_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, AccessToken)
    print '\nGET request url : %s' % (request_url)
    d = get_data_from_url(request_url)
    check__code(d)

    if len(d['data']):

        for x in range(0, len(d['data'])):
            comment_id = d['data'][x]['id']
            comment_text = d['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print (colored('Negative comment :','cyan')) + comment_text
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, AccessToken)
                print 'DELETE request url : %s' % (delete_url)
                delete_info = requests.delete(delete_url).json()

                if delete_info['meta']['code'] == 200:
                    print (colored('Comment successfully deleted!','green'))
                else:
                    print (colored('Unable to delete comment!','red'))
            else:
                print (colored('Positive comment :','cyan')) + comment_text
    else:
        print (colored('There are no existing comments on the post!','cyan'))


'''
>> our application starts from here by providing you many choices
 This function does the following tasks :
  1.  ask you for the username for which you want to perform any of the action.
  2.  ask the user what they want to do.
  3.  and then perform the function corresponding to the choice of the user.
'''


def start_bot():
    while True:
        print '\n'
        print ('%s%sHey! Welcome to InstaBot! %s' % (fg('black'),attr('bold'),attr('reset')))
        print 'Select from these options:\n'

        print "a. Get your own details"
        print "b. Get details of a user by username"
        print "c. Get your own recent post"
        print "d. Get the recent post of a user by username"
        print "e. Get any post of the user by its image number"
        print "f. Get a list of people who have liked the recent post of a user"
        print "g. Like the recent post of a user"
        print "h. Get the recent post liked by self"
        print "i. Get a list of comments on the recent post of a user"
        print "j. Make a comment on the recent post of a user"
        print "k. Delete negative comments from the recent post of a user"
        print "l. Exit"

        choice = raw_input("\nEnter your choice: ")
        if choice == "a":
            self_info()

        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)

        elif choice == "c":
            get_own_recent_post()

        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_recent_post(insta_username)

        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_any_post_of_user(insta_username)

        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_list(insta_username)

        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)

        elif choice == "h":
            get_recently_liked_media()

        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           list_of_comments(insta_username)

        elif choice=="j":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)

        elif choice=="k":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)

        elif choice == "l":
            exit()

        else:                                               # message popup if user selects wrong option.

            print (colored('%s wrong choice %s' % (attr('bold'), attr('reset')),'red'))

start_bot()