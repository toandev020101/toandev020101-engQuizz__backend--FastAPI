from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings
from app.crud import crud_test, crud_exam, crud_exam_detail, crud_notification
from app.schemas import TestCreateSchema, TestUpdateSchema, ExamCreateSchema, ExamDetailCreateSchema, \
    NotificationCreateSchema
from app.services.notification_service import NotificationService
from app.utils import to_list_dict, to_datetime, to_date_time_full_format

settings = get_settings()


class TestService:
    @staticmethod
    async def get_pagination(_limit: int, _page: int, search_term: str, status_test: str,
                             session: AsyncSession):
        tests = await crud_test.find_pagination(_limit=_limit, _page=_page, search_term=search_term,
                                                status_test=status_test, session=session)

        total = await crud_test.count_all(session=session)
        return {"tests": to_list_dict(objects=tests), "total": total}

    @staticmethod
    async def get_one_by_id(id: int, session: AsyncSession):
        test = await crud_test.find_one_by_id(id=id, session=session)

        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đề thi!")

        return {"test": test.dict()}

    @staticmethod
    async def add_one(creator_id: int, test_data: TestCreateSchema, session: AsyncSession):
        test_data_exams = test_data.exams
        del test_data.exams
        test_data.start_date = to_datetime(test_data.start_date)
        test_data.end_date = to_datetime(test_data.end_date)
        test_data.creator_id = creator_id
        created_test = await crud_test.create_one(test_data=test_data, session=session)

        exams_data = []
        for exam in test_data_exams:
            exam_data = ExamCreateSchema(user_id=exam.get("user_id"), test_id=created_test.id)
            exams_data.append(exam_data)
        created_exams = await crud_exam.create_list(exams_data=exams_data, session=session)

        exam_details_data = []
        for index, exam in enumerate(test_data_exams):
            for idx, question_id in enumerate(exam.get("question_ids")):
                exam_detail_data = ExamDetailCreateSchema(exam_id=created_exams[index].id, question_id=question_id,
                                                          position=idx)
                exam_details_data.append(exam_detail_data)

        await crud_exam_detail.create_list(exam_details_data=exam_details_data, session=session)

        user_ids = []
        for exam in test_data_exams:
            user_ids.append(exam["user_id"])
        notification_data = NotificationCreateSchema(title="Bạn có một bài thi mới",
                                                     content=f"{created_test.name} ({created_test.easy_quantity + created_test.average_quantity + created_test.difficult_quantity} câu)\nTừ {to_date_time_full_format(created_test.start_date)} đến {to_date_time_full_format(created_test.end_date)}\nThời gian làm bài {round(created_test.exam_time / 60)} phút",
                                                     user_ids=user_ids)

        await NotificationService.add_one(creator_id=creator_id, notification_data=notification_data,
                                          type_message="info", session=session)
        return {"test": created_test.dict()}

    @staticmethod
    async def update_one(id: int, test_data: TestUpdateSchema, session: AsyncSession):
        test = await crud_test.find_one_by_id(id=id, session=session)

        if not test:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đề thi!")

        test_data_exams = test_data.exams
        del test_data.exams
        test_data.start_date = to_datetime(test_data.start_date)
        test_data.end_date = to_datetime(test_data.end_date)
        updated_test = await crud_test.update_one(id=test.id, test_data=test_data, session=session)

        exam_ids = []
        for exam in test.exams:
            exam_ids.append(exam.id)
        await crud_exam.delete_list(ids=exam_ids, session=session)

        exams_data = []
        for exam in test_data_exams:
            exam_data = ExamCreateSchema(user_id=exam.get("user_id"), test_id=updated_test.id)
            exams_data.append(exam_data)
        created_exams = await crud_exam.create_list(exams_data=exams_data, session=session)

        exam_details_data = []
        for index, exam in enumerate(test_data_exams):
            for idx, question_id in enumerate(exam.get("question_ids")):
                exam_detail_data = ExamDetailCreateSchema(exam_id=created_exams[index].id, question_id=question_id,
                                                          position=idx)
                exam_details_data.append(exam_detail_data)

        await crud_exam_detail.create_list(exam_details_data=exam_details_data, session=session)

        user_ids = []
        for exam in test_data_exams:
            user_ids.append(exam["user_id"])
        notification_data = NotificationCreateSchema(title="Một bài thi mà bạn có tham gia đã cập nhật!",
                                                     content=f"{updated_test.name} ({updated_test.easy_quantity + updated_test.average_quantity + updated_test.difficult_quantity} câu)\nTừ {to_date_time_full_format(updated_test.start_date)} đến {to_date_time_full_format(updated_test.end_date)}\nThời gian làm bài {round(updated_test.exam_time / 60)} phút",
                                                     user_ids=user_ids)

        await NotificationService.add_one(creator_id=updated_test.creator_id, notification_data=notification_data,
                                          type_message="warning", session=session)
        return {"test": updated_test.dict()}

    @staticmethod
    async def remove_one(id: int, session: AsyncSession):
        removed_test = await crud_test.delete_one(id=id, session=session)
        if not removed_test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đề thi!")

        user_ids = []
        for exam in removed_test.exams:
            user_ids.append(exam.user_id)
        notification_data = NotificationCreateSchema(title="Một bài thi mà bạn có tham gia đã bị xóa!",
                                                     content=f"{removed_test.name} ({removed_test.easy_quantity + removed_test.average_quantity + removed_test.difficult_quantity} câu)\nTừ {to_date_time_full_format(removed_test.start_date)} đến {to_date_time_full_format(removed_test.end_date)}\nThời gian làm bài {round(removed_test.exam_time / 60)} phút",
                                                     user_ids=user_ids)

        await NotificationService.add_one(creator_id=removed_test.creator_id, notification_data=notification_data,
                                          type_message="error", session=session)

        return removed_test.dict()

    @staticmethod
    async def remove_list(ids: List[int], session: AsyncSession):
        removed_tests = await crud_test.delete_list(ids=ids, session=session)
        if not removed_tests:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đề thi!")

        for removed_test in removed_tests:
            user_ids = []
            for exam in removed_test.exams:
                user_ids.append(exam.user_id)
            notification_data = NotificationCreateSchema(title="Một bài thi mà bạn có tham gia đã bị xóa!",
                                                         content=f"{removed_test.name} ({removed_test.easy_quantity + removed_test.average_quantity + removed_test.difficult_quantity} câu)\nTừ {to_date_time_full_format(removed_test.start_date)} đến {to_date_time_full_format(removed_test.end_date)}\nThời gian làm bài {round(removed_test.exam_time / 60)} phút",
                                                         user_ids=user_ids)

            await NotificationService.add_one(creator_id=removed_test.creator_id, notification_data=notification_data,
                                              type_message="error", session=session)
        return to_list_dict(objects=removed_tests)
