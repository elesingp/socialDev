import googleapiclient.discovery
import pandas as pd
import numpy as np

# ВИДОС https://www.youtube.com/watch?v=zJpvltGOtMc
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC0la9wfk2qkmChlWpLdcH9fiA7kps4WMs"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

comments = []

# Функция для извлечения комментариев верхнего уровня
def get_top_level_comments(videoId):
    nextPageToken = None
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            maxResults=100,
            pageToken=nextPageToken
        )
        response = request.execute()
        
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            # Для комментариев верхнего уровня parentId будет None
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay'],
                'Top Level',
                None  # parentId для комментария верхнего уровня
            ])
            # Получаем ответы на комментарий, если они есть, передаем parentId
            get_replies(item['snippet']['topLevelComment']['id'])
        
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break

# Функция для извлечения ответов на комментарии
def get_replies(parentId):
    nextPageToken = None
    while True:
        reply_request = youtube.comments().list(
            part="snippet",
            parentId=parentId,
            maxResults=100,
            pageToken=nextPageToken
        )
        reply_response = reply_request.execute()
        
        for item in reply_response['items']:
            reply = item['snippet']
            comments.append([
                reply['authorDisplayName'],
                reply['publishedAt'],
                reply['updatedAt'],
                reply['likeCount'],
                reply['textDisplay'],
                'Reply',
                parentId  # Добавляем parentId для ответа
            ])
        
        nextPageToken = reply_response.get('nextPageToken')
        if not nextPageToken:
            break

# Получаем комментарии верхнего уровня и ответы
get_top_level_comments("1GuVkexgaQI")

# Создаем DataFrame с добавленным столбцом parentId
df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text', 'comment_type', 'parent_id'])

# топ по лайкам на комментариях
df_sorted = df.sort_values('like_count', ascending=False)

# Выводим отсортированный DataFrame
print(df_sorted)

comments = np.array(df['text'])

print(comments)


