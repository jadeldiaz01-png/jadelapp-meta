from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from datetime import date
from typing import Any
from urllib.parse import urlencode

import requests
import streamlit as st

APP_NAME = "Jadel Pages API"
APP_DOMAIN = "jadelapp-meta.streamlit.app"
CONTACT_EMAIL = "darklife_jade@hotmail.com"
BASE_URL = f"https://{APP_DOMAIN}"
DEFAULT_GRAPH_VERSION = "v25.0"
SCOPES = ("pages_show_list", "pages_read_engagement", "pages_manage_posts")
VIEWS = {"home", "privacy", "terms", "data-deletion", "review-demo"}


class GraphError(RuntimeError):
    pass


def setting(name: str, default: str = "") -> str:
    try:
        return str(st.secrets[name]).strip()
    except (KeyError, FileNotFoundError):
        return os.getenv(name, default).strip()


def graph_version() -> str:
    value = setting("META_GRAPH_VERSION", DEFAULT_GRAPH_VERSION)
    return value if value.startswith("v") else f"v{value}"


def redirect_uri() -> str:
    return setting("META_REDIRECT_URI", f"{BASE_URL}/")


def view() -> str:
    value = str(st.query_params.get("view", "home")).strip().lower()
    return value if value in VIEWS else "home"


def nav() -> None:
    links = [
        ("Inicio", "home"),
        ("Demostración", "review-demo"),
        ("Privacidad", "privacy"),
        ("Condiciones", "terms"),
        ("Eliminación", "data-deletion"),
    ]
    st.markdown(" · ".join(f"[{label}]({BASE_URL}/?view={target})" for label, target in links))
    st.divider()


def make_state(app_secret: str) -> str:
    nonce = secrets.token_urlsafe(18)
    issued = str(int(time.time()))
    payload = f"{nonce}.{issued}"
    signature = hmac.new(app_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def valid_state(value: str, app_secret: str, max_age: int = 600) -> bool:
    try:
        nonce, issued, signature = value.split(".", 2)
        issued_at = int(issued)
    except (TypeError, ValueError):
        return False
    if not nonce or abs(int(time.time()) - issued_at) > max_age:
        return False
    payload = f"{nonce}.{issued}"
    expected = hmac.new(app_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def oauth_url(app_id: str, app_secret: str) -> str:
    query = urlencode(
        {
            "client_id": app_id,
            "redirect_uri": redirect_uri(),
            "state": make_state(app_secret),
            "scope": ",".join(SCOPES),
            "response_type": "code",
            "auth_type": "rerequest",
        }
    )
    return f"https://www.facebook.com/{graph_version()}/dialog/oauth?{query}"


def graph(
    method: str,
    path: str,
    *,
    token: str | None = None,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"https://graph.facebook.com/{graph_version()}/{path.lstrip('/')}"
    request_params = dict(params or {})
    request_data = dict(data or {})
    if token:
        if method.upper() == "GET":
            request_params["access_token"] = token
        else:
            request_data["access_token"] = token
    try:
        response = requests.request(
            method,
            url,
            params=request_params,
            data=request_data,
            timeout=(5, 30),
        )
    except requests.RequestException as exc:
        raise GraphError("No fue posible comunicarse con Meta Graph API.") from exc
    if not response.ok:
        try:
            error = response.json().get("error", {})
            message = error.get("message", "Meta rechazó la solicitud.")
            code = error.get("code", response.status_code)
        except ValueError:
            message = "Meta rechazó la solicitud."
            code = response.status_code
        raise GraphError(f"Meta Graph API ({code}): {message}")
    if not response.content:
        return {"success": True}
    try:
        return response.json()
    except ValueError as exc:
        raise GraphError("Meta devolvió una respuesta no válida.") from exc


def handle_callback(app_id: str, app_secret: str) -> None:
    code = str(st.query_params.get("code", "")).strip()
    state = str(st.query_params.get("state", "")).strip()
    error = str(st.query_params.get("error", "")).strip()
    if error:
        st.error(str(st.query_params.get("error_description", "Autorización cancelada.")))
        return
    if not code:
        return
    if not valid_state(state, app_secret):
        st.error("El estado OAuth es inválido o expiró. Inicia la conexión nuevamente.")
        return
    try:
        token_payload = graph(
            "GET",
            "oauth/access_token",
            params={
                "client_id": app_id,
                "client_secret": app_secret,
                "redirect_uri": redirect_uri(),
                "code": code,
            },
        )
        user_token = str(token_payload.get("access_token", "")).strip()
        if not user_token:
            raise GraphError("Meta no devolvió un token de usuario.")
        profile = graph("GET", "me", token=user_token, params={"fields": "id,name"})
    except GraphError as exc:
        st.error(str(exc))
        return
    st.session_state["user_token"] = user_token
    st.session_state["profile"] = {"id": profile.get("id"), "name": profile.get("name")}
    st.query_params.clear()
    st.query_params["view"] = "review-demo"
    st.rerun()


def clear_session() -> None:
    for key in ("user_token", "profile", "pages", "last_post"):
        st.session_state.pop(key, None)


def home() -> None:
    st.title(APP_NAME)
    st.subheader("Administración autorizada de páginas de Facebook")
    st.write(
        "La aplicación conecta una cuenta mediante Facebook Login, muestra las páginas "
        "que administra, permite seleccionar una página y publica contenido únicamente "
        "después de una confirmación explícita."
    )
    st.info(
        "La publicación automática permanece desactivada. La demostración para revisión "
        "solo funciona cuando las credenciales se configuran en Streamlit Secrets."
    )
    st.markdown(
        f"""
- **Dominio:** `{APP_DOMAIN}`
- **Contacto:** [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})
- **Permisos:** `{SCOPES[0]}`, `{SCOPES[1]}`, `{SCOPES[2]}`
"""
    )


def privacy() -> None:
    st.title("Política de privacidad")
    st.caption("Vigente desde 2026-07-18")
    st.markdown(
        f"""
**Responsable:** {APP_NAME}. Contacto: [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL}).

### Datos tratados
La aplicación puede recibir el identificador y nombre básico de la cuenta autenticada,
la lista de páginas que administra, identificadores de página, tokens autorizados y
datos básicos de las publicaciones creadas mediante la aplicación.

### Finalidades
Autenticar al usuario, mostrar sus páginas, permitir una selección explícita, publicar
contenido aprobado y confirmar el resultado de la publicación.

### Conservación y seguridad
La demostración mantiene tokens únicamente en memoria de sesión. No se escriben tokens
en GitHub ni se muestran en pantalla. Se utiliza HTTPS, validación de estado OAuth y
mensajes de error que no revelan secretos.

### Compartición
No vendemos datos personales. Los datos solo se transmiten a Meta y a la infraestructura
necesaria para ejecutar la función solicitada.

### Derechos
Puedes solicitar acceso o eliminación escribiendo a
[{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL}) o usando las
[instrucciones de eliminación]({BASE_URL}/?view=data-deletion).
"""
    )


def terms() -> None:
    st.title("Condiciones del servicio")
    st.markdown(
        f"""
Al utilizar **{APP_NAME}**, confirmas que tienes autorización para administrar las
páginas que conectas. Eres responsable del contenido que introduces y debes revisarlo
antes de pulsar **Publicar**.

No se permite publicar contenido ilegal, engañoso, abusivo, que infrinja derechos de
terceros o que viole las políticas de Meta. La aplicación puede suspenderse por
mantenimiento, seguridad, pérdida de permisos o incumplimiento.

La disponibilidad depende de Streamlit y Meta Graph API. El tratamiento de datos se
describe en la [Política de privacidad]({BASE_URL}/?view=privacy).

Contacto: [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL}).
"""
    )


def deletion() -> None:
    st.title("Eliminación de datos de usuario")
    st.markdown(
        f"""
### Eliminar la integración desde Facebook
1. Abre **Configuración y privacidad → Configuración**.
2. Ve a **Integraciones comerciales** o **Apps y sitios web**.
3. Selecciona **{APP_NAME}** y pulsa **Eliminar**.

### Solicitud por correo
Escribe a [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL}) con el asunto
**“Eliminación de datos — Jadel Pages API”** e incluye tu nombre, correo de contacto y
una declaración solicitando la eliminación.

La solicitud se procesará dentro de un máximo de 30 días. Cuando existan, se eliminarán
tokens, identificadores, preferencias y registros asociados. La demostración actual no
guarda tokens de forma persistente.
"""
    )


def review_demo() -> None:
    st.title("Demostración para Meta App Review")
    st.write(
        "Flujo real y controlado para demostrar `pages_show_list`, "
        "`pages_read_engagement` y `pages_manage_posts`."
    )

    app_id = setting("META_APP_ID")
    app_secret = setting("META_APP_SECRET")
    if not app_id or not app_secret:
        st.warning("Falta configurar Meta OAuth en Streamlit Secrets.")
        st.code(
            f'META_APP_ID = "..."\\nMETA_APP_SECRET = "..."\\n'
            f'META_REDIRECT_URI = "{BASE_URL}/"\\nMETA_GRAPH_VERSION = "{DEFAULT_GRAPH_VERSION}"',
            language="toml",
        )
        return

    handle_callback(app_id, app_secret)
    user_token = str(st.session_state.get("user_token", "")).strip()

    if not user_token:
        st.subheader("1. Conectar Facebook")
        st.write(
            "La persona autoriza únicamente los permisos necesarios y puede cancelar "
            "antes de concederlos."
        )
        st.link_button("Continuar con Facebook", oauth_url(app_id, app_secret), type="primary")
        return

    profile = st.session_state.get("profile", {})
    st.success(f"Conectado como {profile.get('name', 'usuario autorizado')}")

    left, right = st.columns(2)
    if left.button("Actualizar páginas", use_container_width=True):
        st.session_state.pop("pages", None)
    if right.button("Desconectar sesión", use_container_width=True):
        clear_session()
        st.rerun()

    st.subheader("2. Mostrar páginas administradas")
    st.caption("Permiso: pages_show_list")
    if "pages" not in st.session_state:
        try:
            result = graph(
                "GET",
                "me/accounts",
                token=user_token,
                params={"fields": "id,name,access_token,tasks", "limit": 100},
            )
            st.session_state["pages"] = result.get("data", [])
        except GraphError as exc:
            st.error(str(exc))
            return

    pages = st.session_state.get("pages", [])
    if not pages:
        st.warning("Meta no devolvió páginas administradas para esta cuenta.")
        return

    page_map = {
        f"{page.get('name', 'Página')} — {page.get('id', '')}": page for page in pages
    }
    label = st.selectbox("Selecciona la página de prueba", list(page_map))
    selected = page_map[label]
    page_token = str(selected.get("access_token", "")).strip()
    if not page_token:
        st.error("La página seleccionada no devolvió un Page Access Token.")
        return

    st.subheader("3. Publicar contenido aprobado")
    st.caption("Permiso: pages_manage_posts")
    message = st.text_area(
        "Contenido de prueba",
        value=f"[Meta App Review Test] Publicación autorizada desde {APP_NAME}. {int(time.time())}",
        max_chars=2000,
    )
    confirmed = st.checkbox("Confirmo que administro la página y autorizo esta prueba.")

    if st.button("Publicar", type="primary", disabled=not confirmed or not message.strip()):
        try:
            created = graph(
                "POST",
                f"{selected['id']}/feed",
                data={"message": message.strip(), "access_token": page_token},
            )
            post_id = str(created.get("id", "")).strip()
            if not post_id:
                raise GraphError("Meta no devolvió el ID de la publicación.")
            post = graph(
                "GET",
                post_id,
                token=page_token,
                params={"fields": "id,message,created_time,permalink_url"},
            )
            st.session_state["last_post"] = {**post, "_token": page_token}
            st.success("Publicación creada y verificada.")
        except GraphError as exc:
            st.error(str(exc))

    post = st.session_state.get("last_post")
    if post:
        st.subheader("4. Confirmar la publicación")
        st.caption("Permiso: pages_read_engagement")
        st.json(
            {
                "id": post.get("id"),
                "message": post.get("message"),
                "created_time": post.get("created_time"),
                "permalink_url": post.get("permalink_url"),
            }
        )
        if post.get("permalink_url"):
            st.link_button("Abrir publicación en Facebook", str(post["permalink_url"]))
        if st.button("Eliminar publicación de prueba"):
            try:
                graph(
                    "DELETE",
                    str(post["id"]),
                    data={"access_token": str(post["_token"])},
                )
                st.session_state.pop("last_post", None)
                st.success("Publicación eliminada.")
                st.rerun()
            except GraphError as exc:
                st.error(str(exc))

    st.info(
        "En la grabación muestra el login, consentimiento, lista de páginas, selección, "
        "publicación, confirmación y eliminación. No muestres tokens ni secretos."
    )


def main() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="📄", layout="centered")
    nav()
    render = {
        "home": home,
        "privacy": privacy,
        "terms": terms,
        "data-deletion": deletion,
        "review-demo": review_demo,
    }
    render[view()]()
    st.divider()
    st.caption(f"© {date.today().year} {APP_NAME} · {CONTACT_EMAIL} · {graph_version()}")


if __name__ == "__main__":
    main()
