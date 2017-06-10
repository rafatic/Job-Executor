# Job-Executor
Client-Server platform allowing on-demand complex tasks execution

This platform is based on a message queue architecture, the client can ask the execution of a problem and how he wants to divide it.
The server downloads the appropriate source code from a CDN and executes in order to send a partial result to the Client.
The client then reassembles the partial results and deducts the final result from it.

Right now, the client is a desktop GUI made with pika, in the future, it is plan to create a web application allowing more flexibility.
The purpose of this job execution platform will be to execute Genetic algorithms divided between different sites.
In general, it will be thought to resolve small to medium NP problems.
