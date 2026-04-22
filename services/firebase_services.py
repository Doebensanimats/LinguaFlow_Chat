import firebase_admin
from firebase_admin import credentials, firestore
import uuid

db = None


def init_firebase():
    global db
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def create_room():
    return str(uuid.uuid4())[:8]


def send_message(room_id, data):
    db.collection("rooms").document(room_id)\
      .collection("messages").add(data)


def get_messages(room_id):
    return db.collection("rooms").document(room_id)\
      .collection("messages").order_by("time").stream()