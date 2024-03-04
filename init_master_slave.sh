{
  "swagger": "2.0",
  "info": {
    "version": "1.0.0",
    "title": "Flask API",
    "description": "API endpoints for managing users and content"
  },
  "basePath": "/",
  "paths": {
    "/users": {
      "get": {
        "summary": "Get all users",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      },
      "post": {
        "summary": "Create a new user",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      },
      "put": {
        "summary": "Update an existing user",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      }
    },
    "/content": {
      "get": {
        "summary": "Get all content",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      },
      "post": {
        "summary": "Create new content",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      },
      "put": {
        "summary": "Update content",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      }
    },
    "/mongo-data": {
      "post": {
        "summary": "Create new data in MongoDB",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      }
    },
    "/two-phase-commit": {
      "post": {
        "summary": "Execute two-phase commit logic",
        "responses": {
          "200": {
            "description": "Success"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      }
    }
  }
}
