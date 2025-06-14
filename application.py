#!/usr/bin/env python3
"""
AWS Elastic Beanstalk Application Entry Point
Spirit of the Immortals Ltd - Smart Shopping Platform
"""

from secure_aws_shopping import app

# AWS Elastic Beanstalk looks for 'application' variable
application = app

if __name__ == "__main__":
    # For local testing with uvicorn
    import uvicorn
    uvicorn.run(application, host='0.0.0.0', port=8000)
