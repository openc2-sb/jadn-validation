# from datetime import datetime


# class DateTime:
    
#     # Allow different formats?  See date.py
#     date_time: str = None
    
#     def __init__(self, date_time: any = None):
#         self.date_time = date_time
    
#     def validate(self):
#         if isinstance(self.date_time, str) and (not self.date_time.lstrip('-').isdigit()):
#             try:
#                 datetime.strptime(self.date_time, self.date_format)
#             except ValueError:
#                 raise ValueError(f"Incorrect date-time format.  Received {self.date_time}")
#         else:
#             try:
#                 datetime.fromtimestamp(int(self.date_time))
#             except ValueError:
#                 raise ValueError(f"Invalid timestamp value: {self.date_time}.")

from datetime import datetime

class DateTime:
    date_time: str = None

    def __init__(self, date_time: any = None, date_format: any = None):
        self.date_time = date_time

    # def validate(self):
    #     if isinstance(self.date_time, str):
    #         # Try RFC 3339/ISO 8601 format
    #         try:
    #             # Accept 'Z' for UTC by replacing with '+00:00'
    #             datetime.fromisoformat(self.date_time.replace("Z", "+00:00"))
    #         except Exception:
    #             raise ValueError(f"Incorrect date-time format. Received: {self.date_time}")
    #     else:
    #         try:
    #             # Accept int or float timestamp
    #             datetime.fromtimestamp(float(self.date_time))
    #         except Exception:
    #             raise ValueError(f"Invalid timestamp value: {self.date_time}.")
    
    def validate(self):
        """
        Validates the input as either an RFC 3339/ISO 8601 date-time string or an integer timestamp.
        Accepts:
          - Strings in RFC 3339/ISO 8601 format (e.g., '2023-08-13T16:07:54Z')
          - Integers or strings representing integers (e.g., 1751677200 or '1751677200')
        """
        if isinstance(self.date_time, str):
            # If it's a string of digits (possibly negative), treat as timestamp
            if self.date_time.lstrip('-').isdigit():
                try:
                    datetime.fromtimestamp(int(self.date_time))
                    return
                except Exception:
                    raise ValueError(f"Invalid timestamp value: {self.date_time}.")
            else:
                # Try RFC 3339/ISO 8601 format
                try:
                    # Accept 'Z' for UTC by replacing with '+00:00'
                    datetime.fromisoformat(self.date_time.replace("Z", "+00:00"))
                    return
                except Exception:
                    raise ValueError(f"Incorrect date-time format. Received: {self.date_time}")
        elif isinstance(self.date_time, int):
            try:
                datetime.fromtimestamp(self.date_time)
                return
            except Exception:
                raise ValueError(f"Invalid timestamp value: {self.date_time}.")
        else:
            raise ValueError(f"Unsupported type for date_time: {type(self.date_time)}")    