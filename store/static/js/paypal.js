window.paypal
    .Buttons({
        style: {
            shape: "rect",
            layout: "vertical",
            color: "gold",
            label: "paypal",
            tagline: false, // Quita la descripción extra si quieres un estilo más minimalista
            height: 45 // Ajusta la altura del botón si deseas hacerlos más grandes o pequeños
        },
        createOrder: async function() {
            // Código para manejar el pedido y la integración con el servidor
            // Este ya lo tienes bien estructurado
        },
    }).render("#paypal-button-container");
