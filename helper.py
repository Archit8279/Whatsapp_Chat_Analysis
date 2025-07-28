from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

links=[]
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>'].shape[0]

    
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def fetch_busiest_users(df):
    df = df[df['users'] != 'group_notification']
    x = df['users'].value_counts().head()
    new_df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns = {'count':'percentage'})
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df = df[df['messages'] != '<Media omitted>']
    df_wc = wc.generate(df['messages'].str.cat(sep = " "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['messages'] != '<Media omitted>']

    def is_only_emoji_word(word):
        emoji_chars = ''.join(char for char in word if emoji.is_emoji(char))
        return word == emoji_chars and word != ''



    words = []

    for message in temp['messages']:
        for word in message.split():
            if (word not in links) and not is_only_emoji_word(word):
                if word.lower() not in stop_words:
                    words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    emoji_df =  pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(
        columns = {0:'emoji',1:'count'})
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['dayname'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index = 'dayname', columns = 'period', values = 'messages',
                                       aggfunc = 'count').fillna(0)
    
    return user_heatmap



