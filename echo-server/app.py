from boto3.session import Session

from chalice import Chalice
from chalice import WebsocketDisconnectedError

app = Chalice(app_name="echo-server")
app.websocket_api.session = Session()
app.experimental_feature_flags.update([
    'WEBSOCKETS'
])


@app.on_ws_message()
def message(event):
    try:
        app.websocket_api.send(
            connection_id=event.connection_id,
            message=event.body,
        )
    except WebsocketDisconnectedError as e:
        pass  # Disconnected so we can't send the message back.