import base64
import requests

PAYPAL_CLIENT_ID = 'AQsnfM1xEYlatgz4VMEAHqeFRIna4SFtmbwXgfNOmU2CjAFjSEPsapN5kyTsYQlP_XIpOJ9dGBqnBCJN'
PAYPAL_CLIENT_SECRET = 'ECXAkeEZnolTBZTDtiPkqE-taRadcLJAcy9p5B9whL-_bxkAWQl-zc9IPKbwaO27rT8lOUdnhX4btXcl'
#base url es la url de prueba 
# Esta nos ayuara a simular los pagos de paypal
BASE_URL = 'https://api-m.sandbox.paypal.com'

def generateAccessToken():
    #Esto nos ayudara a las peticiones
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError("Error en las credenciales o no tienes las credenciales")
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode('utf-8')
    
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data = {"grant_type":"client_credentials"},
        headers = {"Authorization": f"Basic {auth}"}
    )
    ##Con este print veremos la respuesta en la terminal de que hemos accedido a las funciones y procesos de comprar y pagar
    print(response.json())
    data = response.json()
    return data['access_token']


def crearOrden(carro_productos):
    print(carro_productos)
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
                        "value": "1"
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

'''
import express from "express";
import "dotenv/config";
import {
    ApiError,
    CheckoutPaymentIntent,
    Client,
    Environment,
    LogLevel,
    OrdersController,
    PaymentsController,
} from "@paypal/paypal-server-sdk";
import bodyParser from "body-parser";

const app = express();
app.use(bodyParser.json());

const {
    PAYPAL_CLIENT_ID,
    PAYPAL_CLIENT_SECRET,
    PORT = 8080,
} = process.env;

const client = new Client({
    clientCredentialsAuthCredentials: {
        oAuthClientId: PAYPAL_CLIENT_ID,
        oAuthClientSecret: PAYPAL_CLIENT_SECRET,
    },
    timeout: 0,
    environment: Environment.Sandbox,
    logging: {
        logLevel: LogLevel.Info,
        logRequest: { logBody: true },
        logResponse: { logHeaders: true },
    },
}); 
const ordersController = new OrdersController(client);
const paymentsController = new PaymentsController(client);

/**
 * Create an order to start the transaction.
 * @see https://developer.paypal.com/docs/api/orders/v2/#orders_create
 */
const createOrder = async (cart) => {
    const collect = {
        body: {
            intent: "CAPTURE",
            purchaseUnits: [
                {
                    amount: {
                        currencyCode: "USD",
                        value: "100",
                    },
                },
            ],
        },
        prefer: "return=minimal",
    }; 

    try {
        const { body, ...httpResponse } = await ordersController.ordersCreate(
            collect
        );
        // Get more response info...
        // const { statusCode, headers } = httpResponse;
        return {
            jsonResponse: JSON.parse(body),
            httpStatusCode: httpResponse.statusCode,
        };
    } catch (error) {
        if (error instanceof ApiError) {
            // const { statusCode, headers } = error;
            throw new Error(error.message);
        }
    }
};

// createOrder route
app.post("/api/orders", async (req, res) => {
    try {
        // use the cart information passed from the front-end to calculate the order amount detals
        const { cart } = req.body;
        const { jsonResponse, httpStatusCode } = await createOrder(cart);
        res.status(httpStatusCode).json(jsonResponse);
    } catch (error) {
        console.error("Failed to create order:", error);
        res.status(500).json({ error: "Failed to create order." });
    }
});



/**
 * Capture payment for the created order to complete the transaction.
 * @see https://developer.paypal.com/docs/api/orders/v2/#orders_capture
 */
const captureOrder = async (orderID) => {
    const collect = {
        id: orderID,
        prefer: "return=minimal",
    };

    try {
        const { body, ...httpResponse } = await ordersController.ordersCapture(
            collect
        );
        // Get more response info...
        // const { statusCode, headers } = httpResponse;
        return {
            jsonResponse: JSON.parse(body),
            httpStatusCode: httpResponse.statusCode,
        };
    } catch (error) {
        if (error instanceof ApiError) {
            // const { statusCode, headers } = error;
            throw new Error(error.message);
        }
    }
};

// captureOrder route
app.post("/api/orders/:orderID/capture", async (req, res) => {
    try {
        const { orderID } = req.params;
        const { jsonResponse, httpStatusCode } = await captureOrder(orderID);
        res.status(httpStatusCode).json(jsonResponse);
    } catch (error) {
        console.error("Failed to create order:", error);
        res.status(500).json({ error: "Failed to capture order." });
    }
});


app.listen(PORT, () => {
    console.log(`Node server listening at http://localhost:${PORT}/`);
}); 

'''