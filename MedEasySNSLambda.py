import boto3
import json


topic_arn = "arn:aws:sns:us-east-1:053631896887:SnsPatientDetails"
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
    #print(event)
    for record in event['Records']:
        #Fetching patient name from event
        name = record['dynamodb']['NewImage']['PatientName']['S']
        #Fetching message
        msg = record['dynamodb']['NewImage']
        msgf = json.dumps(msg,indent=12)
        
    #message = "Hi "+ str(name) +","+"\n\nWe are processing your Prescription to your selected Pharmacy.\n\nPlease find your Prescription below:\n"+ "\nPatientId : "+ str(id)+"\nPatientName : "+ str(name)+"\nDisease : "+ str(disease)+"\nDate : "+ str(date)+"\nFollowUpDate : "+ str(fdate)+"\nDoctor : "+ str(doctor)+"\nClinicName : "+ str(clinic)+"\nMedicines : "+ str(medicines)+"\nDosage : "+ str(dosage)+"\nAdvice : "+ str(advice)+"\nPharmacy : "+ str(pharmacy)+"\n\nSoon you will receive a follow up email from your respective Pharmacy.\n\nThankyou,\nMedEasy"
    message = "Hi " + str(name) + ","+"\n\nWe are processing your Prescription to your selected Pharmacy.\n\nPlease find your Prescription below:\n" + str(msgf) +"\n\nSoon you will receive a follow up email from your respective Pharmacy.\n\nThankyou,\nMedEasy"
    subject = "MEDEASY"
    SNSResult = send_sns(message, subject)
    if SNSResult :
        print("Notification Sent..") 
        return SNSResult
    else:
        return False