
###Installation Guide
1. `git clone https://github.com/Ronald-C/Clubin-.git`
2. [Stormpath](https://stormpath.com/) for user management
  *  Create a Stormpath application & Download `apiKey.properties` to **security/**
  *  Export `STORMPATH_APPLICATION_HREF` environmental variable 
3. Configure MySQL authorization in **security/config.json**
4. Resolve Python dependencies `sudo pip install -r requirements.txt`
5. Run `python router.py`
