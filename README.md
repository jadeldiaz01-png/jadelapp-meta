# Jadel Pages API

Aplicación pública de Streamlit para presentar la información legal requerida por Meta Developers y preparar la revisión de permisos de Facebook Pages.

## Configuración de Meta Developers

- **Nombre para mostrar:** Jadel Pages API
- **Espacio de nombres:** vacío
- **Dominio de la aplicación:** `jadelapp-meta.streamlit.app`
- **Correo de contacto:** `darklife_jade@hotmail.com`
- **Política de privacidad:** `https://jadelapp-meta.streamlit.app/?view=privacy`
- **Condiciones del servicio:** `https://jadelapp-meta.streamlit.app/?view=terms`
- **Eliminación de datos:** `https://jadelapp-meta.streamlit.app/?view=data-deletion`

## Ejecución local

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Rutas públicas

La aplicación utiliza el parámetro de consulta `view` para mostrar documentos separados:

- `?view=privacy`
- `?view=terms`
- `?view=data-deletion`

Estas páginas no deben requerir autenticación y deben permanecer accesibles durante Meta App Review.

## Seguridad

No almacenes en este repositorio:

- Meta App Secret
- Page access tokens
- User access tokens
- Contraseñas
- Credenciales OAuth

Usa Streamlit Secrets o un gestor de secretos para cualquier credencial privada.

## Estado de producción

La existencia de estas páginas no sustituye la aprobación de Meta. Mantén la publicación automática y el acceso público bloqueados hasta obtener Advanced Access y App Review aprobado para los permisos requeridos.
