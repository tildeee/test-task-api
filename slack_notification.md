# Completing a Task Notification

## Goal

When a task becomes complete, a Slack bot should post and say so with the message:

```
Someone just completed the task Task Title! Congratulations!
```

## Structure

- Slackbot Setup Walkthrough
  - Skip this if you want to use my Slackbot token
  - Theoretically, I think the whole class could use one Slackbot token
  - I would recommend asking Roundtable groups to share a workspace
- Route Walkthrough

## Slackbot Setup Walkthrough

Goal is:

1. Create a Slackbot
1. Give the Slackbot the required permissions
1. Get it authorized in one workspace
1. Retrieve the bot token
1. Use the bot token in your Flask app/route

### Create a Slackbot

Go to https://api.slack.com/

Go to "Your Apps" or sign in. - Sign into the workspace that you want the Slackbot to live in - You can always go back to the "Your apps" page using the button on the top right

Make a new app. The app name doesn't matter, but if the students are each making one, adding their first name to it is a good requirement ("Simon's bot")

Making a new app should bring you to a new page.

### Add features and functionality

1. click permissions
1. Scroll down to bot token scopes. Add `chat:write` and `chat:write.public`
1. Scroll back up: "install to workspace" is enabled. click that button.
1. Brings you to the authorization page that says "hey hUMAN, ARE YOU GOOD WITH THIS?" check out the permissions (matches the bot scope). say yes.
1. After you say yes, it should list in "OAuth Tokens for your team" and "Bot User OAuth Access Token". That value is your bot token. Should always start with `xoxb`
1. Copy the token. Whenever you want to get back here, go to "Your apps" (top right), click your app, open "features and functionality", go to "OAuth & Permissions"

### Verify

1. Go to test https://api.slack.com/methods/chat.postMessage/test (if you click on the tab "Documentation", it will show you all the documentation)
1. Fill out the following params:
   - token: paste in your bot token
   - channel: put in the name of a channel like "general" (don't use general)
   - text: type a nice message for everyone to read
1. Hit Test Method button
1. Scroll down to see the response

- admire the URL + header it's giving you

### Verify AGAIN

1. open postman
1. make a new request
   - open new tab
   - change method to POST
   - use this as request URL `https://slack.com/api/chat.postMessage`
   - in "Params", fill the following values:
     - channel: "test"
     - text: "asdfsdf"
   - go to "Headers" and add this new key value pair
     - Authorization: "Bearer xoxb-150..."
     - NB: Instead of this, you COULD put in a param of token: token. It works. Better to do this method tho

## Route Walkthrough

You're probably starting with a route like this:

```python
@task_page.route('/tasks/<task_id>/complete', methods=['PATCH'])
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)

    if task.completed_at:
        task.completed_at = None
    else:
        task.completed_at = datetime.utcnow()

    db.session.commit()

    return {"task": build_dict_from_task(task)}
```

### Hint: `requests` to Make API Calls

`requests` is a module that will make our API calls. Here's how to use it:

- `import requests`

- `requests.post()` returns a Response object.

- `requests.post()` has one positional arg: the URL
    - Our URL for Slack is `https://slack.com/api/chat.postMessage`

- Set request body payload using the keyword argument `data`
    - We can send in a dictionary, which contains all the payload info (aka `"channel"` and `"text"`)

- Set request headers using the keyword argument `headers`
    - We can send in a dictionary, aka `"Authorization"` and `f"Bearer {os.environ.get()}`
    - `os.environ.get()` is how we get the env vars

- We can jsonify the Response object (that `post` gives back) with `.json()` on it


