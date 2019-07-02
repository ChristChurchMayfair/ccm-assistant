# Christ Church Mayfair Amazon Alexa Skill

[![Travis Build status](https://travis-ci.org/ChristChurchMayfair/ccm-alexa-skill.svg?branch=master)](https://travis-ci.org/ChristChurchMayfair/ccm-alexa-skill)

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
Add rows to [this Google Sheet](https://docs.google.com/spreadsheets/d/1DXPesctGzPii73a-DtqgdJ0f73MLi5qNYC3fSUrBzyM/edit?usp=sharing).

### Running and testing locally:
- Install dependencies by running `pip install -r src/requirements.txt`
- Add these environment variables:
  - `PYTHONPATH` - the file path of the `src/` directory
- Make the file, `src/alexa_secrets.py`, containing API keys and the like. Copy across the content from
  `src/alexa_secrets.py.template` and either get your own keys or email mauriceyap@hotmail.co.uk
