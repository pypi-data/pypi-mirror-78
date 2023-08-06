import os
zCDJn=Exception
from localstack.utils.common import short_uid
from localstack.utils.aws import aws_stack
from localstack.dashboard import infra as dashboard_infra
from localstack_ext.bootstrap.aws_models import RDSDatabase,RDSCluster
get_graph_orig=dashboard_infra.get_graph
def get_resources(fetch_func):
 try:
  result=[]
  fetch_func(result)
  return result
 except zCDJn:
  pass
 return[]
def get_rds_databases(name_filter,pool,env):
 def fetch_func(result):
  client=aws_stack.connect_to_service('rds')
  dbs=client.describe_db_instances()
  for inst in dbs['DBInstances']:
   obj=RDSDatabase(id=inst['DBInstanceArn'])
   result.append(obj)
 return get_resources(fetch_func)
def get_rds_clusters(name_filter,pool,env):
 def fetch_func(result):
  client=aws_stack.connect_to_service('rds')
  clusters=client.describe_db_clusters()
  for cluster in clusters['DBClusters']:
   obj=RDSCluster(id=cluster['DBClusterArn'])
   result.append(obj)
 return get_resources(fetch_func)
def get_graph(*args,**kwargs):
 os.environ['AWS_ACCESS_KEY_ID']=os.environ.get('AWS_ACCESS_KEY_ID')or 'foobar'
 os.environ['AWS_SECRET_ACCESS_KEY']=os.environ.get('AWS_SECRET_ACCESS_KEY')or 'foobar'
 result=get_graph_orig(*args,**kwargs)
 env=kwargs.get('env')
 name_filter=kwargs.get('name_filter')
 pool={}
 node_ids={}
 databases=get_rds_databases(name_filter,pool=pool,env=env)
 rds_clusters=get_rds_clusters(name_filter,pool=pool,env=env)
 for db in databases:
  uid=short_uid()
  node_ids[db.id]=uid
  result['nodes'].append({'id':uid,'arn':db.id,'name':db.name(),'type':'rds_db'})
 for cluster in rds_clusters:
  uid=short_uid()
  node_ids[cluster.id]=uid
  result['nodes'].append({'id':uid,'arn':cluster.id,'name':cluster.name(),'type':'rds_cluster'})
 return result
def patch_dashboard():
 dashboard_infra.get_graph=get_graph
# Created by pyminifier (https://github.com/liftoff/pyminifier)
