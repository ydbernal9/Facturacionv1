from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza el formulario HTML
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', fecha=fecha_actual)

@app.route('/generar_factura', methods=['POST'])
def generar_factura():
    # Obtener datos del formulario
    nombreCliente = request.form['nombreCliente']
    nitCliente = request.form['nitCliente']
    telefono = request.form['telefono']
    email = request.form['email']

    productos = [
        {'producto': request.form['producto1'], 'cantidad': int(request.form['cantidadProductos1'])},
        {'producto': request.form['producto2'], 'cantidad': int(request.form['cantidadProductos2'])},
    ]

    subtotal = 0
    total_iva = 0
    productos_procesados = []

    # Calcular el total
    for producto in productos:
        if producto['producto']:  # Verifica si el producto fue seleccionado
            precio_unitario, iva = map(float, producto['producto'].split('-'))
            total_con_iva =int(producto['cantidad'] * precio_unitario)
            iva_total = total_con_iva * (iva / 100)
            subtotal += (total_con_iva - iva_total)
            total_iva += iva_total

            productos_procesados.append({
                'nombre': "Pantalones" if precio_unitario == 119000 else "Camisas",
                'cantidad': producto['cantidad'],
                'precio_unitario': precio_unitario,
                'iva': iva,
                'precio_total': total_con_iva
            })

    valor_a_pagar = subtotal + total_iva

    # Renderiza la factura con los cálculos
    return render_template('factura.html', 
                           nombreCliente=nombreCliente, 
                           nitCliente=nitCliente, 
                           telefono=telefono, 
                           email=email, 
                           productos=productos_procesados, 
                           subtotal=int(subtotal), 
                           total_iva=int(total_iva), 
                           valor_a_pagar=int(valor_a_pagar), 
                           fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    app.run(debug=True)
