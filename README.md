# Web-based File Uploading App

![App Screenshot](screenshot.png)

Welcome to the **Web-based File Uploading App**! This application allows you to seamlessly upload files to an **Amazon Simple Storage Service (S3)** bucket and conveniently share the download link via email using **Amazon Simple Email Service (SES)**. The app is built with **Flask**, powered by the **boto3** library for AWS integration, and deployed on an **Amazon Elastic Compute Cloud (EC2)** instance.

## Features

- **User-Friendly Interface**: Easily upload files through the web interface.
- **Secure Storage**: Uploaded files are stored in a dedicated **Amazon S3** bucket.
- **Email Notifications**: Send email notifications with download links using **Amazon SES**.
- **Real-Time Deployment**: The app is hosted on an **Amazon EC2** instance.
- **Compatibility**: Supports a wide range of file types and sizes.

## Experience the App

Experience the app by visiting the live deployment: [**Web-based File Uploading App**](http://3.95.34.76/)

**Please Note**: The **Amazon SES** configuration is currently in a sandbox environment, which supports only pre-verified email addresses, including "subhojeetchowdhury98@gmail.com". If you wish to use other email addresses for testing, please contact us, and we will verify them for you.

## Installation and Usage

To run the app locally on your computer, follow these steps:

1. Ensure you have Python installed on your PC.

2. Clone the repository and navigate to the project directory:

   ```bash
   git clone <my-repo-link>
   cd file-uploader
   pip install flask boto3

 
3. Set up your AWS credentials and configure Amazon S3 and Amazon SES in the aws_credentials.py

  ```bash
  python app.py

4. Access the app through your web browser at http://localhost:5000/

## Acknowledgements
This app is made possible by the remarkable services and tools provided by Amazon Web Services.
