from posts.models import Post, Comment, Sido, Sigungu
from users.models import User
import random

User.objects.all().delete()
for user_id in range(1, 11):
    user = User.objects.create_user(email='user%d@naver.com' % user_id, nickname='사용자 %d' % user_id, password='12345678')
    print(user)

Sido.objects.all().delete()
sido_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
for sido_name in sido_list:
    sido = Sido(name=sido_name)
    sido.save()
    print(sido)
    for sigungu_num in range(1, 6):
        sigungu = Sigungu(sido=sido, name='%s%d' % (sido.name, sigungu_num))
        sigungu.save()
        print(sigungu)

field_list = ['web', 'android', 'ios', 'game', 'ml', 'bigdata', 'iot', 'blockchain', 'vr', 'etc']
for post_id in range(1, 101):
    user = User.objects.filter(nickname='사용자 %d' % random.randint(1, 10))[0]
    sido_name = random.choice(sido_list)
    area = Sigungu.objects.filter(name='%s%d' % (sido_name, random.randint(1, 5)))[0]
    r1 = random.randint(0, len(field_list)-1)
    r2 = random.randint(0, len(field_list)-1)
    while r1 == r2:
        r2 = random.randint(0, len(field_list)-1)
    post = Post(user=user, area=area, field='%s,%s' % (field_list[r1], field_list[r2]), content='선거와 국민투표의 공정한 관리 및 정당에 관한 사무를 처리하기 위하여 선거관리위원회를 둔다. 국가는 농수산물의 수급균형과 유통구조의 개선에 노력하여 가격안정을 도모함으로써 농·어민의 이익을 보호한다.\n대통령은 제3항과 제4항의 사유를 지체없이 공포하여야 한다. 근로조건의 기준은 인간의 존엄성을 보장하도록 법률로 정한다.')
    post.save()
    print(post)
    for i in range(10):
        user = User.objects.filter(nickname='사용자 %d' % random.randint(1, 10))[0]
        content = '댓글 달고 갑니당 :3'
        comment = Comment(post=post, user=user, content=content)
        comment.save()

print('end')
