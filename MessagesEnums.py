class MessagesEnums:

    request_messages = ("GET_PLT","GET_GNR", "GET_CMS", "SEN_FIL", "CON_CLS")

    response_messages = ( "SEN_PLT", "SEN_GNR","SEN_CMS", "RCV_FIL", "ERR_MSG")

    #Definitions

    #GET_PLT - Get playlist from server
    #GET_GNR - Get All genres
    #GET_CMS - Get chat mesages from the server
    #SEN_FIL - Send File to the server
    #CON_CLS - Close connection to the server

    #SEN_PLT - Send Playlist to the client
    #SEN_GNR - Send list of genres to the client
    #SEN_CMS - Send Chat Messages to the client
    #RCV_FIL - Received File from Client
    #ERR_MSG - Error Message
