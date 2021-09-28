from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC9cf22489c5a70b9d7f2f3eac43d43ff6"
# Your Auth Token from twilio.com/console
auth_token = "988ef53515797d7c53dfa595bb6a15f6"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+237677123206",
    from_="+18302614953",
    body="Hello from Python!")

print(message.sid)
