# Jadel Pages API

Aplicación Streamlit para presentar las páginas legales requeridas por Meta y demostrar,
de forma real y controlada, el uso de permisos de Facebook Pages.

## URLs públicas

- Inicio: `https://jadelapp-meta.streamlit.app/`
- Demostración: `https://jadelapp-meta.streamlit.app/?view=review-demo`
- Privacidad: `https://jadelapp-meta.streamlit.app/?view=privacy`
- Condiciones: `https://jadelapp-meta.streamlit.app/?view=terms`
- Eliminación: `https://jadelapp-meta.streamlit.app/?view=data-deletion`

## Permisos demostrados

- `pages_show_list`
- `pages_read_engagement`
- `pages_manage_posts`

La aplicación solicita los permisos mediante Facebook Login, muestra las páginas devueltas
por Meta, exige selección y confirmación explícitas, publica un post de prueba, lo lee
nuevamente y permite eliminarlo.

## Configuración segura

En Streamlit Community Cloud, abre **App settings → Secrets** y configura:

```toml
META_APP_ID = "..."
META_APP_SECRET = "..."
META_REDIRECT_URI = "https://jadelapp-meta.streamlit.app/"
META_GRAPH_VERSION = "v25.0"
```

Configura la misma URI, carácter por carácter, en Facebook Login.

Nunca publiques el App Secret, User Access Token ni Page Access Token en GitHub.

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Para OAuth local necesitas registrar una URI de redirección de desarrollo separada y
configurarla mediante variables de entorno o `.streamlit/secrets.toml`, que está ignorado
por Git.

## Grabación para Meta App Review

Consulta [`META_APP_REVIEW_SCREENCAST.md`](META_APP_REVIEW_SCREENCAST.md). El video debe
mostrar el flujo real de extremo a extremo y no una maqueta.

## Estado de producción

La existencia de esta demostración no equivale a aprobación. Mantén producción pública y
publicación automática bloqueadas hasta que Meta conceda Advanced Access y App Review para
los permisos solicitados.
