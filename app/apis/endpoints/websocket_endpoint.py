import asyncio
import json
from datetime import datetime

import pytz
from fastapi import APIRouter, WebSocket, Depends, HTTPException, status

from app.apis.depends import get_session
from app.core import get_settings
from app.schemas import ExamUpdateSchema, ExamDetailUpdateSchema
from app.services import ExamService, ExamDetailService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/websocket", tags=["Websocket"])
user_exams = []


@router.websocket("/send/{exam_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, exam_id: int, user_id: int, session=Depends(get_session)):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message['type'] == 'choice_answer':
                exam_detail_data = ExamDetailUpdateSchema(answer_id=message['answer_id'],
                                                          is_answer_draft=message["is_answer_draft"])
                await ExamDetailService.update_answer_id_by_id(exam_id=exam_id, question_id=message["question_id"],
                                                               exam_detail_data=exam_detail_data, session=session)

            if message['type'] == 'submit':
                updated_exam = await ExamService.submit_exam(id=exam_id, session=session)
                exam_index = None
                for i, user_exam in enumerate(user_exams):
                    if user_exam["exam_id"] == exam_id and user_exam["user_id"] == user_id:
                        exam_index = i
                        break

                exam_data = ExamUpdateSchema(exam_time_at=user_exams[exam_index]["exam_time_at"],
                                             exam_time=updated_exam.test.exam_time - user_exams[exam_index][
                                                 "time_down"])
                await ExamService.update_exam_time_by_id(id=exam_id, exam_data=exam_data, session=session)
                del user_exams[exam_index]
                await websocket.close()
                return


    except ValueError as ve:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format.")
    except Exception as e:
        await websocket.close(code=status.WS_1006_ABNORMAL_CLOSURE)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error.")


@router.websocket("/receive/{exam_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, exam_id: int, user_id: int, session=Depends(get_session)):
    await websocket.accept()
    data = await ExamService.get_one_by_id(id=exam_id, session=session)
    time_down = data["exam"]["test"]["exam_time"] - data["exam"]["exam_time"]
    exam_time_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')) if data["exam"]["exam_time_at"] is None else data["exam"][
        "exam_time_at"]

    exam_index = None
    for i, user_exam in enumerate(user_exams):
        if user_exam["exam_id"] == exam_id and user_exam["user_id"] == user_id:
            exam_index = i
            break

    if exam_index is None:
        user_exams.append(
            {"exam_id": exam_id, "user_id": user_id, "time_down": time_down, "exam_time_at": exam_time_at})
    else:
        exam_time_at = user_exams[exam_index]["exam_time_at"]

    try:
        while True:
            time_down = user_exams[exam_index]["time_down"]

            if time_down > 0:
                message = {"time_down": time_down, "type": "set_time"}
            else:
                message = {"type": "submit"}

            await websocket.send_text(json.dumps(message))
            if message.get("type") == "submit":
                updated_exam = await ExamService.submit_exam(id=exam_id, session=session)
                exam_data = ExamUpdateSchema(exam_time_at=exam_time_at,
                                             exam_time=updated_exam.test.exam_time - time_down)
                await ExamService.update_exam_time_by_id(id=exam_id, exam_data=exam_data, session=session)
                if exam_index:
                    user_exams.remove(user_exams[exam_index])
                await websocket.close()
                return

            await asyncio.sleep(1)
            time_down -= 1
            user_exams[exam_index]["time_down"] = time_down
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error.")
    finally:
        exam_data = ExamUpdateSchema(exam_time_at=exam_time_at,
                                     exam_time=data["exam"]["test"]["exam_time"] - time_down)
        await ExamService.update_exam_time_by_id(id=exam_id, exam_data=exam_data, session=session)
        if exam_index:
            user_exams.remove(user_exams[exam_index])
