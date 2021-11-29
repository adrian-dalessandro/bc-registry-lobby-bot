# BC Lobbyist Registry Twitter Bot
The purpose of this tool is to scrape the first page of the BC lobbyist registry and then parse each logged lobbying event, convert the lobby event data into a string using the liquid markup parser, and 
then tweet the string to a specified twitter account. We will detail here the steps necessary for modifying the output of the bot. There are three files that you should be concerned with:
1. app.info.json
2. tweet.format.txt
3. filters.json
## Updating Twitter App Information
**Relevant File**: app.info.json  
Suppose that you want the twitter bot to send it's output to a new twitter account. You will need to collect 4 pieces of information and place them in the app.info.json file, which is formatted as such:
```json
{"API Key": "YOUR API KEY HERE", 
 "API Key Secret": "YOUR API KEY SECRET HERE", 
 "Access Token": "YOUR ACCESS TOKEN HERE", 
 "Access Token Secret": "YOUR ACCESS TOKEN SECRET HERE"}
```
Essentially, you are providing a set of access credentials to the bot that tells twitter it has permission to perform actions on your account (e.g. sending tweets). To get these access credentials, you n
eed to [sign up for a Twitter developer account](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). After you have registered for an account and receive
d your notification of approval, you must now create an app. Follow these steps:
1. Visit the [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)
2. Click "+ Add App"
3. When choosing an App Environment, select "Production" and click "next"
4. Give your app a unique name and click "next"
5. Copy the API Key and paste it into the app.info.json file where specified (must be surrounded by quotation marks)
6. Copy the API Key Secret and paste it into the app.info.json file where specified ( ... quotation marks)
7. **IMPORTANT**: For security purposes, these API keys are only ever provided to you one time. New keys can be generated, but you will only ever receive those keys once.
8. Click "App Settings", and click "Edit" under app permissions. Change permissions from "Read" to "Read and Write". This allows the app with the provided API keys to also write tweets. Click "Save".
9. At the top of the page (just next to the "Settings" tab), click "Keys and Tokens". We now need to generate your access token.
10. Click "Generate" next to "Access Token and Secret".
11. Copy the Access Token and paste it into the app.info.json file where specified (... quotation marks)
12. Copy the Access Token Secret and paste it into the app.info.json file where specified (... quotation marks)
13. You now have all of the credentials necessary!
## Updating the Tweet Format
**Relevant File**: tweet.format.txt  
This tool uses the liquid templating language to combine the formatting string in tweet.format.txt with the json formatted content parsed from the lobbyist registry website. The parsed results have the f
ollowing format:
```json
{"organization": "...",
 "officials": [{"name": "...",
   "title": "...",
   "affiliation": "..."},
   "..."],
 "lobbying_date": "...",
 "posted_date": "...",
 "lobbyists": "...",
 "lobby_activity_id": "..."}
 ```
And each key can be referrenced using liquid under these names. For example, if you wanted to iterate over all of the officials, you might try:
```liquid
Update: {%for person in officials%}{{person.name}} ({{person.title}}),{%endfor%} met with lobbyists from {{organization}}
```
# Filtering Organization Names
**Relevant File**: filters.json  
Not all entries in the BC lobbyist registry may be relevant. This tool will only include organization names provided in _filters.json_. All entries must be included in a commo-delimited list with quotati
on marks.
