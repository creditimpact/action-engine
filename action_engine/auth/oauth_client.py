class OAuthClient:
    """Basic OAuth client stub for initiating and completing authorization."""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    async def initiate_authorization(self, scope: str) -> str:
        """Simulate starting an OAuth authorization flow and return an auth URL."""
        # In a real implementation this would generate the provider's auth URL
        # including client_id, scope, redirect_uri and possibly state parameter.
        return f"https://auth.example.com/authorize?client_id={self.client_id}&scope={scope}&redirect_uri={self.redirect_uri}"

    async def fetch_token(self, authorization_response: str) -> dict:
        """Simulate exchanging the authorization response for an access token."""
        # Actual implementation would exchange the provided authorization code
        # with the provider's token endpoint. Here we simply return a dummy token.
        return {
            "access_token": "dummy-access-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "authorization_response": authorization_response,
        }

