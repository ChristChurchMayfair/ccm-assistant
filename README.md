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
Add rows to `src/resources/data/passages.csv` **making sure that the dates are in `YYYY-MM-DD`
format.** If you're using Excel, select the date column, *Format > Cells* and select the
`YYYY-MM-DD` format.

### Running and testing locally:
- Install dependencies by running `pip install -r src/requirements.txt`
- Add these environment variables:
  - `LAMBDA_TASK_ROOT` - the file path of the `src/` directory
  - `PYTHONPATH` - the file path of the `src/` directory
- Make the file, `src/secrets.py`, containing API keys and the like. Copy across the content from
  `src/secrets.py.template` and either get your own keys or email mauriceyap@hotmail.co.uk
  
### TODO:
- [] Add tests
- [] Migrate bible passage database from static csv file to Google Sheets
- [] Investigate licencing for using NIV bible
- [] Improve handling of errors in general
- [] Add instructions for forking and using for other churches, including deployment etc.
