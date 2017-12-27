# jmw_math561_project

There are two sets of files here.

simulate_stream.py allows a user developing an application to process the complete transactions as they are generated for streaming. No access to sockets is required, just some content files to read from: wedge_transactions_*

stream_generator.py and stream_processor.py are a server client pair. stream_generator.py binds to a socket and listens for a connection. stream_processor.py opens a socket and requests transactions from the generator embedded in stream_generator.py; stream_processor.py then reduces the full transaction data to a subset and then writes the a JSON file with the compiled selected transactions. The wedge_transactions_* files will work with stream_generator.py if you adjust input_path in the script to their location.

************
Full write-up from class
************

# Stream Generation and Processing

Network sockets are a common method for moving data around. In principle, sockets are a system resource that provides a landing point for a connection from a second socket. Connections between sockets use ports, communication endpoints that are always associated with an IP address, which is a unique numerical identifier for a computer on a network. Therefore, for two computers to communicate across a network, each requires an IP address with an available port, e.g. 192.168.100.101:12000 (where the element before the colon is the IP address and the element following the colon is the port), as well as applications that access the ports using sockets.

Python provides a sockets library that can be used to incorporate sockets in an application. In this implementation, sockets are used to move data about transactions from a dataset of 90 million transactions conducted at the Wedge Coop in Minneapolis from a generator to a processor. The generator is analogous to a cash register in this scenario as it is the repository of transaction files and the processor is analogous to a monitoring system that one or more cash registers can transmit transactions to for consolidation among generator nodes as well as reduction and analysis of the data.

The generator acts as the server in the server-client relationship that characterizes a socket connection because the generator binds to a port at its IP address and listens for incoming connections. When a client, in this case the processor, connects to the socket listening at the port and IP address of the generator, a channel between the two applications is opened and data can flow across it. At a point designated in the logic of the application, the socket is closed; nothing of the connection persists on the client (processor) and the server (generator) reverts to listening.

In this case, the data that flows across the socket connection is a transaction record from the Wedge Coop dataset. The transactions are stored in text files in an Amazon Web Services (AWS) S3 bucket that is mounted on an Ubuntu Linux AWS EC2 instance. Transactions are extracted from the text files using a generator function, get_data(), which creates an iterator that can be called as long as there is source material to feed the next iteration. The server application calls get_data() to create the trans_generator object. When an incoming socket connection is established by a connecting client (also an EC2 instance in this case), a call on the trans_generator object yields a transaction string that can be pushed through the socket to the client for processing.

To illustrate the possibilities of having data traverse a network and arrive this way, the client processor includes logic designed to monitor the flow of produce transactions. On arrival of the transaction data at the client processor through the socket connection, the string received is decoded, split into fields and evaluated for relevance to the task of monitoring produce transactions. If the department field of the transaction indicates that the transaction involves produce, the UPC, description, quantity, scale weight and amount spent on the item are stored in a dictionary, either as a new entry or by totaling the transaction with prior transactions involving the same UPC. After a batch of transactions is processed, the processor application writes the reduced results to a JSON file. Such a file could be parsed by any number of applications to generate reports, visualizations and other useful information.

All materials for the application, including a prototype generator function for that allows development for processing the stream without relying on sockets and some transaction files for fodder, are posted at https://github.com/techxorcist/jmw_math561_project
