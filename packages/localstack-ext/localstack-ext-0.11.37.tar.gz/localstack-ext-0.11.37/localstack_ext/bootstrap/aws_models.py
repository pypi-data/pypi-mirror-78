from localstack.utils.aws import aws_models
AGkNC=super
AGkNJ=None
AGkNr=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AGkNC(LambdaLayer,self).__init__(arn)
  self.cwd=AGkNJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,AGkNr,env=AGkNJ):
  AGkNC(RDSDatabase,self).__init__(AGkNr,env=env)
 def name(self):
  return self.AGkNr.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,AGkNr,env=AGkNJ):
  AGkNC(RDSCluster,self).__init__(AGkNr,env=env)
 def name(self):
  return self.AGkNr.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
