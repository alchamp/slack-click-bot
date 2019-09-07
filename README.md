This slack bot will do some clicking and typing and then take a screenshot and post it in slack

# Create Slack Custom Bot
1. Go to this link https://my.slack.com/apps/A0F7YS25R-bots
2. Connect
3. Add Intergration
4. Copy API Token Some Where
6. Copy Bot Name
5. Scroll Down Save Integration

# Install Python and Slack Client
1. Install Python https://www.python.org/downloads/release/python-2716/
2. Install Slack Client `C:\Python27\Scripts\pip.exe install slackclient`
3. Install pyautogui `C:\Python27\Scripts\pip.exe install pyautogui`

# Update bot.config 
## Note For INSTRUCTIONS
`d_input` will be replaced with whatever comes after `snap` i.e. `@testbot snap xyz`

## Current Format
```
SLACK_BOT_TOKEN
SLACK_BOT_USER
INSTRUCTION
...
INSTRUCTION
```

## Example Config
```
xoxb-0000000-111111-123455566
testbot
click,1000,500
type,d_input
press,enter,a
press,enter
press,enter
type,words
```

### Valid Instructions Types
```"click,x,y" : x = left/right postion on screen , y = up/down position on screen ```<br>
```"type,text" : text = text that will be typed. ```<br>
```"press,a,b,c,..." : a,b,c will be pressed one after another```<br>

### Running Bot
#### Start Bot
1. In powershell or commandline run `C:\Python27\python.exe -u .\Main.py`
#### Use Bot
1. Go to slack channel 
2. @ your bot by name to invite your bot to the channel.
3. @BOTNAME snap xyz i.e. `@testbot snap xyz`
4. Wait for screenshot to be posted
#### Stop
`CTRL-C`