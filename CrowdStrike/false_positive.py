from g_functions import CLIENTS, get_auth, get_ldts

if __name__ == "__main__":
    for client in CLIENTS:
        falcon = get_auth(client)
        auth = falcon.authenticate()

        if auth:
            filter_query = "(behaviors.filename:'Projeto1.exe') + (status:'new')"
            id_list = get_ldts(falcon, filter_query)

            BODY = {
                "assigned_to_uuid": "f7302597-19c1-4ece-a6d6-3a2e221052d5",
                "comment": "new",
                "ids": id_list,
                "status": "ignored"
            }
            response = falcon.command("UpdateDetectsByIdsV2", body=BODY)

            print(response)