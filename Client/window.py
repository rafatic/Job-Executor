#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from jobRequest import jobRequest
from jobResult import jobResult
from jobErrorResult import jobErrorResult
import os
import pika
import xml.etree.ElementTree as ET
import socket



class Window(Frame):

    # Initialization of the window and its elements
    # Adds an on click listener on "Send"
    def __init__(self, parent):


        if len(sys.argv) < 4:
            print("Command usage :")
            print("     Client.py <RabbitMq IP address> <user> <password> <port> (optionnal : default 5672)")
            sys.exit()
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.centerWindow()
        self.initUI()

        # The pid is used to name the queue where the client will wait for the job results
        pid = os.getpid()

      
        
        credentials = pika.PlainCredentials(sys.argv[2], sys.argv[3])
        port = 5672
        # If a RabbitMq port has been defined in argument
        if len(sys.argv) == 5:
            port = int(sys.argv[4])
        # Creation and establishement of the job result message queue connection
        try:
            parameters = pika.ConnectionParameters(sys.argv[1], port, '/', credentials)
            self.connection = pika.BlockingConnection(parameters)
            # Creation and declaration of the job request channel
            self.channelJobRequest = self.connection.channel()
        # If the connection has failed, an error is raised an the application is stopped
        except pika.exceptions.ConnectionClosed, ConnectionError:
            print("Error while connecting to the RabbitMq server")
            print(ConnectionError.message)
            sys.exit()
        # If the athentification to the queue has failed, an error is raised and the application is stopped
        except pika.exceptions.ProbableAuthenticationError, AuthError:
            print("RabbitMq authentification error")
            print(AuthError.message)
            sys.exit()


        # job request queue declaration
        self.channelJobRequest.queue_declare(queue='job_queue', durable=True)

        
        # Creation and declaration of the job result channel
        self.channelJobResult = self.connection.channel()
        self.channelJobResult.exchange_declare(exchange='result_queue',
                                                    type='direct')

        self.result = self.channelJobResult.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

        # The result channel is tied to the corresponding queue
        # The reception quque is named after the application's pid and the local IP address
        self.channelJobResult.queue_bind(exchange='result_queue',
                               queue=self.queue_name,
                               routing_key=str(pid) + socket.gethostbyname(socket.gethostname()))

        

    # Function allowing to center the window in the screen
    def centerWindow(self):
      
        w = 800
        h = 600

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def initUI(self):

        # Global variables declaration
        # Those variables are associatet to the different window's inputs
        global txtNomCommande, txtArguments, txtDatasource, txtPath, txtResultat, txtLogin, txtPassword, txtNbExec

        self.parent.title("Client")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)


        # Associate the button to the window close event
        quitButton = Button(self, text="Quitter",
            command=self.quit)
        quitButton.place(x=700, y=550)

        Label(self, text="Fill the informations relative to the program you want to execute : ").grid(row=0, column=0, sticky=W)
        
        # Frame creation
        formFrame = Frame(self)
        formFrame.pack()
        formFrame.place(x=10, y=30)

        

        Label(formFrame, text="Command : ").grid(row=1, column=0, sticky=W)
        txtNomCommande = StringVar()
        txtNomCommande = Entry(formFrame, textvariable=txtNomCommande)
        txtNomCommande.grid(row=1, column=1, sticky=W)

        Label(formFrame, text="Arguments : ").grid(row=2, column=0, sticky=W)
        txtArguments = StringVar()
        txtArguments = Entry(formFrame, textvariable=txtArguments)
        txtArguments.grid(row=2, column=1, sticky=W)

       
        Label(formFrame, text="Datasource : ").grid(row=3, column=0, sticky=W)
        txtDatasource = StringVar()
        txtDatasource = Entry(formFrame, textvariable=txtDatasource)
        txtDatasource.grid(row=3, column=1, sticky=W)


        Label(formFrame, text="Path : ").grid(row=4, column=0, sticky=W)
        txtPath = StringVar()
        txtPath = Entry(formFrame, textvariable=txtPath)
        txtPath.grid(row=4, column=1, sticky=W)

        Label(formFrame, text="Login : ").grid(row=5, column=0, sticky=W)
        txtLogin = StringVar()
        txtLogin = Entry(formFrame, textvariable=txtLogin)
        txtLogin.grid(row=5, column=1, sticky=W)

        Label(formFrame, text="Password : ").grid(row=6, column=0, sticky=W)
        txtPassword = StringVar()
        txtPassword = Entry(formFrame, textvariable=txtPassword, show="*")
        txtPassword.grid(row=6, column=1, sticky=W)

        Label(formFrame, text="Number of executions ").grid(row=7, column=0, sticky=W)
        txtNbExec = StringVar()
        txtNbExec = Entry(formFrame, textvariable=txtNbExec)
        txtNbExec.grid(row=7, column=1, sticky=W)

        
        submitJob = Button(formFrame, text="Send", command=self.sendJob).grid(row=8, column=0, sticky=W)


        resultFrame = Frame(self)
        resultFrame.pack()
        resultFrame.place(x=300, y=30)

        # MessageBox result
        txtResultat = Text (resultFrame)
        txtResultat.grid(row=0, column=0, sticky=W)

    # Window close procedure
    def quit(self):
        # If a connection has been opened, it is closed 
        if self.connection.is_open:
            self.connection.close()
        exit(0)

    # job request sending procedure
    # This procedure is called when the user clicks on "Send"
    def sendJob(self):
        txtResultat.delete(1.0, END)
        self.printResult("Execution in progress...")
 
        
        request = jobRequest(txtNomCommande.get(), txtArguments.get(), txtDatasource.get(), txtPath.get(), txtLogin.get(), txtPassword.get(), str(os.getpid()) + socket.gethostbyname(socket.gethostname()) )
        

        argTaille = request.args



        # ----------------------------------------------------------------------------------------------------------------------------------------------------
        # THIS PART IS MADE FOR THE N QUEEN PROBLEM AND NOTHING ELSE, IT WILL BE REMOVED IN THE FUTURE AS THE SOFTWARE WILL ALLOW THE EXECUTION OF ANY PROBLEM
        # ----------------------------------------------------------------------------------------------------------------------------------------------------


        # On définit le nombre de colonne que chaque executeur devra calculer en fonction du nombre total de colonnes et du nombre d'éxecutions demandées
        nbCol = int(argTaille) / int(txtNbExec.get())  
        # On définit si le nombre total de colonnes et le nombre d'exécutions sont entièrement divisibles
        remain = int(argTaille) % int(txtNbExec.get())  
        firstCol = 0
        lastCol = 0


        # Envoie de N requêtes où N = nombre d'éxecutions demandées    
        for i in range(0, int(txtNbExec.get())):
            publishStatus = False
            firstCol = lastCol
            lastCol += nbCol

            # Si le nombre total de colonnes et le nombre d'executions ne sont pas entièrement divisibles, on répartis le nombre restant de colonnes entre chaque execution
            # Exemple : nDames 7 sur 2 executions
            # 7 % 2 = 1
            # 7 / 2 = 3
            # Chaque exécution portera sur un intervalle de 3 colonnes.
            # Il restera une colonne à calculer.
            # Cette colonne est attribuée arbitrairement à une exécution
            if  remain != 0:
                lastCol += 1
                remain -= 1

           
            # Construction de la chaine d'argument
            # La chaine d'arguments est de la forme : 7 0 2 tel que :
            #   7 : taille du tableau
            #   0 : première colonne à calculer
            #   2 : dernière colonne à calculer
            request.args = argTaille + " " + str(firstCol) + " " + str(lastCol)

            # BlockingConnection.basic_publish retourne False si l'envoi ne s'est pas realisé
            publishStatus = self.channelJobRequest.basic_publish(exchange='',
                                            routing_key='job_queue',
                                            body=request.toXML(),
                                            properties=pika.BasicProperties(
                                            delivery_mode = 2,
                                            ))

            # Dans le cas ou l'envoi est un echec, on tente de renvoyer le message (BlockingConnection.basic_publish = false)
            # 3 essais sont reaslisé, si aucun ne fonctionne, la requete est abandonnée
            nbRetry = 0
            while publishStatus != True | nbRetry != 3:
                publishStatus = self.channelJobRequest.basic_publish(exchange='',
                                            routing_key='job_queue',
                                            body=request.toXML(),
                                            properties=pika.BasicProperties(
                                            delivery_mode = 2,
                                            ))
                nbRetry += 1

            if publishStatus == False & nbRetry == 3:
                self.printResult("Abandon de la requete : impossible de contacter le serveur RabbitMq")
                return
            

        print(" [x] Requetes envoyees")


        resultReceived = 0
        # Création des objets JobResult déstinés à recevoir les résultats d'exécution
        lstResults = [ jobResult() for i in range(0, int(txtNbExec.get()))]
        jobHasFailed = False
        
        # Tant que tous les résultats n'ont pas étés recus
        while resultReceived < int(txtNbExec.get()):
            method_frame, header_frame, body = self.channelJobResult.basic_get(queue = self.queue_name)
            # Si le message recu contient bien des données
            if body != None:
                # Lorsque le premier résultat est recu, on efface la zone de texte de résultat
                if resultReceived == 0:
                    txtResultat.delete(1.0, END)

                # Si le message contient le résultat d'une exécution
                if ET.fromstring(body).tag == '{http://www.w3.org/2001/XMLSchema-instance}jobResult':
                    # le résultat est enregistré et est ensuite affiché
                    lstResults[resultReceived].XmlToObject(body)
                    print lstResults[resultReceived].toString()
                    self.printResult(lstResults[resultReceived].toString())
                # Si le message correspond à une erreur
                elif ET.fromstring(body).tag == '{http://www.w3.org/2001/XMLSchema-instance}error':
                    # L'erreur est enregistrée puis affichée
                    jobError = jobErrorResult()
                    jobError.XmlToObject(body)
                    self.printResult(jobError.toString())
                    jobHasFailed = True
                    
                resultReceived += 1

        self.printResult("---------------------\n")

        if jobHasFailed == False:
            # L'objet finalResult fait la synthèse de l'ensemble des résultats obtenus
            finalResult = jobResult()
            finalResult.execTime = 0
            finalResult.result = 0
            finalResult.command = lstResults[0].command[:-4]
            for i in range(0, len(lstResults)):
                finalResult.execTime += lstResults[i].execTime
                finalResult.result += lstResults[i].result
            # Le résultat final est affiché
            print finalResult.toString()
            
            self.printResult("Résultat total : \n")
            self.printResult(finalResult.toString())
        else:
            self.printResult("L'exécution d'un ou plusieurs site a echouée")
 

    def printResult(self, string):
        txtResultat.insert(INSERT, string)


   