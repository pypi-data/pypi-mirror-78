import boto3, json

class DigioFunction:
    def __init__(self, stackName= 'villa-wallet-dev', user=None, pw=None, region='ap-southeast-1'):
        self.lambdaClient = boto3.client(
            'lambda',
            aws_access_key_id = user,
            aws_secret_access_key = pw ,
            region_name = region
          )
        self.stackName = stackName

    def invoke(self, functionName, data):
        response = self.lambdaClient.invoke(
            FunctionName = functionName,
            InvocationType = 'RequestResponse',
            Payload=json.dumps(data)
        )
        return json.loads(response['Payload'].read())

    def auth(self, data:dict):
        functionName = f'{self.stackName}-auth'
        return self.invoke(functionName = functionName, data=data)

    def angbao(self, data:dict):
        functionName = f'{self.stackName}-angbao'
        return self.invoke(functionName = functionName, data=data)

    def cancelQr(self, data:dict):
        functionName = f'{self.stackName}-cancel'
        return self.invoke(functionName = functionName, data=data)

    def redeem(self, data:dict):
        functionName = f'{self.stackName}-redeem'
        return self.invoke(functionName = functionName, data=data)

    def payment(self, data:dict):
        functionName = f'{self.stackName}-payment'
        return self.invoke(functionName = functionName, data=data)

    def topup(self, data:dict):
        functionName = f'{self.stackName}-topup'
        return self.invoke(functionName = functionName, data=data)

    def void(self, data:dict):
        functionName = f'{self.stackName}-void'
        return self.invoke(functionName = functionName, data=data)


