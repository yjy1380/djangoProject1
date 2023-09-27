from django.shortcuts import render, redirect
from django.http import JsonResponse
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher
import json
from app01 import models
from app01.utils.pagination import Pagination

# Create your views here.
def home(request):
    return render(request, 'home.html')


def browse(request):
    # 去数据库中获取所有的列表
    #  [对象,对象,对象]

    # 处理接收到的值
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["miRNAname__contains"] = search_data

    queryset = models.miRNA.objects.filter(**data_dict).order_by("-PMID")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'browse.html', context)


def dieasenetwork(request):
    return render(request, 'dieasenetwork.html')


def sortDict(searchResult):
    target_data = []
    for item in searchResult:
        n1 = {}
        n1['cate'] = str(item['n1'].labels)
        n1['name'] = item['n1']['name']
        rel = {}
        rel['name'] = item['rel'].__class__.__name__
        n2 = {}
        n2['cate'] = str(item['n2'].labels)
        n2['name'] = item['n2']['name']
        target_data.append({
            'n1': n1,
            'rel': rel,
            'n2': n2
        })
    newdata = [{key: {key2: value.replace(': ', ':') for key2, value in sub_dict.items()} for key, sub_dict in
                dict_item.items()} for dict_item in target_data]
    return newdata

class neo4jconn:
    def __init__(self):
        # 在这里初始化你的对象
        self.graph = Graph("neo4j://localhost:7687", auth=("neo4j", "123789456yjy"))  # 连接neo4j图数据库


        # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        result = self.graph.run("MATCH (n1:person {name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # print(result[0][2].labels)
        # print(result[0][1].__class__.__name__)
        return result


    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        answer = self.graph.run(
            "MATCH (n1:person {name:\"" + entity + "\"})-[rel:" + relation + "]->(n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询 整个知识图谱体系
    def zhishitupu(self):
        answer = self.graph.run("MATCH (n1:person)- [rel] -> (n2) RETURN n1,rel,n2 ").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity1):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2:major {name:\"" + entity1 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1)- [rel] -> (n2:level {name:\"" + entity1 + "\"}) RETURN n1,rel,n2").data()
            if (len(answer) == 0):
                answer = self.graph.run(
                    "MATCH (n1)- [rel] -> (n2:univer {name:\"" + entity1 + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2+关系 [rel:" + relation + "]
    def findOtherEntities2(self, entity, relation):
        answer = self.graph.run("MATCH (n1)- [rel:" + relation + "] -> (n2:major {name:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1)- [rel:" + relation + "] -> (n2:level {name:\"" + entity + "\"}) RETURN n1,rel,n2").data()
            if (len(answer) == 0):
                answer = self.graph.run(
                    "MATCH (n1)- [rel:" + relation + "] -> (n2:univer {name:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        return answer

def mirtargetnetwork(request):
    ctx = {}
    searchResult = {}
    if (request.GET):
        db = neo4jconn()
        entity1 = request.GET['entity1_text']
        relation = request.GET['relation_name_text']
        entity2 = request.GET['entity2_text']
        # 若只输入entity1,则输出与entity1有直接关系的实体和关系
        if (len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
            searchResult = db.findRelationByEntity1(entity1)
            newdata=sortDict(searchResult)
            return render(request, 'mirtargetnetwork.html', {'searchResult': json.dumps(newdata, ensure_ascii=False)})
        # 若只输入entity2则,则输出与entity2有直接关系的实体和关系
        if (len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
            searchResult = db.findRelationByEntity2(entity2)
            newdata = sortDict(searchResult)
            return render(request, 'mirtargetnetwork.html', {'searchResult': json.dumps(newdata, ensure_ascii=False)})
        # 若输入entity1和relation，则输出与entity1具有relation关系的其他实体
        if (len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0):
            searchResult = db.findOtherEntities(entity1, relation)
            newdata=sortDict(searchResult)
            return render(request, 'mirtargetnetwork.html', {'searchResult': json.dumps(newdata, ensure_ascii=False)})
        # 若输入entity2和relation，则输出与entity2具有relation关系的其他实体
        if (len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0):
            searchResult = db.findOtherEntities2(entity2, relation)
            newdata=sortDict(searchResult)
            return render(request, 'mirtargetnetwork.html', {'searchResult': json.dumps(newdata, ensure_ascii=False)})
        # 全为空 则输出整个知识图谱
        if (len(entity1) == 0 and len(relation) == 0 and len(entity2) == 0):
            searchResult = db.zhishitupu()
            newdata=sortDict(searchResult)
            return render(request, 'mirtargetnetwork.html', {'searchResult': json.dumps(newdata, ensure_ascii=False)})
    return render(request, 'mirtargetnetwork.html',{'searchResult': json.dumps(searchResult, ensure_ascii=False)})



def download(request):
    return render(request, 'download.html')


def help(request):
    return render(request, 'help.html')




