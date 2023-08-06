from flask import Flask, render_template, request
from botocore.exceptions import ClientError
import boto3
import aws_credentials

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('uploadForm.html')


@app.route('/upload', methods=['POST'])
def upload():
    emails = request.form.get('emails')
    file = request.files['fileInput']

    s3_client = boto3.client('s3', aws_access_key_id=aws_credentials.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=aws_credentials.AWS_SECRET_ACCESS_KEY, region_name=aws_credentials.AWS_REGION)

    # Upload the file to S3
    s3_key = f"uploads/{file.filename}"
    s3_client.upload_fileobj(file, aws_credentials.S3_BUCKET_NAME, s3_key)

    # save file name to dynamodb for billing purpose
    saveFilenameToDynamodb(file.filename)

    # Generate the download link
    downloadLink = f"https://{aws_credentials.S3_BUCKET_NAME}.s3.{aws_credentials.AWS_REGION}.amazonaws.com/{s3_key}"

    recipientEmails = emails.split(',')
    sendEmail(recipientEmails, downloadLink)

    return render_template('success.html')

def saveFilenameToDynamodb(filename):
    dynamodb_client = boto3.client('dynamodb', aws_access_key_id=aws_credentials.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=aws_credentials.AWS_SECRET_ACCESS_KEY, region_name=aws_credentials.AWS_REGION)
    response = dynamodb_client.put_item(
        TableName=aws_credentials.DYNAMODB_TABLE_NAME,
        Item={
            'fileName': {'S': filename}
        }
    )
    print("Filename saved to DynamoDB:", response)



def sendEmail(recipientEmails, downloadLink):
    SENDER = "papasanis.pegasian@gmail.com"

    SUBJECT = "Download link for uploaded file"

    # The HTML body of the email.
    HTML = """
        <html>
        <head></head>
        <body>
            <h4>Here is the download link</h4>
            <p>
                <a href="{downloadLink}">Click here to download</a>
            </p>
        </body>
        </html>
        """
    BODY_HTML = HTML.format(downloadLink=downloadLink)

    CHARSET = "UTF-8"

    client = boto3.client('ses', aws_access_key_id=aws_credentials.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=aws_credentials.AWS_SECRET_ACCESS_KEY, region_name=aws_credentials.AWS_REGION)

    try:

        response = client.send_email(
            Destination={
                'ToAddresses': recipientEmails,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


if __name__ == '__main__':
    app.run(debug=True)
