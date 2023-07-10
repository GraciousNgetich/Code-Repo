"""
    Final AWS Lambda function skeleton. 

"""

# Lambda dependencies
import boto3    # Python AWS SDK
import json     # Used for handling API-based data.
import base64   # Needed to decode the incoming POST data
from botocore.exceptions import ClientError  # Catch errors on client side
import numpy as np  # Array manipulation
import random


# <<< You will need to add additional libraries to complete this script >>>

# ** Insert key phrases function **
# --- Insert your code here ---
def key_phrase_finder(list_of_important_phrases, list_of_extracted_phrases):

    listing = []
    PhraseChecker = None

    res = str(list_of_extracted_phrases).split()

    for important_word in list_of_important_phrases:
        names = res
        names2 = [word for word in names if important_word in word]
        isnot_empty = np.array(names2).size > 0

        if isnot_empty == True:
            listing = np.append(listing, names2)

        else:
            listing = listing

    if np.array(listing).size > 0:
        PhraseChecker = True

    else:
        PhraseChecker = False

    return listing, PhraseChecker

# -----------------------------

# ** Insert sentiment extraction function **
# --- Insert your code here ---


def find_max_sentiment(Comprehend_Sentiment_Output):

    sentiment_score = 0

    if Comprehend_Sentiment_Output['Sentiment'] == 'POSITIVE':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Positive']

    elif Comprehend_Sentiment_Output['Sentiment'] == 'NEGATIVE':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Negative']

    elif Comprehend_Sentiment_Output['Sentiment'] == 'NEUTRAL':
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Neutral']

    else:
        sentiment_score = Comprehend_Sentiment_Output['SentimentScore']['Mixed']

    print(sentiment_score, Comprehend_Sentiment_Output['Sentiment'])

    return Comprehend_Sentiment_Output['Sentiment'], sentiment_score
# -----------------------------

# ** Insert email responses function **
# --- Insert your code here ---


def email_response(name, critical_phrase_list, list_of_extracted_phrases, AWS_Comprehend_Sentiment_Dump):

    # Function Constants
    SENDER_NAME = 'Your Names'

    # --- Check for the sentiment of the message and find dominant sentiment score ---
    Sentiment_finder = find_max_sentiment(AWS_Comprehend_Sentiment_Dump)
    overwhelming_sentiment = Sentiment_finder[0]
    overwhelming_sentiment_score = Sentiment_finder[1]

    # --- Check for article critical phrases ---
    Phrase_Matcher_Article = key_phrase_finder(
        critical_phrase_list,  list_of_extracted_phrases)
    Matched_Phrases_Article = Phrase_Matcher_Article[0]
    Matched_Phrases_Checker_Article = Phrase_Matcher_Article[1]

    # --- Check for project phrases ---
    Phrase_Matcher_Project = key_phrase_finder(['github', 'git', 'Git',
                                                'GitHub', 'projects',
                                                'portfolio', 'Portfolio'],
                                               list_of_extracted_phrases)
    Matched_Phrases_Project = Phrase_Matcher_Project[0]
    Matched_Phrases_Checker_Project = Phrase_Matcher_Project[1]

    # --- Check for C.V phrases ---
    Phrase_Matcher_CV = key_phrase_finder(['C.V', 'resume', 'Curriculum Vitae',
                                           'Resume', 'CV'],
                                          list_of_extracted_phrases)
    Matched_Phrases_CV = Phrase_Matcher_CV[0]
    Matched_Phrases_Checker_CV = Phrase_Matcher_CV[1]

    # --- Generate standard responses ---
    # === DO NOT MODIFY THIS TEXT FOR THE PURPOSE OF PREDICT ASSESSMENT ===
    Greetings_text = f'Good day {name},'

    CV_text = 'I see that you mentioned my C.V in your message. \
I am happy to forward you my C.V in response. \
If you have any other questions or C.V related queries please do get in touch. '

    Project_Text = 'The projects I listed on my site only include \
the ones not running in production. I have \
several other projects that might interest you.'

    Article_Text = 'In your message you mentioned my blog posts and data science articles. \
I have several other articles published in academic journals. \
Please do let me know if you are interested - I am happy to forward them to you'

    Negative_Text = f"I see that you are unhappy in your response. \
Can we please set up a session to discuss why you are not happy, \
be it with the website, my personal projects or anything else. \
                    \n\nLooking forward to our discussion. \n\nKind Regards, \n\nMy Name"

    Neutral_Text = f"Thank you for your email. Let me know if you need any additional information.\
                    \n\nKind Regards, \n\n{SENDER_NAME}"

    Farewell_Text = f"Thank you for your email.\n\nIf there is anything else I can assist \
you with please let me know and I will set up a meeting for us to meet\
 in person.\n\nKind Regards, \n\n{SENDER_NAME}"
    # =====================================================================

    # --- Email Logic ---
    if overwhelming_sentiment == 'POSITIVE':
        if ((Matched_Phrases_Checker_CV == True) &
            (Matched_Phrases_Checker_Article == True) &
                (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, CV_text, Article_Text,
                       Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) &
              (Matched_Phrases_Checker_Article == False) &
              (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, CV_text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) &
              (Matched_Phrases_Checker_Article == False) &
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, CV_text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) &
              (Matched_Phrases_Checker_Article == True) &
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) &
              (Matched_Phrases_Checker_Article == False) &
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == False) &
              (Matched_Phrases_Checker_Article == False) &
              (Matched_Phrases_Checker_Project == True)):

            mytuple = (Greetings_text, Project_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        elif ((Matched_Phrases_Checker_CV == True) &
              (Matched_Phrases_Checker_Article == True) &
              (Matched_Phrases_Checker_Project == False)):

            mytuple = (Greetings_text, CV_text, Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

        else:
            mytuple = (Greetings_text, Project_Text,
                       Article_Text, Farewell_Text)
            Text = "\n \n".join(mytuple)

    elif overwhelming_sentiment == 'NEGATIVE':
        mytuple = (Greetings_text, Negative_Text)
        Text = "\n \n".join(mytuple)

    else:
        mytuple = (Greetings_text, Neutral_Text)
        Text = "\n \n".join(mytuple)

    return Text

# -----------------------------

# Lambda function orchestrating the entire predict logic


def lambda_handler(event, context):

    # Perform JSON data decoding
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))

    # ** Insert code to write to dynamodb **
    # <<< Ensure that the DynamoDB write response object is saved
    #    as the variable `db_response` >>>
    # --- Insert your code here ---

    # <--- Replace this value with your code.
    rid = random.randint(1, 1000000000)
    # -----------------------------

    # ** Instantiate the DynamoDB service with the help of the boto3 library **

    # --- Insert your code here ---
    # <--- Replace this value with your code.
    dynamodb = boto3.resource('dynamodb')
    # -----------------------------

    # Instantiate the table. Remember pass the name of the DynamoDB table created in step 4
    table = dynamodb.Table('Your DynamoBd Table Name')

    # Do not change the name of this variable
    db_response = table.put_item(Item={'ResponseID': rid,  # <--- Insert the correct variable,
                                       # <--- Insert the correct variable
                                       'Name': dec_dict['name'],
                                       # <--- Insert the correct variable
                                       'Email': dec_dict['email'],
                                       # <--- Insert the correct variable
                                       'Cell': dec_dict['phone'],
                                       # <--- Insert the correct variable
                                       'Message': dec_dict['message']
                                       })
    # -----------------------------

    # --- Amazon Comprehend ---
    comprehend = boto3.client(service_name='comprehend')

    # --- Insert your code here ---
    # <--- Insert code to place the website message into this variable
    enquiry_text = dec_dict['message']
    # -----------------------------

    # --- Insert your code here ---
    # <---Insert code to get the sentiment with AWS comprehend
    sentiment = comprehend.detect_sentiment(
        Text=enquiry_text, LanguageCode='en')
    # -----------------------------

    # --- Insert your code here ---
    # <--- Insert code to get the key phrases with AWS comprehend
    key_phrases = comprehend.detect_key_phrases(
        Text=enquiry_text, LanguageCode='en')
    # -----------------------------

    # Get list of phrases in numpy array
    phrase = []
    for i in range(0, len(key_phrases['KeyPhrases'])-1):
        phrase = np.append(phrase, key_phrases['KeyPhrases'][i]['Text'])

    # ** Use the `email_response` function to generate the text for your email response **
    # <<< Ensure that the response text is stored in the variable `email_text` >>>
    # --- Insert your code here ---

    # Do not change the name of this variable
    email_text = email_response(dec_dict["name"], [
                                "Journal", "journal", "Publication", "publication", "blog", "Blog", "Article", "article"], phrase, sentiment)

    # -----------------------------

    # ** SES Functionality **

    # Insert code to send an email, using AWS SES, with the above defined
    # `email_text` variable as it's body.
    # <<< Ensure that the SES service response is stored in the variable `ses_response` >>>
    # --- Insert your code here ---
    SENDER = 'Your Verified Email address'
    # -----------------------------

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    # --- Insert your code here ---
    RECIPIENT = dec_dict['email']
    # -----------------------------

    # The subject line for the email.
    # --- DO NOT MODIFY THIS CODE ---
    SUBJECT = f"Data Engineering Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = boto3.client('ses')
    # Do not change the name of this variable
    try:
        # Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])

    # ** Create a response object to inform the website
    #    that the workflow executed successfully. **

    # ...

    # Do not modify the email subject line
    SUBJECT = f"Data Engineering Portfolio Project Website - Hello {dec_dict['name']}"

    # -----------------------------

    # ** Create a response object to inform the website that the
    #    workflow executed successfully. Note that this object is
    #    used during predict marking and should not be modified.**
    # --- DO NOT MODIFY THIS CODE ---
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
            'Name': dec_dict['name'],
            'Email': dec_dict['email'],
            'Cell': dec_dict['phone'],
            'Message': dec_dict['message'],
            'DB_response': db_response,
            'SES_response': ses_response,
            'Email_message': email_text
        })
    }
    # -----------------------------

    return lambda_response
