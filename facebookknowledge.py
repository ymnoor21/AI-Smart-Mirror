import facebook
from dateutil import parser

class ReactionEnum(enumerate):
    LIKE = 'LIKE'
    LOVE = 'LOVE'
    HAHA = 'HAHA'
    WOW = 'WOW'
    SAD = 'SAD'
    ANGRY = 'ANGRY'


class FacebookKnowledge(object):
    def __init__(self):
        # https://developers.facebook.com/tools/accesstoken/
        self.user_token = \
            "EAAa4YDLtrSMBAELcZCGmzroCZBQuC04HlPs4yV95XbjdKBGLR" \
            "YCyCGMTABniflPnPkBWTwdV7q9PU5zViHDmLQs2r8kZBKgC9di" \
            "3a0f8z7hBjElZC1u7k98vAXOxcduZCJCnnvX7LklyH6PoPxd8G"

        # Facebook API Version
        self.version = "2.8"
        self.data = None

    def get_last_post_info(self):
        graph = facebook.GraphAPI(access_token=self.user_token,
                                  version=self.version)

        info = graph.get_object(id='me?fields=feed.limit(1){'\
                                'message,story,comments.limit(10){'\
                                'created_time,from{name,id},message,id},'\
                                'reactions}')

        if info['feed']['data']:
            self.data = info['feed']['data'][0]

        return self.data

    def get_reactions(self):
        if self.data:
            return self.data['reactions']['data']
        else:
            return []

    def get_reactions_count(self):
        reactions = self.get_reactions()

        if reactions:
            like, love, haha, wow, sad, angry = 0, 0, 0, 0, 0, 0

            for reaction in reactions:
                if ReactionEnum.LIKE == reaction['type']:
                    like += 1
                elif ReactionEnum.LOVE == reaction['type']:
                    love += 1
                elif ReactionEnum.HAHA == reaction['type']:
                    haha += 1
                elif ReactionEnum.WOW == reaction['type']:
                    wow += 1
                elif ReactionEnum.SAD == reaction['type']:
                    sad += 1
                elif ReactionEnum.ANGRY == reaction['type']:
                    angry += 1

            return {
                'like': like,
                'love': love,
                'haha': haha,
                'wow': wow,
                'sad': sad,
                'angry': angry,
            }
        else:
            return {}

    def get_total_likes_count(self):
        reactions_count = self.get_reactions_count()

        if reactions_count:
            total = reactions_count['like'] +\
                    reactions_count['love'] +\
                    reactions_count['haha'] +\
                    reactions_count['wow'] +\
                    reactions_count['sad'] +\
                    reactions_count['angry']

            return total
        else:
            return 0

    def get_comments(self):
        comments_list = []

        if self.data:
            comments = self.data['comments']['data']

            if comments:
                for comment in comments:
                    dt = parser.parse(comment['created_time'])
                    cmt_created_at = dt.strftime("%b %d, %Y %I:%M%p")
                    cmt_message = comment['message']
                    cmt_by = comment['from']['name']

                    comments_list.append({
                        'comment_by': cmt_by,
                        'comment': cmt_message,
                        'created_by': cmt_created_at,
                    })

        return comments_list

    def get_comments_count(self):
        comments = self.get_comments()

        if comments:
            return len(comments)
        else:
            return 0
