from polls.models import *
from polls.post   import post_maker as pm
from datetime     import datetime   as dt
def create_subject_data():
    subject(name='net' , last_num=3, done_num=2).save()
    subject(name='db'  , last_num=3, done_num=2).save()
    subject(name='data', last_num=3, done_num=2).save()
    subject(name='sys' , last_num=3, done_num=2).save()

    subject(name='os'     , last_num=3, done_num=2).save()
    subject(name='sec'    , last_num=3, done_num=2).save()
    subject(name='ai'     , last_num=3, done_num=2).save()
    subject(name='graphic', last_num=3, done_num=2).save()
    # subject.objects.create(..)도 가능
    print("======data-insertion succeed")
def create_lecture_data():
    lecture('net','1-1',True,True,True).save()
    lecture('net','1-2',True,True,True).save()
    lecture('net','2-1',True,True,True).save()
    lecture('net','2-2',True,True,True).save()
def create_Post_test_data():
    for i in range(0,13):
        Post_test(title="this is "+str(i),pub_date=dt.now(),body=pm.getPost() ).save()
    print("Lecture data Insertion succeed!!")
def update_Post_test_data():
    for row in Post_test.objects.filter(id__gt=10):
        row.body = pm.getArticle()
        row.save()
        print("{} : title {} \n ".format(row.id,row.title)+"-"*10+"\n content : {}".format(row.body))
    print("*********updating done ********")
# if __name__ == "__main__" :
    # create_lecture_data()