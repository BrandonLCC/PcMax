import base64
import requests

#Token del usuario ID de prueba (jhon)
PAYPAL_CLIENT_ID = 'AQsnfM1xEYlatgz4VMEAHqeFRIna4SFtmbwXgfNOmU2CjAFjSEPsapN5kyTsYQlP_XIpOJ9dGBqnBCJN'
#Token secreto (Contraseña del usuario de prueba)
PAYPAL_CLIENT_SECRET = 'ECXAkeEZnolTBZTDtiPkqE-taRadcLJAcy9p5B9whL-_bxkAWQl-zc9IPKbwaO27rT8lOUdnhX4btXcl'
#base url es la url de prueba 

# Esta nos ayuara a simular los pagos de paypal (Sin utizar)
BASE_URL = 'https://api-m.sandbox.paypal.com'

def generateAccessToken():
    #Esto nos ayudara a las peticiones: Si no hay usuario o erreores de credenciales
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError("Error en las credenciales o no tienes las credenciales")
    
    #Parte de la documentacion.
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode('utf-8')
    
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data = {"grant_type":"client_credentials"},
        headers = {"Authorization": f"Basic {auth}"}

    )

    #Debe retornar si o si en json
    data = response.json()
    return data['access_token']


def crearOrden(valorFinalCarro):
    try:
        access_token = generateAccessToken()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    #Monto y el formato de la moneda
                    "amount": {
                        "currency_code": "USD",
                        "value": str(valorFinalCarro)
                    }
                }
            ]
        }

        #Lo importante de los headers es los tokens de acceso
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()    

    except Exception as error:
        print("Error:", error)
