#!/usr/bin/python
# -*- coding: utf-8 -*-

import pika
import sys
import signal
import time
import paramiko
import os
import subprocess
from jobRequest import jobRequest
from jobResult import jobResult
from jobErrorResult import jobErrorResult


def sigint_handler(signal, frame):
    connection.close()
    sys.exit(0)

# Connects to the remote server and downloads the file to execute
def serverConnection(request):

    dir = os.path.dirname(__file__)
    targetDir = os.path.join(dir, "scripts")
    # If the file to execute is not present locally
    if os.path.isfile(targetDir + "/"+ request.command) != True :
        try:
            # Creates and establishes the connexion to the server
            transport = paramiko.Transport(request.url, 22)
            transport.connect(username = request.login, password = request.password)
        # If the connexion failed, an error is raised and sent in the jobResult queue
        except paramiko.SSHException, sshError:
            print "Error - Failed to connect to the remote server : " + sshError.message
            error = jobErrorResult("SSH Error", str(sshError.args), sshError.message)

            transport.close()
            return error.toXML()
        

        sftp = paramiko.SFTPClient.from_transport(transport)
        
        try:
            # Download the file to execute
            # The file is stored in the "scripts" folder
            sftp.get( request.path + "/" + request.command, targetDir + "/" + request.command)
        except IOError, fileError:
            # If the connexion failed, an error is raised and sent in the jobResult queue
            print "Error - Failed to download the file : " + fileError.message
            error = jobErrorResult("File Error", str(fileError.args), fileError.message)
            sftp.close()
            transport.close()
            return error.toXML()
        sftp.close()
        transport.close()

    
    # Once the file is downloaded, it is executed
    try:
        #The arguments chain is split around spaces, allowing to tread them independently
        argsTab = request.args.split()
        
        # The file is executed
        programReturnValue = subprocess.check_output(["python", "scripts/" + request.command, argsTab[0], argsTab[1], argsTab[2]])
    
    except subprocess.CalledProcessError, e:
        # If the execution failed, an error is raised and is sent in the jobResult queue
        print "Execution error : " + e.output
        error = jobErrorResult("Execution Error", e.returncode, e.message)
        return error.toXML()
        
    # Once the execution is finished, the result is stored in a "JobResult" object
    outputTab = programReturnValue.split(":")
    result = jobResult(request.command + " " + request.args, outputTab[0], outputTab[1])

    print "Result : " + programReturnValue
    # The result is sent as an XML string
    return result.toXML()


# This callback is called whenever a job request is received
def callbackJobRequest(ch, method, properties, body):
    print(body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    request = jobRequest()
    request.XmlToObject(body)
    
    print(request.toString())
    # Calls the procedure that downloads the file to execute
    response = serveurConnection(request)
    channelJobResult.basic_publish(exchange='result_queue',
                          routing_key=request.sender,
                          body=response)
    
    
    print("result sent")





def main():

    if len(sys.argv) < 4:
        print("Command usage :")
        print("     Serveur.py <rabbitMq server local IP> <user> <password> <port> (optionnal : default : 5672)")
        
        sys.exit()

    # Sets up the interruption signal
    signal.signal(signal.SIGINT, sigint_handler)

    global connection, channelJobResult
    credentials = pika.PlainCredentials(sys.argv[2], sys.argv[3])
    port = 5672
    # If a RabbitMq port has been defined in argument
    if len(sys.argv) == 5:
        port = int(sys.argv[4])

    # Creation and establishement of the job request queue connection
    try:
        parameters = pika.ConnectionParameters(sys.argv[1], port, '/', credentials)
        connection = pika.BlockingConnection(parameters)

    # If the connection has failed, an error is raised ans the application is stopped
    except pika.exceptions.ConnectionClosed, ConnectionError:
        print("Error while connection to the RabbitMq server")
        print(ConnectionError.message)
        sys.exit()
    # If the queue authentification has failed, an error is raised and the application is stopped
    except pika.exceptions.ProbableAuthenticationError, AuthError:
        print("Error while authenticating to the RabbitMq server")
        print(AuthError.message)
        sys.exit()

    # Creation and declaration of the job request channel
    channelJobRequest = connection.channel()

    channelJobRequest.queue_declare(queue='job_queue', durable=True)

    # Creation and declaration of the response channel
    channelJobResult = connection.channel()

    channelJobResult.exchange_declare(exchange='result_queue',
                                      type='direct')
    # The application indicates that it cannot receive more than one message at a time
    channelJobRequest.basic_qos(prefetch_count=1)

    channelJobRequest.basic_consume(callbackJobRequest,
                          queue='job_queue'
                          )

    print(' [*] Awaiting message, to exit, press CTRL+C')
    # Starts to consume messages in the job request queue
    channelJobRequest.start_consuming()
    
    



if __name__ == '__main__' :
    main()
