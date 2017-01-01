import facebook


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
            return None

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
            return None

    def get_comments(self):
        if self.data:
            return self.data['comments']['data']
        else:
            return None

    def get_comments_count(self):
        comments = self.get_comments()

        if comments:
            return len(comments)
        else:
            return 0


if __name__ == "__main__":
    fbk = FacebookKnowledge()
    data = fbk.get_last_post_info()

    if data:
        try:
            message = data['message']
        except KeyError:
            message = data['story']

        reactions_count = fbk.get_reactions_count()

        print(fbk.get_comments_count())

