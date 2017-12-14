# jmw_math561_project

There are two sets of files here.

simulate_stream.py allows a user developing an application to process the complete transactions as they are generated for streaming. No access to sockets is required, just some content files to read from: wedge_transactions_*

stream_generator.py and stream_processor.py are a server client pair. stream_generator.py binds to a socket and listens for a connection. stream_processor.py opens a socket and requests transactions from the generator embedded in stream_generator.py; stream_processor.py then reduces the full transaction data to a subset and then writes the a JSON file with the compiled selected transactions. The wedge_transactions_* files will work with stream_generator.py if you adjust input_path in the script to their location.
