from alcloud.feature.txt_feature import extract_bow, extract_cv, extract_doc2vec

data = [
         'This is the first document.',
         'This is the second second document.',
         'And the third one.',
         'Is this the first document?',
         ]

print(extract_doc2vec(data).shape)
print(extract_bow(data).shape)
print(extract_cv(data).shape)

data = [
    u'用户登录后，可以选择创建标注项目或参与已有的标注项目。对于创建项目，',
    u'用户需要定义项目的各个选项，包括数据类型，标注类型，查询策略等等。并上传数据',
    u'（或特征矩阵）至服务器。待服务器提取完特征，并开始返回样本后，',
    u'用户即可在客户端标注数据并提交。项目创建者可以随时修改项目的某些设置',
         ]

print(extract_doc2vec(data).shape)
print(extract_bow(data).shape)
print(extract_cv(data).shape)
