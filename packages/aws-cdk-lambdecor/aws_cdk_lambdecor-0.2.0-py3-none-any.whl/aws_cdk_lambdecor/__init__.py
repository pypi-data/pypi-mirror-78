import inspect
import json
import hashlib

from aws_cdk import core as cdk
from aws_cdk import aws_lambda as lamb
from aws_cdk import aws_s3 as s3
from aws_cdk import custom_resources as cr

class aws_lambda(object):

  def __init__(self, scope):
    self._scope = scope

  def __call__(self, func):

    def wrapper(*args, **kwargs):

      hashed = hashlib.md5(bytes(json.dumps(args) + json.dumps(kwargs), 'UTF-8'))
      hashi = hashed.hexdigest()[:9]
      function_name = func.__name__ + hashi

      remote = lamb.Function(self._scope, f'LambdaFunction-{function_name}',
        code=lamb.Code.from_inline(self._create_function_code(func)),
        runtime=lamb.Runtime.PYTHON_3_7,
        handler='index.handler',
        timeout=cdk.Duration.minutes(15),
        memory_size=256,
      )

      provider = cr.Provider(self._scope, f'CustomResourceProvider-{function_name}', on_event_handler=remote)

      # stack = cdk.Stack.of(self._scope)
      resource = cdk.CustomResource(self._scope, f'CustomResource-{function_name}',
        service_token=provider.service_token,
        properties={

          # avoid any CFN type conversion quirks by serializing
          # on output and deserializing on input
          'args': json.dumps(list(args)),
          'kwargs': json.dumps(dict(kwargs))
        })

      return resource.get_att_string('Value')

    return wrapper

  def _create_function_code(self, func):

    sanitized_function_code = '\n'.join(str(inspect.getsource(func)).splitlines()[1:])

    return f'''
import json
import urllib3

# this is the original native python function
{sanitized_function_code}

# this is the CFN handler
def handler(event, context):
  print(json.dumps(event))

  request_type = event['RequestType']
  props = event['ResourceProperties']

  if request_type == 'Delete':
    pass

  args_prop = props.get('args', '[]')
  kwargs_prop = props.get('kwargs', '{{}}')

  # deserialize on input since we serialize on output
  args = json.loads(args_prop)
  kwargs = json.loads(kwargs_prop)

  # invoke the original function with the original arguments.
  return_value = {func.__name__}(*args, **kwargs)

  return {{'Data': {{'Value': return_value}}}}

'''
