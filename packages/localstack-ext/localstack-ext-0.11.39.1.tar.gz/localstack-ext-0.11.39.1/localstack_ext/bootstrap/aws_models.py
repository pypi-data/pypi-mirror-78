from localstack.utils.aws import aws_models
gqYbi=super
gqYbt=None
gqYbM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gqYbi(LambdaLayer,self).__init__(arn)
  self.cwd=gqYbt
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,gqYbM,env=gqYbt):
  gqYbi(RDSDatabase,self).__init__(gqYbM,env=env)
 def name(self):
  return self.gqYbM.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,gqYbM,env=gqYbt):
  gqYbi(RDSCluster,self).__init__(gqYbM,env=env)
 def name(self):
  return self.gqYbM.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
