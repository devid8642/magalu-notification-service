from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from magalu_notification.schemas.general import ErrorSchema, SuccessSchema
from magalu_notification.schemas.notification import (
    NotificationSchema,
    SendNotificationSchema,
)
from magalu_notification.services.exceptions import (
    NotificationAlreadySended,
    NotificationNotFound,
)
from magalu_notification.services.notification_service import (
    get_notification_service,
)

app = FastAPI(version='0.1.0', title='Magalu Notification API')


@app.post('/send/notification', status_code=status.HTTP_201_CREATED)
async def send_notification(
    notification_data: SendNotificationSchema,
) -> NotificationSchema:
    notification_service = get_notification_service()

    notification = await notification_service.create_notification(
        notification_data
    )

    return notification


@app.get(
    '/notification/{notification_id}',
    response_model=NotificationSchema,
    responses={404: {'model': ErrorSchema}},
)
async def get_notification(
    notification_id: int,
) -> NotificationSchema | ErrorSchema:
    notification_service = get_notification_service()

    notification = await notification_service.get_notification(notification_id)

    if not notification:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Notificação não encontrada'},
        )

    return notification


@app.post(
    '/notification/cancel/{notification_id}',
    responses={
        status.HTTP_200_OK: {'model': SuccessSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def cancel_notification(
    notification_id: int,
) -> SuccessSchema | ErrorSchema:
    notification_service = get_notification_service()

    try:
        await notification_service.cancel_notification(notification_id)
    except NotificationNotFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Notificação não encontrada'},
        )
    except NotificationAlreadySended:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Notificação já enviada'},
        )

    return SuccessSchema(message='Notificação cancelada com sucesso')
