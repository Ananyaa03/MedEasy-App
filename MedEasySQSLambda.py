import json
import boto3

topic_arn = "topic_arn"
def send_sns(message, subject):
    try:
        client = boto3.client("sns")
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification send successfully..!!!")
            return True
    except Exception as e:
        print("Error occured while publish notifications and error is : ", e)
        return True

def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb')
    #table name
    table = dynamodb.Table('PharmacyDatabase')
    for record in event['Records']:
        h = json.loads(record['body'])
        #Fetching the message
        m = h['Message']
        #Converting message to string array
        msg = m.split()
        #Fetching the details using array indexes
        fname = msg[43]
        lname = msg[44]
        name = fname + ' '+ lname
        disease = msg[27]
        medicine1 = msg[97]
        medicine2 = msg[101]
        medicine3 = msg[105]
        Meds = medicine1 + ' ' +medicine2+' '+medicine3
        id = msg[128]
        #Adding the detils to dynamodb table
        response = table.put_item(
        Item={
            'id': id,
            'Patientname' : name,
            'Medicines': Meds,
            'Disease': disease
            }
        )
        print(response)
        
    message = "Hi " + str(name) + ","+"\n\nYour Medicines are available.\n\nYou can collect them anytime you want.\n\nThankyou for choosing us,\nPerfect Dose Pharmacy"
    subject = "PHARMACY"
    SNSResult = send_sns(message, subject)
    if SNSResult :
        print("Notification Sent..") 
        return SNSResult
    else:
        return False 
    return {
        'statusCode': 200,
        'body': json.dumps('Data stored Successfully!')
    }
