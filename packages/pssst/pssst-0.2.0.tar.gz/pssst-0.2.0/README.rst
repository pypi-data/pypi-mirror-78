PSSST: Packet Security for Stateless Server Transactions
========================================================

.. note::
    Complete API documentation can be found at ReadTheDocs_.

This module implements the PSSST protocol and provides a very simple interface for client and server endpoints.
PSSST is designed to provide a light weight way for clients to securely communicate with servers.

Using the `pssst` library is very simple. A client is represented by an instance of the `PSSSTClient` class
which is instantiated with the server's *public* key and optionally specifies the client's *private* key and the
cipher suite. A server is represented by an instance of the `PSSSTServer` class which is instantiated with
the server's *private* key and optionally specifies the cipher suite. Each of these classes offer only one method.

The `PSSSTClient` class provides the `pack_request()` method; this takes the request message as its sole argument
and returns a tuple of the encrypted and packed packet and a function that can be used to unpack the reply to that
packet.

The `PSSSTServer` class provides the `unpack_request()` method; this takes an encrypted request packet as its sole
argument and returns a tuple containing the decrypted request message, the authenticated client public key (or
`None` if client authentication is not used) and a function that can be used to pack the reply message into an
encrypted packet. Thus a minimal example of a transaction is as follows:

.. code-block:: python

    client = pssst.PSSSTClient(server_public_key)
    server = pssst.PSSSTServer(server_private_key)

    request_message = b"The Magic Words are Squeamish Ossifrage"

    # Pack the message with the client and unpack it with the server
    request_packet, client_reply_handler = client.pack_request(request_message)
    received_request, client_auth_key, server_reply_handler = server.unpack_request(request_packet)

    # Echo the request back from the server to the client
    reply_packet = server_reply_handler(received_request)
    received_reply = client_reply_handler(reply_packet)
   
.. _ReadTheDocs: https://pssst.readthedocs.io/en/latest/
