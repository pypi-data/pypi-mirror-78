from localstack.utils.aws import aws_models
kfMcg=super
kfMcG=None
kfMcH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  kfMcg(LambdaLayer,self).__init__(arn)
  self.cwd=kfMcG
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,kfMcH,env=kfMcG):
  kfMcg(RDSDatabase,self).__init__(kfMcH,env=env)
 def name(self):
  return self.kfMcH.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,kfMcH,env=kfMcG):
  kfMcg(RDSCluster,self).__init__(kfMcH,env=env)
 def name(self):
  return self.kfMcH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
