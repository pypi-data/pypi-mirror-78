from localstack.utils.aws import aws_models
DgrjN=super
DgrjU=None
Dgrjy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  DgrjN(LambdaLayer,self).__init__(arn)
  self.cwd=DgrjU
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,Dgrjy,env=DgrjU):
  DgrjN(RDSDatabase,self).__init__(Dgrjy,env=env)
 def name(self):
  return self.Dgrjy.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,Dgrjy,env=DgrjU):
  DgrjN(RDSCluster,self).__init__(Dgrjy,env=env)
 def name(self):
  return self.Dgrjy.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
