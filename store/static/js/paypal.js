window.paypal
    .Buttons({
        style: {
            shape: "rect",
            layout: "vertical",
            color: "gold",
            label: "paypal",
            tagline: false, 
            height: 45
        },
        createOrder: async function() {
            
        },
    }).render("#paypal-button-container");
