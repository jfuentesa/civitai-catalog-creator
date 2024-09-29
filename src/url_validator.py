import urllib.parse

class ValidatorInterface:
    def validate(self, url: str) -> bool:
        raise NotImplementedError("Implementa el método 'validate'")
    
    def sanitize(self, url: str) -> str:
        raise NotImplementedError("Implementa el método 'sanitize'")

class UrlValidator(ValidatorInterface):
    # Validate the URL
    def validate(self, url: str) -> bool:
        if not url:
            return False
        
        parsed_url = urllib.parse.urlparse(url)
        
        return all([parsed_url.scheme, parsed_url.netloc])

    # Sanitize the URL
    def sanitize(self, url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        
        if not parsed_url.scheme:
            url = "http://" + url
        
        parsed_url = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment)
        )

