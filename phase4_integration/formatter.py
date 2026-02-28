import json
from datetime import datetime
from typing import Dict, Any, Optional

class ResponseFormatter:
    @staticmethod
    def format_joke_response(joke_data: Dict[str, Any], source: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Formats the joke and its metadata into a standardized JSON response.
        """
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "joke": {
                "text": joke_data.get("text"),
                "length_class": joke_data.get("length_class"),
                "lameness_level": joke_data.get("lameness_level")
            },
            "meta": {
                "source": source,
                "character_count": len(joke_data.get("text", "")),
                "additional": metadata or {}
            }
        }
        return json.dumps(response, indent=2)

    @staticmethod
    def format_error_response(message: str, error_type: str = "system_error") -> str:
        """
        Formats error messages into a standardized JSON response.
        """
        response = {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": {
                "type": error_type,
                "message": message
            }
        }
        return json.dumps(response, indent=2)
