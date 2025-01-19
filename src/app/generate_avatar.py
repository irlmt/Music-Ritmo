from fastapi import APIRouter
import python_avatars as pa
import base64
import os
import tempfile

router = APIRouter()

@router.get("/generate_avatar/")
def generate_random_avatar():
    try:
        avatar = pa.Avatar.random()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            avatar.render(tmp_file.name)
            with open(tmp_file.name, "rb") as file:
                base64_avatar = base64.b64encode(file.read()).decode("utf-8")

        os.remove(tmp_file.name)

        return {"avatar_base64": base64_avatar}
    except Exception as e:
        return {"error": str(e)}