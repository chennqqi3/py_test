# coding: utf-8

from util import db_util
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '192.168.5.241', 'port': 9200}])

query = db_util.get_query()

all_the_text = open('communication_search.json').read()

def query_demand():
    demand_list = list()
    query.Query("SELECT a.*, GROUP_CONCAT(DISTINCT b.label) AS keyword_label FROM capvision_fun.demands a LEFT JOIN capvision_fun.demand_labels b ON a.id = b.demand_id WHERE a.proj_id IS NOT NULL GROUP BY a.id ")
    for row in query.record:
        demand = dict(id=row['id'], demand=row['demand'], date=row['date'],proj_id=row['proj_id'], label=row['keyword_label'])

        demand_list.append(demand)
    print(demand_list)


def elastic_search_consultant(keyword):
    print es.get(index="qa_email", body=all_the_text, doc_type="email")
    pass


if __name__ == '__main__':
    # query_demand()
    print(all_the_text)
    elastic_search_consultant('CON')
