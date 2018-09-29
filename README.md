# Christ Church Mayfair Amazon Alexa Skill

![https://travis-ci.org/ChristChurchMayfair/ccm-alexa-skill](https://travis-ci.org/ChristChurchMayfair/ccm-alexa-skill.svg?branch=master)

AWS Lambda function for Christ Church Mayfair Assistant Alexa skill.

## Features:
- Gets the Bible passage reading for each service
  
  *Alexa, get me the reading for the morning service this Sunday from CCM?*
  
  ***It's Matthew chapter 17, verses 21 to 28 - would you like me to read it?***
  
- Plays recordings of past sermons

  *Alexa, ask CCM to play me the sermon at two weeks ago in the evening*
  
  ***Okay. [The sermon recording]***
  
- Tells you when the next event is

  *Alexa, when's the next event from CCM?*
  
  ***The next event is prayer meeting tomorrow evening at 6 in the evening***
  
## Contributing
### Adding bible passage readings for future sermons
Add rows to [this Google Sheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vQqiE5BF-VtKfaV9NtpwYqgT3Ijw5pRmfbg7mzIIMrV5huonrAYQPawIHzoqA-_fAsUgP4Bvcs6NgUk/pub?output=csv).

### Running and testing locally:
- Install dependencies by running `pip install -r src/requirements.txt`
- Add these environment variables:
  - `PYTHONPATH` - the file path of the `src/` directory
- Make the file, `src/secrets.py`, containing API keys and the like. Copy across the content from
  `src/secrets.py.template` and either get your own keys or email mauriceyap@hotmail.co.uk
