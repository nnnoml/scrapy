# -*- coding: utf-8 -*-
import pymysql

def conn():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='guanji',
        charset='utf8'
        )
    return db.cursor()

comp_name = ['hp001','hp002','hp003','112','113']

cnn = [];
all_comp_list = [];
db = conn()
db.execute("select bp.id,bp.comp_id from board_list as b INNER join board_port_list as bp on b.id = bp.board_id where b.bar_id = 1 and bp.comp_id <> ''")
info = db.fetchall()
for vo in info:
    bbc = [];
    bbc.append(vo[0])
    bbc.append(vo[1])
    for voo in vo[1].split(','):
        all_comp_list.append(voo)
    cnn.append(bbc)


print(all_comp_list)
print(cnn)

no_find_list = []
for comp in all_comp_list:
    if comp not in comp_name:
        no_find_list.append(comp)

print(no_find_list)

for comp in no_find_list:
    status = False
    for vo in cnn:
        if comp in vo[1].split(','):
            print(vo[0],vo[1])
        # for voo in vo[1].split(','):
        #     if voo.find(comp) ==-1 :
        #         print(vo)
        #         status = True


#     status = False
#     for row in range(len(cnn)):
#         for voo in cnn[row][1].split(','):
#             if voo.find(comp) !=-1 :
#                 status = True
#                 break
#     if status == False:
#         print(comp)

    # if status:
    #     print(cnn[row][0],cnn[row][1])



