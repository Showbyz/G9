"""
Vistas públicas para cuando no se identifica un tenant.
"""
import sys
from django.shortcuts import render, redirect
from django.http import HttpResponse


def public_index(request):
    """
    Vista pública para la raíz cuando no se identifica un tenant.
    Redirige al panel de administración global.
    """
    import sys
    sys.stdout.write('[PUBLIC INDEX] Vista ejecutada\n')
    sys.stdout.flush()
    
    # Devolver una respuesta simple con un link al panel global
    return HttpResponse("""
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/global/login/">
        <title>Portal de Autoatención</title>
    </head>
    <body>
        <h1>Redirigiendo...</h1>
        <p>Si no eres redirigido automáticamente, <a href="/global/login/">haz click aquí</a>.</p>
    </body>
    </html>
    """, status=302, headers={'Location': '/global/login/'})


def public_welcome(request):
    """
    Vista de bienvenida pública.
    """
    return HttpResponse("""
    <html>
    <head>
        <title>Portal de Autoatención</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            a {
                display: inline-block;
                padding: 15px 30px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 10px;
            }
            a:hover {
                background: #f0f0f0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Portal de Autoatención</h1>
            <p>Bienvenido al sistema de gestión de ayudantías</p>
            <a href="/global/login/">Acceder al Panel de Administración</a>
        </div>
    </body>
    </html>
    """)

