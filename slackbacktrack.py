from slackclient import SlackClient
import time

# define our archive function
def archive(messages, channel, slack):
    """
    Archives the provided messages into an HTML file, formatting them correctly,
    which is then posted to slack into the #archives channel.

    Args:
        messages: A list of messages to archive.
        channel: A specific channel within the Slack team.
        slack: Passing through our slack variable.
    """
    # Append each message's text to a string.
    output = ""
    for message in messages:
        output += message.text

    # Submit string to slack.
    slack.api_call("files.upload", content=output, filetype="html", filename="test.html", title="test", channels="archives")



# define our main function
def main():
    """
    Sets up the application.
    """

    # setup slack API token and create a client.
    api_token = "foo"
    slack = SlackClient(api_token)

    # create a connection with Slack.
    slack.rtm_connect()

    # create a list of messages.
    messages = []

    # loop inside this forever.
    while True:
        # read the events that slack has sent us.
        events = slack.rtm_read()

        for event in events:

            # Wanna make sure the event type is correct, we should probably also
            # record message edits and deletes too.
            if event['type']  == "message":

            # if the number of messages is below 10,000 store it,
            # if the number of messages is above 10,000, archive the file.
                if len(messages) < 10:
                    # append the event to our messages list.
                    messages.append(event)

                else:
                    # write to file and post to archives channel
                    archive(messages)

        # wait one second.
        time.sleep(1)



# Fancy way of running our program, which now begins here.
if __name__ == "__main__":
    main()
