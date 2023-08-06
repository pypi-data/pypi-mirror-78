from localstack.utils.aws import aws_models
tacHN=super
tacHB=None
tacHL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tacHN(LambdaLayer,self).__init__(arn)
  self.cwd=tacHB
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,tacHL,env=tacHB):
  tacHN(RDSDatabase,self).__init__(tacHL,env=env)
 def name(self):
  return self.tacHL.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,tacHL,env=tacHB):
  tacHN(RDSCluster,self).__init__(tacHL,env=env)
 def name(self):
  return self.tacHL.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
