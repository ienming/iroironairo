import os
from pymongo import MongoClient
from get_database import get_database

db = get_database('exchange_japan')
collection = db.photos

# # 定義要刪除的數據的條件，這裡以 ['name'] 欄位為例
# name_to_delete = 'IMG_7290'  # 替換為您要刪除的名稱

# # 使用 delete_one 方法刪除符合條件的數據
# result = collection.delete_one({'name': name_to_delete})

# 指定要刪除的 'name' 值列表
# names_to_delete = ['John', 'Alice', 'Bob']  # 替換為要刪除的名稱列表
names_to_delete = ['IMG_7304',
'IMG_7339',
'IMG_7341',
'IMG_7350',
'IMG_7352',
'IMG_7354',
'IMG_7360',
'IMG_7364',
'IMG_7381',
'IMG_7402',
'IMG_7403',
'IMG_7444',
'IMG_7459',
'IMG_7537',
'IMG_7577',
'IMG_7558',
'IMG_7591',
'IMG_7593',
'IMG_7578',
'IMG_7597',
'IMG_7620',
'IMG_7622',
'IMG_7623',
'IMG_7626',
'IMG_7644',
'IMG_7778',
'IMG_7779',
'IMG_7824',
'IMG_7842',
'IMG_7882',
'IMG_7884',
'IMG_7964',
'IMG_7967',
'IMG_7981',
'IMG_7982',
'IMG_7983',
'IMG_7986',
'IMG_8019',
'IMG_8021',
'IMG_8023',
'IMG_8050',
'IMG_8067',
'IMG_394BFA3A-F10B-4D98-B2D8-2118B80DB7AD',
'IMG_8102',
'IMG_8106',
'IMG_8108',
'IMG_8175',
'IMG_8196',
'IMG_8239',
'IMG_8243',
'IMG_8254',
'IMG_8261',
'IMG_8271',
'IMG_8275',
'IMG_8282',
'IMG_8289',
'IMG_8292',
'IMG_8302',
'IMG_8318',
'IMG_8319',
'IMG_8326',
'IMG_8333',
'IMG_8336',
'IMG_8339',
'IMG_8345',
'IMG_8347',
'IMG_8350',
'IMG_8357',
'IMG_8358',
'IMG_8360',
'IMG_8363',
'IMG_8405',
'IMG_8407',
'IMG_0413D353-6ACE-4415-B64D-0A17DECAFDFE',
'IMG_8452',
'IMG_8455',
'IMG_8470',
'IMG_8471',
'IMG_8476',
'IMG_8478',
'IMG_8482',
'IMG_8486',
'IMG_8487',
'IMG_8488',
'IMG_8490',
'IMG_8492',
'IMG_8502',
'IMG_8503',
'IMG_8504',
'IMG_8516',
'IMG_8551',
'IMG_8571',
'IMG_48F447FD-F75D-4058-B9FE-47C51A5227DB',
'IMG_8858',
'IMG_8842',
'IMG_8864',
'IMG_8871',
'IMG_8876',
'IMG_8922',
'IMG_8925',
'IMG_9004',
'IMG_9012',
'IMG_9013',
'IMG_9014',
'IMG_9016',
'IMG_9020',
'IMG_9037',
'IMG_9043',
'IMG_9085',
'IMG_9089',
'IMG_9114',
'IMG_9120',
'IMG_9134',
'IMG_9136',
'IMG_9139',
'IMG_9141',
'IMG_9145',
'IMG_9173',
'IMG_9174',
'IMG_9181',
'IMG_9184',
'IMG_9196',
'IMG_9199',
'IMG_9217',
'IMG_9219',
'IMG_9225',
'IMG_9271',
'IMG_9279',
'IMG_9288',
'IMG_9292',
'IMG_9302',
'IMG_9335',
'IMG_9360',
'IMG_9373',
'IMG_9456',
'IMG_9461',
'IMG_9470',
'IMG_9471',
'IMG_9475',
'IMG_9489',
'IMG_9498',
'IMG_9502',
'IMG_9505',
'IMG_9524',
'IMG_9531',
'IMG_9581',
'IMG_9586',
'IMG_9602',
'IMG_9616',
'IMG_9617',
'IMG_9631',
'IMG_9656',
'IMG_9658',
'IMG_9667',
'IMG_9669',
'IMG_9672',
'IMG_9675',
'IMG_9738',
'IMG_9743',
'IMG_9751',
'IMG_9761',
'IMG_9764',
'IMG_9767',
'IMG_9775',
'IMG_9776',
'IMG_9787',
'IMG_9788',
'IMG_9789',
'IMG_9790',
'IMG_9794',
'IMG_9795',
'IMG_9803',
'IMG_9804',
'IMG_9805',
'IMG_9843',
'IMG_9845',
'IMG_9847',
'IMG_9850',
'IMG_9851',
'IMG_9853',
'IMG_9854',
'IMG_9857',
'IMG_9860',
'IMG_9869',
'IMG_9871',
'IMG_9872',
'IMG_9874',
'IMG_9879',
'IMG_9880',
'IMG_9881',
'IMG_9892',
'IMG_9898',
'IMG_9902',
'IMG_9903',
'IMG_9909',
'IMG_9917',
'IMG_9929',
'IMG_9943',
'IMG_9950',
'IMG_9951',
'IMG_9952',
'IMG_9953',
'IMG_9954',
'IMG_9956',
'IMG_9957',
'IMG_9958',
'IMG_9996',
'IMG_0004',
'IMG_0013',
'IMG_0020',
'IMG_0025',
'IMG_0052',
'IMG_0055',
'IMG_0061',
'IMG_0073',
'IMG_0076',
'IMG_0082',
'IMG_0086',
'IMG_0093',
'IMG_0101',
'IMG_0102',
'IMG_0104',
'IMG_0105',
'IMG_0109',
'IMG_0110',
'IMG_0113',
'IMG_0115',
'IMG_0123',
'IMG_0133',
'IMG_0136',
'IMG_0137',
'IMG_0138',
'IMG_0139',
'IMG_0144',
'IMG_0147',
'IMG_0152',
'IMG_0176',
'IMG_0177',
'IMG_0178',
'IMG_0282',
'IMG_0308',
'IMG_0310',
'IMG_0312',
'IMG_0313',
'IMG_0320',
'IMG_0321',
'IMG_0322',
'IMG_0325',
'IMG_0334',
'IMG_0355',
'IMG_0368',
'IMG_0371',
'IMG_0375',
'IMG_0376',
'IMG_0380',
'IMG_0381',
'IMG_0382',
'IMG_0385',
'IMG_0386',
'IMG_0387',
'IMG_0393',
'IMG_0394',
'IMG_0438',
'IMG_0455',
'IMG_0461',
'IMG_0476',
'IMG_0529',
'IMG_0534',
'IMG_0546',
'IMG_0554',
'IMG_0558',
'IMG_0562',
'IMG_0564',
'IMG_0572',
'IMG_0576',
'IMG_0579',
'IMG_0593',
'IMG_0595',
'IMG_0596',
'IMG_0598',
'IMG_0602',
'IMG_0604',
'IMG_0605',
'IMG_0607',
'IMG_0611',
'IMG_0616',
'IMG_0619',
'IMG_0624',
'IMG_0680',
'IMG_0681',
'IMG_0688',
'IMG_0689',
'IMG_0691',
'IMG_0694',
'IMG_0696',
'IMG_0697',
'IMG_0700',
'IMG_0705',
'IMG_0710',
'IMG_0714',
'IMG_0715',
'IMG_0716',
'IMG_0718',
'IMG_0720',
'IMG_0722',
'IMG_0723',
'IMG_0737',
'IMG_0741',
'IMG_0742',
'IMG_0743',
'IMG_0744',
'IMG_0745',
'IMG_0746',
'IMG_0747',
'IMG_0748',
'IMG_0749',
'IMG_0750',
'IMG_0751',
'IMG_0752',
'IMG_0753',
'IMG_0757',
'IMG_0759',
'IMG_0760',
'IMG_0761',
'IMG_0763',
'IMG_0766',
'IMG_0769',
'IMG_0772',
'IMG_0774',
'IMG_0775',
'IMG_0778',
'IMG_0779',
'IMG_0780',
'IMG_0811',
'IMG_0812',
'IMG_0818',
'IMG_0821',
'IMG_0822',
'IMG_0829',
'IMG_0841',
'IMG_0846',
'IMG_0850',
'IMG_0853',
'IMG_0854',
'IMG_0855',
'IMG_0864',
'IMG_0865',
'IMG_0867',
'IMG_0869',
'IMG_0978',
'IMG_0892',
'IMG_0923',
'IMG_0938',
'IMG_0950',
'IMG_0952',
'IMG_0953',
'IMG_0958',
'IMG_0964',
'IMG_0975',
'IMG_0939',
'IMG_0962',
'IMG_0963',
'IMG_0986',
'IMG_0993',
'IMG_0994',
'IMG_0995',
'IMG_0996',
'IMG_1001',
'IMG_1002',
'IMG_1017',
'IMG_1018',
'IMG_1019',
'IMG_1020',
'IMG_1025',
'IMG_1033',
'IMG_1040',
'IMG_1041',
'IMG_1052',
'IMG_1054',
'IMG_1058',
'IMG_1059',
'IMG_1060',
'IMG_1063',
'IMG_1067',
'IMG_1077',
'IMG_1086',
'IMG_1071',
'IMG_1091',
'IMG_1119',
'IMG_1097',
'IMG_1098',
'IMG_1101',
'IMG_1104',
'IMG_1116',
'IMG_1144',
'IMG_1145',
'IMG_1143',
'IMG_1133',
'IMG_1147',
'IMG_1155',
'IMG_1157',
'IMG_1160',
'IMG_1159',
'IMG_1167',
'IMG_1217',
'IMG_1218',
'IMG_1189',
'IMG_1220',
'IMG_1224',
'IMG_1227',
'IMG_1228',
'IMG_1240',
'IMG_1243',
'IMG_1244',
'IMG_1252',
'IMG_1232',
'IMG_1249',
'IMG_1262',
'IMG_1266',
'IMG_1264',
'IMG_1271',
'IMG_1299',
'IMG_1305',
'IMG_1307',
'IMG_1317',
'IMG_1320',
'IMG_1324',
'IMG_1316',
'IMG_1328',
'IMG_1331',
'IMG_1340',
'IMG_1327',
'IMG_1350',
'IMG_1360',
'IMG_1370',
'IMG_1373',
'IMG_1368',
'IMG_1369']


# 使用 delete_many 方法刪除符合條件的文檔（'name' 值在列表中的文檔）
result = collection.delete_many({'name': {'$in': names_to_delete}})

# 打印刪除的文檔數量
print(f"Deleted {result.deleted_count} documents with names: {', '.join(names_to_delete)}")