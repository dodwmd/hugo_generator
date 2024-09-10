class BlogGeneratorException(Exception):
    """Base exception for the blog generator."""
    pass

class APIError(BlogGeneratorException):
    """Raised when an API request fails."""
    pass

class ContentGenerationError(BlogGeneratorException):
    """Raised when content generation fails."""
    pass
