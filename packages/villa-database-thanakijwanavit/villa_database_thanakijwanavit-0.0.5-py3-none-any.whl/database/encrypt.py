import boto3, json

class EncryptorClient:
  def __init__(self, user=None, pw=None, region='ap-southeast-1'):
    self.lambda_ = boto3.client('lambda',
                      aws_access_key_id = user,
                      aws_secret_access_key = pw,
                      region_name = region )
  def invoke(self, functionName, payload):
    response = self.lambda_.invoke(
      FunctionName = functionName ,
      InvocationType= 'RequestResponse',
      LogType = 'Tail',
      Payload = json.dumps(payload).encode()
    )
    if 'Payload' in response.keys():
      responsePayload = json.loads(response.get('Payload').read())
      return responsePayload
    return response
  def test(self, payload = {'test': 'test'},
           functionName = 'villa-wallet-dev-WalletEncryptors-C2MXDS23RI2D-test' ):
    return self.invoke(functionName, payload)
  def encrypt(self, payload = {},
              functionName = 'villa-wallet-dev-WalletEncryptors-C2MXDS23RI2D-encryptor'):
    return self.invoke(functionName, payload)
  def decrypt(self, payload = {},
              functionName = 'villa-wallet-dev-WalletEncryptors-C2MXDS23RI2D-decryptor'):
    return self.invoke(functionName, payload)
  def hash(self, payload = {},
              functionName = 'villa-wallet-dev-WalletEncryptors-C2MXDS23RI2D-phonehasher'):
    return self.invoke(functionName, payload)
  def setDefault(self, payload = {},
              functionName = 'villa-wallet-dev-WalletEncryptors-C2MXDS23RI2D-set-default'):
    return self.invoke(functionName, payload)

