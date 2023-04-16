from supabase.client import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

class Supabase:
    """A proxy class with the sole purpose of instantiating the Supabase SDK. Requires a 
    """
    client = None
    supabase_url = None
    supabase_key = None

    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")

    def createClient(self):
        """Used to initalized the Supabase SDK (requires an internet connection always, hence
        is placed in its own function)
        """
        if self.client is None:
            missing_environment_varables = self.supabase_key is None or self.supabase_url is None  
            if not missing_environment_varables:
                self.client: Client = create_client(supabase_url=self.supabase_url, supabase_key=self.supabase_key)
            else:
                raise "Missing env vars (SUPABASE_KEY or SUPABASE_URL)"
        return self.client
