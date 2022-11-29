import boto3

class PatientData:

    def __init__(self):
        client = boto3.resource('dynamodb')
        self.table = client.Table('PatientDataTable')
        
    
    #To add the details to dynamodb table
    def  Add_data(self , event):
        response = self.table.put_item(
            Item={
                'id': event['id'],
                'PatientName': event['PatientName'],
                'Age': event['Age'],
                'Date': event['Date'],
                'Temp(deg)': event['Temp(deg)'],
                'BP': event['BP'],
                'Doctor': event['Doctor'],
                'Address':event['Address'],
                'Disease': event['Disease'],
                'MedicineName': event['MedicineName'],
                'Dosage': event['Dosage'],
                'Advice': event['Advice'],
                'FollowUpDate': event['FollowUpDate'],
                'Pharmacy': event['Pharmacy']
                
            }
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': 'Record ' + event['id'] + ' added'
        }  
        
        
    #To read the details from dynamodb table    
    def  Read_data(self , event):
        response = self.table.get_item(
            Key={
                'id': event['id']
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return {
                'statusCode': '404',
                'body': 'Not found'
            }
    
    
    #To delete the details from dynamodb table        
    def  Delete_data(self , event):
        response = self.table.delete_item(
            Key={
                'id': event['id']
            }
        )

        return {
                'statusCode': '200',
                'body': 'Deleted the item with id :' + event['id']
            }
            
    #To update the details in dynamodb table        
    def  Update_data(self , event):
        response = self.table.update_item(
            Key={'id': event['id']},
            ExpressionAttributeNames={
                '#A': 'PatientName',
                '#B': 'Age',
                '#C': 'Date',
                '#D': 'Temp(deg)',
                '#E': 'BP',
                '#F': 'Doctor',
                '#G': 'Address',
                '#H': 'Disease',
                '#I': 'MedicineName',
                '#J': 'Dosage',
                '#K': 'Advice',
                '#L': 'FollowUpDate',
                '#M': 'Pharmacy'
            },
            ExpressionAttributeValues={
                ':a': event['PatientName'],
                ':b': event['Age'],
                ':c': event['Date'],
                ':d': event['Temp(deg)'],
                ':e': event['BP'],
                ':f': event['Doctor'],
                ':g': event['Address'],
                ':h': event['Disease'],
                ':i': event['MedicineName'],
                ':j': event['Dosage'],
                ':k': event['Advice'],
                ':l': event['FollowUpDate'],
                ':m': event['Pharmacy']
                
            },
            UpdateExpression='SET #A = :a, #B = :b, #C = :c, #D = :d,  #E = :e, #F = :f, #G = :g, #H = :h, #I = :i, #J = :j, #K = :k, #L = :l, #M = :m',
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': 'Record ' + event['id'] + ' updated'
        }
        
def lambda_handler(event, context):
    if event:
        patient_Object =  PatientData()
        if event['task']  == "create":
            create_result =  patient_Object.Add_data(event['data'])
            return create_result
            
        elif event['task']  == "read":
            read_result =  patient_Object.Read_data(event['data'])
            return read_result
            
        elif event['task']  == "delete":
            delete_result =  patient_Object.Delete_data(event['data'])
            return delete_result
            
        elif event['task']  == "update":
            update_result =  patient_Object.Update_data(event['data'])
            return update_result
            
        else :
            return {
                    'statusCode': '404',
                    'body': 'Not found'
            }
    