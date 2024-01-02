# Videor

An open source low-level API to allow you to transcode videos and generate subtitles, thumbnails, and video segments. Built on top of the **ffmpeg**(https://github.com/FFmpeg/FFmpeg) and **OpenAI Whisper model**(https://huggingface.co/openai/whisper-medium), it is designed to be a simple and easy to use Asynchronous API wrapper over well maintained and optimised utilties that you can quickly setup and hit the ground running in no time!

### Setting up the project
Note: Project setup and scripts are tested on Unix environments. You may need to change the setup.sh to make it run on other environemnts
1) Git clone the project to your local
   ```
   git clone https://github.com/tanmaymunjal/Videor.git 
   cd Videor
   ```
 2) Setup a virtual environment and activate into it
    ```
    python -m venv env
    source env/bin/activate
    ```
3)  Install all python requirements and setup install the Videor module
    ```
    pip install -r requirements.txt
    python setup.py install
    ```
4) Setup ffmpeg dependency
   ```
   ./setup.sh
   ```
5) Create a api_auth.json in API folder. Something like this, customise this to your own
   secret key and hashed password
    ```
    {
    "secret_key":"123",
    "auth_config":{
        "tanmaymunjal": {
            "username": "tanmaymunjal",
            "full_name": "Tanmay Munjal",
            "email": "tanmaymunjal64@gmail.com",
            "hashed_password": "123",
            "disabled": false
        }
    }}
    ```
6) Get the API running!
   ```
   cd API
   python api.py
   ```
   
  And there you go, the project should now be up and running in your local!
 
