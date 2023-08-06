import grpc
import binascii
import requests
import os

_SIGNATURE_HEADER_KEY = 'x-signature'
_auth_host = 'https://auth.pravah.io'
_auth_port = '5000'

class AuthGateway(grpc.AuthMetadataPlugin):

    def set_auth(self, auth_token, client_id=''):
        #self.client_id = client_id
        self.auth_token = auth_token

    def __call__(self, context, callback):
        """Implements authentication by passing metadata to a callback.
        Implementations of this method must not block.
        Args:
          context: An AuthMetadataContext providing information on the RPC that
            the plugin is being called to authenticate.
          callback: An AuthMetadataPluginCallback to be invoked either
            synchronously or asynchronously.
        """
        # Example AuthMetadataContext object:
        # AuthMetadataContext(
        #     service_url=u'https://localhost:50051/helloworld.Greeter',
        #     method_name=u'SayHello')
        
        #real_path = os.path.join(os.path.dirname(__file__), 'chain.pravah.io.crt')
        res = requests.post(_auth_host + ':' + _auth_port + '/token', json={
	        "authentication_token": self.auth_token
        }, timeout=15, verify=True)

        resJSON = res.json()
        err = resJSON.get('error', None)
        if err != None:
          raise Exception('Err in obtaining access token: ' + err)
          return
        
        cnt = resJSON.get('token', None)
        if cnt == None:
          raise Exception('No token found.')
          return

        callback(((_SIGNATURE_HEADER_KEY, cnt),), None)