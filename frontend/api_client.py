import requests
import streamlit as st
from typing import Optional, Dict, Any

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def _handle_response(self, response: requests.Response) -> Any:
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_detail = response.json().get("detail", str(e))
            except:
                # If response is not JSON (e.g. 500 HTML or text), use text
                error_detail = f"{response.status_code} {response.text[:200]}"
            
            st.error(f"API Error: {error_detail}")
            return None
        except Exception as e:
            st.error(f"Request Error: {str(e)}")
            return None

    def get(self, endpoint: str, params: Optional[Dict] = None):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            return None

    def post(self, endpoint: str, data: Dict):
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            return None

    def put(self, endpoint: str, data: Optional[Dict] = None):
        try:
            response = requests.put(f"{self.base_url}/{endpoint}", json=data)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            return None

    def delete(self, endpoint: str):
        try:
            response = requests.delete(f"{self.base_url}/{endpoint}")
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")
            return None

api = APIClient()
